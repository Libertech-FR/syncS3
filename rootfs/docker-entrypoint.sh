#!/bin/bash
cat /template/config.conf|envsubst >/config.conf
./sync.py --config /config.conf
