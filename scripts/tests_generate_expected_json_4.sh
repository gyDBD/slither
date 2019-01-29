#!/usr/bin/env bash

DIR="$(cd "$(dirname "$0")" && pwd)"

# generate_expected_json file.sol detectors
generate_expected_json(){
    # generate output filename
    # e.g. file: uninitialized.sol detector: uninitialized-state
    # ---> uninitialized.uninitialized-state.json
    output_filename="$(basename $1 .sol).$2.json"

    # run slither detector on input file and save output as json
    slither "$1" --disable-solc-warnings --detect "$2" --json "$DIR/../tests/expected_json/$output_filename" --solc solc-0.4.25

}



generate_expected_json tests/init_success.sol "function-auth"