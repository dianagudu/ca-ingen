import numpy as np
import yaml

from ingen.helper import to_dict


class BundleParams():

    def __init__(self, amount, model_file, domain,
                 binning_type, binning_counts):
        self.__amount = amount
        self.__model_file = model_file
        self.__domain = domain
        self.__binning_type = binning_type
        self.__binning_counts = binning_counts

    def to_dict(self):
        props = ["amount", "model_file", "domain",
                 "binning_type", "binning_counts"]
        return to_dict(self, props)

    @staticmethod
    def from_dict(dobj):
        return BundleParams(**dobj)

    @property
    def amount(self):
        return self.__amount

    @property
    def model_file(self):
        return self.__model_file

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
        self.__slope = slope
        self.__fixed = fixed

    @staticmethod
    def from_dict(dobj):
        return CostModelParams(np.array(dobj["slope"]),
                               np.array(dobj["fixed"]))

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
