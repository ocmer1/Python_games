from Tkinter import *
import random

WIDTH = 400
HEIGHT = 400
dotsize = 20
offset = 19
textmsg = "Press space to start"
in_game = False
CENTER = [WIDTH / 2 - dotsize, HEIGHT / 2 - dotsize, WIDTH / 2, HEIGHT / 2]

class Snake:
	def __init__(self, pos, length, direction='Left'):
		self.pos = pos
		self.length = length
		self.appended = False
		self.body = []
		self.body.append(canvas.create_oval(self.pos, fill='Red', outline='Red', tags="Dot"))
		self.direction = direction
		self.prev_direction = direction
		for i in range(1, self.length):
			dotpos = [0,0,0,0]
			dotpos[0] = self.pos[0] + i * dotsize + 1
			dotpos[1] = self.pos[1]
			dotpos[2] = self.pos[2] + i * dotsize + 1
			dotpos[3] = self.pos[3]
			self.body.append(canvas.create_oval(dotpos, fill='Yellow', outline='Yellow', tags="Dot")) 
				
	def grow(self):
		self.body.append(canvas.create_oval(canvas.coords(self.body[-1]), fill='Yellow', outline='Yellow', tags="Dot"))
		self.length += 1
		self.appended = True
		
	def crawl(self, direction):
		new_coords = []
		vel = {"Left": [-dotsize,0,-dotsize,0], "Right":[dotsize,0,dotsize,0],"Up":[0,-dotsize,0,-dotsize],"Down":[0,dotsize,0,dotsize]}
		if self.appended:
			temp_length = self.length - 1
			self.appended = False
		else:
			temp_length = self.length
		for i in range(0, temp_length - 1):
			new_coords.append(canvas.coords(self.body[i]))
		for i in range(1, temp_length):
			canvas.coords(self.body[i], new_coords[i-1][0], new_coords[i-1][1], new_coords[i-1][2], new_coords[i-1][3]) 
		self.pos[0] += vel[direction][0]	
		self.pos[1] += vel[direction][1]	
		self.pos[2] += vel[direction][2]	
		self.pos[3] += vel[direction][3]
		canvas.coords(self.body[0], self.pos[0], self.pos[1], self.pos[2], self.pos[3])
		self.prev_direction = direction

def generate_random_pos():
	random_pos_x = random.randrange(dotsize, WIDTH - dotsize * 2, dotsize)
	random_pos_y = random.randrange(dotsize, HEIGHT - dotsize * 2, dotsize)
	return [random_pos_x + 2, random_pos_y + 2, random_pos_x + dotsize - 2, random_pos_y + dotsize - 2]

def new_apple():
	global apple
	canvas.delete("Apple") 
	random_pos = generate_random_pos()
	for i in range(my_snake.length):
		while my_snake.body[i] in canvas.find_overlapping(random_pos[0], random_pos[1], random_pos[2], random_pos[3]):
			random_pos = generate_random_pos()
	apple = canvas.create_oval(random_pos, fill="Green", outline="Green", tags="Apple")

def check_apple():
	global score, speed
	if apple in canvas.find_overlapping(my_snake.pos[0], my_snake.pos[1], my_snake.pos[2], my_snake.pos[3]):
		new_apple()
		my_snake.grow()
		score += 1
		scoretext = "Score: " + str(score)
		canvas.itemconfig(scorelabel, text=scoretext)
		speed = int(speed * 0.9)

def check_collide():
	global in_game
	if not my_snake.body[0] in canvas.find_enclosed(offset, offset, WIDTH-offset, HEIGHT-offset):
		canvas.after_cancel(timer)
		textmsg = "Hit edge! Score: " + str(score) + " Press space to reset"
		canvas.itemconfig(scorelabel, text=textmsg)
		in_game = False

	for i in range(1, len(my_snake.body)):
		if my_snake.body[i] in canvas.find_overlapping(my_snake.pos[0] + 1, my_snake.pos[1] + 1, my_snake.pos[2] - 1, my_snake.pos[3] - 1):
			canvas.after_cancel(timer)
			textmsg = "Hit self! Score: " + str(score) + " Press space to reset"
			canvas.itemconfig(scorelabel, text=textmsg)
			in_game = False
		
def update():
	global timer
	my_snake.crawl(my_snake.direction)
	timer = canvas.after(speed, update)
	check_apple()
	check_collide()

def keydown(key):
	directions = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
	if key.keysym in directions and not my_snake.prev_direction == directions[key.keysym]:
		my_snake.direction = key.keysym
	if key.keysym == "space" and in_game == False:
		new_game()

def new_game():
	global score, apple, my_snake, in_game, speed
	canvas.delete("Dot")
	canvas.delete("Apple")
	snakepos = [WIDTH / 2 - dotsize, HEIGHT / 2 - dotsize, WIDTH / 2, HEIGHT / 2]
	my_snake = Snake(snakepos, 3)
	in_game = True
	apple = 0
	score = 0
	speed = 500
	scoretext = "Score: " + str(score)
	canvas.itemconfig(scorelabel, text=scoretext)
	new_apple()
	update()

root = Tk()
root.wm_title("Snake")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0, bg="Black")
canvas.create_rectangle(offset, offset, WIDTH-offset, HEIGHT-offset, outline="White")
scorelabel = canvas.create_text(200, 10, text=textmsg, fill='White', font=('Arial, 12'))
canvas.pack()
canvas.bind("<KeyPress>", keydown)

my_snake = Snake(CENTER, 3)

canvas.focus_set()
root.mainloop()     
