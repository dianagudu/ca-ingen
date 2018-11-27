import yaml
from enum import Enum

from ingen.helper import to_dict


class Resources_Rel_Types(Enum):
    RANDOM = 1
    SAME = 2
    SCARCITY = 3


class BidSetParams():

    def __init__(self, amount, model_file,
                 binning_type, binning_counts, domain):
        self.__amount = amount
        self.__model_file = model_file
        self.__binning_type = binning_type
        self.__binning_counts = binning_counts
        self.__domain = domain

    def to_dict(self):
        props = ["amount", "model_file", "binning_type",
                 "binning_counts", "domain"]
        return to_dict(self, props)

    @staticmethod
    def from_dict(dobj):
        return BidSetParams(**dobj)

    @property
    def amount(self):
        return self.__amount

    @property
    def model_file(self):
        return self.__model_file

    @property
    def binning_type(self):
        return self.__binning_type

    @property
    def binning_counts(self):
        return self.__binning_counts

    @property
    def domain(self):
        return self.__domain


class ValuationsParams():

    def __init__(self, dist_means, b_sigma, a_sigma, resource_rel):
        self.__dist_means = dist_means
        self.__b_sigma = b_sigma
        self.__a_sigma = a_sigma
        self.__resource_rel = resource_rel

    @staticmethod
    def from_dict(dobj):
        return ValuationsParams(**dobj)

    def to_dict(self):
        props = ["dist_means", "b_sigma", "a_sigma", "resource_rel"]
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

    @property
    def resource_rel(self):
        return self.__resource_rel


class AuctionSetParams():

    def __init__(self, bids, asks, valuations):
        self.__bids = bids
        self.__asks = asks
        self.__valuations = valuations

    @staticmethod
    def from_dict(dobj):
        bp = BidSetParams.from_dict(dobj["bids"])
        ap = BidSetParams.from_dict(dobj["asks"])
        vp = ValuationsParams.from_dict(dobj["valuations"])
        return AuctionSetParams(bp, ap, vp)

    def to_dict(self):
        dobj = {
            "bids": self.bids.to_dict(),
            "asks": self.asks.to_dict(),
            "valuations": self.valuations.to_dict()
        }
        return dobj

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
    def valuations(self):
        return self.__valuations

