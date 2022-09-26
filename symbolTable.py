class SymbolTable:
    table = {}

    @staticmethod
    def getValue(identifier):
        if identifier not in SymbolTable.table:
            #print(SymbolTable.table)
            raise Exception("Unrecognized symbol")
        return SymbolTable.table[identifier]

    @staticmethod
    def setValue(id, value):
        SymbolTable.table[id.value] = value
    
    @staticmethod
    def getTable():
        # METHOD FOR DEBUGGING ONLY
        print(f"SymbolTable: {SymbolTable.table}")