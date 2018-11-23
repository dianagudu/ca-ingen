from ingen.model import Model

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
        self.__b_model = Model.from_file(params.b_model_file)
        self.__a_model = Model.from_file(params.a_model_file)
        #create binning from binning types

    def generate(self):

        bid_set = BidSetGenerator.generate(self.b_model, self.b_binning,
                                           self.params.b_amount,
                                           self.params.b_domain, bbasep, bsigma)
        ask_set = BidSetGenerator.generate(self.a_model, self.a_binning,
                                           self.params.a_amount,
                                           self.params.a_domain, abasep, asigma)

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


class AuctionSetParams():

    def __init__(self, b_amount, a_amount,
                 b_model_file, a_model_file,
                 b_binning_type, a_binning_type,
                 b_domain, a_domain):
        self.__b_amount = b_amount
        self.__a_amount = a_amount
        self.__b_model_file = b_model_file
        self.__a_model_file = a_model_file
        self.__b_binning_type = b_binning_type
        self.__a_binning_type = a_binning_type
        self.__b_domain = b_domain
        self.__a_domain = a_domain

    @property
    def b_amount(self):
        return self.__b_amount

    @property
    def a_amount(self):
        return self.__a_amount

    @property
    def b_model_file(self):
        return self.__b_model_file

    @property
    def a_model_file(self):
        return self.__a_model_file

    @property
    def b_binning_type(self):
        return self.__b_binning_type

    @property
    def a_binning_type(self):
        return self.__a_binning_type

    @property
    def b_domain(self):
        return self.__b_domain

    @property
    def a_domain(self):
        return self.__a_domain
