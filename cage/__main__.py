import numpy as np

from operator import add

from ingen.model import Model
from ingen.binning import RegularBinning

from .bidset import BidSetGenerator


model = Model.from_file("/tmp/a")
bing = RegularBinning(8, model.binning.domain)
amount = 5
base_prices = np.array([1., 2., 0.5])
new_domain = (np.array(bing.counts) + 0.5) * 4

bidset = BidSetGenerator.generate(model, bing, amount,
                                  new_domain, base_prices, sigma=0.1)

np.set_printoptions(precision=4)
print("Quantities:\n", bidset.quantities)
print("Base prices:", base_prices)
print("Bid values:", bidset.values)

# todo: scale and round bid quantities to integer values
# add some variance around base prices for the bid set
# create base prices from given parameters
# relate base prices for bids and asks through overlap given means and spreads
