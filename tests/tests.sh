#!/bin/bash

set -ex

for i in tests/fixtures/*.yaml
do

    testname="$(basename $i .yaml)"
    python puppet-jenkins-plugins.py "tests/fixtures/${testname}.yaml" --update-center-json "tests/fixtures/${testname}.json" 2>&1 | tee "tests/result.${testname}.log"
    diff "tests/result.${testname}.log" "tests/fixtures/${testname}.output"

done


# Test with actual update center

python puppet-jenkins-plugins.py "tests/fixtures/one.yaml"
