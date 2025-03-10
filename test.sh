#!/bin/bash

set -e

BUILD_FOLDER="build"
FILE_NAME="test"
FILE_PATH_PREFIX="${BUILD_FOLDER}/${FILE_NAME}"

echo "Extracting ocaml code from twoHonestParties.mlw..."

mkdir -p "${BUILD_FOLDER}"

why3 --extra-config=extraConf.conf -L src extract -D ocaml64 -D src/mydriver.drv twoHonestParties.TwoHonestPartiesVsAdversary --recursive -o "${FILE_PATH_PREFIX}.ml" || (echo "Extraction failed"; exit 1)

echo "Compiling ocaml code..."
cd "${BUILD_FOLDER}"
# '-w -26' supresses 'unused variable' warnings
ocamlbuild -quiet -pkg zarith -cflags -w,-26 "${FILE_NAME}.native" || (echo "Compilation failed"; exit 1)

echo "Compilation complete. Running test of simple payment..."
./"${FILE_NAME}.native" || (echo "Simple payment test FAILED"; exit 1)
echo "Simple payment test PASSED"
