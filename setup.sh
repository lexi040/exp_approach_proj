#!/bin/bash

set -e

echo "setting up conda environment"
conda env create -f environment.yml || conda env update -f environment.yml

echo "setup complete"

#to make this script excutable run
#chmod +x setup.sh
#to execute script run
#./setup.sh
#in terminal