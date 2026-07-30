#! /bin/bash

set -eu -o pipefail

SCRIPT_DIR=${BASH_SOURCE%/*}

if [[ $REPO == "facebookresearch/pytorch3d" ]]; then
  if [[ $COMPUTE_PLATFORM == "cu118" ]] && [[ $OS == "Windows" ]]; then
    CUB_VERSION="1.17.2"
    mkdir cub
    curl -L https://github.com/NVIDIA/cub/archive/${CUB_VERSION}.tar.gz | tar -xzf - --strip-components=1 --directory cub
    echo "CUB_HOME=$PWD/cub" >> "$GITHUB_ENV"
  fi
fi

if [[ $REPO == "facebookresearch/fairseq" ]]; then
  pip install cython

  # Fix 'std': ambiguous symbol error in compiled_autograd.h when compiling CUDA extensions on Windows
  # https://github.com/pytorch/pytorch/issues/173232
  if [[ $OS == "Windows" ]] && [[ $COMPUTE_PLATFORM != "cpu" ]]; then
    COMPILED_AUTOGRAD="$(python -c 'import torch, os; print(os.path.dirname(torch.__file__))')/include/torch/csrc/dynamo/compiled_autograd.h"
    sed -i 's/#if defined(_WIN32) && (defined(USE_CUDA) || defined(USE_ROCM))/#if defined(_WIN32) \&\& defined(__NVCC__)/' "$COMPILED_AUTOGRAD"
  fi
fi

if [[ $REPO == "NVlabs/tiny-cuda-nn" ]]; then
  source "$SCRIPT_DIR"/.github/workflows/cuda/${OS}_env.sh
  echo "LIBRARY_PATH=/usr/local/cuda/lib64/stubs" >> "$GITHUB_ENV"
  echo "TCNN_CUDA_ARCHITECTURES=${TORCH_CUDA_ARCH_LIST}" | sed "s/\(\.\|\+PTX\)//g" >> "$GITHUB_ENV"

  SETUPTOOLS_VERSION=$(pip show setuptools | grep '^Version:' | awk '{print $2}')
  if python -c "from packaging.version import Version; exit(0 if Version('$SETUPTOOLS_VERSION') >= Version('82') else 1)"; then
    pip install 'setuptools<82'
  fi
fi

if [[ $REPO == "open-mmlab/mmcv" ]]; then
  pip install addict yapf
  SETUPTOOLS_VERSION=$(pip show setuptools | grep '^Version:' | awk '{print $2}')
  if python -c "from packaging.version import Version; exit(0 if Version('$SETUPTOOLS_VERSION') >= Version('82') else 1)"; then
    pip install 'setuptools<82'
  fi

  # Fix 'std': ambiguous symbol error in compiled_autograd.h when compiling CUDA extensions on Windows
  # https://github.com/pytorch/pytorch/issues/173232
  if [[ $OS == "Windows" ]] && [[ $COMPUTE_PLATFORM != "cpu" ]]; then
    COMPILED_AUTOGRAD="$(python -c 'import torch, os; print(os.path.dirname(torch.__file__))')/include/torch/csrc/dynamo/compiled_autograd.h"
    sed -i 's/#if defined(_WIN32) && (defined(USE_CUDA) || defined(USE_ROCM))/#if defined(_WIN32) \&\& defined(__NVCC__)/' "$COMPILED_AUTOGRAD"
  fi

  echo "MMCV_WITH_OPS=1" >> "$GITHUB_ENV"

  if python -c "import sys; sys.exit(0 if sys.version_info >= (3, 13) else 1)"; then
    patch -p0 < "$SCRIPT_DIR"/mmc-patch-for-linux-and-windows/mmcv_py313plus.patch
  fi

  if [[ $OS == "Windows" ]] && python -c "from packaging.version import Version; exit(0 if Version('$TORCH_VERSION') >= Version('2.13') else 1)"; then
    patch -p0 < "$SCRIPT_DIR"/mmc-patch-for-linux-and-windows/mmcv_win_cpp20.patch
  fi
fi

if [[ $REPO == "Dao-AILab/flash-attention" ]]; then
  pip install psutil

  echo FLASH_ATTENTION_FORCE_BUILD=TRUE >> "$GITHUB_ENV"
  source "$SCRIPT_DIR"/.github/workflows/cuda/${OS}_env.sh
  echo "FLASH_ATTN_CUDA_ARCHS=${TORCH_CUDA_ARCH_LIST}" | sed "s/\(\.\|\+PTX\)//g" >> "$GITHUB_ENV"

  echo NVCC_THREADS=1 >> "$GITHUB_ENV"
  if [[ $OS == "Linux" ]]; then
    echo MAX_JOBS=2 >> "$GITHUB_ENV"
  elif [[ $OS == "Windows" ]]; then
    echo MAX_JOBS=3 >> "$GITHUB_ENV"
  fi
fi

if [[ $REPO == "opencv/opencv-python" ]] || [[ $REPO == "opencv-python" ]]; then
  if [[ $OS == "Linux" ]]; then
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
      build-essential cmake git pkg-config \
      libjpeg-dev libpng-dev libtiff-dev \
      libavcodec-dev libavformat-dev libswscale-dev \
      libv4l-dev libxvidcore-dev libx264-dev \
      libunwind-dev \
      libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
      gstreamer1.0-tools \
      dpkg-dev

    pip install --upgrade pip setuptools wheel scikit-build cmake ninja numpy packaging
  fi

  echo "ENABLE_CONTRIB=1" >> "$GITHUB_ENV"
  echo "ENABLE_HEADLESS=1" >> "$GITHUB_ENV"
  echo "CMAKE_ARGS=-DWITH_GSTREAMER=ON -DWITH_FFMPEG=ON" >> "$GITHUB_ENV"
fi
