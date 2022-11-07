from aux import mprint

class SymbolTable:
    table = {}

    @staticmethod
    def getValue(identifier):
        if identifier not in SymbolTable.table:
            mprint(SymbolTable.table)
            raise Exception("Unrecognized symbol (have you declared it?")
        if SymbolTable.table[identifier] is None:
            mprint(SymbolTable.table)
            raise Exception("No value assigned to identifier")
        return SymbolTable.table[identifier]

    @staticmethod
    def setValue(id, type,value):
        SymbolTable.table[id.value] = (type, value)
    
    @staticmethod
    def getTable():
        # METHOD FOR DEBUGGING ONLY
        print(f"SymbolTable: {SymbolTable.table}")