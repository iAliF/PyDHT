import argparse
import re
from re import Pattern

from serial import Serial, SerialException

parser = argparse.ArgumentParser()
parser.add_argument('port', type=str, help='Serial port')
parser.add_argument('baud', type=int, help='Baud rate')

RE_PATTERN: Pattern = re.compile(r'(\d+\.\d+)\|(\d+\.\d+)\|(\d+\.\d+)')
serial: Serial


def start():
    while True:
        try:
            data = serial.readline().decode().strip()
            if not (match := RE_PATTERN.match(data)):
                print("Invalid data")
                continue

            temp, hum, index = match.groups()
            print(f"Temperature: {temp} | Humidity: {hum} | Heat Index: {index}")

        except KeyboardInterrupt:
            print("Exiting ...")
            break
        except SerialException:
            print("Something went wrong. Check connections and run this script again.")
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
