import numpy as np
import scipy
from scipy import sparse
from warnings import warn


def get_type(counts):
    return counts.dtype

# NEED TO FIND A BETTER WAY TO DO THE INTEGER CHECK
def find_type_max(counts):
    curr_counts = counts
    # Convert to numpy array
    if sparse.issparse(counts):
        curr_counts = counts.toarray()
    elif not isinstance(counts, np.ndarray):
        curr_counts = np.array(counts)

    # Check if the counts are integers or nan. If they are neither, throw
    # a warning and return np.float64.
    if not np.array_equal(curr_counts[~np.isnan(curr_counts)],
                          curr_counts[~np.isnan(curr_counts)].round()):
      warn("Counts matrix must only contain integers or NaN")
      return np.float64

    # We know the type is int, so just check which integer type we need to
    # return based on the size of the max integer
    max_num = np.max(curr_counts)
   
    if max_num > 4294967295:
        the_dtype = np.uint64
    elif max_num > 65535 and max_num <= 4294967295:
        the_dtype = np.uint32
    else:
         the_dtype = np.uint16

    return the_dtype
