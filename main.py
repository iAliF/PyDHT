import argparse

from serial import Serial, SerialException

parser = argparse.ArgumentParser()
parser.add_argument('port', type=str, help='Serial port')
parser.add_argument('baud', type=int, help='Baud rate')

serial: Serial


def start():
    while True:
        try:
            print(serial.readline())
        except KeyboardInterrupt:
            print("Exiting ...")
            break


def main():
    args = parser.parse_args()

    try:
        global serial
        serial = Serial(args.port, args.baud)
    except SerialException:
        print("couldn't open this port")
        return

    start()


if __name__ == '__main__':
    main()
