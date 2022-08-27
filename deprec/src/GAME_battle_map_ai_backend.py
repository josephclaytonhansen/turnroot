def circleToSquare(m,s,move_squares):
    cells = []
    cells_weight = []
    cells_split = []
    width = (m*2) + 1
    height = (m*2) + 1
    for x in range(-m, m+1):
        for y in range(-m, m+1):
            cells.append((x+s[0],y+s[1]))
            if (x+s[0],y+s[1]) in move_squares:
                cells_weight.append("1")
            else:
                cells_weight.append("0")
    
    for i in range(0, len(cells_weight), width):
        cells_split.append(cells_weight[i:i + width])
    return (cells_split)

def gridWeight(l):
    pass
