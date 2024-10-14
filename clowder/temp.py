import numpy as np


def flatten_numpy(tensor):
    return np.reshape(tensor, (tensor.shape[0], -1))


# Usage example
input_tensor = np.random.rand(2, 3, 4)
flattened_tensor = flatten_numpy(input_tensor)
print(flattened_tensor)
