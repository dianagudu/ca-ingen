#!/usr/bin/env python3
import click

# im naming it as pylib so that we won't get confused between os.path and
# sys.path
from sys import path as pylib
import os.path
pylib += [os.path.abspath('r/../../inputgen')]

from cage.auctionset import AuctionSet
from cage.auctionset import AuctionSetGenerator
from cage.params import AuctionSetParams

@click.group()
def cli():
    pass


@cli.group(short_help='create auction instance', name='create')
def create():
    pass


@create.command(short_help='create auction instance from config file', name='from-file')
@click.option("--n", type=int, help="number of instances to create")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def create_from_file(n, input, output):
    asg = AuctionSetGenerator(AuctionSetParams.from_file(input))
    if n is None:
        asg.generate().save(output)
    else:
        for i in range(0, n):
            asg.generate().save(output + "." + str(i))


if __name__ == '__main__':
    cli()
