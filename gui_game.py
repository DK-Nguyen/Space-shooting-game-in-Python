# TIE-02106 Introduction to Programming
# Nguyen Duy Khoa, nguyen29@student.tut.fi, student number: 272580
# Nguyen Quang Tung, quangtung.nguyen@student.tut.fi, student number: 272575
# Solution of task 13.6: Design and implementation of a graphical user interface

"""
This program implements a spaceship shooting game which makes use of some advanced
topics not covered in the course like inheritance, Turtle library which we learned
from Youtube and Google. However, we guarantee that the code is original and we
spent a lot of time on studying to understand the new concepts and adding new features to
the game and make it our own unique version.
"""


import tkinter as tk
import random
import turtle
import os


ENEMY_NUMBER = 1
LIVES = 3


class UserInterface:
    """
    This class is used to set up the game
    """
    def __init__(self):
        # make the game window and create a Canvas
        self.__root = tk.Tk()
        self.__root.title("Star wars!")
        self.__canvas = tk.Canvas(master=self.__root, width=800, height=800)
        self.__canvas.grid(column=0, row=0)
        # set up the scores and lives labels
        self.__lives = LIVES
        self.__livesShown = tk.StringVar()
        self.__livesShown.set(str(self.__lives))
        self.__score = 0
        self.__scoreShown = tk.StringVar()
        self.__scoreShown.set(str(self.__score))
        self.__gameStatus = "playing"
        # put the buttons on
        self.__buttons = tk.Frame(self.__root, width=35)
        tk.Button(self.__buttons, text="Start", command=self.start).grid()
        tk.Button(self.__buttons, text="Quit", command=self.__root.destroy).grid()
        self.__buttons.grid(column=1, row=0)
        # put the labels on
        self.__scoreboard = tk.Frame(self.__root, width=35, height=100)
        tk.Label(self.__scoreboard, text='Lives').grid()
        tk.Label(self.__scoreboard, textvariable=self.__livesShown).grid()
        tk.Label(self.__scoreboard, text='Game Score').grid()
        tk.Label(self.__scoreboard, textvariable=self.__scoreShown).grid()
        tk.Label(self.__scoreboard, text='Click Start to play.\n'
                                         'Use Arrow Keys to move\n'
                                         'and Space to shoot', fg="red").grid()
        self.__scoreboard.grid(column=2, row=0)
        # now we draw the game screen
        self.__pen = turtle.RawTurtle(self.__canvas)
        self.draw_border()
        self.__screen = self.__pen.getscreen()
        self.__screen.bgpic("s.gif")

        self.__player = None
        self.__bullet = None
        self.__enemies = None
        self.__gameOver = None

        self.__root.mainloop()

    def get_canvas(self):
        return self.__canvas

    def draw_border(self):
        # use this function to draw the border for the game
        self.__pen.speed(0)
        self.__pen.color("white")
        self.__pen.penup()
        self.__pen.setposition(-300, -300)
        self.__pen.pendown()
        self.__pen.pensize(3)
        for i in range(4):
            self.__pen.forward(600)
            self.__pen.left(90)
        self.__pen.hideturtle()

    def start(self):
        self.__lives = LIVES
        self.__score = 0
        self.__livesShown.set(str(self.__lives))
        self.__scoreShown.set(str(self.__score))

        if self.__player is not None:
            self.__player.reset()
        if self.__enemies is not None:
            for i in self.__enemies:
                i.reset()
        if self.__bullet is not None:
            self.__bullet.reset()
        if self.__gameOver is not None:
            self.__gameOver.grid_remove()

        self.__gameStatus = "playing"
        # create the characters for the game
        self.__player = Player("turtle", "red", 0, 0, self.get_canvas())
        self.__bullet = Bullet("triangle", "white", 0, 0, self.get_canvas(), self.__player)
        # create multiple enemies
        self.__enemies = []
        for i in range(ENEMY_NUMBER):
            self.__enemies.append(Enemies("circle", "yellow",
                                          random.randint(-290, 290), random.randint(-290, 290), self.get_canvas()))

        # biding the arrow keys to the player's functions to move the player
        self.__screen.onkey(self.__player.turn_left, "Left")
        self.__screen.onkey(self.__player.turn_right, "Right")
        self.__screen.onkey(self.__player.go_up, "Up")
        self.__screen.onkey(self.__player.go_down, "Down")
        self.__screen.onkey(self.__bullet.fire, "space")
        self.__screen.listen()

        while self.__gameStatus == "playing":
            self.__player.moving_forward()
            for an_enemy in self.__enemies:
                an_enemy.moving_forward()
                # check for collision between the player and the enemies
                if self.__player.collided(an_enemy):
                    os.system("afplay spaceship_exploded.wav&")
                    an_enemy.goto(random.randint(-290, 290), random.randint(-290, 290))
                    if self.__lives > 0:
                        self.__lives -= 1
                        self.__livesShown.set(str(self.__lives))
                    else:
                        self.__gameStatus = "game over"
                        self.__gameOver = tk.Label(self.__scoreboard, text='Game Over!\n'
                                                                           'Click Start to play again!', fg="blue")
                        self.__gameOver.grid()
                        break
                # check for collision between the bullet and the enemies
                if self.__bullet.collided(an_enemy):
                    os.system("afplay exploded.wav&")
                    an_enemy.goto(random.randint(-290, 290), random.randint(-290, 290))
                    self.__bullet.goto(-1000, 1000)
                    self.__bullet.set_status("ready")
                    self.__score += 1
                    self.__scoreShown.set(str(self.__score))

            self.__bullet.moving_forward()


class Characters(turtle.RawTurtle):
    """class Characters is a child of the turtle.RawTurtle class. Therefore it and its children will
    have all of the methods that the turtle.RawTurtle class has.
    Characters is the parent of the classes Player and Enemies.
    Therefore its attributes do not have the "__" in the beginning
    """

    def __init__(self, character_shape, color, initial_x, initial_y, canvas):
        # each character will be a RawTurtle
        turtle.RawTurtle.__init__(self, canvas=canvas, shape=character_shape)
        self.speed(0)  # the speed animation, 0 is the fastest
        self.penup()  # pull the pen up
        self.color(color)
        self.forward(0)  # Move the turtle forward by the specified distance
        self.setpos(initial_x, initial_y)
        self.velocity = 1

    def moving_forward(self):
        self.forward(self.velocity)

        # detecting the boundaries
        if self.xcor() > 290:
            self.setheading(180)

        if self.xcor() < -290:
            self.setheading(0)

        if self.ycor() > 290:
            self.setheading(270)

        if self.ycor() < -290:
            self.setheading(90)

    # This function is to detect the collisions between the player and the enemies
    def collided(self, other):
        if (self.xcor() >= other.xcor() - 20) and (self.xcor() <= other.xcor() + 20) \
                and (self.ycor() >= other.ycor() - 20) and (self.ycor() <= other.ycor() + 20):
            return True
        else:
            return False


class Player(Characters):
    """class Player is the one that the player control
       it is a child of the Characters class """
    def __init__(self, character_shape, color, initial_x, initial_y, canvas):
        # initiate the class using inheritance
        Characters.__init__(self, character_shape, color, initial_x, initial_y, canvas)
        self.velocity = 9  # this overrides the self.velocity = 1 of the parent class
        self.__lives = 3  # the player gets 3 lives to play

    def turn_left(self):
        self.setheading(180)

    def turn_right(self):
        self.setheading(0)

    def go_up(self):
        self.setheading(90)

    def go_down(self):
        self.setheading(270)


class Enemies(Characters):
    """class Enemies is the enemies of the player
       it is a child of the Characters class """
    def __init__(self, character_shape, color, initial_x, initial_y, canvas):
        Characters.__init__(self, character_shape, color, initial_x, initial_y, canvas)
        self.velocity = 15
        self.setheading(random.randint(0, 360))

    def moving_forward(self):
        self.forward(self.velocity)

        # detecting the boundaries
        if self.xcor() > 290:
            self.setheading(random.randint(90, 270))

        if self.xcor() < -290:
            self.setheading(random.randint(-90, 90))

        if self.ycor() > 290:
            self.setheading(random.randint(180, 360))

        if self.ycor() < -290:
            self.setheading(random.randint(0, 180))


class Bullet(Characters):
    """Creating the bullet for the player to shoot
    This class is also a child of the Characters class"""
    def __init__(self, character_shape, color, initial_x, initial_y, canvas, player):
        Characters.__init__(self, character_shape, color, initial_x, initial_y, canvas)
        self.velocity = 50
        self.__status = "ready"
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.__player = player
        self.goto(-1000, 1000)

    def set_status(self, new_status):
        self.__status = new_status

    def fire(self):
        if self.__status == "ready":
            os.system("afplay shoot.wav&")
            # move the bullet to the coordinate of the player
            self.goto(self.__player.xcor(), self.__player.ycor())
            self.setheading(self.__player.heading())
            self.__status = "firing"

    def moving_forward(self):  # override the moving_forward method from the Character class
        if self.__status == "firing":
            self.forward(self.velocity)
        # if the bullet is outside of the borders: it is ready again to be fired
        if self.xcor() < -290 or self.xcor() > 290 or self.ycor() > 290 or self.ycor() < -290:
            self.__status = "ready"


def main():
    ui = UserInterface()


main()


