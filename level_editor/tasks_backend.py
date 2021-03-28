def getFillSquares(tl_corner, br_corner, ratio):
    self.tl_corner = tl_corner
    self.br_corner = br_corner
    self.squares = []
    self.ratio = ratio

    self.total_rows = int(self.br_corner/self.ratio)
    self.bl_corner = self.br_corner - ( (self.br_corner - (self.ratio*self.total_rows)) - self.tl_corner)
    self.total_columns = (self.br_corner - (self.ratio*self.total_rows)) - self.tl_corner

    for y in range(0, self.total_columns+1):
        for x in range(0, self.total_rows+1):
            self.squares.append((y+bl_corner)-(ratio*x))
    self.squares.sort()
    return self.squares

