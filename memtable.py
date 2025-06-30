import bisect

class Memtable:
    """
    An in-memory data structure that keeps key-value pairs sorted by key.
    It uses Python's `bisect` module to maintain order.
    """
    def __init__(self):
        # Stores data as a sorted list of (key, value) tuples.
        self._data = []

    def set(self, key, value):
        """
        Adds a key-value pair, maintaining sorted order. O(log n) for search,
        O(n) for insertion due to list shifting.
        If the key already exists, its value is updated.
        """
        # bisect_left finds the insertion point for the key to maintain order.
        i = bisect.bisect_left(self._data, (key, ''))
        
        # If key already exists at this position, update the value.
        if i < len(self._data) and self._data[i][0] == key:
            self._data[i] = (key, value)
        # Otherwise, insert the new (key, value) pair at this position.
        else:
            self._data.insert(i, (key, value))

    def get(self, key):
        """
        Retrieves a value for a given key using binary search. O(log n).
        """
        # Find the potential position of the key.
        i = bisect.bisect_left(self._data, (key, ''))
        
        # If the key is found at this position, return its value.
        if i < len(self._data) and self._data[i][0] == key:
            return self._data[i][1]
        
        return None

    def get_sorted_items(self):
        """
        Returns all key-value pairs, which are already sorted. O(1).
        """
        return self._data

    def clear(self):
        """Clears the memtable."""
        self._data = []

    def __len__(self):
        """Returns the number of items in the memtable."""
        return len(self._data)