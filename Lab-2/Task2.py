from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

window_width, window_height = 800, 600

# Points system variables
points = []
points_speed = 0.5
is_frozen = False
blink_mode = False
blink_start_time = 0
boundary_xmin, boundary_xmax = -300, 300
boundary_ymin, boundary_ymax = -200, 200

# ===== Point Class =====
class BouncingPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = [random.random(), random.random(), random.random()]
        self.original_color = self.color[:]
        self.dx = random.choice([-1, 1]) * random.uniform(0.3, 1.0)
        self.dy = random.choice([-1, 1]) * random.uniform(0.3, 1.0)
        self.size = random.uniform(3.0, 8.0)
        self.visible = True
        
    def update(self, speed_factor):
        if is_frozen:
            return
            
        self.x += self.dx * speed_factor
        self.y += self.dy * speed_factor
        
        if self.x <= boundary_xmin or self.x >= boundary_xmax:
            self.dx = -self.dx
            self.x = max(boundary_xmin, min(self.x, boundary_xmax))
            
        if self.y <= boundary_ymin or self.y >= boundary_ymax:
            self.dy = -self.dy
            self.y = max(boundary_ymin, min(self.y, boundary_ymax))
    
    def draw(self):
        if not self.visible:
            return
            
        glColor3f(self.color[0], self.color[1], self.color[2])
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

# ===== Drawing Functions =====
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

def draw_boundary():
    """Draw the boundary box"""
    glColor3f(1.0, 1.0, 1.0)  # White boundary
    glLineWidth(2.0)
    glBegin(GL_LINES)
    # Bottom line
    glVertex2f(boundary_xmin, boundary_ymin)
    glVertex2f(boundary_xmax, boundary_ymin)
    # Top line
    glVertex2f(boundary_xmin, boundary_ymax)
    glVertex2f(boundary_xmax, boundary_ymax)
    # Left line
    glVertex2f(boundary_xmin, boundary_ymin)
    glVertex2f(boundary_xmin, boundary_ymax)
    # Right line
    glVertex2f(boundary_xmax, boundary_ymin)
    glVertex2f(boundary_xmax, boundary_ymax)
    glEnd()

# ===== Point Management =====
def create_point(x, y):
    """Create a new bouncing point at specified coordinates"""
    new_point = BouncingPoint(x, y)
    points.append(new_point)
    print(f"Created point at ({x:.1f}, {y:.1f}) with color {new_point.color}")

def update_blink():
    """Update blinking effect for all points"""
    if not blink_mode:
        return
        
    current_time = time.time()
    blink_progress = (current_time - blink_start_time) % 1.0  # 1 second cycle
    
    for point in points:
        if blink_progress < 0.5:
            # First half: fade to background
            fade_factor = blink_progress / 0.5
            point.color = [
                point.original_color[0] * (1 - fade_factor),
                point.original_color[1] * (1 - fade_factor),
                point.original_color[2] * (1 - fade_factor)
            ]
        else:
            # Second half: fade back to original color
            fade_factor = (blink_progress - 0.5) / 0.5
            point.color = [
                point.original_color[0] * fade_factor,
                point.original_color[1] * fade_factor,
                point.original_color[2] * fade_factor
            ]

def reset_blink():
    """Reset all points to their original colors"""
    for point in points:
        point.color = point.original_color[:]

# ===== Input Handlers =====
def mouse_listener(button, state, x, y):
    """Handle mouse clicks"""
    if state != GLUT_DOWN:
        return
        
    # Convert screen coordinates to OpenGL coordinates
    gl_x = x - (window_width / 2)
    gl_y = (window_height / 2) - y
    
    # Check if click is within boundary
    if (boundary_xmin <= gl_x <= boundary_xmax and 
        boundary_ymin <= gl_y <= boundary_ymax):
        
        if button == GLUT_RIGHT_BUTTON:
            # Right click: create new point
            create_point(gl_x, gl_y)
            print(f"Points count: {len(points)}")
            
        elif button == GLUT_LEFT_BUTTON:
            # Left click: toggle blink mode
            global blink_mode, blink_start_time
            blink_mode = not blink_mode
            
            if blink_mode:
                blink_start_time = time.time()
                print("Blink mode: ON")
            else:
                reset_blink()
                print("Blink mode: OFF")

def keyboard_listener(key, x, y):
    """Handle keyboard input"""
    global is_frozen, points_speed
    
    if key == b' ':
        # Spacebar: toggle freeze
        is_frozen = not is_frozen
        state = "FROZEN" if is_frozen else "UNFROZEN"
        print(f"Points {state}")
        
    elif key == b'q' or key == b'Q':
        exit()

def special_key_listener(key, x, y):
    """Handle special keys (arrow keys)"""
    global points_speed
    
    if is_frozen:
        return
        
    if key == GLUT_KEY_UP:
        # Increase speed
        points_speed = min(points_speed * 1.5, 10.0)
        print(f"Speed increased: {points_speed:.2f}")
        
    elif key == GLUT_KEY_DOWN:
        # Decrease speed
        points_speed = max(points_speed / 1.5, 0.1)
        print(f"Speed decreased: {points_speed:.2f}")

# ===== Projection Setup =====
def setup_projection():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, -300, 300, 0, 1)
    glMatrixMode(GL_MODELVIEW)

# ===== Display & Animation =====
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    
    # Set black background
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw boundary
    draw_boundary()
    
    # Draw all points
    for point in points:
        point.draw()
    
    glutSwapBuffers()

def animate():
    # Update blink effect
    update_blink()
    
    # Update point positions
    for point in points:
        point.update(points_speed)
    
    glutPostRedisplay()

# ===== Main Function =====
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Bouncing Points - Interactive System")
    
    # Register callbacks
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    
    print("=== Bouncing Points System ===")
    print("RIGHT CLICK: Create random colored point")
    print("LEFT CLICK: Toggle blinking effect")
    print("UP ARROW: Increase speed")
    print("DOWN ARROW: Decrease speed")
    print("SPACEBAR: Freeze/Unfreeze all points")
    print("Q: Quit")
    print(f"\nBoundary: X[{boundary_xmin}, {boundary_xmax}], Y[{boundary_ymin}, {boundary_ymax}]")
    
    glutMainLoop()

if __name__ == "__main__":
    main()