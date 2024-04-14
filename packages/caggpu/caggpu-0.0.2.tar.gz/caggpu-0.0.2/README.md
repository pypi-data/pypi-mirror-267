# GPU Utility Package

This Python module provides tools for managing GPUs in a machine learning or high-performance computing environment. It allows users to identify free GPUs with a specified amount of available memory and optionally set the `CUDA_VISIBLE_DEVICES` or other required gpu environment variable to use those GPUs.

## Features

- **Check for Free GPUs**: Determine which GPUs on the system have a minimum specified amount of free memory.
- **Set CUDA Environment**: Automatically set the `CUDA_VISIBLE_DEVICES` environment variable to use GPUs that meet the memory requirements.

## Requirements

- Python 3.8 or higher
- `pynvml`: Python bindings for the NVIDIA Management Library
- `subprocess` module (standard in Python)

## Usage

**Getting Free GPUs**
You can retrieve a list of GPUs that have at least a specified amount of free memory. You can specify whether to use the NVIDIA System Management Interface (nvidia-smi) or the NVML library.

```
from gpu_modules import get_free_gpus

# Get free GPUs with at least 10 GB of free memory using NVML
free_gpus = get_free_gpus(10240)
print("Free GPUs:", free_gpus)

# Alternatively, use nvidia-smi to check for free GPUs
free_gpus_smi = get_free_gpus(10240, use_nvidia_smi=True)
print("Free GPUs using nvidia-smi:", free_gpus_smi)

```

## Setting CUDA Visible Devices
To set the CUDA_VISIBLE_DEVICES environment variable automatically based on free memory:
```
from gpu_modules import set_cuda_visible_devices

# Set CUDA_VISIBLE_DEVICES for GPUs with at least 10 GB free memory
if set_cuda_visible_devices(10240):
    print("CUDA_VISIBLE_DEVICES set successfully.")
else:
    print("No free GPUs available.")

```

## Contributing
Contributions to this project are welcome. Please submit a pull request or open an issue to discuss proposed changes or report bugs.