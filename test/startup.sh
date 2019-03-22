#!/usr/bin/env bash

nohup gunicorn -b 0.0.0.0:4000 -t 500 -w 3 endpoint:app &
