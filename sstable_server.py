import socket, os, json
from sstable import SSTable
import atexit

SOCKET_PATH = "/tmp/db_socket"

def main():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    db = SSTable()

    atexit.register(db.flush)
    
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(SOCKET_PATH)
        server.listen()
        print(f"Server started at {SOCKET_PATH}")
        while True:
            conn, _ = server.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    continue
                cmd = json.loads(data.decode())
                if cmd["type"] == "get":
                    print(f"GET command received for key: {cmd['key']}")
                    value = db.get(cmd["key"])
                    if value is not None:
                        conn.sendall(json.loads(value).encode())
                    else:
                        conn.sendall(b"null")
                elif cmd["type"] == "set":
                    print(f"SET command received for key: {cmd['key']} with value: {cmd['value']}")
                    db.set(cmd["key"], json.dumps(cmd["value"]))
                    conn.sendall(b"OK")
                    
if __name__ == "__main__":
    main()