#!/usr/bin/env bash

### Test Detectors

DIR="$(cd "$(dirname "$0")" && pwd)"

# test_slither file.sol detectors
test_slither(){

    expected="$DIR/../tests/expected_json/$(basename $1 .sol).$2.json"

    # run slither detector on input file and save output as json
    slither "$1" --disable-solc-warnings --detect "$2" --json "$DIR/tmp-test.json" --solc solc-0.4.25
    if [ $? -eq 255 ]
    then
        echo "Slither crashed"
        exit -1
    fi

    if [ ! -f "$DIR/tmp-test.json" ]; then
        echo ""
        echo "Missing generated file"
        echo ""
        exit 1
    fi

    result=$(python "$DIR/json_diff.py" "$expected" "$DIR/tmp-test.json")

    rm "$DIR/tmp-test.json"
    if [ "$result" != "{}" ]; then
      echo ""
      echo "failed test of file: $1, detector: $2"
      echo ""
      echo "$result"
      echo ""
      exit 1
    fi

    # run slither detector on input file and save output as json
    slither "$1" --disable-solc-warnings --detect "$2" --compact-ast --json "$DIR/tmp-test.json" --solc solc-0.4.25
    if [ $? -eq 255 ]
    then
        echo "Slither crashed"
        exit -1
    fi

    if [ ! -f "$DIR/tmp-test.json" ]; then
        echo ""
        echo "Missing generated file"
        echo ""
        exit 1
    fi

    result=$(python "$DIR/json_diff.py" "$expected" "$DIR/tmp-test.json")

    rm "$DIR/tmp-test.json"
    if [ "$result" != "{}" ]; then
      echo ""
      echo "failed test of file: $1, detector: $2"
      echo ""
      echo "$result"
      echo ""
      exit 1
    fi
}




test_slither tests/init_success.sol "function-auth"

