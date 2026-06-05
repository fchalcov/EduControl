#!/usr/bin/env bash
set -o errexit

cd back
chmod +x build.sh start.sh
./build.sh
