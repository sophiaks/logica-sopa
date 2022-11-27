class FuncTable:
    table = {}

    @staticmethod
    def getFunc(idvalue):
        if idvalue not in FuncTable.table:
            raise Exception(f"Unrecognized symbol {idvalue} (have you declared it?)")
        # Returns second value of the tuple -> reference 
        return FuncTable.table[idvalue][1]

    @staticmethod
    def decFunc(func_type, id, reference):
        FuncTable.table[id] = (func_type, reference)

    def setValue(self, id_value, value):
        self.assign_right_type(id_value, value)
        self.table[id_value] = value
    
    @staticmethod
    def getTable():
        # METHOD FOR DEBUGGING ONLY
        print(f"SymbolTable: {FuncTable.table}")