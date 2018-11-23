
import numpy as np

class BasePrices():

    def __init__(self, res_amount, params):
        self.__values = np.random.rand(res_amount)