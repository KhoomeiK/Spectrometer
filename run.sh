#!/bin/bash

# 1. copy NUCLEO_BINARY.bin to nucleo board: cp NUCLEO_BINARY.bin /Volumes/NODE_F401RE
# 2. set usb port as env variable: export port="/dev/tty.usbmodem143120"
# 3. make this file executable: chmod +x run.sh
# 4. run this file: ./run.sh

function finish {
  p=$(ps ax | grep "python -m flask run" | awk 'NR==1{print $1}')
  echo $p
  kill $p
}
trap finish EXIT

cd backend
python -m flask run &
cd ..
npm run start