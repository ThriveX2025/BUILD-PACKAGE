import json
import os
from dataclasses import dataclass
from itertools import product


@dataclass
class TorchRelease:
    python_versions: tuple
    compute_platforms: tuple


LINUX_X64 = "ubuntu-22.04"
WINDOWS_X64 = "windows-2022"
MACOS_ARM64 = "macos-15"

TORCH_RELEASES = {
    "2.3.0": TorchRelease(("3.8", "3.9", "3.10", "3.11", "3.12"), ("cpu", "cu118", "cu121", "rocm6.0")),
    "2.3.1": TorchRelease(("3.8", "3.9", "3.10", "3.11", "3.12"), ("cpu", "cu118", "cu121", "rocm6.0")),
    "2.4.0": TorchRelease(("3.8", "3.9", "3.10", "3.11", "3.12"), ("cpu", "cu118", "cu121", "cu124", "rocm6.1")),
    "2.4.1": TorchRelease(("3.8", "3.9", "3.10", "3.11", "3.12"), ("cpu", "cu118", "cu121", "cu124", "rocm6.1")),
    "2.5.0": TorchRelease(("3.9", "3.10", "3.11", "3.12", "3.13"), ("cpu", "cu118", "cu121", "cu124", "rocm6.2")),
    "2.5.1": TorchRelease(("3.9", "3.10", "3.11", "3.12", "3.13"), ("cpu", "cu118", "cu121", "cu124", "rocm6.2")),
    "2.6.0": TorchRelease(("3.9", "3.10", "3.11", "3.12", "3.13"), ("cpu", "cu118", "cu124", "cu126", "rocm6.2.4")),
    "2.7.0": TorchRelease(("3.9", "3.10", "3.11", "3.12", "3.13"), ("cpu", "cu118", "cu126", "cu128", "rocm6.3")),
    "2.7.1": TorchRelease(("3.9", "3.10", "3.11", "3.12", "3.13"), ("cpu", "cu118", "cu126", "cu128", "rocm6.3")),
    "2.8.0": TorchRelease(("3.9", "3.10", "3.11", "3.12", "3.13"), ("cpu", "cu126", "cu128", "cu129", "rocm6.4")),
    "2.9.0": TorchRelease(
        ("3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"), ("cpu", "cu126", "cu128", "cu130", "rocm6.4")
    ),
    "2.9.1": TorchRelease(
        ("3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"), ("cpu", "cu126", "cu128", "cu130", "rocm6.4")
    ),
    "2.10.0": TorchRelease(
        ("3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"), ("cpu", "cu126", "cu128", "cu130", "rocm7.1")
    ),
    "2.11.0": TorchRelease(
        ("3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"), ("cpu", "cu126", "cu128", "cu130", "rocm7.2")
    ),
    "2.12.0": TorchRelease(
        ("3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"), ("cpu", "cu126", "cu130", "cu132", "rocm7.2")
    ),
    "2.13.0": TorchRelease(
        ("3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"), ("cpu", "cu126", "cu130", "cu132", "rocm7.2")
    ),
}


def add_os(oses_list: list, os_name: str, os_env_var: str):
    if os.environ[os_env_var] == "true":
        oses_list.append(os_name)


def main():
    repo_raw = os.environ.get("REPO", "mmcv").strip()
    repo_map = {
        "mmcv": "open-mmlab/mmcv",
        "open-mmlab/mmcv": "open-mmlab/mmcv",
        "opencv-python": "opencv/opencv-python",
        "opencv/opencv-python": "opencv/opencv-python",
        "mmaction2": "open-mmlab/mmaction2",
        "open-mmlab/mmaction2": "open-mmlab/mmaction2",
    }

    if repo_raw not in repo_map:
        raise ValueError(f"Invalid repository '{repo_raw}'. Allowed repositories are: 'mmcv', 'opencv-python', 'mmaction2'")

    repo_name = repo_map[repo_raw]

    limit_python = os.environ.get("LIMIT_PYTHON")
    if limit_python:
        limit_python = limit_python.split(",")
    limit_compute_platform = os.environ.get("LIMIT_COMPUTE_PLATFORM")
    if limit_compute_platform:
        limit_compute_platform = limit_compute_platform.split(",")

    if repo_name == "opencv/opencv-python":
        py_versions = limit_python if limit_python else ["3.10", "3.11", "3.12", "3.13"]
        jobs = []
        if os.environ.get("LINUX_WHEELS", "true") == "true":
            for py_ver in py_versions:
                for runner_os in ["ubuntu-24.04", "ubuntu-22.04"]:
                    jobs.append({
                        "os": runner_os,
                        "torch-version": "2.5.0",
                        "python-version": py_ver,
                        "compute-platform": "cpu",
                    })
        if not jobs:
            raise RuntimeError("No jobs to do for opencv-python")
        print(json.dumps({"include": jobs}))
        return

    torch_versions = os.environ.get("TORCH_VERSION", "2.5.0").split(",")
    oses_names = []
    add_os(oses_names, LINUX_X64, "LINUX_WHEELS")
    add_os(oses_names, WINDOWS_X64, "WINDOWS_WHEELS")
    add_os(oses_names, MACOS_ARM64, "MACOS_WHEELS")
    if not oses_names:
        raise RuntimeError("Select at least one OS")

    jobs = []
    for torch_version in torch_versions:
        for os_name, python_version, compute_platform in product(
            oses_names, TORCH_RELEASES[torch_version].python_versions, TORCH_RELEASES[torch_version].compute_platforms
        ):
            if os_name == MACOS_ARM64 and compute_platform != "cpu":
                continue
            if compute_platform.startswith("rocm"):
                continue

            if limit_python and python_version not in limit_python:
                continue
            if limit_compute_platform and compute_platform not in limit_compute_platform:
                continue

            if torch_version.startswith("2.5") and python_version == "3.13" and os_name != LINUX_X64:
                continue

            pv = [int(x) for x in python_version.replace("t", "").split(".")]
            if os_name == MACOS_ARM64 and pv[1] <= 9:
                continue

            jobs.append({
                "os": os_name,
                "torch-version": torch_version,
                "python-version": python_version,
                "compute-platform": compute_platform,
            })

    if not jobs:
        raise RuntimeError("No jobs to do")

    strategy_matrix = {"include": jobs}
    print(json.dumps(strategy_matrix))


if __name__ == "__main__":
    main()
