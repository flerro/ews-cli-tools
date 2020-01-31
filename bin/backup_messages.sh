#!/usr/bin/env bash

BASE_DIR=`dirname $0`
cd `dirname $BASE_DIR`

if [ ! -d 'venv' ]; then
  echo "Create virtualenv for EWS tools in $BASE_DIR/venv"
  exit 1
fi

source venv/bin/activate
python app/backup.py