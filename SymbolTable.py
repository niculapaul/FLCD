class SymbolTable(object):
    def __init__(self, length):
        self.array = [None for i in range(0, length)]
        self.fill = 0

    def __str__(self):
        return str([str(ident) for ident in self.array])

    def hash(self, key):
        sumString = 0
        for i in key:
            sumString += ord(i)
        return sumString % len(self.array)

    def add(self, symbol):
        index = self.hash(symbol)
        self.fill += 1
        if self.fill > len(self.array):
            self.expand()
        if self.array[index] is not None:
            if symbol in self.array[index]:
                print("the " + str(symbol) + " symbol found at index " + str(index))
                return index
            for val in self.array[index]:
                if (val == symbol):
                    return
                else:
                    self.array[index].append(symbol)
                    return index
        else:
            self.array[index] = []
            self.array[index].append(symbol)

    def get(self, symbol):
        index = self.hash(symbol)
        if self.array[index] is None:
            return None
        else:
            for val in self.array[index]:
                if (val == symbol):
                    return symbol
            return None

    def expand(self):
        print("symbol table expanded")
        expandedTable = SymbolTable(len(self.array) * 2)
        for i in range(len(self.array)):
            if self.array[i] is None:
                continue
            for val in self.array[i]:
                expandedTable.add(val)
        self.array = expandedTable.array


if __name__ == '__main__':
    st = SymbolTable(3)
    st.add("numar1")
    st.add("1")
    st.add("25")
    st.add("50")
    st.add("nu")
    st.add("a")
    st.add("a")
    st.add("b")
    print(st)
    print(st.get("numar1"), "at index:", st.hash("numar1"))
    print(st.get("1"), "at index:", st.hash("1"))
    print(st.get("25"), "at index:", st.hash("25"))
