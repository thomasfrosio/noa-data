#!/bin/bash
# Generates data
# ==============

# Before running the tests, run this script once.
# This will generate the test data needed by noa. All data files will be overwritten.
# Then, it sets the NOA_TEST_DATA environmental variable used by noa.

# Some colours in your life
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# This script should generates all data. Should be withing python3.8 with numpy and mrcfile.
for package in numpy mrcfile; do
  python -c "import ${package}" >/dev/null 2>&1 || {
    echo -e "${RED}noa-tests: please add \"${package}\" to the current python environment${NC}"
    exit 1
  }
done

echo -e "${GREEN}noa-tests: generating data - start${NC}"
find archive -type f -name "Data*.py" -exec echo "noa-tests: running" {} \; -exec python {} \;
echo -e "${GREEN}noa-tests: generating data - done${NC}"

NOA_TEST_DATA="$(
  cd "$(dirname "$0")" >/dev/null 2>&1 || exit
  pwd -P
)" # https://stackoverflow.com/questions/4774054

echo -e "${GREEN}noa-tests: remember to export NOA_TEST_DATA to \"${NOA_TEST_DATA}\"${NC}"

