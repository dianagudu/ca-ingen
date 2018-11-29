import numpy as np
from enum import Enum

from ingen.bundles import BundleGenerator
from ingen.model import Model
from ingen.binning import BinningGenerator

from .params import CostModelParams


class BidSet_Type(Enum):
    BIDS = 1
    ASKS = 2


class BidSet():

    def __init__(self, quantities, values, metadata):
        self.__quantities = quantities
        self.__values = values
        self.__metadata = metadata

    @staticmethod
    def from_dict(dobj):
        return BidSet(np.array(dobj["quantities"]),
                      np.array(dobj["values"]),
                      dobj["metadata"])

    def to_dict(self):
        return {
            "metadata": self.metadata,
            "values": self.values.tolist(),
            "quantities": self.quantities.tolist()
        }

    @property
    def quantities(self):
        return self.__quantities

    @property
    def values(self):
        return self.__values

    @property
    def metadata(self):
        return self.__metadata


class BidSetParams():

    def __init__(self, bundle_params, cost_model, sigma):
        model = Model.from_file(bundle_params.model_file)
        binning = BinningGenerator.generate(
            bundle_params.binning_type,
            bundle_params.binning_counts,
            model.binning.domain)
        self.__bundle_generator = BundleGenerator(model, binning)
        self.__domain_scaling = np.array(bundle_params.domain) / \
                                np.array(binning.domain)
        self.__amount = bundle_params.amount
        self.__cost_model = cost_model
        self.__sigma = sigma

    @staticmethod
    def from_auction_set_params(params, type):
        if type == BidSet_Type.ASKS:
            bundle_params = params.asks
            sigma = params.valuations.a_sigma
            new_slope = params.cost_model.slope * (
                1 - params.valuations.dist_means / 2.
            )
            cost_model = CostModelParams(new_slope, params.cost_model.fixed)
        elif type == BidSet_Type.BIDS:
            bundle_params = params.bids
            sigma = params.valuations.b_sigma
            new_slope = params.cost_model.slope * (
                1 + params.valuations.dist_means / 2.
            )
            cost_model = CostModelParams(new_slope, params.cost_model.fixed)
        else:
            raise Exception("Invalid bidset type.")

        return BidSetParams(bundle_params, cost_model, sigma)

    @property
    def bundle_generator(self):
        return self.__bundle_generator

    @property
    def domain_scaling(self):
        return self.__domain_scaling

    @property
    def amount(self):
        return self.__amount

    @property
    def cost_model(self):
        return self.__cost_model

    @property
    def sigma(self):
        return self.__sigma


class BidSetGenerator():

    @staticmethod
    def __gen_bundles(bidset_params):
        # generate amount bundles using given model
        bundles = bidset_params.bundle_generator.generate(bidset_params.amount)

        # rescale quantities to new domain and round to integer values
        return np.round(bundles.data * bidset_params.domain_scaling)

    @staticmethod
    def __gen_values(quantities, bidset_params):
        # compute valuations according to cost_model
        values = np.sum(quantities *
                        bidset_params.cost_model.slope +
                        bidset_params.cost_model.fixed,
                        axis=1)

        # add some variance for each bid, e.g. spread around base prices
        # var is obtained from normal distribution around origin
        #     represented as % of valuation
        var = np.random.randn(bidset_params.amount) * bidset_params.sigma
        values += np.multiply(values, var)

        return values

    @staticmethod
    def generate(bidset_params):
        quantities = BidSetGenerator.__gen_bundles(bidset_params)
        values = BidSetGenerator.__gen_values(quantities, bidset_params)
        metadata = {
            "binning_seed": bidset_params.bundle_generator.binning.random_seed,
            "bundle_seed": bidset_params.bundle_generator.last_seed
        }

        return BidSet(quantities, values, metadata)
