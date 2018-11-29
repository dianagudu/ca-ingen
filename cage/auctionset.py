import numpy as np
import yaml
from time import time

from .bidset import BidSetGenerator
from .bidset import BidSetParams
from .bidset import BidSet_Type


class AuctionSet():

    def __init__(self, bid_set, ask_set, params):
        self.__bid_set = bid_set
        self.__ask_set = ask_set
        self.__params = params

    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            dobj = yaml.load(f)
        return AuctionSet.from_dict(dobj)

    def save(self, filename):
        with open(filename, "w") as f:
            yaml.dump(self.to_dict(), f)

    @staticmethod
    def from_dict(dobj):
        return AuctionSet(dobj["bids"].from_dict(),
                          dobj["asks"].from_dict(),
                          dobj["params"].from_dict())

    def to_dict(self):
        return {
            "params": self.params.to_dict(),
            "bids": self.bid_set.to_dict(),
            "asks": self.ask_set.to_dict()
        }

    @property
    def bid_set(self):
        return self.__bid_set

    @property
    def ask_set(self):
        return self.__ask_set

    @property
    def params(self):
        return self.__params


class AuctionSetGenerator():

    def __init__(self, params):
        self.__params = params
        self.__bidset_params = BidSetParams.from_auction_set_params(
            params, BidSet_Type.BIDS
        )
        self.__askset_params = BidSetParams.from_auction_set_params(
            params, BidSet_Type.ASKS
        )

    def generate(self):
        # generate bids and asks
        bid_set = BidSetGenerator.generate(self.bidset_params)
        ask_set = BidSetGenerator.generate(self.askset_params)

        return AuctionSet(bid_set, ask_set, self.params)

    @property
    def params(self):
        return self.__params

    @property
    def bidset_params(self):
        return self.__bidset_params

    @property
    def askset_params(self):
        return self.__askset_params
