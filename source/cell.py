class Cell:
    row = None
    col = None
    number = None
    has_mine = False
    def __init__(self,row=None,col=None):
        self.row = row
        self.col = col
    def set_has_mine(self,value):
        self.has_mine = value
    def set_number(self,n):
        self.number=n
    def get_has_mine(self):
        return self.has_mine
    def get_row(self):
        return self.row
    def get_col(self):
        return self.col
    def get_number(self):
        return self.number
    def __eq__(self, other):
        '''Override for self==other'''
        if isinstance(other, Cell):
            return self.row == other.row and self.col == other.col
        return False
    # Without the __hash__ function, comparing sets containing objects of the Cell class would not work correctly 
    # because the set comparison operation requires the elements of the set to be hashable. 
    # In Python, an object must implement the __hash__ method to be hashable, which means it can be used as a key in a dictionary or as an element in a set.
    def __hash__(self):
        return hash((self.row, self.col))