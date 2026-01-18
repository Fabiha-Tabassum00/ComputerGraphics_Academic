from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


raindrops = []
rain_direction = 0.0
rain_bend_speed = 2.5
maximum_rain_bend_possible = 30.0

background_color = [1, 1, 1]

house_color = [0.8, 0.8, 1.0]
roof_color = [0.29, 0.0, 0.51]
door_color = [0.25, 0.41, 0.88] 
window_color = [0.25, 0.41, 0.88]
day_to_night_speed = 0.02
is_in_transition = False
transition_target = None

animation_speed = 0.09

def initializing_rain(count=200):
    global raindrops
    raindrops = []
    for _ in range(count):
        raindrops.append({
            'x': random.uniform(-800, 800),
            'y': random.uniform(-800, 800),
            'speed': random.uniform(6.0, 9.0),
            'length': random.uniform(8.0, 45.0)
        })

def draw_point(x, y, size=1.0):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_line(x1, y1, x2, y2, width=1.0):
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_triangle(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()

def draw_rectangle(x, y, width, height):
    glBegin(GL_TRIANGLES)
    
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x, y + height)
    
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

def draw_house():
    
    # house
    glColor3f(1,1,1)
    draw_rectangle(-180, -150, 360, 150)
    
    # roof
    glColor3f(roof_color[0], roof_color[1], roof_color[2])
    draw_triangle(-220, 0, 0, 80, 220, 0)
    
    # door
    glColor3f(door_color[0], door_color[1], door_color[2])
    draw_rectangle(-30, -150, 60, 80)
    
    # door-handle
    glColor3f(0.9, 0.9, 0.1)
    draw_point(15, -100, 5.0)
    
    # windows
    glColor3f(window_color[0], window_color[1], window_color[2])
    
    # left-window
    draw_window(-90, -50, 40)
    # right-window
    draw_window(40, -50, 40)

def draw_window(x, y, size):
    draw_line(x, y, x + size, y, 2.0)
    draw_line(x + size, y, x + size, y + size, 2.0)
    draw_line(x + size, y + size, x, y + size, 2.0)
    draw_line(x, y + size, x, y, 2.0)
    
    draw_line(x, y + size/2, x + size, y + size/2, 2.0)
    draw_line(x + size/2, y, x + size/2, y + size, 2.0)

def draw_rain():
    glColor3f(0.0, 0.0, 1.0) 
    for drop in raindrops:
        end_x = drop['x'] + rain_direction
        end_y = drop['y'] - drop['length']
        
        draw_line(drop['x'], drop['y'], end_x, end_y, 1)

def update_rain():
    for drop in raindrops:
        drop['y'] -= drop['speed'] * animation_speed
        drop['x'] += rain_direction * 0.01  
        
        if drop['y'] < -300:       # resetting when the dropss reach below screen
            drop['y'] = random.uniform(800, 600)
            drop['x'] = random.uniform(-350, 350)


def keyboard_listener(key, x, y):
    global is_transitioning, transition_target
    
    if key == b'd' or key == b'D':
        is_transitioning = True
        transition_target = "day"
        print("Transitioning to Day")
    
    elif key == b'n' or key == b'N':
        is_transitioning = True
        transition_target = "night"
        print("Transitioning to Night")
    
    elif key == b'q' or key == b'Q':
        exit()

def special_key_listener(key, x, y):

    global rain_direction
    
    if key == GLUT_KEY_LEFT:
        # bending left
        rain_direction = max(rain_direction - rain_bend_speed, -maximum_rain_bend_possible)
        print(f"Rain bending LEFT: {rain_direction:.1f}")
    
    elif key == GLUT_KEY_RIGHT:
        # bending left
        rain_direction = min(rain_direction + rain_bend_speed, maximum_rain_bend_possible)
        print(f"Rain bending RIGHT: {rain_direction:.1f}")

def setup_projection():
    glViewport(0, 0, 800, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, -300, 300, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    glClearColor(0, 0, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    draw_house()
    draw_rain()
    
    glutSwapBuffers()

def animate():
    update_rain()
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(800, 500)
    glutInitWindowPosition(200, 200)
    glutCreateWindow(b"House in Rainfall")
    
    initializing_rain(30)
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    
    
    glutMainLoop()

if __name__ == "__main__":

    main()
