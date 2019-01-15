#!/usr/bin/env python3
import click
import json
import decimal

# im naming it as pylib so that we won't get confused between os.path and
# sys.path
from sys import path as pylib
import os.path
pylib += [os.path.abspath('r/../../inputgen')]

from cage.params import AuctionSetParams
from cage.auctionset import AuctionSetGenerator
from cage.auctionset import AuctionSet


def positive_float(f):
    if float(f) < 0:
        raise ValueError(None)
    else:
        return float(f)


def normal_float(f):
    if float(f) < 0 or float(f) > 1:
        raise ValueError(f)
    else:
        return float(f)


def validate_csl(ctx, param, value):
    try:
        return [positive_float(x) for x in value.split(",")]
    except ValueError:
        raise click.BadParameter(
            '%s should be a comma-separated list of floats >= 0, not \'%s\'' % (param.name, value))
    pass


def validate_bidset_params(ctx, param, value):
    try:
        if value is None:
            raise ValueError(None)
        data = json.loads(value)
        data["amount"] = int(data["amount"])
        # ...
        return data
    except ValueError as err:
        raise click.BadParameter('')
    except KeyError as err:
        raise click.BadParameter(
            'please specify %s as part of %s.' % (param.name, err))


def validate_valuations_params(ctx, param, value):
    try:
        if value is None:
            raise ValueError(None)
        data = json.loads(value)
        data["dist_means"] = normal_float(data["dist_means"])
        data["a_sigma"] = normal_float(data["a_sigma"])
        data["b_sigma"] = normal_float(data["b_sigma"])
        return data
    except ValueError as err:
        raise click.BadParameter(
            'all valuation params should be floats in [0,1], not \'%s\'' % err)
    except KeyError as err:
        raise click.BadParameter(
            'please specify %s as part of valuations.' % err)


def validate_cost_model_params(ctx, param, value):
    try:
        if value is None:
            raise ValueError(None)
        data = json.loads(value)
        if not isinstance(data["slope"], list):
            raise ValueError(None)
        if not isinstance(data["fixed"], list):
            raise ValueError(None)
    except ValueError:
        raise click.BadParameter(
            'should be a dict containing slope and fixed arrays, not \'%s\'' % value)
    except KeyError as err:
        raise click.BadParameter(
            'please specify %s as part of cost_model.' % err)

    try:
        # convert slope and fixed values to lists of floats
        data["slope"] = [positive_float(x) for x in data['slope']]
        data["fixed"] = [positive_float(x) for x in data['fixed']]
    except ValueError:
        raise click.BadParameter('slope and fixed should contain floats >=0.')

    if len(data["slope"]) != len(data["fixed"]):
        raise click.BadParameter(
            'slope and fixed should have the same length.')

    return data


@click.group()
def cli():
    pass


@cli.group(short_help='create auction instance', name='create')
def create():
    pass


@create.command(short_help='create auction instance from config file', name='from-file')
@click.option("--count", type=int, help="number of instances to create")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def create_from_file(count, input, output):
    asg = AuctionSetGenerator(AuctionSetParams.from_file(input))
    if count is None:
        asg.generate().save(output)
    else:
        for i in range(0, count):
            asg.generate().save(output + "." + str(i))


@create.command(short_help='create auction instance from json-formatted params', name='from-dicts')
@click.option("--count", type=int, help="number of instances to create")
@click.option("--bids", callback=validate_bidset_params, required=True)
@click.option("--asks", callback=validate_bidset_params, required=True)
@click.option("--cost_model", callback=validate_cost_model_params, required=True, help="")
@click.option("--valuations", callback=validate_valuations_params, required=True)
@click.argument("output", type=click.Path())
def create_from_dicts(count, bids, asks, cost_model, valuations, output):
    asp_dobj = {
        "bids": bids,
        "asks": asks,
        "cost_model": cost_model,
        "valuations": valuations
    }
    print(asp_dobj)
    return
    asg = AuctionSetGenerator(AuctionSetParams.from_dict(asp_dobj))
    if count is None:
        asg.generate().save(output)
    else:
        for i in range(0, count):
            asg.generate().save(output + "." + str(i))


@create.command(short_help='create auction instance from individual params', name='from-params')
@click.option("--count", type=int, help="number of instances to create")
@click.option("--bids-amount", type=click.IntRange(min=1), default=100,
              help="number of bids to generate")
@click.option("--bids-model", type=click.Path(exists=True))
@click.option("--bids-binning-type")
@click.option("--bids-binning-count")
@click.option("--bids-domain")
@click.option("--cost-slope", callback=validate_csl, required=True,
              help="variable cost per resource as comma-separated list")
@click.option("--cost-fixed", callback=validate_csl, required=True,
              help="fixed cost per resource as comma-separated list")
@click.option("--dist-means", type=click.FloatRange(0, 1), default=0.0,
              help="relative distance between bid and ask slopes")
@click.option("--a-sigma", type=click.FloatRange(0, 1), default=0.05,
              help="ask value spread around base prices (relative stddev)")
@click.option("--b-sigma", type=click.FloatRange(0, 1), default=0.05,
              help="bid value spread around base prices (relative stddev)")
@click.argument("output", type=click.Path())
def create_from_params(count,
                       bids_amount, bids_model, bids_binning_type, bids_binning_count, bids_domain,
                       cost_slope, cost_fixed,
                       dist_means, a_sigma, b_sigma,
                       output):
    if len(cost_slope) != len(cost_fixed):
        raise click.BadParameter(
            'cost-slope and cost-fixed should have the same length.')

    asp_dobj = {
        "bids": {
            "amount": bids_amount,
            "model": bids_model,
            "binning_type": bids_binning_type,
            "binning_counts": bids_binning_count,
            "domain": bids_domain
        },
        "asks": {},
        "cost_model": {
            "slope": cost_slope,
            "fixed": cost_fixed
        },
        "valuations": {
            "dist_means": dist_means,
            "a_sigma": a_sigma,
            "b_sigma": b_sigma
        }
    }
    print(asp_dobj)
    return
    asg = AuctionSetGenerator(AuctionSetParams.from_dict(asp_dobj))
    if count is None:
        asg.generate().save(output)
    else:
        for i in range(0, count):
            asg.generate().save(output + "." + str(i))


if __name__ == '__main__':
    cli()
