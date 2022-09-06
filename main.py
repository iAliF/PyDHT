import argparse
import re
import time
from re import Pattern

from serial import Serial, SerialException

RE_PATTERN: Pattern = re.compile(r'(\d+)\|(\d+\.\d+)\|(\d+\.\d+)\|(\d+\.\d+)')

parser = argparse.ArgumentParser()
serial: Serial


def sync_time():
    print("Syncing time with Arduino")
    serial.timeout = 3

    while True:
        serial.write(f"TIME|{time.time()}".encode())
        data = serial.readline().decode().strip()
        if data == 'SYNCED':
            break

    serial.timeout = None


def start():
    print("Starting loop")

    while True:
        try:
            data = serial.readline().decode().strip()
            if not (match := RE_PATTERN.match(data)):
                print("Invalid data")
                continue

            u_time, temp, hum, index = match.groups()

            if args.verbose:
                print(f"{u_time} | Temperature: {temp}°C | Humidity: {hum}% | Heat Index: {index}°C")
        except KeyboardInterrupt:
            print("Exiting ...")
            break
        except SerialException:
            print("Something went wrong. Check connections and run this script again.")
            break

    serial.close()


def main():
    try:
        global serial
        serial = Serial(args.port, args.baud)
    except SerialException:
        print("couldn't open this port")
        return

    sync_time()
    start()


if __name__ == '__main__':
    parser.add_argument('port', type=str, help='Serial port')
    parser.add_argument('baud', type=int, help='Baud rate')
    parser.add_argument('-v', '--verbose', type=bool, action=argparse.BooleanOptionalAction, help='Verbose mode')
    args = parser.parse_args()

    main()
