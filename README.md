# MMCV & OpenCV Package Builder Repository

This repository serves as a comprehensive toolset for building and indexing `mmcv` and `opencv-python` (with GStreamer & FFmpeg hardware acceleration) binaries. It includes GitHub workflows to build pre-compiled wheel binaries across Linux and Windows platforms as well as Debian (`.deb`) packages.

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

## How to Trigger the GitHub Action Workflow

The workflow file is located at [`.github/workflows/build_package.yml`](file:///.github/workflows/build_package.yml).

### Method A: Via GitHub Web Interface

1. Go to your repository on GitHub (**`ThriveX2025/MMCV-BUILD-WHEEL`**).
2. Click the **Actions** tab.
3. Select **Build Package** from the left sidebar.
4. Click **Run workflow** on the top right.

#### Building `opencv-python` (OpenCV with GStreamer)
- **`repo`**: Select `opencv-python`
- **`repo-tag`**: Branch or tag (e.g. `master` or `4.10.0.84`; leave empty for default)
- **`limit-python`**: Targeted Python versions (e.g. `3.12` or `3.10,3.11,3.12`)
- **`torch-version`**: *(Ignored for OpenCV)*
- **`linux-wheels`**: Keep checked (`true`)

#### Building `mmcv` (PyTorch C++/CUDA ops)
- **`repo`**: Select `mmcv`
- **`repo-tag`**: Tag (e.g. `v2.2.0`)
- **`torch-version`**: PyTorch version(s) (e.g. `2.5.0` or `2.4.0,2.5.0`)
- **`limit-python`**: Target Python versions (e.g. `3.12` or `3.10,3.11,3.12`)
- **`limit-compute-platform`**: Target compute platform (e.g. `cu121`, `cu124`, `cpu`)

---

### Method B: Via GitHub CLI (`gh`)

```bash
# Trigger OpenCV with GStreamer build for Python 3.12
gh workflow run build_package.yml -f repo=opencv-python -f limit-python=3.12

# Trigger MMCV build for PyTorch 2.5.0 and CUDA 12.1
gh workflow run build_package.yml -f repo=mmcv -f torch-version=2.5.0 -f limit-compute-platform=cu121
```

---

## Installation Guide

### Option 1: Installation via Pip (Package Index)

Install built wheel packages directly from this repository's PEP 503 package index:

```bash
pip install --extra-index-url https://thrivex2025.github.io/MMCV-BUILD-WHEEL mmcv
```

### Option 2: Installing OpenCV GStreamer Debian Package

Download the generated `opencv-python-gstreamer.deb` package from GitHub Releases or the package index, then run:

```bash
sudo apt update
sudo apt install ./opencv-python-gstreamer.deb
```

*This automatically installs system dependencies (`libgstreamer1.0-dev`, `gstreamer1.0-plugins-good`, `libavcodec-extra`, etc.) and places the pre-built wheel file under `/opt/opencv_custom_wheel/` for virtual environment use.*

---

## Supported Combinations

- **OS:** Linux (`ubuntu-22.04`), Windows (`windows-2022`)
- **PyTorch:** `2.3.0` – `2.13.0` (for `mmcv`)
- **OpenCV:** GStreamer 1.0 & FFmpeg accelerated builds (for `opencv-python`)

---

## Pitfalls

- **No Support for Pip Cache:**
  `pip` relies on HTTP caching, but GitHub generates dynamic redirections for release assets. Use `--no-cache-dir` if you encounter caching issues during installation.
