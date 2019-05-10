# python imports
import serial
import config
import time

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='./build')
CORS(app)

# @app.route('/')
# def index():
#     return send_from_directory(app.static_folder, 'index.html')

@app.route('/api')
def api():
    # TODO copy bin to device
    # open serial port
    try:
        print(config.baudrate)
        ser = serial.Serial(config.port, config.baudrate)
        # share the serial handle with the stop-thread so cancel_read may be called
        # SerQueue.put(ser)
        # disable controls
        # panelsleep(panel)
        config.stopsignal = 0

        # start the progressbar
        # panel.progress.config(mode="determinate")
        # threadprogress = threading.Thread(
        #     target=progressthread, args=(progress_var,), daemon=True)
        # threadprogress.start()

        # wait to clear the input and output buffers, if they're not empty data is corrupted
        while (ser.in_waiting > 0):
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            time.sleep(0.01)

        # Transmit key 'ER'
        config.txfull[0] = 69
        config.txfull[1] = 82
        # split 32-bit integers to be sent into 8-bit data
        config.txfull[2] = (config.SHperiod >> 24) & 0xff
        config.txfull[3] = (config.SHperiod >> 16) & 0xff
        config.txfull[4] = (config.SHperiod >> 8) & 0xff
        config.txfull[5] = config.SHperiod & 0xff
        config.txfull[6] = (config.ICGperiod >> 24) & 0xff
        config.txfull[7] = (config.ICGperiod >> 16) & 0xff
        config.txfull[8] = (config.ICGperiod >> 8) & 0xff
        config.txfull[9] = config.ICGperiod & 0xff
        # averages to perfom
        config.txfull[10] = config.AVGn[0]
        config.txfull[11] = config.AVGn[1]

        # transmit everything at once (the USB-firmware does not work if all bytes are not transmitted in one go)
        ser.write(config.txfull)

        # wait for the firmware to return data
        config.rxData8 = ser.read(7388)
        with open('readData.txt', 'wb') as file:
            file.write(config.rxData8)

        # close serial port
        ser.close()

        # enable all buttons
        # panelwakeup(panel)

        if (config.stopsignal == 0):
            # combine received bytes into 16-bit data
            for rxi in range(0, 3694):
                config.rxData16[rxi] = (
                    config.rxData8[2*rxi+1] << 8) + config.rxData8[2*rxi]

            # plot the new data
            # panel.bupdate.invoke()
            # hold values for saving data to file as the SHperiod and ICGperiod may be updated after acquisition
            config.SHsent = config.SHperiod
            config.ICGsent = config.ICGperiod

            return jsonify({'data': config.rxData16.tolist()})

        # SerQueue.queue.clear()

    except serial.SerialException:
        return "Something went wrong"
        # messagebox.showerror(
        #     "By the great otter!", "There's a problem with the specified serial connection.")

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)