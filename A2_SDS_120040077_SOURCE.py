import turtle
import random
from functools import partial
import time

key_up, key_down, key_left, key_right, key_space = "Up", "Down", "Left", "Right", "space"
HEADING_BY_KEY = {key_up: 90, key_down: 270, key_left: 180, key_right: 0}
g_snake = None
g_monster = None
g_screen = None
g_intro = None
g_keypressed = None
g_pause = False
g_food = None
g_snake_size = 5  # the initial length of the tail
food_storage = {}  # dictionary in the form of  (x, y) : value
position = []  # contain the location of food (x, y)
opp_move = None
g_snake_speed = 200 #dun put turtle.turtle in the main loop
g_mon_speed = None
g_mon_dir = None
g_game_finished = False
g_win = False
g_defeat = False
g_motion = None
time_show = None
g_start_time = None
g_contact_num = 0
g_snakebody_pos = []
efficient_body_pos=[]

def pause():
    '''is used to pause the game'''
    global g_pause
    g_pause = not g_pause


def game_over():
    global g_game_finished, g_win, g_defeat
    if (abs(g_snake.xcor() - g_monster.xcor()) <= 10 and
        abs(g_snake.ycor() - g_monster.ycor()) <= 10 and
        food_storage != {}):
        '''the snake is caught by the monster'''
        g_game_finished = True
        g_defeat = True
    elif (food_storage == {}):
        g_game_finished = True
        g_win = True


def available_move():
    '''judge the available move for snake when it got stuck'''
    global Xc, Yc, opp_move
    Xc = g_snake.xcor()
    Yc = g_snake.ycor()
    if (-239 < Xc < 239 and -239 < Yc < 239):
        opp_move = ['Up', 'Down', 'Right', 'Left']
    if (Xc >= 239):
        if(Yc >= 239):
            opp_move = ['Left', 'Down']
        elif(Yc <= -239):
            opp_move = ['Up', 'Left']
        else:
            opp_move = ['Up', 'Left', 'Down']
    if (Xc <= -239):
        if(Yc >= 239):
            opp_move = ['Right', 'Down']
        elif(Yc <= -239):
            opp_move = ['Up', 'Right']
        else:
            opp_move = ['Up', 'Right', 'Down']
    if (Yc <= -239):
        if (Xc >= 239):
            opp_move = ['Up', 'Left']
        elif(Xc <= -239):
            opp_move = ['Up', 'Right']
        else:
            opp_move = ['Left', 'Right', 'Up']
    if (Yc >= 239):
        if (Xc >= 239):
            opp_move = ['Left', 'Down']
        elif(Xc <= -239):
            opp_move = ['Right', 'Down']
        else:
            opp_move = ['Left', 'Right', 'Down']


def set_screen():
    screen = turtle.Screen()
    screen.setup(width=500 + 80 * 2, height=500 + 80 * 3)
    screen.title("Snake by Zhouliang")
    screen.tracer(0)
    margin = turtle.Turtle() #set the margin
    margin.shape("square")
    margin.penup()
    margin.pensize(2)
    margin.goto(-250, 250)
    margin.pendown()
    margin.forward(500)
    margin.setheading(270)
    margin.forward(500)
    margin.setheading(180)
    margin.forward(500)
    margin.setheading(90)
    margin.forward(500)
    margin.forward(80)
    margin.setheading(0)
    margin.forward(500)
    margin.setheading(270)
    margin.forward(80)
    margin.hideturtle()
    screen.update()
    return screen


def set_role(shape="square", color="red", x=0, y=0):
    '''set_role is used to inintialize the head of snake
    & the monster'''
    role = turtle.Turtle()
    role.penup()
    role.shape("square")
    role.color(color)
    role.goto(x, y)
    return role


def set_intro():
    intro = set_role(shape="square", color="black", x=-200, y=100)
    intro.hideturtle()
    intro.write('''welcome to zhouliang's version of this game,
    you are going to use four arrow keys 
    to move the snake around the 
    screen, trying to consume all the food 
    before the monster catches you,
    click anywhere to start
    ''', font=('arial', 14, 'normal'))
    g_screen.update()
    return intro


def food_init():
    '''initialize all the food'''
    global food_storage, position
    value = 1
    for i in range(9):
        while True:
            x = random.randint(-11, 11) * 20
            y = random.randint(-11, 11) * 20
            if ((x, y) not in position and
                    (x, y) != (0, 0)):    # food do not overlap with the head at first
                food_storage[(x, y)] = value
                position.append((x, y))
                value += 1
                break
            else:
                continue


def food_consume():
    global g_snake_size, eat, ate, g_snake_speed
    eat = False
    ate = False
    for (x, y) in food_storage.keys():
        if(abs(g_snake.xcor() - x) <= 20 and abs(g_snake.ycor() - y) <= 20 and g_keypressed != None):
            eat = True
            ate = True
            del_x = x
            del_y = y
            for i in range(food_storage[(x, y)]):
                g_snake_size += 1
                g_snake_speed = 210
    if (eat == True):
        del food_storage[(del_x, del_y)]
        eat = False


def food_display():
    '''display the food on the screen'''
    print(food_storage)
    food_consume()
    g_food.hideturtle()
    g_food.clear()
    for (x, y) in food_storage:
        g_food.penup()
        g_food.goto(x, y)
        g_food.pendown()
        g_food.write(food_storage[(x, y)], font=("Arial", 14, 'normal'))
    g_screen.update()
    g_screen.ontimer(food_display, 500)

def time_display():
    while(True):
        if (g_game_finished == False):
            passed_time = time.time()
            time_gap = passed_time - g_start_time
            time_show.clear()
            time_show.up()
            time_show.goto(-60, 260)
            time_show.pendown()
            time_show.write('Time:', font=('arial', 14, 'normal'))
            time_show.penup()
            time_show.goto(0, 260)
            time_show.pendown()
            time_show.write(int(time_gap), font=('arial', 14, 'normal'))
            time_show.hideturtle()
        else:
            break
    g_screen.update()
    g_screen.ontimer(time_display, 1000)

def motion_display():
    g_motion.clear()
    g_motion.pendown()
    g_motion.write(g_keypressed, font=('arial', 14, 'normal'))
    g_motion.hideturtle()
    g_screen.update()
    g_screen.ontimer(motion_display, 500)

def contact_display():
    g_contact.clear()
    g_contact.penup()
    g_contact.goto(-200, 260)
    g_contact.pendown()
    g_contact.write('contact:', font=('arial', 14, 'normal'))
    g_contact.penup()
    g_contact.goto(-120, 260)
    g_contact.pendown()
    g_contact.write(g_contact_num, font=('arial', 14, 'normal'))
    g_contact.hideturtle()
    g_screen.update()
    g_screen.ontimer(contact_display, 1000)

def contact_count():
    global g_contact_num
    for (Xs, Ys) in efficient_body_pos:
        if abs(g_monster.xcor() - Xs) < 20 and abs(g_monster.ycor() - Ys) < 20:
            g_contact_num += 1
            print(g_contact_num)
            
def setSnakeheading(key):
    if key in HEADING_BY_KEY:
        g_snake.setheading(HEADING_BY_KEY[key])


def keypressed_dir(key):
    global g_keypressed
    g_keypressed = key
    setSnakeheading(key)


def onTimerSnake():
    global g_keypressed, g_snake_speed, g_contact_num, efficient_body_pos
    game_over()
    if g_keypressed == None:
        g_screen.ontimer(onTimerSnake, 200)
        return
    if (-230 <= g_snake.xcor() <= 230 and
        -230 <= g_snake.ycor() <= 230 and
        g_pause == False and
        g_game_finished == False):
        print(g_pause)
        head_color = g_snake.color()
        g_snake.up()
        g_snake.color("blue", "black")
        g_snake.stamp()
        Xs = g_snake.xcor()
        Ys = g_snake.ycor()
        g_snakebody_pos.append((Xs, Ys))
        efficient_body_pos = g_snakebody_pos[-(g_snake_size):]
        contact_count()
        # print(efficient_body_pos)
        g_snake.forward(20)
        if len(g_snake.stampItems) > g_snake_size:
            g_snake.clearstamps(1)
        g_snake.color(*head_color)
        g_screen.update()
        g_screen.ontimer(onTimerSnake, g_snake_speed)
    else:
        available_move()
        new_key = g_keypressed
        if new_key in opp_move and g_pause == False and g_game_finished == False:
            keypressed_dir(new_key)
            head_color = g_snake.color()
            g_snake.up()
            g_snake.color("blue", "black")
            g_snake.stamp()
            Xs = g_snake.xcor()
            Ys = g_snake.ycor()
            g_snakebody_pos.append((Xs, Ys))
            efficient_body_pos = g_snakebody_pos[-(g_snake_size):]
            contact_count()
            g_snake.forward(20)
            if len(g_snake.stampItems) > g_snake_size:
                g_snake.clearstamps(1)
            g_snake.color(*head_color)
        else:
            if(g_game_finished == True):
                if (g_win == True):
                    #write win
                    win = set_role(shape="square", color="black",
                                   x=g_snake.xcor(), y=g_snake.ycor()+40)
                    win.hideturtle()
                    win.write('''win!''', font=('arial', 14, 'normal'))
                elif (g_defeat == True):
                    #write game over
                    defeat = set_role(
                        shape="square", color="black", x=g_snake.xcor(), y=g_snake.ycor()+40)
                    defeat.hideturtle()
                    defeat.write('''game over!''', font=('arial', 14, 'normal'))
            print(g_pause)
            g_snake.forward(0)
        g_screen.update()
        g_screen.ontimer(onTimerSnake, g_snake_speed)
        g_snake_speed = 200


def onTimerMonster():
    global g_mon_speed, g_mon_dir
    g_mon_speed = random.randint(300, 320)
    if (g_monster.xcor() <= g_snake.xcor() and g_monster.ycor() <= g_snake.ycor()):
        '''the head of snake on the upper right of monster'''
        if (abs(g_monster.xcor() - g_snake.xcor()) <= abs(g_monster.ycor() - g_snake.ycor())):
            g_mon_dir = 'Up'
        else:
            g_mon_dir = 'Right'
    if (g_monster.xcor() <= g_snake.xcor() and g_monster.ycor() > g_snake.ycor()):
        '''the head of snake on the lower right of monster'''
        if (abs(g_monster.xcor() - g_snake.xcor()) <= abs(g_monster.ycor() - g_snake.ycor())):
            g_mon_dir = 'Down'
        else:
            g_mon_dir = 'Right'
    if (g_monster.xcor() > g_snake.xcor() and g_monster.ycor() > g_snake.ycor()):
        '''the head of snake on the lower left of monster'''
        if (abs(g_monster.xcor() - g_snake.xcor()) <= abs(g_monster.ycor() - g_snake.ycor())):
            g_mon_dir = 'Down'
        else:
            g_mon_dir = 'Left'
    if (g_monster.xcor() > g_snake.xcor() and g_monster.ycor() <= g_snake.ycor()):
        '''the head of snake on the lower left of monster'''
        if (abs(g_monster.xcor() - g_snake.xcor()) <= abs(g_monster.ycor() - g_snake.ycor())):
            g_mon_dir = 'Up'
        else:
            g_mon_dir = 'Left'
    '''the following code block allows monster to move'''
    g_monster.setheading(HEADING_BY_KEY[g_mon_dir])
    g_monster.stamp()
    g_monster.forward(20)
    g_monster.clearstamps(1)
    g_screen.update()
    g_screen.ontimer(onTimerMonster, g_mon_speed)


def start_game(x, y):
    # g_screen.onscreenclick(None) #not finished yet
    global g_start_time
    g_intro.clear()
    g_start_time = time.time()
    food_init()
    g_screen.ontimer(time_display, 500)
    g_screen.ontimer(food_display, 500)
    # while True: #while the game is not over
    g_screen.onkey(partial(keypressed_dir, key_up), key_up)
    g_screen.onkey(partial(keypressed_dir, key_down), key_down)
    g_screen.onkey(partial(keypressed_dir, key_left), key_left)
    g_screen.onkey(partial(keypressed_dir, key_right), key_right)
    g_screen.onkey(pause, "space")
    g_screen.ontimer(onTimerSnake, 500)
    g_screen.ontimer(onTimerMonster, 1000)
    g_screen.ontimer(motion_display, 500)
    g_screen.ontimer(contact_display, 500)

if __name__ == "__main__":
    g_screen = set_screen()
    g_snake = set_role("square", "red", 0, 0)
    g_monster = set_role("square", "purple", x=-110, y=-110)
    g_motion = set_role("square", "black", x=200, y=260)
    g_motion.hideturtle()
    g_food = set_role("square", "black")
    g_food.hideturtle()
    time_show = set_role("square", "black", x=0, y=260)
    time_show.hideturtle()
    g_contact = set_role("square", "black", x=-200, y=260)
    g_contact.hideturtle()
    g_intro = set_intro()
    g_screen.onclick(start_game)
    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()
