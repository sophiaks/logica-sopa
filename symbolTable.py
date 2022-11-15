from aux import mprint

class SymbolTable:
    table = {}

    @staticmethod
    # Receives STR type with identifier name
    def getValue(idvalue):
        if idvalue not in SymbolTable.table:
            raise Exception(f"Unrecognized symbol {idvalue} (have you declared it?)")
        if SymbolTable.table[idvalue] is None: 
            pass
        return SymbolTable.table[idvalue]

    @staticmethod
    def setValue(idvalue, value):
        SymbolTable.table[idvalue] = value

    @staticmethod
    def dec_var(var_type, id):
        SymbolTable.table[id] = (var_type, None)
    
    @staticmethod
    def getTable():
        # METHOD FOR DEBUGGING ONLY
        print(f"SymbolTable: {SymbolTable.table}")