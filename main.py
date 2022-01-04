
class HashTable(object):
    def __init__(self, length=17):
        self.array = [None for i in range(0, length)]
        self.fill = 0

    def hash(self, key):
        sumString = 0
        for i in key:
            sumString += ord(i)
        return sumString % len(self.array)

    def add(self, symbol):
        self.fill += 1
        if self.fill > len(self.array):
            self.double()
        index = self.hash(symbol)
        if self.array[index] is not None:
            for val in self.array[index]:
                if (val == symbol):
                    break
                else:
                    self.array[index].append(symbol)
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

    def double(self):
        # print("hashTable expanded")
        newHtb = HashTable(len(self.array) * 2)
        for i in range(len(self.array)):
            if self.array[i] is None:
                continue
            for val in self.array[i]:
                newHtb.add(val)
        self.array = newHtb.array


class OaiScanner(object):
    def __init__(self, file, token):
        self.tokenFile = token
        self.programFile = file
        self.specTokens = []
        self.PIF = []
        self.ST = HashTable(3)
        self.getTokens()
        self.word = ""
        self.stringFlag = False
        self.operatorFlag = False
        self.specialChrFlag = False
        self.vectorLenght = False
        self.readOrWriteFlag = False

    def getTokens(self):
        file = open(self.tokenFile, "r")

        while (True):
            line = file.readline()
            if not line:
                break
            tokeni = line.split()
            tokenCode = int(tokeni[0])
            tokenString = tokeni[1]
            self.specTokens.append([tokenCode, tokenString])
        file.close()
        # print(self.specTokens)

    def detectFurtherOperators(self, op, newch):
        operatorNew = op + newch
        for i in self.specTokens:
            if i[1].find(operatorNew) != -1:
                return True
        return False

    def checkLetter(self, i):
        if i in [" ", ";", "`", "'", "\n"] and self.stringFlag is not True:
            self.procesIndex(self.word)
            self.operatorFlag = False
            self.vectorLenght = False
            self.procesIndex(i)
            return
        if self.operatorFlag:
            if self.detectFurtherOperators(self.word, i):
                self.word += i
                return
            elif self.vectorLenght == True and i == "<":
                self.procesIndex(self.word.split("<")[0])
                self.word = "<<"
                self.vectorLenght = False
            elif self.vectorLenght == True and i == ">":
                self.procesIndex(self.word.split(">")[0])
                self.word = ">>"
                self.vectorLenght = False
            elif self.vectorLenght == True and i == ".":
                self.procesIndex(self.word.split(".")[0])
                self.word = ".."
                self.vectorLenght = False
            else:
                if self.word[0] == "-" or self.word[0] == "+":
                    if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        self.word += i
                        self.operatorFlag = False
                        return
                if self.word[len(self.word) - 1] != "<" or self.word == "<<":
                    self.procesIndex(self.word)
                if self.word[len(self.word) - 1] != ">" or self.word == ">>":
                    self.procesIndex(self.word)
                if self.word[len(self.word) - 1] != "." or self.word == "...":
                    self.procesIndex(self.word)
                self.operatorFlag = False
                self.vectorLenght = False
                self.checkLetter(i)
                return
        if self.readOrWriteFlag:
            if self.word == "<" and i == "<":
                self.word += i
        if i in ["?", "<", ">", "~", "(", ")", ".", "{", "}", ":", "+", "-", "/", "*", "#"]:
            if i != "." and i != "<" and i != ">":
                self.procesIndex(self.word)
            else:
                self.vectorLenght = True
            self.operatorFlag = True
            self.word += i
            return
        if i == "\"" and self.stringFlag != True:
            self.stringFlag = True
            self.procesIndex(self.word)
            self.word = i
            return
        if self.stringFlag:
            if self.specialChrFlag:
                self.word += i
                self.specialChrFlag = False
                return
            else:
                if i == "\\":
                    self.specialChrFlag = True
                    return
                else:
                    if i == "\"":
                        self.word += i
                        self.procesIndex(self.word)
                        self.stringFlag = False
                        return
                    else:
                        self.word += i
                        return
        self.word += i
        return

    def splitProgram(self):
        file = open(self.programFile, "r")
        lineRow = 0
        while True:
            line = file.readline()
            if not line:
                break
            lineCollumn = 0
            lineRow += 1
            for i in line:
                lineCollumn += 1
                try:
                    self.checkLetter(i)
                except Exception as e:
                    print(e, lineRow, ":", lineCollumn, " has a lexical error")

        file.close()

    def isConst(self, word):
        if word[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\""]:
            return True
        return False


    def procesIndex(self, word):
        # check for .. as error
        self.word = ""
        if word == "" or word == "\n" or word == " ":
            return
        if self.isLexicallyWrong(word):
            raise Exception(word + " is wrong")
        for i in self.specTokens:
            if i[1] == word:
                self.PIF.append([word, -1])
                return
        if self.isConst(word):
            self.PIF.append(["const", self.ST.fill + 1])
        else:
            self.PIF.append(["identifier", self.ST.fill + 1])
        self.ST.add(word)

    def isLexicallyWrong(self, word):
        if word[0] == "0" and len(word) > 1 and word[1] != ".":
            return True
        if word[0] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            for i in word:
                if i not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
                    return True
        for i in word:
            if i not in ["a", "s", "d", "f", "g", "h", "j", "k", "g", "l", ";", "p", "o", "i", "y", "u", "t",
                         "r", "e", "w", "q", "z", "x", "c", "v", "b", "n", "m",
                         ",", ".", "/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                         "-", "+", "`", "%", "'", "<", ">", "?", "!", "=", "{", "}", "\"", ":", ")", "(",
                         "*", "#", "Z", "X", "C", "V", "B", "N", "M", "A", "S",
                         "D", "F", "G", "H", "J", "K", "L", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]:
                return True
        return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sc = OaiScanner("P1.oai", "token.in")
    sc.splitProgram()
    f = open("PIF.out", "w")
    string = ""
    for i in sc.PIF:
        string += str(i[0]) + " : " + str(i[1]) + "\n"
    f.write(string)
    f.close()
    f = open("ST.out", "w")
    f.write("ST is represented on a hashTable! \n")
    for i in sc.ST.array:
        if i != None:
            for j in i:
                f.write(str(sc.ST.hash(j)) + " --> " + str(j))
                f.write("\n")
    f.close()
