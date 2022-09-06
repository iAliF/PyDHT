import argparse

parser = argparse.ArgumentParser()
parser.add_argument('port', type=str, help='Serial port')
parser.add_argument('baud', type=int, help='Baud rate')


def main():
    args = parser.parse_args()


if __name__ == '__main__':
    main()
