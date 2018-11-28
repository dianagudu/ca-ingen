import numpy as np
from time import time

from .bidset import BidSetGenerator
from .bidset import BidSetParams
from .bidset import BidSet_Type


class AuctionSet():

    def __init__(self, bid_set, ask_set):
        self.__bid_set = bid_set
        self.__ask_set = ask_set

    def load(self, filename):
        pass

    def save(self, filename):
        pass

    @property
    def bid_set(self):
        return self.__bid_set

    @property
    def ask_set(self):
        return self.__ask_set


class AuctionSetGenerator():

    def __init__(self, params):
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

        return AuctionSet(bid_set, ask_set)

    @property
    def bidset_params(self):
        return self.__bidset_params

    @property
    def askset_params(self):
        return self.__askset_params
