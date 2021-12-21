#!/bin/bash
# Generates data
# ==============

# Before running the tests, run this script once.
# This will generate the test data needed by noa. All data files will be overwritten.

# Some colours in your life
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# This script should generate all data. Should be >= python3.
for package in numpy mrcfile scipy yaml; do
  python -c "import ${package}" >/dev/null 2>&1 || {
    echo -e "${RED}noa-tests: please add \"${package}\" to the current python environment${NC}"
    exit 1
  }
done
pip install -e .

echo -e "${GREEN}noa-tests: generating data - start${NC}"
find assets -type f -name "Data*.py" -exec echo "noa-tests: running" {} \; -exec python {} \;
echo -e "${GREEN}noa-tests: generating data - done${NC}"

PATH_NOA_DATA="$(
  cd "$(dirname "$0")" >/dev/null 2>&1 || exit
  pwd -P
)" # https://stackoverflow.com/questions/4774054

echo -e "${GREEN}noa-tests: remember to export PATH_NOA_DATA to \"${PATH_NOA_DATA}\"${NC}"
