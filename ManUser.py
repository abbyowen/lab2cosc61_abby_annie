class ManUser:
    def __init__(self):
        self.id = None
        self.role = None
    
    def get_id(self):
        return self.id
    
    def set_id(self, id_num):
        self.id = id_num
    
    def set_role(self, role_val):
        self.role = role_val
    
    def get_role(self):
        return self.role