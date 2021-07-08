# def circleToSquare(rows):
#     width = -1
#     widths = []
#     full_widths = []
#     paddings = []
#     cells = []
#     cells_split = []
#     going_up = True
#     done = False
#     start = 1
# 
#     while not done:
#         if width == rows:
#             going_up = False
#         if going_up:
#             width += 2
#         else:
#             width -=2
#         widths.append(width)
#         full_widths.append(rows)
#         paddings.append(int((rows-width)/2))
#         if going_up == False and width == 1:
#             done = True
# 
#     count = -1    
#     for x in widths:
#         count +=1
#         for y in range(0,paddings[count]):
#             cells.append("0")
#         for l in range(0,widths[count]):
#             cells.append("1")
#         for y in range(0,paddings[count]):
#             cells.append("0")
# 
#     for i in range(0, len(cells), rows):
#         cells_split.append(cells[i:i + rows])
#         
#     return (cells_split,cells)

#well that didn't work

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
#Get that WEIGHT
    
