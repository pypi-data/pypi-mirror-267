"""Package containing your_project name."""

from __future__ import annotations

from .nvidia_cuda import get_free_gpus, set_cuda_visible_devices

__all__ = ["get_free_gpus", "set_cuda_visible_devices"]
__version__ = "0.0.2"
