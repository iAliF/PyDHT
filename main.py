import argparse
import re
from datetime import datetime
from re import Pattern

from influxdb_client import InfluxDBClient, Point
from serial import Serial, SerialException

import config

RE_PATTERN: Pattern = re.compile(r'(\d+)\|(\d+\.\d+)\|(\d+\.\d+)\|(\d+\.\d+)')

parser = argparse.ArgumentParser()
serial: Serial

client = InfluxDBClient(f"http://{config.HOST}:{config.PORT}", config.TOKEN, org=config.ORG, bucket=config.BUCKET)
write_api = client.write_api()


def sync_time():
    print("Syncing time with Arduino")
    serial.timeout = 3

    while True:
        serial.write(f"TIME|{datetime.utcnow().timestamp()}".encode())
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

            u_time, temp, hum, index = map(float, match.groups())
            u_time = int(u_time)

            if args.verbose:
                print(f"{u_time} | Temperature: {temp}°C | Humidity: {hum}% | Heat Index: {index}°C")

            point = Point(config.NAME) \
                .field('temperature', temp) \
                .field('humidity', hum) \
                .field('heat_index', index) \
                .time(datetime.fromtimestamp(u_time))
            write_api.write(
                config.BUCKET,
                config.ORG,
                point
            )
        except KeyboardInterrupt:
            print("Exiting ...")
            break
        except SerialException:
            print("Something went wrong. Check connections and run this script again.")
            break

    client.close()
    write_api.close()
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
