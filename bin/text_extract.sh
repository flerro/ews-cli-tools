#!/usr/bin/env bash

BASE_DIR=`dirname $0`
cd `dirname $BASE_DIR`

if [ ! -f "$1" ]; then
  echo ""
  echo "No input file specified."
  echo ""
  echo "Usage: $0 multipart_message.eml"
  echo ""
  exit 1
fi

if [ ! -d 'venv' ]; then
  echo "Create virtualenv for EWS tools in $BASE_DIR/venv"
  exit 1
fi

source venv/bin/activate
python app/text_extract.py "$0"