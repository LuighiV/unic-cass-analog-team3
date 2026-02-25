#!/bin/bash

#Based on https://github.com/iic-jku/IIC-OSIC-TOOLS/tree/main/_build/images/magic
# Env variables
export TOOLS=$HOME/tools
export MAGIC_REPO_URL="https://github.com/rtimothyedwards/magic.git"
export MAGIC_REPO_COMMIT="8.3.599"
export MAGIC_NAME="magic"

set -e
cd /tmp || exit 1

git clone --filter=blob:none "${MAGIC_REPO_URL}" "${MAGIC_NAME}"
cd "${MAGIC_NAME}" || exit 1
git checkout "${MAGIC_REPO_COMMIT}"
./configure --prefix="${TOOLS}/${MAGIC_NAME}"
make database/database.h
make -j"$(nproc)"
make install

echo "$MAGIC_NAME $MAGIC_REPO_COMMIT" > "${TOOLS}/${MAGIC_NAME}/SOURCES"
