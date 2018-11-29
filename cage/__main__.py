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

dataset1.save("/tmp/dataset1")
dataset2.save("/tmp/dataset2")

# todo: scale and round bid quantities to integer values
# add some variance around base prices for the bid set
# create base prices from given parameters
# relate base prices for bids and asks through overlap given means and spreads
