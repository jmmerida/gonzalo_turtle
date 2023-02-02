import turtle
import segno
from typing import Tuple


class Maze:
    """Class that represents a Maze to uncover the secrets
    of the teacher Gonzalo.

    Args:
        filename (str): Filepath of the maze file. Walls are defined by the "#" character,
        the " "(space character) represents the path, and the "S" is the players starting position
    """

    start_x: int
    start_y: int

    def __init__(self, filename: str) -> None:

        self.wn = turtle.Screen()
        self.wn.title("Maze Game")
        self.wn.bgcolor("black")
        self.wn.setup(700, 700)

        self.wall_pen = turtle.Turtle()
        self.wall_pen.penup()
        self.wall_pen.speed(0)
        self.wall_pen.color("white")
        self.wall_pen.pensize(5)
        self.wall_pen.fillcolor("white")

        self.player = turtle.Turtle()
        self.player.shape("turtle")
        self.player.color("white")
        self.player.penup()

        self.filename = filename
        self.maze = []
        self.load_maze()
        self.start_x = len(self.maze[0]) * 25
        self.start_y = len(self.maze) * 25
        self.draw_walls()
        self.set_player_position()
        self.bind_keys()

    def load_maze(self) -> None:
        """Loads the maze based in the loaded file"""

        with open(self.filename, "r", encoding="UTF-8") as file:
            for line in file:
                self.maze.append(list(line.strip()))

    def draw_walls(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == "#":
                    self.wall_pen.goto(j * 50 - self.start_x, self.start_y - i * 50)
                    self.wall_pen.pendown()
                    self.wall_pen.begin_fill()
                    for _ in range(4):
                        self.wall_pen.forward(50)
                        self.wall_pen.right(90)
                    self.wall_pen.end_fill()
                    self.wall_pen.penup()
                if self.maze[i][j] == "X":
                    dot = turtle.Turtle()
                    dot.speed(0)
                    dot.shape("circle")
                    dot.color("blue")
                    dot.penup()
                    dot.setposition(
                        j * 50 - self.start_x + 25, -i * 50 + self.start_y - 25
                    )
                    dot.stamp()

    def set_player_position(self) -> None:
        """Sets the player position"""

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == "GONZA":
                    self.player.goto(
                        j * 50 - self.start_x + 25, self.start_y - i * 50 - 25
                    )

    def bind_keys(self) -> None:
        """Performs the binding of the keys to the player actions"""

        self.wn.listen()
        self.wn.onkeypress(self.go_up, "Up")
        self.wn.onkeypress(self.go_right, "Right")

    def go_up(self) -> None:
        """Performs the "go up" action"""

        x, y = self.update_position()
        print("x = {0}, y = {1}".format(x, y))
        print(self.maze[y - 1][x])
        if y < len(self.maze) - 1 and self.maze[y + 1][x] != "#":
            self.player.sety(self.player.ycor() + 50)

    def go_down(self) -> None:
        """Performs the "go down" action"""

        x, y = self.update_position()
        print("x = {0}, y = {1}".format(x, y))
        print(self.maze[y + 1][x])
        if y > 0 and self.maze[y - 1][x] != "#":
            self.player.sety(self.player.ycor() - 50)
            self.win()

    def go_left(self) -> None:
        """Performs the "go left" action"""

        x, y = self.update_position()
        print("x = {0}, y = {1}".format(x, y))
        print(self.maze[y][x - 1])
        if x > 0 and self.maze[y][x - 1] != "#":
            self.player.setx(self.player.xcor() - 50)
            self.win()

    def go_right(self) -> None:
        """Performs the "go right" action"""

        x, y = self.update_position()
        print("x = {0}, y = {1}".format(x, y))
        print(self.maze[y][x + 1])
        if x < len(self.maze[0]) - 1 and self.maze[y][x + 1] != "#":
            self.player.setx(self.player.xcor() + 50)
            self.win()

    def update_position(self) -> Tuple[int, int]:
        x = int((self.player.xcor() + self.start_x) / 50)
        y = int((self.start_y - self.player.ycor()) / 50)
        return x, x

    def has_won(self, x: int, y: int) -> bool:
        return self.maze[y][x] == "X"

    def win(self) -> None:
        x, y = self.update_position()
        if self.has_won(x, y):
            self.draw_reward()

    def draw_reward(self) -> None:
        qr = segno.make(
            "git clone https://github.com/jmmerida/gonzalo_turtle.git && checkout gonza"
        )
        qr.save("config/chisme.png", border=5, scale=20)

        self.wn.clear()
        self.wn.bgpic("config/chisme.png")

    def run(self) -> None:
        """Represents the mainloop"""
        while True:
            self.wn.update()
        self.wn.mainloop()
