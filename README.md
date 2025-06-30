# py_sstable

**py_sstable** is a toy, educational implementation of a Log-Structured Merge-Tree (LSM-Tree) storage engine, inspired by the concepts in the book *Designing Data-Intensive Applications* by Martin Kleppmann. This project demonstrates the basics of log-structured storage, memtables, SSTables, sparse indexing, and Bloom filters in Python.

## Project Structure

- **sstable.py**: Core LSM-Tree logic, manages memtable and SSTable files.
- **memtable.py**: In-memory sorted key-value store.
- **sstable_writer.py**: Writes sorted key-value pairs to disk as SSTable and builds sparse index and Bloom filter.
- **sstable_reader.py**: Reads from SSTable files using sparse index and Bloom filter.
- **simple_bloom_filter.py**: Simple Bloom filter implementation for fast negative lookups.
- **sstable_server.py**: UNIX socket server exposing set/get operations.
- **main.py**: Command-line client to interact with the server.
- **stress_test.py**: Script to stress test the system by inserting and reading many keys.

## How to Run

### 1. Start the Server

Open a terminal and run:

```bash
python -m sstable_server
```

This starts the UNIX socket server at `/tmp/db_socket`.

### 2. Use the CLI

In another terminal, you can set and get keys using the CLI:

- **Set a key:**
  ```bash
  python -m main set mykey 123
  ```

- **Get a key:**
  ```bash
  python -m main get mykey
  ```

### 3. Run the Stress Test

To stress test the system with 1000 random keys:

```bash
python stress_test.py
```

This will:
- Start the server in the background
- Insert 1000 random key-value pairs
- Read all keys back and print the sum and average of the values

## Notes

- This project is for educational purposes only and is **not** production-ready.
- All data is stored in the `db_files/` directory, which is recreated on each run of the stress test.
- The server and CLI communicate via UNIX domain sockets.