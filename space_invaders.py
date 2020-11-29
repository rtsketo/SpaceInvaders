# Space Invaders
# python 2.7.12 on Mac
# Thanks to Christian Thompson 
# Python Game Programming Tutorial: Space Invaders
# http://christianthompson.com/

import math
import os
import platform
import random
import turtle
import winsound


# Play sound file
def play_sound(file): pass
def play_sound_win(file): winsound.PlaySound(file, winsound.SND_ASYNC)
def play_sound_mac(file): os.system(f"afplay {file}&")
def play_sound_lnx(file): os.system(f"aplay {file}&")


# Define play_sound based on OS
if platform.system() == "Windows":
    play_sound = play_sound_win
elif platform.system() == "Darwin":
    play_sound = play_sound_mac
else:
    play_sound = play_sound_lnx

# Set up the screen
win = turtle.Screen()
win.bgcolor("black")
win.title("Space Invaders")
win.bgpic("space_invaders_background.gif")

# Register the graphics for the game
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pensize(3)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 100

# Draw the score on stage
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
score_string = "Score: %s" % score
score_pen.write(score_string, False, align="left", font=("Arial", 14, "bold"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.speed(0)
player.penup()
player.setposition(0, -250)
player.setheading(90)

player_speed = 15

# Choose number of enemies
number_of_enemies = 4

# Create an empty list of enemies
enemiesList = []

# Add enemies to the list
# We need to create more turtle objects

for i in range(number_of_enemies):
    # Create the enemy
    enemiesList.append(turtle.Turtle())

for enemy in enemiesList:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.speed(0)
    enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(100, 200)
    enemy.setposition(x, y)

enemy_speed = 2

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.speed(0)
bullet.penup()
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bullet_speed = 20

# Define bullet state
# we have 2 states:
# ready - ready to fire bullet
# fire - bullet is firing

bullet_state = "ready"


# Move the player left and right
# noinspection PyShadowingNames
def move_left():
    x = player.xcor()
    x = x - player_speed
    if x < -280:
        x = -280
    player.setx(x)


# noinspection PyShadowingNames
def move_right():
    x = player.xcor()
    x = x + player_speed
    if x > 280:
        x = 280
    player.setx(x)


# noinspection PyShadowingNames
def fire_bullet():
    # Declare bullet_state as a global if it needs change
    global bullet_state
    if bullet_state == "ready":
        play_sound("laser.wav")
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        bullet_state = "fire"


def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# Main game loop
while True:
    for enemy in enemiesList:
        # This is a forever loop
        # Move the enemy
        x = enemy.xcor()
        x = x + enemy_speed
        enemy.setx(x)

        # Move enemy back and down
        if enemy.xcor() > 280:
            enemy_speed = enemy_speed * -1
            y = enemy.ycor()
            y = y - 40
            enemy.sety(y)
        if enemy.xcor() < -280:
            enemy_speed = enemy_speed * -1
            y = enemy.ycor()
            y = y - 40
            enemy.sety(y)

        # Check for collision between bullet and enemy
        if is_collision(bullet, enemy):
            play_sound("explosion.wav")
            # Reset the bullet
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 200)
            enemy.setposition(x, y)
            # Update the score
            score += 10
            score_string = "Score: %s" % score
            score_pen.clear()
            score_pen.write(score_string, False, align="left", font=("Arial", 14, "bold"))

        # Check for collision between enemy and player
        if is_collision(player, enemy):
            play_sound("explosion.wav")
            player.hideturtle()
            enemy.hideturtle()
            print("GAME OVER")
            break

    # Move the bullet only when bullet_state is "fire"
    if bullet_state == "fire":
        y = bullet.ycor()
        y = y + bullet_speed
        bullet.sety(y)

    # Check to see if bullet has reached the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"

# delay = raw_input("Press enter to finish")
