class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    # use default hash function (maybe use sum of ASCII codes of chars later)
    def hash_function(self, key):
        return hash(key) % self.size

    def __str__(self) -> str:
        result = ""
        index = -1
        for bucket in self.table:
            index += 1
            if bucket is None:
                continue
            for key, value in bucket:
                result += f"{key}: ({index}, {value})\n"
        return result

    def insert(self, key, value=-1):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = []
            self.table[index].append((key, 0))
            return index, 0
        else:
            key_exists = any(existing_key == key for existing_key, _ in self.table[index])

            if not key_exists:
                value = len(self.table[index])
                self.table[index].append((key, value))
                return index, value
            return None, None

    def lookup(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for stored_key, value in self.table[index]:
                if key == stored_key:
                    return index, value
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
    index, value = st.insert("a")
    print(f"1st: index: {index}, value: {value}")
    # This one should not be inserted
    index, value = st.insert("a")
    print(f"2st: index: {index}, value: {value}")

    index, value = st.insert("b")
    print(f"3st: index: {index}, value: {value}")

    index, value = st.insert("c")
    print(f"4st: index: {index}, value: {value}")



    # Looking up values
    value1 = st.lookup("a")
    value2 = st.lookup("b")
    value3 = st.lookup("c")

    print("Lookup a:", value1)
    print("Lookup b:", value2)
    print("Lookup c:", value3)

    # Removing an entry
    st.remove("a")

    # Checking after removal
    value1 = st.lookup("a")
    print("Lookup variable1 after removal:", value1)
