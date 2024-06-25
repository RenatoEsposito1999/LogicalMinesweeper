class Cell:
    row = None
    col = None
    number = None
    has_mine = False
    def __init__(self,row,col):
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
