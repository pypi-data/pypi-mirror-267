"""NVIDIA GPU Modules."""

from __future__ import annotations

import os

import pynvml  # type: ignore


def get_free_gpus(min_free_memory: int = 10240) -> list:  # Memory in MB
    """Get a list of free GPUs with at least min_free_memory memory available.

    Args:
        min_free_memory (int): Minimum free memory required in MB.

    Returns:
        list: List of free GPUs."""
    pynvml.nvmlInit()
    count = pynvml.nvmlDeviceGetCount()
    free_gpus = []
    for i in range(count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        if mem_info.free / 1024**2 >= min_free_memory:
            free_gpus.append(str(i))
    return free_gpus


def set_cuda_visible_devices(min_free_memory: int = 10240) -> bool:
    """Set CUDA_VISIBLE_DEVICES to free GPUs with at least min_free_memory memory available.

    Args:
        min_free_memory (int): Minimum free memory required in MB.

    Returns:
        bool: True if free GPUs are available, False otherwise."""

    free_gpus = get_free_gpus(min_free_memory)

    if free_gpus:
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(free_gpus)
        return True
    return False
