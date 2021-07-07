def circleToSquare(rows):
    width = -1
    widths = []
    full_widths = []
    paddings = []
    cells = []
    cells_split = []
    going_up = True
    done = False
    start = 1

    while not done:
        if width == rows:
            going_up = False
        if going_up:
            width += 2
        else:
            width -=2
        widths.append(width)
        full_widths.append(rows)
        paddings.append(int((rows-width)/2))
        if going_up == False and width == 1:
            done = True

    count = -1    
    for x in widths:
        count +=1
        for y in range(0,paddings[count]):
            cells.append("0")
        for l in range(0,widths[count]):
            cells.append("1")
        for y in range(0,paddings[count]):
            cells.append("0")

    for i in range(0, len(cells), rows):
        cells_split.append(cells[i:i + rows])
        
    return (cells_split,cells)

