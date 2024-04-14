"""NVIDIA GPU Modules."""

from __future__ import annotations

import logging
import os
import subprocess

import pynvml  # type: ignore


def get_free_gpus(
    min_free_memory: int = 10240, use_nvidia_smi: bool = False
) -> list:  # Memory in MB
    """Get a list of free GPUs with at least min_free_memory memory available.

    Args:
        min_free_memory (int): Minimum free memory required in MB.
        use_nvidia_smi (bool): Use nvidia-smi to get GPU information.

    Returns:
        list: List of free GPUs."""
    free_gpus = []
    if use_nvidia_smi:
        try:
            # Run nvidia-smi command to get GPU memory usage
            smi_output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=index,memory.free",
                    "--format=csv,noheader,nounits",
                ]
            ).decode("utf-8")

            # Find GPUs with enough free memory
            for line in smi_output.strip().split("\n"):
                gpu_index, free_memory = line.split(",")
                if int(free_memory) >= min_free_memory:
                    free_gpus.append(gpu_index.strip())
        except Exception as e:
            logging.error(f"Error running nvidia-smi: {e}")
    else:
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
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
