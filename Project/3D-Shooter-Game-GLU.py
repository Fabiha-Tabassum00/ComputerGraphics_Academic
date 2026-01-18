from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Camera vars
camera_pos = [0, -300, 200]
camera_angle = 0

# Player
player_pos = [0, 0, 2]  # x, y, z
player_angle = 0  # direction
player_bullets = 15
player_hearts = 5.0
player_grenades = 1
player_speed = 3

# Game state
game_state = "playing"
current_wave = 1
wave_delay = 0
wave_clear_time = 0

# Bullets
bullets = []
bullet_speed = 60

# Bombs
thrown_bombs = []
bomb_speed = 25
particles = []

# Enemies
enemies = []

# Treasure boxes
treasure_boxes = [
    {"x": -420, "y": 420, "z": 0, "open_time": 0},
    {"x": 420, "y": 450, "z": 0, "open_time": 0},
    {"x": -430, "y": -420, "z": 0, "open_time": 0},
    {"x": 430, "y": -430, "z": 0, "open_time": 0},
    {"x": 250, "y": 420, "z": 0, "open_time": 0}
]

# Buildings
buildings = [
    # Buildings along horizontal street
    (-400, 100, 80, 70, 65, (0.5, 0.5, 0.6)),
    (-400, -100, 80, 70, 50, (0.6, 0.5, 0.5)),
    (-180, 100, 90, 80, 80, (0.5, 0.6, 0.5)),
    (-180, -100, 90, 80, 60, (0.55, 0.55, 0.6)),
    (180, 100, 80, 70, 70, (0.6, 0.55, 0.5)),
    (180, -100, 80, 70, 55, (0.5, 0.5, 0.55)),
    (400, 100, 100, 80, 100, (0.55, 0.6, 0.55)),
    (400, -100, 100, 80, 75, (0.6, 0.5, 0.55)),
    
    # Buildings along vertical street
    (100, -400, 70, 80, 60, (0.5, 0.55, 0.6)),
    (-100, -400, 70, 80, 55, (0.55, 0.5, 0.6)),
    (100, -200, 80, 90, 80, (0.6, 0.55, 0.55)),
    (-100, -200, 80, 90, 70, (0.5, 0.6, 0.55)),
    (100, 200, 70, 80, 65, (0.55, 0.55, 0.5)),
    (-100, 200, 70, 80, 58, (0.6, 0.5, 0.5)),
    (100, 400, 80, 80, 75, (0.5, 0.5, 0.6)),
    (-100, 400, 80, 80, 62, (0.55, 0.6, 0.5)),
    
    # Corner buildings
    (-350, -350, 90, 90, 45, (0.5, 0.55, 0.55)),
    (350, 350, 90, 90, 52, (0.55, 0.5, 0.55)),
    (-380, 350, 80, 80, 48, (0.6, 0.55, 0.5)),
    (380, -350, 80, 80, 50, (0.5, 0.6, 0.55)),
]

# Trees
trees = [
    # Quadrant 1 (top-left)
    (-450, 450, 3, 15, 12),
    (-350, 280, 4, 18, 14),
    (-480, 150, 3, 14, 11),
    (-250, 420, 3, 16, 13),
    
    # Quadrant 2 (top-right)
    (450, 480, 3, 16, 12),
    (280, 450, 4, 19, 15),
    (480, 280, 3, 15, 12),
    (250, 350, 3, 17, 13),
    
    # Quadrant 3 (bottom-left)
    (-460, -450, 3, 16, 12),
    (-280, -320, 4, 18, 14),
    (-250, -460, 3, 15, 11),
    (-380, -250, 3, 17, 13),
    
    # Quadrant 4 (bottom-right)
    (460, -460, 3, 16, 12),
    (350, -280, 4, 19, 14),
    (280, -450, 3, 15, 12),
    (420, -250, 3, 18, 13),
]

# Street lights
street_lights = [
    # Along horizontal street
    (-400, 50), (-400, -50),
    (-200, 50), (-200, -50),
   
    (200, 50), (200, -50),
    (400, 50), (400, -50),
    
    # Along vertical street
    (50, -400), (-50, -400),
    (50, -200), (-50, -200),
   
    (50, 200), (-50, 200),
    (50, 400), (-50, 400),
]

# Timing
last_time = time.time()
boss_spawned = False
animation_time = 0  # boss animation

fovY = 60
GRID_LENGTH = 500


def spawn_wave(wave_num):
    # spawn enemies for wave
    global enemies, boss_spawned
    enemies.clear()
    
    if wave_num == 1:
        for i in range(10):
            angle = random.random() * 2 * math.pi
            radius = random.uniform(300, 400)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            enemies.append(["soldier", x, y, 0, 1, 0])
    
    elif wave_num == 2:
        for i in range(5):
            angle = random.random() * 2 * math.pi
            radius = random.uniform(280, 380)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            enemies.append(["soldier", x, y, 0, 1, 0])
        for i in range(5):
            angle = random.random() * 2 * math.pi
            radius = random.uniform(320, 420)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            enemies.append(["minion", x, y, 3, 2, 0])
    
    elif wave_num == 3:
        for i in range(10):
            angle = random.random() * 2 * math.pi
            radius = random.uniform(300, 420)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            enemies.append(["minion", x, y, 3, 2, 0])
    
    elif wave_num == 4:
        for i in range(8):
            angle = random.random() * 2 * math.pi
            radius = random.uniform(280, 380)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            enemies.append(["soldier", x, y, 0, 1, 0])
        for i in range(8):
            angle = random.random() * 2 * math.pi
            radius = random.uniform(320, 420)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            enemies.append(["minion", x, y, 3, 2, 0])
    
    elif wave_num == 5:
        enemies.append(["boss", 0, 420, 0, 30, 0])
        boss_spawned = True


def draw_gun():
    # draw gun
    glPushMatrix()
    
    # position gun
    glTranslatef(1.5, 0, 1.5)
    
    # Gun barrel - dark gray metallic
    glColor3f(0.3, 0.3, 0.35)
    glPushMatrix()
    glTranslatef(3, 0, 0)  # Extend forward
    glScalef(4, 0.6, 0.6)
    glutSolidCube(1)
    glPopMatrix()
    
    # Gun handle - brown
    glColor3f(0.4, 0.25, 0.1)
    glPushMatrix()
    glTranslatef(0.5, 0, -0.8)
    glScalef(1.2, 0.8, 1.5)
    glutSolidCube(1)
    glPopMatrix()
    
    # Gun chamber - darker gray
    glColor3f(0.2, 0.2, 0.25)
    glPushMatrix()
    glTranslatef(1, 0, 0)
    glScalef(1.5, 0.9, 0.9)
    glutSolidCube(1)
    glPopMatrix()
    
    # Sight - red dot
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(2, 0, 0.7)
    gluSphere(gluNewQuadric(), 0.15, 10, 10)
    glPopMatrix()
    
    glPopMatrix()


def draw_player():
    # draw player
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    
    # rotate player
    glRotatef(player_angle * 180 / math.pi, 0, 0, 1)
    
    # Body (cube) - bright blue
    glColor3f(0.2, 0.5, 1.0)
    glPushMatrix()
    glScalef(1, 1, 1.2)
    glutSolidCube(3)
    glPopMatrix()
    
    # Head (sphere) - lighter blue
    glColor3f(0.4, 0.7, 1.0)
    glTranslatef(0, 0, 2.8)
    gluSphere(gluNewQuadric(), 1.3, 20, 20)
    
    # draw gun
    draw_gun()
    
    glPopMatrix()


def draw_soldier(x, y, z):
    # draw soldier
    glPushMatrix()
    glTranslatef(x, y, z + 1.5)
    
    # Body (cube) - dark red
    glColor3f(0.8, 0.1, 0.1)
    glPushMatrix()
    glScalef(1, 1, 1.2)
    glutSolidCube(3)
    glPopMatrix()
    
    # Head (sphere) - red
    glColor3f(1, 0.2, 0.2)
    glTranslatef(0, 0, 2.5)
    gluSphere(gluNewQuadric(), 1.1, 20, 20)
    
    # Spike helmet - cylinder pointing up
    glColor3f(0.6, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 1.2)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 0.4, 0.1, 1.5, 15, 10)
    glPopMatrix()
    
    # weapon
    glColor3f(0.5, 0.3, 0.1)
    glPushMatrix()
    glTranslatef(1.5, 0, 0)  # Position at side
    glRotatef(45, 0, 1, 0)   # Angle it forward
    gluCylinder(gluNewQuadric(), 0.3, 0.3, 4, 12, 8)
    glPopMatrix()
    
    
    
    glPopMatrix()


def draw_minion(x, y, z):
    # draw minion
    global animation_time
    
    glPushMatrix()
    glTranslatef(x, y, z + 1.8)
    
    # Main body - purple cube
    glColor3f(0.7, 0.3, 0.9)
    glPushMatrix()
    glScalef(1.2, 1.2, 1.2)
    glutSolidCube(2.5)
    glPopMatrix()
    
    # Left horn - tapered cylinder
    glColor3f(0.5, 0.1, 0.6)
    glPushMatrix()
    glTranslatef(-1.8, 0, 1.8)
    glRotatef(45, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.5, 0.15, 1.8, 15, 10)
    glPopMatrix()
    
    # Right horn - tapered cylinder
    glPushMatrix()
    glTranslatef(1.8, 0, 1.8)
    glRotatef(-45, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.5, 0.15, 1.8, 15, 10)
    glPopMatrix()
    
    
    # left wing flap
    wing_flap = math.sin(animation_time * 8) * 45
    glColor3f(0.8, 0.4, 1)
    glPushMatrix()
    glTranslatef(-1.8, 0, 1)
    glRotatef(wing_flap, 1, 0, 0)  # Flap rotation
    glScalef(0.8, 2.2, 0.15)
    glutSolidCube(1)
    glPopMatrix()
    
    # right wing flap
    glPushMatrix()
    glTranslatef(1.8, 0, 1)
    glRotatef(-wing_flap, 1, 0, 0)  # Opposite flap
    glScalef(0.8, 2.2, 0.15)
    glutSolidCube(1)
    glPopMatrix()
    
    # Eyes - bright magenta
    glColor3f(1, 0, 1)
    glPushMatrix()
    glTranslatef(-0.8, 0.9, 1.2)
    gluSphere(gluNewQuadric(), 0.4, 12, 12)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0.8, 0.9, 1.2)
    gluSphere(gluNewQuadric(), 0.4, 12, 12)
    glPopMatrix()
    
    glPopMatrix()


def draw_boss(x, y, z):
    # draw boss
    global animation_time
    
    glPushMatrix()
    glTranslatef(x, y, z + 8)
    
    # Core - large metallic cube
    glColor3f(0.2, 0.2, 0.3)
    glPushMatrix()
    glScalef(3.5, 3.5, 3.5)
    glutSolidCube(1)
    glPopMatrix()
    
    # Head - floating sphere above core
    glColor3f(0.9, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 5)
    gluSphere(gluNewQuadric(), 2.5, 25, 25)
    glPopMatrix()
    
    # Left arm - cylinder extending left
    glColor3f(0.5, 0.5, 0.6)
    glPushMatrix()
    glTranslatef(-4, 0, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.8, 0.6, 5, 15, 10)
    glPopMatrix()
    
    # Right arm - cylinder extending right
    glPushMatrix()
    glTranslatef(4, 0, 0)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.8, 0.6, 5, 15, 10)
    glPopMatrix()
    
    # Left hand - cube at end of arm
    glColor3f(0.8, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(-6.5, 0, 0)
    glScalef(1.2, 1.2, 1.2)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right hand - cube at end of arm
    glPushMatrix()
    glTranslatef(6.5, 0, 0)
    glScalef(1.2, 1.2, 1.2)
    glutSolidCube(1)
    glPopMatrix()
    
    # boss orbitals
    orbital_radius = 6
    for i in range(4):
        base_angle = (i / 4) * 2 * math.pi
        orbital_angle = base_angle + animation_time * 3
        
        orbital_x = orbital_radius * math.cos(orbital_angle)
        orbital_y = orbital_radius * math.sin(orbital_angle)
        
        glColor3f(0.2, 0.8, 1)  # Cyan
        glPushMatrix()
        glTranslatef(orbital_x, orbital_y, 2)
        gluSphere(gluNewQuadric(), 1.2, 15, 15)
        glPopMatrix()
    
    glPopMatrix()


def draw_bullet(x, y, z):
    # draw bullet
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 1, 0)
    gluSphere(gluNewQuadric(), 0.6, 15, 15)
    # trail
    glColor3f(1, 0.8, 0)
    glTranslatef(0, 0, -0.5)
    gluSphere(gluNewQuadric(), 0.4, 10, 10)
    glPopMatrix()


def draw_minion_bullet(x, y, z):
    # draw minion bullet
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 0.5, 15, 15)
    # trail
    glColor3f(0.8, 0, 0)
    glTranslatef(0, 0, -0.5)
    gluSphere(gluNewQuadric(), 0.3, 10, 10)
    glPopMatrix()


def draw_hp_bar(x, y, z, current_hp, max_hp):
    # draw hp bar
    glPushMatrix()
    glTranslatef(x, y, z+2)
    glRotatef(90, 1, 0, 0)    
    bar_width = 4
    bar_height = 1
    
    # health percent
    health_percent = max(0, min(1, current_hp / max_hp))
    
    # background
    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(-bar_width/2, -0.2, 0)
    glVertex3f(bar_width/2, -0.2, 0)
    glVertex3f(bar_width/2, bar_height, 0)
    glVertex3f(-bar_width/2, bar_height, 0)
    glEnd()
    
    # health bar color
    if health_percent > 0.5:
        r = (1 - health_percent) * 2
        g = 1
    else:
        r = 1
        g = health_percent * 2
    
    glColor3f(r, g, 0)
    glBegin(GL_QUADS)
    glVertex3f(-bar_width/2, -0.2, 0.01)
    glVertex3f(-bar_width/2 + bar_width * health_percent, -0.2, 0.01)
    glVertex3f(-bar_width/2 + bar_width * health_percent, bar_height, 0.01)
    glVertex3f(-bar_width/2, bar_height, 0.01)
    glEnd()
    
    glPopMatrix()


def draw_bomb(x, y, z):
    # draw bomb
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 1.2, 15, 15)
    # fuse
    glColor3f(0.8, 0.4, 0.1)
    glTranslatef(0, 0, 1.2)
    gluCylinder(gluNewQuadric(), 0.15, 0.1, 0.8, 8, 4)
    glPopMatrix()


def draw_particle(x, y, z):
    # draw particle
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 1, 1)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex3f(0, 0, 0)
    glEnd()
    glPopMatrix()


def draw_treasure_box(x, y, z, is_open):
    # draw treasure box
    glPushMatrix()
    glTranslatef(x, y, z + 2)
    
    if is_open:
        glColor3f(0.4, 0.3, 0.2)
    else:
        glColor3f(1, 0.84, 0)
    
    glColor3f(0.9, 0.7, 0)
    glutSolidCube(3.2)
    
    # lock
    glColor3f(0.6, 0.4, 0.1)
    glTranslatef(0, 1.7, 0)
    gluSphere(gluNewQuadric(), 0.6, 15, 15)
    
    glPopMatrix()


def draw_sky_box():
    # draw sky
    sky_size = 700
    
    # sky color
    if boss_spawned and len(enemies) > 0:
        glColor3f(0.6, 0.1, 0.1)
    else:
        glColor3f(0.4, 0.6, 0.9)
    
    glPushMatrix()
    glTranslatef(0, 0, sky_size / 2)
    
    # draw box faces
    # Top face
    glBegin(GL_QUADS)
    glVertex3f(-sky_size, -sky_size, sky_size)
    glVertex3f(sky_size, -sky_size, sky_size)
    glVertex3f(sky_size, sky_size, sky_size)
    glVertex3f(-sky_size, sky_size, sky_size)
    glEnd()
    
    # Bottom face
    glBegin(GL_QUADS)
    glVertex3f(-sky_size, -sky_size, -sky_size)
    glVertex3f(-sky_size, sky_size, -sky_size)
    glVertex3f(sky_size, sky_size, -sky_size)
    glVertex3f(sky_size, -sky_size, -sky_size)
    glEnd()
    
    # Front face
    glBegin(GL_QUADS)
    glVertex3f(-sky_size, sky_size, -sky_size)
    glVertex3f(-sky_size, sky_size, sky_size)
    glVertex3f(sky_size, sky_size, sky_size)
    glVertex3f(sky_size, sky_size, -sky_size)
    glEnd()
    
    # Back face
    glBegin(GL_QUADS)
    glVertex3f(-sky_size, -sky_size, -sky_size)
    glVertex3f(sky_size, -sky_size, -sky_size)
    glVertex3f(sky_size, -sky_size, sky_size)
    glVertex3f(-sky_size, -sky_size, sky_size)
    glEnd()
    
    # Right face
    glBegin(GL_QUADS)
    glVertex3f(sky_size, -sky_size, -sky_size)
    glVertex3f(sky_size, sky_size, -sky_size)
    glVertex3f(sky_size, sky_size, sky_size)
    glVertex3f(sky_size, -sky_size, sky_size)
    glEnd()
    
    # Left face
    glBegin(GL_QUADS)
    glVertex3f(-sky_size, -sky_size, -sky_size)
    glVertex3f(-sky_size, -sky_size, sky_size)
    glVertex3f(-sky_size, sky_size, sky_size)
    glVertex3f(-sky_size, sky_size, -sky_size)
    glEnd()
    
    glPopMatrix()


def draw_walls():
    # draw walls
    wall_height = 25
    
    # North wall
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.35)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glColor3f(0.2, 0.2, 0.25)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glEnd()
    
    # South wall
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.35)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glColor3f(0.2, 0.2, 0.25)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()
    
    # East wall
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.35)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glColor3f(0.2, 0.2, 0.25)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()
    
    # West wall
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.35)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glColor3f(0.2, 0.2, 0.25)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glEnd()


def draw_building(x, y, width, depth, height, color):
    # draw building
    glPushMatrix()
    glTranslatef(x, y, height / 2)
    glColor3f(*color)
    glScalef(width, depth, height)
    glutSolidCube(1)
    glPopMatrix()
    
    # Draw windows
    glColor3f(1, 1, 0.7)
    window_spacing = 25
    window_size = 10
    
    # Front face windows
    for wz in range(20, int(height - 20), window_spacing):
        for wx in range(-int(width/2) + 15, int(width/2) - 10, window_spacing):
            glPushMatrix()
            glTranslatef(x + wx, y - depth/2 - 0.5, wz)
            glScalef(window_size, 1, window_size)
            glutSolidCube(1)
            glPopMatrix()


def draw_tree(x, y, trunk_radius, trunk_height, foliage_radius):
    # draw tree
    glPushMatrix()
    glTranslatef(x, y, 0)
    
    # Trunk
    glColor3f(0.4, 0.25, 0.1)
    gluCylinder(gluNewQuadric(), trunk_radius, trunk_radius * 0.7, trunk_height, 10, 5)
    
    # Foliage
    glColor3f(0.1, 0.6, 0.1)
    glTranslatef(0, 0, trunk_height)
    gluSphere(gluNewQuadric(), foliage_radius, 12, 12)
    
    glPopMatrix()


def draw_street_light(x, y):
    # draw street light
    pole_height = 12
    
    glPushMatrix()
    glTranslatef(x, y, 0)
    
    # Pole
    glColor3f(0.3, 0.3, 0.3)
    gluCylinder(gluNewQuadric(), 0.5, 0.5, pole_height, 8, 4)
    
    # Arm
    glTranslatef(0, 0, pole_height)
    glPushMatrix()
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 0.3, 0.3, 3, 6, 2)
    glPopMatrix()
    
    # Light
    glTranslatef(3, 0, 0)
    glColor3f(1, 1, 0.5)
    gluSphere(gluNewQuadric(), 1.2, 10, 10)
    
    glPopMatrix()


def draw_streets():
    # draw streets
    street_width = 80
    
    # Horizontal street
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -street_width/2, 0.25)
    glVertex3f(GRID_LENGTH, -street_width/2, 0.25)
    glVertex3f(GRID_LENGTH, street_width/2, 0.25)
    glVertex3f(-GRID_LENGTH, street_width/2, 0.25)
    glEnd()
    
    # vertical
    glBegin(GL_QUADS)
    glVertex3f(-street_width/2, -GRID_LENGTH, 0.25)
    glVertex3f(street_width/2, -GRID_LENGTH, 0.25)
    glVertex3f(street_width/2, GRID_LENGTH, 0.25)
    glVertex3f(-street_width/2, GRID_LENGTH, 0.25)
    glEnd()
    
    # markings
    glColor3f(1, 1, 1)
    
    glBegin(GL_LINES)
    for i in range(-GRID_LENGTH + 20, GRID_LENGTH, 40):
        if abs(i) > street_width/2:
            glVertex3f(i, 0, 1)
            glVertex3f(i + 20, 0, 1)
    glEnd()
    
    glBegin(GL_LINES)
    for i in range(-GRID_LENGTH + 20, GRID_LENGTH, 40):
        if abs(i) > street_width/2:
            glVertex3f(0, i, 1)
            glVertex3f(0, i + 20, 1)
    glEnd()


def draw_city():
    # draw city
    draw_streets()
    
    for building in buildings:
        draw_building(*building)
    
    for tree in trees:
        draw_tree(*tree)
    
    for light in street_lights:
        draw_street_light(*light)


def update_game(dt):
    # update game
    global player_bullets, player_hearts, player_grenades
    global bullets, thrown_bombs, particles, enemies
    global current_wave, wave_delay, wave_clear_time, game_state
    global boss_spawned
    
    if game_state != "playing":
        return
    
    # waves
    if len(enemies) == 0 and current_wave <= 5:
        if wave_delay == 0:
            wave_clear_time = time.time()
            wave_delay = 1
            if current_wave > 1:
                player_bullets = min(30, player_bullets + 8)
                player_hearts = min(10, player_hearts + 2)
        elif time.time() - wave_clear_time >= 15:
            if current_wave == 5 and boss_spawned:
                game_state = "won"
                return
            current_wave += 1
            if current_wave <= 5:
                spawn_wave(current_wave)
                wave_delay = 0
    
    # bullets
    for bullet in bullets[:]:
        bullet[0] += bullet[3] * dt
        bullet[1] += bullet[4] * dt
        bullet[2] += bullet[5] * dt
        
        if (abs(bullet[0]) > GRID_LENGTH or abs(bullet[1]) > GRID_LENGTH or 
            bullet[2] < 0 or bullet[2] > 100):
            bullets.remove(bullet)
            continue
        
        # player collision
        if bullet[6] in ["minion", "boss"]:
            player_dist = math.sqrt((bullet[0]-player_pos[0])**2 + (bullet[1]-player_pos[1])**2 + (bullet[2]-player_pos[2])**2)
            if player_dist < 2:
                damage = 1
                player_hearts -= damage
                if bullet in bullets:
                    bullets.remove(bullet)
                continue
        
        # enemy collision
        if bullet[6] == "player":
            for enemy in enemies[:]:
                ex, ey, ez = enemy[1], enemy[2], enemy[3]
                hit_radius = 6 if enemy[0] == "boss" else 3
                dist = math.sqrt((bullet[0]-ex)**2 + (bullet[1]-ey)**2 + (bullet[2]-ez)**2)
                if dist < hit_radius:
                    enemy[4] -= 1
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy[4] <= 0:
                        enemies.remove(enemy)
                    break
    
    # bombs
    for bomb in thrown_bombs[:]:
        bomb[0] += bomb[3] * dt
        bomb[1] += bomb[4] * dt
        bomb[2] += bomb[5] * dt
        bomb[5] -= 25 * dt  # Gravity
        
        if bomb[2] <= 0:
            thrown_bombs.remove(bomb)
            # particles
            for _ in range(20):
                angle = random.random() * 2 * math.pi
                speed = random.uniform(15, 35)
                px = bomb[0]
                py = bomb[1]
                pz = bomb[2] + 1
                pdx = math.cos(angle) * speed
                pdy = math.sin(angle) * speed
                pdz = random.uniform(10, 25)
                particles.append([px, py, pz, pdx, pdy, pdz, 0.6])
            
            # damage
            for enemy in enemies[:]:
                ex, ey = enemy[1], enemy[2]
                dist = math.sqrt((bomb[0]-ex)**2 + (bomb[1]-ey)**2)
                if dist < 50:  # Big radius
                    enemy[4] -= 5  # 5 damage
                    if enemy[4] <= 0:
                        enemies.remove(enemy)
    
    # particles
    for particle in particles[:]:
        particle[0] += particle[3] * dt
        particle[1] += particle[4] * dt
        particle[2] += particle[5] * dt
        particle[5] -= 25 * dt
        particle[6] -= dt
        
        if particle[6] <= 0 or particle[2] <= 0:
            particles.remove(particle)
    
    # enemies
    for enemy in enemies:
        enemy_type = enemy[0]
        ex, ey, ez = enemy[1], enemy[2], enemy[3]
        
        dx = player_pos[0] - ex
        dy = player_pos[1] - ey
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            if enemy_type == "soldier":
                speed = player_speed * 4.0
                enemy[1] += (dx / dist) * speed * dt
                enemy[2] += (dy / dist) * speed * dt
            elif enemy_type == "minion":
                speed = player_speed * 2.5
                enemy[1] += (dx / dist) * speed * dt
                enemy[2] += (dy / dist) * speed * dt
                enemy[3] = 3
            elif enemy_type == "boss":
                speed = player_speed * 2.5
                enemy[1] += (dx / dist) * speed * dt
                enemy[2] += (dy / dist) * speed * dt
        
        # contact dmg
        if enemy_type == "soldier":
            dist_to_player = math.sqrt((ex - player_pos[0])**2 + (ey - player_pos[1])**2)
            if dist_to_player < 4:
                enemy[5] -= dt
                if enemy[5] <= 0:
                    player_hearts -= 0.5
                    enemy[5] = 1
        
    # ranged attacks
        if enemy_type in ["minion", "boss"]:
            dist_to_player = math.sqrt((ex - player_pos[0])**2 + (ey - player_pos[1])**2)
            if (enemy_type == "minion" and dist_to_player < 70) or (enemy_type == "boss" and dist_to_player < 180):
                enemy[5] -= dt
                if enemy[5] <= 0:
                    if enemy_type == "minion":
                        # shoot
                        if dist_to_player > 0:
                            proj_speed = 35
                            proj_dx = (player_pos[0] - ex) / dist_to_player * proj_speed
                            proj_dy = (player_pos[1] - ey) / dist_to_player * proj_speed
                            proj_dz = 0
                            bullets.append([ex, ey, ez, proj_dx, proj_dy, proj_dz, "minion"])
                        enemy[5] = 2.0
                    else:
                        # boss shoot
                        if dist_to_player > 0:
                            proj_speed = 25
                            proj_dx = (player_pos[0] - ex) / dist_to_player * proj_speed
                            proj_dy = (player_pos[1] - ey) / dist_to_player * proj_speed
                            proj_dz = 0
                            bullets.append([ex, ey, ez + 2, proj_dx, proj_dy, proj_dz, "boss"])
                        
                        # spiral pattern
                        if dist_to_player > 0:
                            cycle_time = animation_time % 9
                            
                            if cycle_time < 6:
                                for i in range(2):
                                    spiral_angle = (i / 2) * 2 * math.pi + (cycle_time * 0.5) * math.pi
                                    proj_speed = 18
                                    proj_dx = math.cos(spiral_angle) * proj_speed
                                    proj_dy = math.sin(spiral_angle) * proj_speed
                                    proj_dz = 0
                                    
                                    bullets.append([ex, ey, ez + 2, proj_dx, proj_dy, proj_dz, "boss"])
                        
                        enemy[5] = 0.5

    
    # treasure boxes
    current_time = time.time()
    for box in treasure_boxes:
        dist = math.sqrt((player_pos[0] - box["x"])**2 + (player_pos[1] - box["y"])**2)
        if dist < 6 and (box["open_time"] == 0 or current_time - box["open_time"] >= 30):
            box["open_time"] = current_time
            rand = random.random()
            if rand < 0.4:
                player_bullets = min(30, player_bullets + 20)
            elif rand < 0.6:
                player_hearts = min(10, player_hearts + 2)
            else:  # 2/10 probability for bombs
                if player_grenades < 3:
                    player_grenades += 1
    
    if player_hearts <= 0:
        game_state = "lost"


def keyboardListener(key, x, y):
    # keyboard input
    global player_pos, player_angle, game_state, current_wave, enemies
    global player_bullets, player_hearts, player_grenades, boss_spawned
    global wave_delay
    
    if game_state != "playing":
        if key == b'r':
            game_state = "playing"
            player_pos[0] = 0
            player_pos[1] = 0
            player_angle = 0
            player_bullets = 10
            player_hearts = 5
            player_grenades = 0
            current_wave = 1
            wave_delay = 0
            enemies.clear()
            bullets.clear()
            thrown_bombs.clear()
            particles.clear()
            spawn_wave(1)
            boss_spawned = False
            for box in treasure_boxes:
                box["open_time"] = 0
        return
    
    # W - forward
    if key == b'w':
        new_x = player_pos[0] + player_speed * math.cos(player_angle)
        new_y = player_pos[1] + player_speed * math.sin(player_angle)
        if abs(new_x) < GRID_LENGTH - 5 and abs(new_y) < GRID_LENGTH - 5:
            player_pos[0] = new_x
            player_pos[1] = new_y
    
    # S - backward
    if key == b's':
        new_x = player_pos[0] - player_speed * math.cos(player_angle)
        new_y = player_pos[1] - player_speed * math.sin(player_angle)
        if abs(new_x) < GRID_LENGTH - 5 and abs(new_y) < GRID_LENGTH - 5:
            player_pos[0] = new_x
            player_pos[1] = new_y
    
    # A - left
    if key == b'a':
        player_angle += 0.12
        strafe_angle = player_angle - math.pi / 2
        new_x = player_pos[0] + player_speed * math.cos(strafe_angle)
        new_y = player_pos[1] + player_speed * math.sin(strafe_angle)
        if abs(new_x) < GRID_LENGTH - 5 and abs(new_y) < GRID_LENGTH - 5:
            player_pos[0] = new_x
            player_pos[1] = new_y
    
    # D - right
    if key == b'd':
        player_angle -= 0.12
        strafe_angle = player_angle + math.pi / 2
        new_x = player_pos[0] + player_speed * math.cos(strafe_angle)
        new_y = player_pos[1] + player_speed * math.sin(strafe_angle)
        if abs(new_x) < GRID_LENGTH - 5 and abs(new_y) < GRID_LENGTH - 5:
            player_pos[0] = new_x
            player_pos[1] = new_y
    
    # C - cheat
    if key == b'c':
        player_hearts = 10
        player_bullets = 30
        player_grenades = 3


def specialKeyListener(key, x, y):
    # special keys
    global camera_pos
    
    if key == GLUT_KEY_UP:
        camera_pos[2] += 8
    
    if key == GLUT_KEY_DOWN:
        camera_pos[2] = max(50, camera_pos[2] - 8)
    
    if key == GLUT_KEY_LEFT:
        camera_pos[0] -= 8
    
    if key == GLUT_KEY_RIGHT:
        camera_pos[0] += 8


def mouseListener(button, state, x, y):
    # mouse input
    global bullets, thrown_bombs, player_bullets, player_grenades
    
    if game_state != "playing":
        return
    
    # Left click - shoot bullet in direction player is facing (crosshair direction)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if player_bullets > 0:
            player_bullets -= 1
            dx = math.cos(player_angle) * bullet_speed
            dy = math.sin(player_angle) * bullet_speed
            dz = 0
            bullets.append([player_pos[0], player_pos[1], player_pos[2], dx, dy, dz, "player"])
    
    # Right click - throw bomb in direction player is facing
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if player_grenades > 0:
            player_grenades -= 1
            dx = math.cos(player_angle) * bomb_speed
            dy = math.sin(player_angle) * bomb_speed
            dz = 8
            thrown_bombs.append([player_pos[0], player_pos[1], player_pos[2] + 2, dx, dy, dz])


def setupCamera():
    # setup camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    cam_dist = 25
    cam_height = 16
    
    cam_x = player_pos[0] - cam_dist * math.cos(player_angle)
    cam_y = player_pos[1] - cam_dist * math.sin(player_angle)
    cam_z = player_pos[2] + cam_height
    
    look_ahead = 7
    look_x = player_pos[0] + look_ahead * math.cos(player_angle)
    look_y = player_pos[1] + look_ahead * math.sin(player_angle)
    look_z = player_pos[2] + 2
    
    gluLookAt(cam_x, cam_y, cam_z,
              look_x, look_y, look_z,
              0, 0, 1)


def idle():
    # update loop
    global last_time, animation_time
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    animation_time += dt
    update_game(dt)
    glutPostRedisplay()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def showScreen():
    # render screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setupCamera()
    
    # sky
    draw_sky_box()
    
    # ground
   
    glBegin(GL_QUADS)
    glColor3f(0.15, 0.5, 0.15)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glColor3f(0.1, 0.4, 0.1)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()
    
    # elements
    draw_walls()
    draw_city()
    draw_player()
    
    # treasure boxes
    current_time = time.time()
    for box in treasure_boxes:
        is_open = box["open_time"] > 0 and current_time - box["open_time"] < 30
        draw_treasure_box(box["x"], box["y"], box["z"], is_open)
    
    # enemies
    for enemy in enemies:
        enemy_type = enemy[0]
        ex, ey, ez = enemy[1], enemy[2], enemy[3]
        current_hp = enemy[4]
        
        if enemy_type == "soldier":
            draw_soldier(ex, ey, ez)
            draw_hp_bar(ex, ey, ez + 4, current_hp, 1)
        elif enemy_type == "minion":
            draw_minion(ex, ey, ez)
            draw_hp_bar(ex, ey, ez + 5, current_hp, 2)
        elif enemy_type == "boss":
            draw_boss(ex, ey, ez)
            draw_hp_bar(ex, ey, ez + 15, current_hp, 30)
    
    # bullets
    for bullet in bullets:
        if bullet[6] == "minion" or bullet[6] == "boss":
            draw_minion_bullet(bullet[0], bullet[1], bullet[2])
        else:
            draw_bullet(bullet[0], bullet[1], bullet[2])
    
    # bombs
    for bomb in thrown_bombs:
        draw_bomb(bomb[0], bomb[1], bomb[2])
    
    # particles
   
    for particle in particles:
        draw_particle(particle[0], particle[1], particle[2])
    
    
    # UI
    draw_text(10, 770, f"WAVE {current_wave}/5", GLUT_BITMAP_HELVETICA_18)
    draw_text(10, 740, f"Health: {player_hearts:.1f}/10")
    draw_text(10, 710, f"Bullets: {player_bullets}/30")
    draw_text(10, 680, f"Bombs: {player_grenades}/3")
    draw_text(10, 650, f"Enemies Left: {len(enemies)}")
    
    # crosshair
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, -200, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1, 0, 0)
    
    glBegin(GL_LINES)
    glVertex2f(485, 400)
    glVertex2f(515, 400)
    glVertex2f(500, 385)
    glVertex2f(500, 415)
    glEnd()
    
    # center dot
    glPointSize(6)
    glBegin(GL_POINTS)
    glVertex2f(500, 400)
    glEnd()
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    # game over
    if game_state == "won":
        draw_text(350, 400, "VICTORY! Press R to Restart", GLUT_BITMAP_TIMES_ROMAN_24)
    elif game_state == "lost":
        draw_text(330, 400, "GAME OVER! Press R to Restart", GLUT_BITMAP_TIMES_ROMAN_24)
    
    glutSwapBuffers()


def main():
    global last_time
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Wave Shooter Game")
    
    glEnable(GL_DEPTH_TEST)
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    last_time = time.time()
    spawn_wave(1)
    
    glutMainLoop()


if __name__ == "__main__":
    main()