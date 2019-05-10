Spectrometer visualization and testing application in Python/Flask + JavaScript/React

To use:
1. copy NUCLEO_BINARY.bin to nucleo board: cp NUCLEO_BINARY.bin /Volumes/NODE_F401RE
2. set usb port as env variable: export port="/dev/tty.usbmodem143120"
3. make run.sh executable: chmod +x run.sh
4. run run.sh: ./run.sh

- to get new readings, reload webpage (localhost:3000)
- to end session, ctl+c on command line and run.sh will tear down processes