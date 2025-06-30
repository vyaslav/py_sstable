import socket, json, argparse

SOCKET_PATH = "/tmp/db_socket"

def send_command(cmd):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        client.sendall(json.dumps(cmd).encode())
        response = client.recv(4096)
        print(response.decode())



def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    set_p = subparsers.add_parser("set")
    set_p.add_argument("key")
    set_p.add_argument("value")

    get_p = subparsers.add_parser("get")
    get_p.add_argument("key")

    args = parser.parse_args()

    if args.command == "set":
        send_command({"type": "set", "key": args.key, "value": args.value})
    elif args.command == "get":
        send_command({"type": "get", "key": args.key})

if __name__ == "__main__":
    main()