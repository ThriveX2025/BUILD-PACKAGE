# MMCV & OpenCV Package Builder Repository

This repository serves as a comprehensive toolset for building and indexing `mmcv` and `opencv-python` (with GStreamer & FFmpeg acceleration) binaries. It includes GitHub workflows to build pre-compiled wheel binaries across Linux and Windows platforms as well as Debian (`.deb`) packages.

## Key Features

1. **Package Builder Workflow (`build_package.yml`):**
   - Automates building PyTorch & OpenCV packages (`mmcv` and `opencv-python`).
   - For `opencv-python`, builds custom OpenCV wheels with GStreamer (`-DWITH_GSTREAMER=ON`) and FFmpeg (`-DWITH_FFMPEG=ON`) support on Linux, and packages the output into a `.deb` package (`opencv-python-gstreamer.deb`).
   - Custom build patches for Linux and Windows are stored under [`mmc-patch-for-linux-and-windows/`](file:///mnt/d/PROJECTS/WHEEL-BUILDER/mmc-patch-for-linux-and-windows).
   - Uses build attestation to establish provenance for wheels and packages.
   - Publishes built wheel packages and `.deb` files to GitHub Releases.

2. **PEP 503 Compliant Package Index Builder Workflow:**
   - Automatically generates a PEP 503 compliant package index from release binaries (`.whl` and `.deb`).
   - Publishes the index via GitHub Pages for direct integration with `pip` and package management.

---

## Allowed Repositories

The workflow dispatch is locked to accept:
- `mmcv` (OpenMMLab MMCV)
- `opencv-python` (OpenCV Python with GStreamer and FFmpeg support)

---

## Usage with Pip & Apt

### Using the Package Index

To install packages directly from this repository's package index:

```bash
pip install --extra-index-url https://thrivex2025.github.io/MMCV-BUILD-WHEEL <your package list>
```

### Installing OpenCV GStreamer Debian Package

To install the system dependencies and custom OpenCV wheel via the generated `.deb` package:

```bash
sudo apt update
sudo apt install ./opencv-python-gstreamer.deb
```

---

## Supported Combinations

- **OS:** Linux, Windows
- **PyTorch:** `2.3.0` – `2.13.0` (for `mmcv`)
- **OpenCV:** GStreamer 1.0 & FFmpeg accelerated builds (for `opencv-python`)

---

## Pitfalls

- **No Support for Pip Cache:**
  `pip` relies on HTTP caching, but GitHub generates dynamic redirections for release assets. Use `--no-cache-dir` if you encounter caching issues during installation.

