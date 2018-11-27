import numpy as np

from operator import add

from ingen.model import Model
from ingen.binning import RegularBinning

from .bidset import BidSetGenerator
from .params import AuctionSetParams
from .auctionset import AuctionSetGenerator

asp = AuctionSetParams.from_file("/tmp/auction_set_params")
asp.to_file("/tmp/asp2")

asg = AuctionSetGenerator(asp)

dataset = asg.generate()

print("Asks (quantities):\n", dataset.ask_set.quantities)
print("Asks (values):", dataset.ask_set.values)

print("Bids (quantities):\n", dataset.bid_set.quantities)
print("Bids (values):", dataset.bid_set.values)

# todo: scale and round bid quantities to integer values
# add some variance around base prices for the bid set
# create base prices from given parameters
# relate base prices for bids and asks through overlap given means and spreads
