#!/usr/bin/env bash

DIR="$(cd "$(dirname "$0")" && pwd)"

# generate_expected_json file.sol detectors
generate_expected_json(){
    # generate output filename
    # e.g. file: uninitialized.sol detector: uninitialized-state
    # ---> uninitialized.uninitialized-state.json
    output_filename="$(basename $1 .sol).$2.json"

    # run slither detector on input file and save output as json
    slither "$1" --disable-solc-warnings --detect "$2" --json "$DIR/../tests/expected_json/$output_filename" --solc solc

}

generate_expected_json tests/reentrancy.sol "uninitialized-state"
#generate_expected_json tests/backdoor.sol "backdoor"
#generate_expected_json tests/backdoor.sol "suicidal"
#generate_expected_json tests/pragma.0.4.24.sol "pragma"
#generate_expected_json tests/old_solc.sol.json "solc-version"
#generate_expected_json tests/reentrancy-0.5.1.sol "reentrancy-eth"
#generate_expected_json tests/reentrancy-0.5.1.sol "reentrancy"
#generate_expected_json tests/uninitialized_storage_pointer.sol "uninitialized-storage"
#generate_expected_json tests/tx_origin-0.5.1.sol "tx-origin"
#generate_expected_json tests/locked_ether-0.5.1.sol "locked-ether"
#generate_expected_json tests/arbitrary_send-0.5.1.sol "arbitrary-send"
#generate_expected_json tests/inline_assembly_contract-0.5.1.sol "assembly"
#generate_expected_json tests/inline_assembly_library-0.5.1.sol "assembly"
#generate_expected_json tests/constant-0.5.1.sol "constant-function"
generate_expected_json tests/arbitrary_send-0.5.1.sol "init-auth"
generate_expected_json tests/arbitrary_send.sol "init-auth"
generate_expected_json tests/init_success.sol "init-auth"
generate_expected_json tests/0x0d941d0379Bc5Cb2A610a9b0f02Ec6fA4a387dC8.sol "init-auth"