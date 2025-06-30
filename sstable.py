import os
import time
from memtable import Memtable
from sstable_writer import SSTableWriter
from sstable_reader import SSTableReader
import glob
from sortedcontainers import SortedDict
class SSTable:
    """
    A simple Log-Structured Merge-Tree (LSM-Tree) implementation.
    """
    def __init__(self, capacity=100, db_folder="db_files", index_sparsity=10):
        self.capacity = capacity
        self.db_folder = db_folder
        self.index_sparsity = index_sparsity
        self.memtable = Memtable()
        self.index_cache = SortedDict()

        os.makedirs(self.db_folder, exist_ok=True)
                # Find all current sstable files
        current_files = set(glob.glob(os.path.join(self.db_folder, "*.sst")))
        for sst_file in current_files:
            index_file = sst_file.replace(".sst", ".index")
            if os.path.exists(index_file):
                self.index_cache[sst_file] = SSTableReader(sst_file, index_file)

    def set(self, key, value):
        """Sets a key-value pair in the memtable and flushes if full."""
        self.memtable.set(key, value)
        if len(self.memtable) >= self.capacity:
            self.flush()

    def get(self, key):
        """
        Gets a value. Checks memtable first, then SSTables from newest to oldest.
        """
        # 1. Check memtable (fastest)
        value = self.memtable.get(key)
        if value is not None:
            print(f"Found in memtable: {key} -> {value}")
            return value

        print(f"Searching in SSTables for key: {key}")
        # Search SSTables from newest to oldest
        for sst_file in reversed(self.index_cache.keys()):
            reader = self.index_cache.get(sst_file)
            if reader:
                value = reader.get(key)
            if value is not None:
                print(f"Found in SSTable {sst_file}: {key} -> {value}")
                return value
        print(f"Key {key} not found in memtable or SSTables.")
        return None

    def flush(self):
        """
        Flushes the memtable to a new SSTable and index file on disk.
        """
        if not self.memtable:
            return

        timestamp = int(time.time() * 1000000)
        data_filename = os.path.join(self.db_folder, f"{timestamp}.sst")
        index_filename = os.path.join(self.db_folder, f"{timestamp}.index")

        writer = SSTableWriter(data_filename, index_filename, self.index_sparsity)
        writer.write(self.memtable.get_sorted_items())
        
        print(f"Flushed memtable to {data_filename} and {index_filename}")
        self.memtable.clear()
        self.index_cache[data_filename] = SSTableReader(data_filename, index_filename)
