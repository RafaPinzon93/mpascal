class symTable(dict):

   def __init__(self, arg):
        super().__init__()
        self.arg = arg

   def add(self, name, value):
        self[name] = value

   def lookup(self, name):
        return self.get(name, None)

   def return_type(self):
        if self.decl:
            return self.decl.returntype
        return None
   def delete()
