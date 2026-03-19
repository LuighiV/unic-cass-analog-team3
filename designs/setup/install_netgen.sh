#!/bin/bash
#Based on https://github.com/iic-jku/IIC-OSIC-TOOLS/blob/main/_build/images/netgen/scripts/install.sh
# Env variables
export TOOLS=$HOME/tools
export NETGEN_REPO_URL="https://github.com/rtimothyedwards/netgen.git"
export NETGEN_REPO_COMMIT="1.5.305"
export NETGEN_NAME="netgen"
set -e
cd /tmp || exit 1

git clone --filter=blob:none "${NETGEN_REPO_URL}" "${NETGEN_NAME}"
cd "${NETGEN_NAME}" || exit 1
git checkout "${NETGEN_REPO_COMMIT}"
./configure CFLAGS="-O2 -g" --prefix="${TOOLS}/${NETGEN_NAME}"
make clean
make -j"$(nproc)"
make install
