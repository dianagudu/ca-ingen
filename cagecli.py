#!/usr/bin/env python3
import click
from yaml.parser import ParserError

# im naming it as pylib so that we won't get confused between os.path and
# sys.path
from sys import path as pylib
import os.path
pylib += [os.path.abspath('r/../../inputgen')]

from cage.params import AuctionSetParams
from cage.auctionset import AuctionSetGenerator


@click.group()
def cli():
    pass


@cli.command(short_help='create auction instances from config file', name='create')
@click.option("--count", type=int, help="number of instances to create")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def create(count, input, output):
    try:
        asg = AuctionSetGenerator(AuctionSetParams.from_file(input))
        if count is None:
            asg.generate().save(output)
        else:
            for i in range(0, count):
                asg.generate().save(output + "." + str(i))
    except ValueError as err:
        raise click.BadParameter(err)
    except ParserError as err:
        raise click.BadParameter(err)


if __name__ == '__main__':
    cli()
