from Tkinter import *
import random

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ballpos = [WIDTH / 2 - BALL_RADIUS, HEIGHT / 2 - BALL_RADIUS, WIDTH / 2 + BALL_RADIUS, HEIGHT / 2 + BALL_RADIUS]

def spawn_ball(direction):
    global ballpos, ball_vel # these are vectors stored as lists
    ballpos = [WIDTH / 2 - BALL_RADIUS, HEIGHT / 2 - BALL_RADIUS, WIDTH / 2 + BALL_RADIUS, HEIGHT / 2 + BALL_RADIUS]
    ball_vel = [random.randrange(120, 240) / 60.0, random.randrange(60, 180) / -60.0]
    if direction == LEFT:
        ball_vel[0] = - ball_vel[0]
    canvas.coords(ball, ballpos[0], ballpos[1], ballpos[2], ballpos[3])
    canvas.coords(paddle1, 0, HEIGHT / 2 - HALF_PAD_HEIGHT, PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT)
    canvas.coords(paddle2, WIDTH - PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT, WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT)
    draw()

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    direction_rand = random.randrange(1,3)
    if direction_rand == 1:
        direction = LEFT
    else:
        direction = RIGHT
    spawn_ball(direction)

def draw():
    global ballpos, ball_vel, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, timer
    if (ballpos[1] < 0) or (ballpos[3] > HEIGHT):
        ball_vel[1] = -ball_vel[1]
        
    if (ballpos[0] < PAD_WIDTH): 
        if (ballpos[1] >= paddle1_pos - 20) and (ballpos[1] <= paddle1_pos + 60):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            canvas.after_cancel(timer)
            spawn_ball(RIGHT)
         
    if (ballpos[2] > WIDTH - PAD_WIDTH):
    	if (ballpos[1] >= paddle2_pos - 20) and (ballpos[1] <= paddle2_pos + 60):
            ball_vel[0] = -ball_vel[0] 
            ball_vel[0] = ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            canvas.after_cancel(timer)
            spawn_ball(LEFT)

                
    if (paddle1_pos + paddle1_vel >= 0) and (paddle1_pos + PAD_HEIGHT + paddle1_vel <= HEIGHT):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel >= 0) and (paddle2_pos + PAD_HEIGHT +  paddle2_vel <= HEIGHT):
        paddle2_pos += paddle2_vel
      
    ballpos[0] += ball_vel[0]
    ballpos[1] += ball_vel[1]
    ballpos[2] += ball_vel[0]
    ballpos[3] += ball_vel[1]
    
    canvas.coords(ball, ballpos[0], ballpos[1], ballpos[2], ballpos[3])
    canvas.coords(paddle1, 0, paddle1_pos, PAD_WIDTH, paddle1_pos + PAD_HEIGHT)
    canvas.coords(paddle2, WIDTH - PAD_WIDTH, paddle2_pos, WIDTH, paddle2_pos + PAD_HEIGHT)
    timer = canvas.after(16, draw)

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key.keysym == "w":
        paddle1_vel = -3
    elif key.keysym == "s":
        paddle1_vel = 3
    elif key.keysym == "Up":
        paddle2_vel = -3
    elif key.keysym == "Down":
        paddle2_vel = 3
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key.keysym == "w":
        paddle1_vel = 0
    elif key.keysym == "s":
        paddle1_vel = 0
    elif key.keysym == "Up":
        paddle2_vel = 0
    elif key.keysym == "Down":
        paddle2_vel = 0
        

root = Tk()
canvas = Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0, bg="Black")
canvas.pack()
canvas.bind("<KeyPress>", keydown)
canvas.bind("<KeyRelease>", keyup)
canvas.create_line(WIDTH / 2, 0,WIDTH / 2, HEIGHT, fill="White")
canvas.create_line(PAD_WIDTH, 0,PAD_WIDTH, HEIGHT, fill="White")
canvas.create_line(WIDTH - PAD_WIDTH, 0,WIDTH - PAD_WIDTH, HEIGHT, fill="White")
ball = canvas.create_oval(ballpos, fill="White", outline="White")
paddle1 = canvas.create_rectangle(0, HEIGHT / 2 - HALF_PAD_HEIGHT, PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT, fill="White")
paddle2 = canvas.create_rectangle(WIDTH - PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT, WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT, fill="White")

canvas.focus_set()

new_game()

mainloop()
