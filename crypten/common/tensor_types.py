#!/usr/bin/env python3
import torch


# helper functions that determine if input is float, int, or base tensor:
def _is_type_tensor(tensor, types):
    """Checks whether the elements of the input tensor are of a given type"""
    if torch.is_tensor(tensor):
        if any(tensor.dtype == type_ for type_ in types):
            return True
    return False


def is_float_tensor(tensor):
    """Checks if the input tensor is a Torch tensor of a float type."""
    return _is_type_tensor(tensor, [torch.float16, torch.float32, torch.float64])


def is_int_tensor(tensor):
    """Checks if the input tensor is a Torch tensor of an int type."""
    return _is_type_tensor(
        tensor, [torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64]
    )