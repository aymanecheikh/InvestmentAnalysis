from enum import Enum, Flag


class Color(Flag):
    RED = 1
    GREEN = 2
    BLUE = 4
    YELLOW = 8
    BLACK = 16


approved_colors: Color = Color.RED | Color.YELLOW | Color.BLACK
my_car_color: Color = Color.BLACK

if my_car_color in approved_colors:
    print("Your car has been approved from a colours perspective.")
else:
    print("We kindly rejected your car.")
