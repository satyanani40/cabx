##Ansible managed

#!/bin/bash


# # # # # # # # # # # # # # # # # # # # #
# This is a SAMPLE runner script
# for this application. If ansible-deployed
# this will be a template.
# # # # # # # # # # # # # # # # # # # # #
PROJ_DIR=/mnt/git/qvd

export PATH=/root/miniconda3/bin:$PATH

source activate qvd_api_env
export ENVIRONMENT=local
export QVD_API_APP_PORT=8000

cd $PROJ_DIR/qvd-api

exec gunicorn -b 0.0.0.0:$QVD_API_APP_PORT -w 1 --threads 4 \
  --log-config $PROJ_DIR/qvd-api/deployment/gunicorn_logging.conf \
  runner:qvd_app
