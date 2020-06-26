#!/usr/bin/env python3

import numpy as np

# LRN layer, based on Krizhevsky's paper
def lrn(data, k=2, alpha=0.0001, beta=0.75, n=5):
    data_shape = data.shape
    out = np.zeros(shape=data_shape)
    for filter_index in range(data_shape[0]):
        for y in range(data_shape[1]):
            for x in range(data_shape[2]):
                filter_start = int(max(0, filter_index - n / 2))
                filter_end = int(min(data_shape[0] - 1, filter_index + n / 2))
                cur_sum = 0
                for j in range(filter_start, filter_end):
                    cur_sum += (data[j, y, x]**2)
                final_res = data[filter_index, y, x] / (
                    (k + alpha * cur_sum)**beta)
                out[filter_index, y, x] = final_res
    return out

if __name__ == '__main__':
    N, C, H, W = 4, 96, 55, 55
    out = np.zeros(shape=[C, H, W])
    data = np.random.rand(C, H, W)
    out = lrn(data)
    print(out)
