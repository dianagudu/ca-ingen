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

dataset1 = asg.generate()
dataset2 = asg.generate()

print("[D1] Asks (quantities):\n", dataset1.ask_set.quantities)
print("[D1] Asks (values):", dataset1.ask_set.values)
print("[D1] Bids (quantities):\n", dataset1.bid_set.quantities)
print("[D1] Bids (values):", dataset1.bid_set.values)

print("[D2] Asks (quantities):\n", dataset2.ask_set.quantities)
print("[D2] Asks (values):", dataset2.ask_set.values)
print("[D2] Bids (quantities):\n", dataset2.bid_set.quantities)
print("[D2] Bids (values):", dataset2.bid_set.values)

# todo: scale and round bid quantities to integer values
# add some variance around base prices for the bid set
# create base prices from given parameters
# relate base prices for bids and asks through overlap given means and spreads
