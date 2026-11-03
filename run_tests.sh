#!/bin/bash

set -e

echo "activating conda environment"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ternus_env

echo "running tests"
python3 -m pytest -v

echo "tests complete"

#run to make executable
#chmod +x run_tests.sh
#run to execute script
#./run_tests.sh