from turtle import Turtle

class Line(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.speed("fastest")
        self.hideturtle()
        self.setheading(270)
        self.shapesize(stretch_wid=0.2, stretch_len=1)

    def draw_line(self):
        self.penup()
        self.goto(0, 280)
        while self.ycor() > -280:
            self.pendown()
            self.forward(20)
            self.penup()
            self.forward(20)
