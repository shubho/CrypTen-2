#!/usr/bin/env python3

import crypten.common.constants as constants
import torch


class Communicator:
    """
    Abstract class defining the functions that a Communicator should implement.
    """

    def initialize(self, **kwargs):
        """Initializes the communicator. Call this function before using it."""
        pass

    def send(self, tensor, dst):
        """Sends the specified tensor to the destination dst."""
        raise NotImplementedError("send is not implemented")

    def recv(self, tensor, src=None):
        """Receives a tensor from an (optional) source src."""
        raise NotImplementedError("recv is not implemented")

    def scatter(self, scatter_list, src, size=None, async_op=False):
        """Scatters a list of tensors to all parties."""
        raise NotImplementedError("scatter is not implemented")

    def reduce(self, tensor, op=None, async_op=False):
        """Reduces the tensor data across all parties."""
        raise NotImplementedError("tensor is not implemented")

    def all_reduce(self, tensor, op=None, async_op=False):
        """Reduces the tensor data across all parties; all get the final result."""
        raise NotImplementedError("tensor is not implemented")

    def gather(self, tensor, dst, async_op=False):
        """Gathers a list of tensors in a single party."""
        raise NotImplementedError("gather is not implemented")

    def all_gather(self, tensor, async_op=False):
        """Gathers tensors from all parties in a list."""
        raise NotImplementedError("all_gather is not implemented")

    def broadcast(self, tensor, src, async_op=False):
        """Broadcasts the tensor to all parties."""
        raise NotImplementedError("broadcast is not implemented")

    def get_world_size(self):
        """Returns the size of the world."""
        raise NotImplementedError("get_world_size is not implemented")

    def get_rank(self):
        """Returns the rank of the current process."""
        raise NotImplementedError("get_rank is not implemented")

    def reset_communication_stats(self):
        """Resets communication statistics."""
        raise NotImplementedError("reset_communication_stats is not implemented")

    def print_communication_stats(self):
        """Prints communication statistics."""
        raise NotImplementedError("print_communication_stats is not implemented")

    def _log_communication(self, nelement):
        """Updates log of communication statistics."""
        raise NotImplementedError("_log_communication is not implemented")


def _logging(func):
    """Decorator that performs logging of communication statistics."""

    def logging_wrapper(self, *args, **kwargs):

        # hack the inputs into some of the functions:
        if self.state["world_size"] < 2:
            if func.__name__ in ["gather", "all_gather"]:
                return [args[0]]
            else:
                return args[0]

        # only log if needed:
        if constants.VERBOSE:
            if isinstance(args[0], (list, tuple)):  # N - 1 tensors communicated
                self._log_communication(args[0][0].nelement() * (len(args[0]) - 1))
            elif torch.is_tensor(args[0]):  # one tensor communicated
                self._log_communication(args[0].nelement())
        return func(self, *args, **kwargs)

    return logging_wrapper