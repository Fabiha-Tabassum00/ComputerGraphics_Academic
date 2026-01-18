from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random 
import time

# declaring globally
diam_speed = 1
diam_speed_max = 5
score = 0
width_win, height_win = 500, 500

# buttons
is_game_running = True
show_play_icon = False
is_game_paused = False
is_cheat_mode_active = False

# sizes and positions of buttons
restart_button = {
    'x': 0, 'y': 460, 'width': 40, 'height': 40
}
exit_button = {
    'x': 460, 'y': 460, 'width': 40, 'height': 40
}
play_button_1 = {
    'x': 220, 'y': 460, 'width': 40, 'height': 40
}
play_button_2 = {
    'x': 240, 'y': 460, 'width': 20, 'height': 40
}

# diamond and catcher positions
diam_postion = 75
diam_color = (1, 0, 0)
diam_shape = [{
    "right_corner": {"x": diam_postion, "y": 500},
    "left_corner": {"x": diam_postion-20, "y": 500},
    "top_point": {"x": diam_postion-10, "y": 510},
    "bottom_point": {"x": diam_postion-10, "y": 490}},  
    diam_color] 

catcher_horizontal = 0
catcher_color = (1, 1, 1)
catcher_shape = [{
    "bottom_edge": {"x1": 20, "y1": 20, "x2": 100, "y2": 20},
    "left_slope": {"x1": 0, "y1": 40, "x2": 20 + 0, "y2": 20},
    "right_slope": {"x1": 100 + 0, "y1": 20, "x2": 120 + 0, "y2": 40},
    "top_edge": {"x1": 0, "y1": 40, "x2": 120 + 0, "y2": 40}
}, catcher_color]

def draw_points(x, y, color):
    glColor3f(*color)
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def convert_coordinate(x,y):
    global height_win
    a = x 
    b = height_win-y
    return (a,b)

def midpoint_line(x1, y1, x2, y2, zone, color):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)  
    y = y1
    # print(x1, y1, x2, y2, zone)
    for x in range(x1, x2+1):
        oz_x, oz_y = convert_to_nonzero_zone(x, y, zone)

        draw_points(oz_x , oz_y, color) 
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1

    
def find_zone(x1, y1, x2, y2):    
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6 
               
def convert_to_zone0(x, y, zone):  
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convert_to_nonzero_zone(x,y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def eight_way_symmetry(x1, y1, x2, y2, color = (1, 1, 0)):
    zone = find_zone(x1, y1, x2, y2)

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    midpoint_line(x1, y1, x2, y2, zone, color)   

def catcher():
    global catcher_data, catcher_pos

    catcher_data[0]["base"]["x1"] = 20 + catcher_pos
    catcher_data[0]["base"]["x2"] = 100 + catcher_pos
    catcher_data[0]["left_diagonal"]["x1"] = catcher_pos
    catcher_data[0]["left_diagonal"]["x2"] = 20 + catcher_pos
    catcher_data[0]["right_diagonal"]["x1"] = 100 + catcher_pos
    catcher_data[0]["right_diagonal"]["x2"] = 120 + catcher_pos
    catcher_data[0]["above"]["x1"] = catcher_pos
    catcher_data[0]["above"]["x2"] = 120 + catcher_pos

    eight_way_symmetry(catcher_data[0]["base"]["x1"], catcher_data[0]["base"]["y1"], catcher_data[0]["base"]["x2"], catcher_data[0]["base"]["y2"], catcher_data[1]) #base
    eight_way_symmetry(catcher_data[0]["left_diagonal"]["x1"], catcher_data[0]["left_diagonal"]["y1"], catcher_data[0]["left_diagonal"]["x2"], catcher_data[0]["left_diagonal"]["y2"], catcher_data[1]) #left diagonal
    eight_way_symmetry(catcher_data[0]["right_diagonal"]["x1"], catcher_data[0]["right_diagonal"]["y1"], catcher_data[0]["right_diagonal"]["x2"], catcher_data[0]["right_diagonal"]["y2"], catcher_data[1]) #right diagonal
    eight_way_symmetry(catcher_data[0]["above"]["x1"], catcher_data[0]["above"]["y1"], catcher_data[0]["above"]["x2"], catcher_data[0]["above"]["y2"], catcher_data[1]) #above    

def diamond():
    global diam_pos
    eight_way_symmetry(diam_pos[0]["edge1"]["x"], diam_pos[0]["edge1"]["y"], diam_pos[0]["edge3"]["x"], diam_pos[0]["edge3"]["y"], diam_pos[1])
    eight_way_symmetry(diam_pos[0]["edge2"]["x"], diam_pos[0]["edge2"]["y"], diam_pos[0]["edge4"]["x"], diam_pos[0]["edge4"]["y"],  diam_pos[1])
    eight_way_symmetry(diam_pos[0]["edge2"]["x"], diam_pos[0]["edge2"]["y"], diam_pos[0]["edge3"]["x"], diam_pos[0]["edge3"]["y"],  diam_pos[1])


def specialKeyListener(key, x, y):
    global catcher_info, catcher_pos, stop, isfrozen, cheat_mode
    if cheat_mode:
        return
    if key==GLUT_KEY_RIGHT:
        if catcher_data[0]["right_diagonal"]["x2"] and catcher_data[0]["above"]["x2"]< 490 and stop and is_game_paused == False:
            catcher_pos += 20
        else:
            pass
    elif key==GLUT_KEY_LEFT:
        if catcher_pos > 0 and stop and is_game_paused == False:
            catcher_pos -= 20
        else:
            pass
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global cheat_mode
    if key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        if cheat_mode:
            print("Cheat Mode: ACTIVATED")
        else:
            print("Cheat Mode: DISABLED")
    glutPostRedisplay()

def has_collided(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])

def draw_arrow():
    eight_way_symmetry(0, 480, 20, 500, (0, 0, 1))
    eight_way_symmetry(0, 480, 20, 460, (0, 0, 1))
    eight_way_symmetry(0, 480, 40, 480, (0, 0, 1))

def draw_pause():
    global pause           
    if pause and is_game_paused:
        eight_way_symmetry(220, 460, 220, 500, (1, 1, 0))
        eight_way_symmetry(220, 460, 260, 480, (1, 1, 0))
        eight_way_symmetry(260, 480, 220, 500, (1, 1, 0))
    else:
        eight_way_symmetry(240, 460, 240, 500, (1, 1, 0))
        eight_way_symmetry(260, 460, 260, 500, (1, 1, 0))
  

def draw_cross():
    eight_way_symmetry(460, 460, 500, 500, (1, 0, 0))
    eight_way_symmetry(460, 500, 500, 460, (1, 0, 0))

def animate():
    global diamond_pos, diamond_color, diamond_x, stop, speed, points, is_game_paused, restart_button, is_cheat_mode_active, is_game_running
    if stop and is_game_paused != True:    
            catcher_box = {
            'x': catcher_data[0]["base"]["x1"],
            'y': catcher_data[0]["base"]["y1"],
            'width': catcher_data[0]["above"]["x2"] - catcher_data[0]["above"]["x1"],
            'height': catcher_data[0]["above"]["y2"] - catcher_data[0]["base"]["y1"]
            }

            diamond_box = {
            'x': diamond_pos[0]["edge1"]["x"],
            'y': diamond_pos[0]["edge4"]["y"],
            'width': abs(diamond_pos[0]["edge1"]["x"] - diamond_pos[0]["edge2"]["x"]),
            'height': abs(diamond_pos[0]["edge3"]["y"] - diamond_pos[0]["edge4"]["y"])
            }

            if cheat_mode and stop:
                target_pos = diamond_pos[0]["edge1"]["x"] - 60
                if catcher_pos < target_pos:
                    catcher_pos += min(10, target_pos - catcher_pos) 
                elif catcher_pos > target_pos:
                    catcher_pos -= min(10, catcher_pos - target_pos) 


    glutPostRedisplay()
    time.sleep(0.01)

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    catcher()
    diamond()
    draw_arrow()
    draw_pause()
    draw_cross()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener) 
glutMainLoop()
