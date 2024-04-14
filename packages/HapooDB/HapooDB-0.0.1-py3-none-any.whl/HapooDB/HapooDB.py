import os

class HapooDB:
    def __init__(self,*title) -> None:
        self.variables = []
        if title:
            self.filename = f"{title[0]}.txt"
        else:
            self.filename = f"HapooDB.txt"
        try:
            try:
                self.file = open(self.filename,"xt")
            except IndexError:
                self.file = open(self.filename,"xt")
            self.file.close() 
        except FileExistsError: 
            pass
    def destroyfile(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)
        else:
            print("!The file, {} does not exist".format(self.filename))
    def declare(self,key,val) -> None:
        self.file = open(self.filename,"at")
        self.file.write(f"{key}={val}\n")
    def closeFile(self) -> None:
        self.file.close()
    def access(self) -> list:
        self.file = open(self.filename,"rt")
        lines = [line.strip("\n") for line in self.file.readlines()]
        variables = {}
        for line in lines:
            line = [element for element in line.split("=")]
            variables[line[0]] = line[1]
        return variables    
    def accessSingle(self,key) -> str:
        self.file = open(self.filename,"rt")
        lines = [line.strip("\n") for line in self.file.readlines()]
        val = None
        for line in lines:
            if key in line:
                val = line.split("=")[1]
            else:
                continue
        try:
            return val.strip("\n")            
        except AttributeError:
            print("!There is no such of key in the DB.")
    def declareCluster(self,keyValPair:dict) -> None:
        self.file = open(self.filename,"at")
        content = list(keyValPair.items())
        for branchlist in content:
            self.file.write(f"{branchlist[0]}={branchlist[1]}\n")      
    def clearFile(self) -> None:
        self.file = open(self.filename,"wt")
        self.file.write('')
    def declareEncryption(self,key,value) -> None: 
        key = self.__private_Encrypt(key)
        value = self.__private_Encrypt(value)

        self.file = open(self.filename,"at")
        self.file.write(f"{key}={value}\n")
    def accessEncryption(self,key):
        self.file = open(self.filename,"rt")
        lines = [line.strip("\n") for line in self.file.readlines()]
        val = None
        for line in lines:
            if self.__private_Encrypt(key) in line:
                val = line.split("=")[1]
                print(val)
            else:
                continue
        try:
            return self.__private_Decrypt(val.strip("\n"))
        except AttributeError:
            print("!There is no such of key in the DB.")
    def __private_Encrypt(self,val):
        alphabets = [letter for letter in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"]
        EncodedMsg = []
        for letter in val:
            if letter in val:
                index = alphabets.index(letter)
                newPosition = (index + 3) % 62
                EncodedMsg.append(alphabets[newPosition])
            else:
                EncodedMsg.append(letter)
        return "".join(EncodedMsg)
    def __private_Decrypt(self,val):
        alphabets = [letter for letter in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"]
        EncodedMsg = []
        for letter in val:
            if letter in val:
                index = alphabets.index(letter)
                newPosition = (index - 3) % 62
                EncodedMsg.append(alphabets[newPosition])
            else:
                EncodedMsg.append(letter)
        return "".join(EncodedMsg)