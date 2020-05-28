from os import system

class Printer:
    @staticmethod
    def printPersistentLine(messageToPrint):
        print(messageToPrint + '\r', end = ''),
    
    @staticmethod
    def clear():
        system('clear')