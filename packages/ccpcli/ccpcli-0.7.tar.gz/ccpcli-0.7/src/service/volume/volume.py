###############################################################################
# Copyright (c) 2024-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepakpant@coredge.io>, April 2023                  #
# Modified by Aman Kadhala <aman@coredge.io>, April 2023                      #
###############################################################################
import json
import os

import click
from src.util.constants import Constants, HttpStatus
from src.util.http_helper import delete_assert
from src.util.http_helper import get_assert, post_assert
from src.util.utils import print_cli, print_info, print_error
from src.util.utils import set_context, validate_size
from src.resource_schemas.volume import volume_list_response


@click.group(name=Constants.COMMAND_GROUP_VOLUME)
@click.pass_context
def volumes(ctx):
    """This command will do all the operations on volumes"""
    pass


@volumes.command(name=Constants.COMMAND_GET)
@click.pass_context
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def get_volume(ctx, output):
    """This command will provide the list of Volume"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}volumes'
    params = {'include_bootable': False}

    res = get_assert(ctx, url=url, params=params)

    if output == Constants.TABULAR_OUTPUT:
        volumes = volume_list_response(res)
    else:
        volumes = res

    print_cli(msg=volumes, output_format=output,
              headers=Constants.TABLE_HEADER_VOLUME)


@volumes.command(name=Constants.COMMAND_DESCRIBE)
@click.pass_context
@click.argument('volume')
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def describe_volume(ctx, volume, output):
    """This command will describe volume"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}volumes{os.sep}{volume}/'
    res = get_assert(ctx, url=url)

    print_cli(msg=[res], output_format=output)


@volumes.command(name=Constants.COMMAND_DELETE)
@click.pass_context
@click.argument('volume')
def delete_volume(ctx, volume):
    """This command will delete network"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}volumes{os.sep}{volume}/'

    delete_assert(ctx, url=url, expected_response_code=202)

    print_info("Volume deleting in progress.")


@volumes.command(name=Constants.COMMAND_CREATE)
@click.pass_context
@click.option('--volume-name', '-vn', help='name of the volume', required=True)
@click.option('--size', '-s', help="size of volume (GB). Default size 50 GB. Size must be a multiple of 50", default=50, callback=validate_size)
@click.option('--volume-type', type=click.Choice(list(Constants.VOLUME_TYPES)), help="Volume types.Default 'hdd-storage'",
              default="hdd-storage")
@click.option('--attach', help="VM ID to attach with volume")
@click.option('--billing-type', type=click.Choice(['MRC', 'HRC']), help="Billing rate Monthly(MRC) or Hourly("
                                                                     "HRC).Default 'MRC'",default='MRC')
def volume_create(ctx, volume_name, size, volume_type, attach, billing_type):

    set_context(ctx)

    component_type = None

    create_volume_payload = {"volume_name": volume_name,
                             "volume_size": size,
                             "billing_unit": billing_type,
                             "bootable": False,
                             "enable_backup": False,
                             "compute_id": attach if attach else ""
                             }

    # get volumes types for fetching component type
    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}volumes{os.sep}volume_types'
    param = {"group":"BLOCK_STORAGE"}
    volume_types = get_assert(ctx, url=url, params=param)

    for item in volume_types:
        if item.get("label") == Constants.VOLUME_TYPES.get(volume_type):
            create_volume_payload["volume_type_id"] = item['id']
            create_volume_payload["volume_type"] = item.get("name")
            component_type = item.get("product_attributes").get("component_type")
            break

    # fetching prices to get component id and billing units for volume
    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}order-management{os.sep}products{os.sep}prices{os.sep}'
    param = {"component_type": component_type}
    prices = get_assert(ctx, url=url, params=param)

    # validating billing units
    units = {price.get("unit") for price in prices}
    if billing_type not in units:
        print_error(f"{','.join(units)}, currently supported billing unit for volume")
        raise click.exceptions.Exit()

    # processing products payload for backend API
    for price in prices:
        if price.get("unit") == billing_type:
            create_volume_payload["products"] = json.dumps({"volume": {"id": price.get("component_id")}})

    # create and attach volume
    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}volumes{os.sep}create-and-attach{os.sep}'

    volume = post_assert(ctx, url=url, data=create_volume_payload, expected_response_code=HttpStatus.ACCEPTED)

    print_cli(msg=volume, output_format=None)
