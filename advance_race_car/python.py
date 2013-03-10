# lines that go in every target program
import RaceCarApp as rc
car = rc.Car()

main()

# translation of source program

# The goal is to steer around the edge of a map and to stop at the initial point that the car began to go around the edge
#
#
# conditional statements edit?
# change make to define?
#
#

def main():
    move_around_track()

def turn(direction):
    car.steer(direction)
    car.drive("forward", 1)
    car.steer("straight")

def move_arround_track:
    # go to the edge of the board(left side)

    if car.can_move("left"):
        turn("left")

    while car.can_move("forward"):
        car.drive("forward", 1)

    # remember the original position so you know when to stop
    original_position = car.get_position()

    # start to go around the board counter-clockwise
    turn(left)

    while car.get_position() != original_position:
        # try to stay next to the boundary
        if car.can_move("right"):
            turn("right")
        elif car.can_move("straight"):
            # drive forward 1 is given after all of the conditionals
            pass
        elif car.can_move("left"):
            turn("left")
        else:
            # error
            pass

        car.drive("forward", 1)
