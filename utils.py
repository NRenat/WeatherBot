def degrees_to_direction(deg):
    directions = [
        "N", "NE", "E", "SE", "S", "SW", "W", "NW"
    ]
    index = int((deg + 22.5) // 45) % 8
    return directions[index]
