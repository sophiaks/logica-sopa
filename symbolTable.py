from aux import mprint

class SymbolTable():
    def __init__(self):
        self.table = {}

    def assign_right_type(self, id_value, value):
        (table_type, table_value) = self.getValue(id_value)
        (assigned_type, assigned_value) = value

        if (table_type.upper() != assigned_type.upper()):
            raise Exception("SymbolTable type does not match assignment type")

    def getValue(self, idvalue):
        if idvalue not in self.table:
            raise Exception(f"Unrecognized symbol {idvalue} (have you declared it?)")
        if self.table[idvalue] is None:
            pass
        return self.table[idvalue]

    def setValue(self, id_value, value):
        self.assign_right_type(id_value, value)
        self.table[id_value] = value

    def var_declared(self, id_value):
        if id_value in self.table.keys():
            raise Exception("Identifier has been previously declared")

    def dec_var(self, var_type, id):
        self.var_declared(id)
        self.table[id] = (var_type, None)
    
    def getTable(self):
        print(f"SymbolTable: {self.table}")