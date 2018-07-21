#!/bin/bash
PROJ_DIR=/local/mnt/projects/feqor
export PATH=/root/miniconda3/bin:$PATH
source activate feqor_api_env
export ENVIRONMENT=local
export QVD_API_APP_PORT=8000
cd PROJ_DIR
python runner.py
