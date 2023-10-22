class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    # use default hash function (maybe use sum of ASCII codes of chars later)
    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = []
            self.table[index].append((key, value))
        else:
            key_exists = any(existing_key == key for existing_key, _ in self.table[index])

            if not key_exists:
                self.table[index].append((key, value))

    def lookup(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for stored_key, value in self.table[index]:
                if key == stored_key:
                    return value
        return None

    def remove(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for stored_key, value in self.table[index]:
                if key == stored_key:
                    self.table[index].remove((stored_key, value))
                    return


if __name__ == "__main__":
    st = SymbolTable(size=2)

    # Inserting identifiers and constants
    st.insert("variable1", 42)
    # This one should not be inserted
    st.insert("variable1", 16)
    st.insert("variable2", 4)
    st.insert("variable3", 3)


    # Looking up values
    value1 = st.lookup("variable1")
    value2 = st.lookup("variable2")
    value3 = st.lookup("variable3")

    print("Lookup variable1:", value1)
    print("Lookup variable2:", value2)
    print("Lookup variable3:", value3)

    # Removing an entry
    st.remove("variable1")

    # Checking after removal
    value1 = st.lookup("variable1")
    print("Lookup variable1 after removal:", value1)
