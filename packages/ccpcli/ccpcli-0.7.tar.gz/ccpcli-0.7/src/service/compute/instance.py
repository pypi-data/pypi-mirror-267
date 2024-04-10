###############################################################################
# Copyright (c) 2024-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Mani Keshari <mani@coredge.io>, April 2024                       #
###############################################################################
import os

import click
from src.util.constants import Constants
from src.util.http_helper import get_assert
from src.util.utils import print_cli
from src.util.utils import set_context
from src.resource_schemas.compute import instance_list_response, flavors_list_response, images_list_response


@click.group(name=Constants.COMMAND_GROUP_INSTANCE)
@click.pass_context
def instances(ctx):
    """This command will do all the operations on instances"""
    pass


@instances.command(name=Constants.COMMAND_GET)
@click.pass_context
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def get_instance(ctx, output):
    """This command will provide the list of Instances"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}computes/'

    res = get_assert(ctx, url=url)

    if output == Constants.TABULAR_OUTPUT:
        instance_list = instance_list_response(res)
    else:
        instance_list = res
    print_cli(msg=instance_list, output_format=output, headers=Constants.INSTANCE_TABLE_HEADERS)


@instances.command(name=Constants.COMMAND_DESCRIBE)
@click.pass_context
@click.argument('instance')
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def describe_instance(ctx, instance, output):
    """This command will describe instance"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}computes{os.sep}{instance}'
    res = get_assert(ctx, url=url)

    print_cli(msg=[res], output_format=output)


@click.group()
@click.pass_context
def flavors(ctx):
    """This command will do all the operations on flavours"""
    pass


@flavors.command(name=Constants.COMMAND_GET)
@click.pass_context
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def get_flavors(ctx, output):
    """This will list flavors"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}computes{os.sep}flavors/'
    res = get_assert(ctx, url=url)
    if output == Constants.TABULAR_OUTPUT:
        flavors_list = flavors_list_response(res)
    else:
        flavors_list = res
    print_cli(msg=flavors_list, output_format=output, headers=Constants.FLAVOUR_TABLE_HEADERS)


@click.group()
@click.pass_context
def images(ctx):
    """This command will do all the operations on flavours"""
    pass


@images.command(name=Constants.COMMAND_GET)
@click.pass_context
@click.option('--output', '-o', help='Supported formats are json,tabular,yaml', required=False)
def get_images(ctx, output):
    """This will list images"""

    # set up the configuration details into ctx object
    set_context(ctx)

    url = f'{ctx.obj.get(Constants.CLOUD_BASE_URL)}{os.sep}computes{os.sep}images/'
    res = get_assert(ctx, url=url)
    if output == Constants.TABULAR_OUTPUT:
        images_list = images_list_response(res)
    else:
        images_list = res
    print_cli(msg=images_list, output_format=output, headers=Constants.IMAGE_TABLE_HEADERS)
