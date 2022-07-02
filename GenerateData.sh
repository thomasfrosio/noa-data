#!/bin/bash
# Generates data
# ==============

# Before running the tests, run this script once.
# It will generate the test data needed by noa.
# All existing generated assets will be overwritten.

# Some colours in our life
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Ensure minimum python version:
if python -c 'import sys; sys.exit(sys.version_info[:2] >= (3,8))' > /dev/null ; then
  >&2 echo -e "${RED}ERROR: \"python\" should point to python3.8 or newer${NC}"
  exit 1
fi

python -m venv env_noa_data
source env_noa_data/bin/activate
pip install -e .

# Generate assets:
echo -e "${GREEN}noa-tests: generating data - start${NC}"
find assets -type f -name "Data*.py" -exec echo "noa-tests: running" {} \; -exec python {} \;
echo -e "${GREEN}noa-tests: generating data - done${NC}"

NOA_DATA_PATH="$(
  cd "$(dirname "$0")" >/dev/null 2>&1 || exit
  pwd -P
)" # https://stackoverflow.com/questions/4774054

echo -e "${GREEN}noa-tests: remember to export NOA_DATA_PATH to \"${NOA_DATA_PATH}\"${NC}"

deactivate
