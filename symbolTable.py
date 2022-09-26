class SymbolTable:
    table = {}

    @staticmethod
    def getValue(key):
        return SymbolTable.table[key]

    @staticmethod
    def setValue(key, value):
        SymbolTable.table[key] = value
    
    @staticmethod
    def getTable():
        print(SymbolTable.table)