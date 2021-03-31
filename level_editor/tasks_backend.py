def getFillSquares(tl_corner, br_corner, ratio):
    squares = []
    total_rows = int((br_corner-tl_corner)/ratio)
    print(total_rows)
    bl_corner = br_corner - ( (br_corner - (ratio*total_rows)) - tl_corner)
    print(bl_corner)
    total_columns = (br_corner - (ratio*total_rows)) - tl_corner
    print(total_columns)

    for y in range(0, total_columns+1):
        for x in range(0, total_rows+1):
            squares.append((y+bl_corner)-(ratio*x))
    squares.sort()
    return squares

def getDoorTiles(tl_corner, ratio):
    tiles = [tl_corner]
    ratio = ratio - 1
    tiles.append(tl_corner+1)
    tiles.append(tl_corner+1+ratio)
    tiles.append(tl_corner+1+ratio+1)
    return[tiles]