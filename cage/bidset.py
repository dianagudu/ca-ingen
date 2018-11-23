import numpy as np

from ingen.bundles import BundleGenerator


class BidSet():

    def __init__(self, quantities, values):
        self.__quantities = quantities
        self.__values = values

    @property
    def quantities(self):
        return self.__quantities

    @property
    def values(self):
        return self.__values


class BidSetGenerator():

    @staticmethod
    def __gen_bundles(model, binning, amount, new_domain):
        # generate amount bundles using given model
        bundles = BundleGenerator(model, binning).generate(amount)

        # rescale quantities to new domain and round to integer values
        scaling_factors = np.array(new_domain) / np.array(bundles.domain)
        quantities = np.multiply(bundles.data, scaling_factors)
        quantities = np.round(quantities)

        return quantities

    @staticmethod
    def __gen_values(quantities, base_prices, sigma):
        # compute additive valuation
        # todo: super-additive valuation?
        values = np.matmul(quantities, base_prices)

        # add some variance for each bid, e.g. spread around base prices
        # var is obtained from normal distribution around origin
        #     represented as % of valuation
        var = np.random.randn(values.shape[0]) * sigma
        values = values + np.multiply(values, var)

        return values

    @staticmethod
    def generate(model, binning, amount, new_domain, base_prices, sigma=1):
        quantities = BidSetGenerator.__gen_bundles(model, binning,
                                                   amount, new_domain)
        values = BidSetGenerator.__gen_values(quantities,
                                              base_prices, sigma)

        return BidSet(quantities, values)
