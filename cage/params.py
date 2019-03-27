import numpy as np
import yaml

from ingen.helper import to_dict
from ingen.binning import Binning_Types

from .helper import ispositivefloat
from .helper import ispositiveint


class BundleParams():

    def __init__(self, amount, model, domain,
                 binning_type, binning_counts):
        # validate input
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError('\'amount\' should be a positive integer.')
        if not (isinstance(domain, np.ndarray) or isinstance(domain, list)) \
                or not all([ispositivefloat(x) for x in domain]):
            raise ValueError('\'domain\' should be a list of floats >= 0.')
        try:
            # convert type to enum
            binning_type = Binning_Types[binning_type.upper()]
        except KeyError:
            alltypes = ", ".join([name.lower() for name, value in Binning_Types.__members__.items()
                        if value.value < 90])
            raise ValueError('\'%s\' not a valid binning_type. Allowed values: %s'
                % (binning_type, alltypes))
        if not isinstance(binning_counts, int) and \
            not (isinstance(binning_counts, list) and
                 all([ispositiveint(x) for x in binning_counts])):
            raise ValueError(
                '\'binning_counts\' should be an int or a list of ints > 0.')
        #
        self.__amount = amount
        self.__model = model
        self.__domain = domain
        self.__binning_type = binning_type
        self.__binning_counts = binning_counts

    def to_dict(self):
        props = ["amount", "model", "domain",
                 "binning_type", "binning_counts"]
        dobj = to_dict(self, props)
        dobj["binning_type"] = self.binning_type.name.lower()
        return dobj

    @staticmethod
    def from_dict(dobj):
        return BundleParams(**dobj)

    @property
    def amount(self):
        return self.__amount

    @property
    def model(self):
        return self.__model

    @property
    def domain(self):
        return self.__domain

    @property
    def binning_type(self):
        return self.__binning_type

    @property
    def binning_counts(self):
        return self.__binning_counts


class CostModelParams():

    def __init__(self, slope, fixed):
        # validate input
        if not (isinstance(slope, np.ndarray) or isinstance(slope, list)) \
                or not all([ispositivefloat(x) for x in slope]):
            raise ValueError('\'slope\' should be a list of floats >= 0.')
        if not (isinstance(fixed, np.ndarray) or isinstance(fixed, list)) \
                or not all([ispositivefloat(x) for x in fixed]):
            raise ValueError('\'fixed\' should be a list of floats >= 0.')
        if len(slope) != len(fixed):
            raise ValueError('\'slope\' and \'fixed\' have different lengths.')
        #
        self.__slope = np.array(slope)
        self.__fixed = np.array(fixed)

    @staticmethod
    def from_dict(dobj):
        return CostModelParams(dobj["slope"], dobj["fixed"])

    def to_dict(self):
        return {
            "slope": self.slope.tolist(),
            "fixed": self.fixed.tolist()
        }

    @property
    def slope(self):
        return self.__slope

    @property
    def fixed(self):
        return self.__fixed


class ValuationParams():

    def __init__(self, dist_means, b_sigma, a_sigma):
        # validate input
        if not isinstance(dist_means, float) or dist_means < 0 or dist_means > 1:
            raise ValueError('\'dist_means\' should be a float in [0,1].')
        if not isinstance(b_sigma, float) or b_sigma < 0 or b_sigma > 1:
            raise ValueError('\'b_sigma\' should be a float in [0,1].')
        if not isinstance(a_sigma, float) or a_sigma < 0 or a_sigma > 1:
            raise ValueError('\'a_sigma\' should be a float in [0,1].')
        #
        self.__dist_means = dist_means
        self.__b_sigma = b_sigma
        self.__a_sigma = a_sigma

    @staticmethod
    def from_dict(dobj):
        return ValuationParams(**dobj)

    def to_dict(self):
        props = ["dist_means", "b_sigma", "a_sigma"]
        return to_dict(self, props)

    @property
    def dist_means(self):
        return self.__dist_means

    @property
    def b_sigma(self):
        return self.__b_sigma

    @property
    def a_sigma(self):
        return self.__a_sigma


class AuctionSetParams():

    def __init__(self, bids, asks, cost_model, valuations):
        self.__bids = bids
        self.__asks = asks
        self.__cost_model = cost_model
        self.__valuations = valuations

    @staticmethod
    def from_dict(dobj):
        bp = BundleParams.from_dict(dobj["bids"])
        ap = BundleParams.from_dict(dobj["asks"])
        cm = CostModelParams.from_dict(dobj["cost_model"])
        vp = ValuationParams.from_dict(dobj["valuations"])
        return AuctionSetParams(bp, ap, cm, vp)

    def to_dict(self):
        return {
            "bids": self.bids.to_dict(),
            "asks": self.asks.to_dict(),
            "cost_model": self.cost_model.to_dict(),
            "valuations": self.valuations.to_dict()
        }

    @staticmethod
    def from_file(filename):
        with open(filename, "r") as f:
            dobj = yaml.load(f)
        return AuctionSetParams.from_dict(dobj)

    def to_file(self, filename):
        with open(filename, "w") as f:
            yaml.dump(self.to_dict(), f)

    @property
    def bids(self):
        return self.__bids

    @property
    def asks(self):
        return self.__asks

    @property
    def cost_model(self):
        return self.__cost_model

    @property
    def valuations(self):
        return self.__valuations
