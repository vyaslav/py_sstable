import subprocess
import random
import sys
import time
import shutil
import os
import json

SERVER_CMD = ["python", "-m", "sstable_server"]
CLI_CMD = ["python", "-m", "main"]
DB_DIR = "db_files"
KEY_COUNT = 5000

def random_key(i):
    return f"key_{i:04d}"

def start_server():
    # Start the server in the background
    proc = subprocess.Popen(SERVER_CMD, stdout=sys.stdout, stderr=sys.stderr)
    time.sleep(2)  # Give server time to start
    return proc

def stop_server(proc):
    proc.terminate()
    proc.wait()

def cli_set(key, value):
    cmd = CLI_CMD + ["set", key, value]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def cli_get(key):
    cmd = CLI_CMD + ["get", key]
    result = subprocess.check_output(cmd)
    return result.decode().strip()

def main():
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
    server_proc = start_server()
    try:
        keys = []
        print(f"Inserting {KEY_COUNT} keys...")
        for i in range(KEY_COUNT):
            key = f"key_{i:04d}"
            random_value = random.randint(1, KEY_COUNT)
            value = {"data": random_value}
            cli_set(key, json.dumps(value))
            keys.append(key)
        print(f"Inserted {KEY_COUNT} keys.")

        print("Reading back and calculating sum and average...")
        total = 0
        for key in keys:
            val = cli_get(key)
            total += json.loads(val)["data"]
        avg = total / len(keys)
        print(f"Sum: {total}")
        print(f"Average: {avg:.2f}")
    finally:
        stop_server(server_proc)

if __name__ == "__main__":
    main()