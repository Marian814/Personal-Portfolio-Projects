import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

game_is_on = True

def exit_game():
    global game_is_on
    game_is_on = False

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(player.go_up, "Up")
screen.onkeypress(player.go_down, "Down")
screen.onkeypress(player.go_right, "Right")
screen.onkeypress(player.go_left, "Left")
screen.onkey(exit_game, "x")

while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move_cars()

    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    if player.is_at_finish_line():
        player.go_to_start()
        scoreboard.increase_level()
        if scoreboard.level % 2 == 0:
            car_manager.level_up_speed()
        elif scoreboard.level < 10:
            car_manager.level_up_cars()

screen.exitonclick()
