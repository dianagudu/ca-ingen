import numpy as np

from ingen.model import Model
from ingen.binning import BinningGenerator

from .bidset import BidSetGenerator


class AuctionSet():

    def __init__(self, bid_set, ask_set):
        self.__bid_set = bid_set
        self.__ask_set = ask_set

    @property
    def bid_set(self):
        return self.__bid_set

    @property
    def ask_set(self):
        return self.__ask_set

    def load(self, filename):
        pass

    def save(self, filename):
        pass


class AuctionSetGenerator():

    def __init__(self, params):
        self.__params = params

        # load models from files
        self.__b_model = Model.from_file(params.bids.model_file)
        self.__a_model = Model.from_file(params.asks.model_file)

        # create binnings from binning types
        self.__b_binning = BinningGenerator.generate(
            params.bids.binning_type,
            params.bids.binning_counts,
            self.__b_model.binning.domain)
        self.__a_binning = BinningGenerator.generate(
            params.asks.binning_type,
            params.asks.binning_counts,
            self.__a_model.binning.domain)

        # create base prices and spreads
        # https://www.rasch.org/rmt/rmt101r.htm
        base_prices = np.random.rand(self.b_binning.dimensions)
        md = min(self.params.valuations.b_sigma,
                 self.params.valuations.a_sigma) * \
            self.params.valuations.dist_means
        self.__b_base_prices = base_prices + md / 2.
        self.__a_base_prices = base_prices - md / 2.

        print("bid [base prices]:", self.b_base_prices)
        print("ask [base prices]:", self.a_base_prices)

    def generate(self):
        bid_set = BidSetGenerator.generate(self.b_model,
                                           self.b_binning,
                                           self.params.bids.amount,
                                           self.params.bids.domain,
                                           self.b_base_prices,
                                           self.params.valuations.b_sigma)
        ask_set = BidSetGenerator.generate(self.a_model,
                                           self.a_binning,
                                           self.params.asks.amount,
                                           self.params.asks.domain,
                                           self.a_base_prices,
                                           self.params.valuations.a_sigma)

        return AuctionSet(bid_set, ask_set)

    @property
    def params(self):
        return self.__params

    @property
    def b_model(self):
        return self.__b_model

    @property
    def a_model(self):
        return self.__a_model

    @property
    def b_binning(self):
        return self.__b_binning

    @property
    def a_binning(self):
        return self.__a_binning

    @property
    def b_base_prices(self):
        return self.__b_base_prices

    @property
    def a_base_prices(self):
        return self.__a_base_prices
