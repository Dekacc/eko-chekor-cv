# Code copied from: https://stackoverflow.com/questions/38250710/how-to-split-data-into-3-sets-train-validation-and-test
import numpy as np


def split_dataset(arr):
    """ Splits the dataset to 80% training, 10% validation, 10% test """
    return np.split(arr, [int(.8*len(arr)), int(.9*len(arr))])


def one_hot_encode(str):
    if str == 'FITS IN A BAG':
        return [1, 0, 0, 0]
    elif str == 'FITS IN A WHEELBARROW':
        return [0, 1, 0, 0]
    elif str == 'CAR NEEDED':
        return [0, 0, 1, 0]
    elif str == 'CLEANED':
        return [0, 0, 0, 1]
