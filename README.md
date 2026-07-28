# MMCV Build Wheel & PyTorch Packages Compiler Repository

This repository serves as a comprehensive toolset for building and indexing MMCV and PyTorch-based packages with custom CUDA/C++ operations. It includes GitHub workflows to build pre-compiled wheel binaries across Linux and Windows platforms.

## Key Features

1. **PyTorch & MMCV Packages Builder Workflow:**
   - Automates building PyTorch-based packages (including MMCV) with custom C++/CUDA ops for various compute platforms (CUDA, CPU).
   - Custom build patches for Linux and Windows are stored under [`mmc-patch-for-linux-and-windows/`](file:///mnt/c/Users/kpd27/Downloads/torch_packages_builder/mmc-patch-for-linux-and-windows).
   - Uses build attestation to establish provenance for wheels.
   - Publishes built wheel packages to GitHub Releases.

2. **PEP 503 Compliant Package Index Builder Workflow:**
   - Automatically generates a PEP 503 compliant package index from release binaries.
   - Publishes the index via GitHub Pages for direct integration with `pip`.

---

## Usage with Pip

### Using the Package Index

To install packages directly from this repository's package index:

```bash
pip install --extra-index-url https://thrivex2025.github.io/MMCV-BUILD-WHEEL <your package list>
```

### Using Specific Package Links

To install from specific package subdirectories:

```bash
pip install --find-links https://thrivex2025.github.io/MMCV-BUILD-WHEEL/<pep 503 normalized name>/ <your package list>
```

For example:

```bash
pip install --find-links https://thrivex2025.github.io/MMCV-BUILD-WHEEL/mmcv/ mmcv
```

### Local Installation

You can also download built wheel binaries and install them locally:

```bash
pip install <path-to-wheel-file>.whl
```

The repository uses the following versioning scheme:

```bash
<package_name>-<version>+<OPTIONAL_commit_hash>pt<PyTorch_version><compute_platform>
```

Where `<compute_platform>` corresponds to `cpu` or `cu<CUDA_version>` (e.g. `cu121`, `cu124`).

### Example Installation Command

```bash
pip install mmcv==2.2.0+pt2.5.0cu121
```

---

## Supported Combinations

- **OS:** Linux, Windows
- **PyTorch:** `2.3.0` – `2.13.0`
- **Patches:** Includes MMCV patches for Python 3.13+ and PyTorch 2.13+ C++20 on Windows in [`mmc-patch-for-linux-and-windows/`](file:///mnt/c/Users/kpd27/Downloads/torch_packages_builder/mmc-patch-for-linux-and-windows).

---

## Pitfalls

- **No Support for Pip Cache:**
  `pip` relies on HTTP caching, but GitHub generates dynamic redirections for release assets. Use `--no-cache-dir` if you encounter caching issues during installation.

## Credits

Special thanks to <https://github.com/rusty1s/pytorch_cluster>.
