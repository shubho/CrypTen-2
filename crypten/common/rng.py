#!/usr/bin/env python3
import crypten
import torch


def generate_random_ring_element(size, ring_size=(2 ** 64)):
    # TODO (brianknott): Check whether this RNG contains the full range we want.
    return torch.randint(
        -(ring_size // 2), (ring_size - 1) // 2, size, dtype=torch.long
    )


def generate_kbit_random_tensor(size, bitlength=crypten.common.constants.K):
    """Helper function to generate a random k-bit number"""
    if bitlength == 64:
        return generate_random_ring_element(size)
    return torch.randint(0, 2 ** bitlength, size, dtype=torch.long)