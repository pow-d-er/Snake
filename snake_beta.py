import curses
from time import sleep
import random
import sys
stdscr = curses.initscr()
curses.start_color()


class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def setter(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self,size,x,y,direction):
        self.size = size
        self.point = []
        self.point.append(Point(x,y))
        self.direction = direction
        self.speed = 1

    def move(self):
        for i in range(1,self.size):
            self.point[-i].setter(self.point[-i - 1].x, self.point[-i - 1].y)
        if self.direction == 1:
            self.point[0].setter(self.point[0].x+2,self.point[0].y)#Right
        if self.direction == 2:
            self.point[0].setter(self.point[0].x,self.point[0].y+1)#Down
        if self.direction == 3:
            self.point[0].setter(self.point[0].x-2, self.point[0].y)#Left
        if self.direction == 4:
            self.point[0].setter(self.point[0].x, self.point[0].y-1)#Up


    def display(self,game):
        if self.point[0].x < 0:
            game.game_over(self)
        if self.point[0].x == game.width:
            game.game_over(self)
        if self.point[0].y < 0:
            game.game_over(self)
        if self.point[0].y == game.height:
            game.game_over(self)

        stdscr.clear()
        for point in self.point:
            stdscr.addstr(point.y,point.x,'  ',
                curses.color_pair(2))

        for i in range(2,self.size):
            if self.point[0].x == self.point[i].x and self.point[0].y == self.point[i].y:
                game.game_over(self)


    def set_direction(self,direction):
        self.direction = direction

    def eat(self):
        self.size += 1
        self.point.append(Point(self.point[-1].x,self.point[-1].y))

    def check(self, key):
        if key == curses.KEY_RIGHT and self.direction != 3:
            self.set_direction(1)
        if key == curses.KEY_DOWN and self.direction != 4:
            self.set_direction(2)
        if key == curses.KEY_LEFT and self.direction != 1:
            self.set_direction(3)
        if key == curses.KEY_UP and self.direction != 2:
            self.set_direction(4)

class Game:
    def __init__(self):
        self.food = []
        self.height, self.width = stdscr.getmaxyx()

    def generate_food(self,snake):
        flag = 1
        if self.food == []:
            x = random.randrange(self.width)
            while flag:
                flag = 0
                while(x%2 == 1):
                    x = random.randrange(self.width)
                y = random.randrange(self.height)
                self.food.append(Point(x,y))
                for point in snake.point:
                    if point == self.food:
                        flag =1


    def display(self):
        for point in self.food:
            stdscr.addstr(point.y,point.x,'  ',curses.color_pair(1))

    def check(self,x,y):
        for food in self.food:
            if food.x == x and food.y == y:
                i = self.food.index(food)
                del self.food[i]
                return 1

    def game_over(self,snake):
        stdscr.clear()
        stdscr.addstr(int(self.height/2),int(self.width/2),'KONIEC GRY')
        stdscr.addstr(int(self.height/2) + 1 ,int(self.width/2),'WYNIK: {}'.format(snake.size))
        stdscr.refresh()
        sleep(2)
        sys.exit(0)

def main(win):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLUE)
    stdscr.nodelay(True)

    game = Game()
    snake = Snake(1,0,0,1)
    counter = 0
    while True:
        for i in range(1,snake.speed+1):
            snake.display(game)
            snake.move()
            if game.check(snake.point[0].x,snake.point[0].y):
                snake.eat()

        game.display()
        stdscr.refresh()
        sleep(0.05)



        key = stdscr.getch()
        snake.check(key)

        game.generate_food(snake)


curses.endwin()

curses.wrapper(main)


if(__name__ == '__main__'):
    main()
