from aux import mprint

class SymbolTable:
    table = {}

    @staticmethod
    def assign_right_type(id_value, value):
        (table_type, table_value) = SymbolTable.getValue(id_value)
        (assigned_type, assigned_value) = value

        if (table_type != assigned_type):
            raise Exception("SymbolTable type does not match assignment type")

    @staticmethod
    # Receives STR type with identifier name
    def getValue(idvalue):
        if idvalue not in SymbolTable.table:
            raise Exception(f"Unrecognized symbol {idvalue} (have you declared it?)")
        if SymbolTable.table[idvalue] is None:
            pass
        return SymbolTable.table[idvalue]

    @staticmethod
    def setValue(id_value, value):
        SymbolTable.assign_right_type(id_value, value)
        SymbolTable.table[id_value] = value

    @staticmethod
    def var_declared(id_value):
        if id_value in SymbolTable.table.keys():
            raise Exception("Identifier has been previously declared")

    @staticmethod
    def dec_var(var_type, id):
        SymbolTable.var_declared(id)
        SymbolTable.table[id] = (var_type, None)

    
    @staticmethod
    def getTable():
        # METHOD FOR DEBUGGING ONLY
        print(f"SymbolTable: {SymbolTable.table}")