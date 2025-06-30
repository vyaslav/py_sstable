import math
import hashlib

class SimpleBloomFilter:
    def __init__(self, capacity, error_rate=0.01):
        self.capacity = capacity
        self.error_rate = error_rate
        self.size = self._get_size(capacity, error_rate)
        self.hash_count = self._get_hash_count(self.size, capacity)
        self.bit_array = 0

    def _get_size(self, n, p):
        return int(-(n * math.log(p)) / (math.log(2) ** 2))

    def _get_hash_count(self, m, n):
        return int((m / n) * math.log(2))

    def _hashes(self, key):
        key_bytes = str(key).encode("utf-8")
        for i in range(self.hash_count):
            data = key_bytes + i.to_bytes(1, "little")  # small salt
            h = int(hashlib.sha256(data).hexdigest(), 16) % self.size
            yield h

    def add(self, key):
        for h in self._hashes(key):
            self.bit_array |= 1 << h

    def not_contains(self, key):
        """
        Returns True if all bits are 0 for this key, meaning the key
        was definitely NOT inserted.
        False means 'maybe present' or actual present.
        """
        return all((self.bit_array & (1 << h)) == 0 for h in self._hashes(key))
