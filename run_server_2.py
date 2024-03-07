# run_server.py
import sys
from Application.server import start_server

HOST = '127.0.0.1'
PORT = 8889

def main():
    start_server(HOST, PORT)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Forced exit. Goodbye!")
    finally:
        sys.exit()