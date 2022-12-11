from aux import mprint

class SymbolTable:
    position = 0
    table = {}

    @staticmethod
    def assign_right_type(id_value, value):
        (table_type, table_value, _pos) = SymbolTable.getValue(id_value)
        (assigned_type, assigned_value, _pos) = value

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
        _type, _value, _pos = value
        (dec_type, dec_val, dec_pos) = SymbolTable.getValue(id_value)
        SymbolTable.table[id_value] = (_type, _value, dec_pos)

    @staticmethod
    def var_declared(id_value):
        if id_value in SymbolTable.table.keys():
            raise Exception("Identifier has been previously declared")

    @staticmethod
    def dec_var(var_type, id):
        # On declaration we assign position
        SymbolTable.var_declared(id)
        SymbolTable.position += 4
        SymbolTable.table[id] = (var_type, None, SymbolTable.position)

    
    @staticmethod
    def getTable():
        # METHOD FOR DEBUGGING ONLY
        print(f"SymbolTable: {SymbolTable.table}")