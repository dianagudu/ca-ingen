import numpy as np

from operator import add

from ingen.model import Model
from ingen.binning import RegularBinning

from .bidset import BidSetGenerator
from .params import AuctionSetParams
from .auctionset import AuctionSetGenerator
from .auctionset import AuctionSet

asp = AuctionSetParams.from_file("example_auction_set_params")
asp.to_file("/tmp/asp2")

asg = AuctionSetGenerator(asp)

dataset1 = asg.generate()
dataset2 = asg.generate()

dataset1.save("/tmp/dataset1")
dataset2.save("/tmp/dataset2")

dataset3 = AuctionSet.load("/tmp/dataset1")
dataset3.save("/tmp/dataset3")
