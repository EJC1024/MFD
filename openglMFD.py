import pygame
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

class Colors(Enum):
    White = (1.0, 1.0, 1.0)
    Black = (0.0, 0.0, 0.0)
    Yellow = (1.0, 1.0, 0.0)
    Red = (1.0, 0.0, 0.0)
    Green = (0.0, 1.0, 0.0)
    Blue = (0.0, 0.0, 1.0)
    Magenta = (1.0, 0.0, 1.0)
    Background = (0.01, 0.23, 0.35)

def initialize_menu_text():
    attitude_text = text("ATTITUDE", Colors.White, 105, 0, 20)
    target_text = text("TARGET", Colors.White, 216, 0, 20)
    nav_text = text("NAV 1/2", Colors.White, 316, 0, 20)
    astrogator_text = text("ASTR.", Colors.White, 425, 0, 20)
    graphs_text = text("GRPH. 1/2", Colors.White, 508, 0, 20)
    vslview_text = text("VESL.VIEW", Colors.White, 605, 0, 20)

    flight_text = text("FLIGHT", Colors.White, 119, 575, 20)
    orbit_text = text("ORB/DISP", Colors.White, 207, 575, 20)
    docking_text = text("DOCKING", Colors.White, 307, 575, 20)
    log_text = text("SHIP/LOG", Colors.White, 407, 575, 20)
    crew_text = text("CREW", Colors.White, 523, 575, 20)
    sci_text = text("SCI/COM", Colors.White, 610, 575, 20)

    menu_texts = [attitude_text, target_text, nav_text, 
                  astrogator_text, graphs_text, vslview_text,
                  flight_text, orbit_text, docking_text,
                  log_text, crew_text, sci_text]
    
    return menu_texts

def gl_init_2d():
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 1024, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 1.0])  # Light position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])  # Light color
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0]) 

def gl_init_3d():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(10, (1024 / 600), 0.1, 50.0)  # FOV, aspect ratio, near, far
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
# If starting with degress:
#1. Call quaternion from angle for each axis of rotation if using degrees
#2. Multiply each axis of rotation
# If starting with quaternion:
#3. Convert quaternion to multi-dimensional matrix
#4. Apply matrix with openGL
def quaternion_from_axis_angle(axis, angle):
    #Returns the quaternion representing rotation around a given axis by a certain angle.
    half_angle = math.radians(angle) / 2
    s = math.sin(half_angle)
    return np.array([math.cos(half_angle), axis[0]*s, axis[1]*s, axis[2]*s])

def multiply_quaternions(q1, q2):
    #Multiplies two quaternions.
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])
    
def quaternion_to_matrix(q):
    #Converts a quaternion to a 4x4 rotation matrix.
    w, x, y, z = q
    return np.array([
        [1 - 2 * (y ** 2 + z ** 2), 2 * (x * y - w * z), 2 * (x * z + w * y), 0],
        [2 * (x * y + w * z), 1 - 2 * (x ** 2 + z ** 2), 2 * (y * z - w * x), 0],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x ** 2 + y ** 2), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

class Screen:
    def __init__(self, texture_path):
        self.texture_id = load_texture(texture_path)

        self.standby_texture = [
            (0.0, 1.0),
            (1.0, 1.0),
            (1.0, 0.0),
            (0.0, 0.0),
        ]
        
        self.standby_vertices = [
            (100, 0),
            (700, 0),
            (700, 600),
            (100, 600)
        ]

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        for tex_coord, vertex in zip(self.standby_texture, self.standby_vertices):
            glTexCoord2f(*tex_coord)
            glVertex2f(*vertex)
        glEnd()

class NavBall:
    def __init__(self):
        self.navball_texture = load_texture('Textures/Trekky.png')
        self.navball = gluNewQuadric()
        gluQuadricTexture(self.navball, GL_TRUE)
        gluQuadricNormals(self.navball, GLU_SMOOTH)  

        glBindTexture(GL_TEXTURE_2D, self.navball_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        self.orientation = np.array([1, 0, 0, 0])

        self.prograde_vector = TexturedQuad(-.08, -.08, -4, .08, .08, Colors.Yellow, 'Textures/ManeuverVectors.png',
                                            True, (0, 0.66), (0.33, 0.66), (0.33, 1), (0, 1))
        
        self.retrograde_vector = TexturedQuad(-0, -0, -4, .08, .08, Colors.Yellow, 'Textures/ManeuverVectors.png', 
                                              True, (.33, .66), (.66, .66), (.66, 1), (.33, 1), 0.5)
        
    def rotate(self, axis, angle_degrees):
        rotation_quat = quaternion_from_axis_angle(axis, angle_degrees)
        self.orientation = multiply_quaternions(self.orientation, rotation_quat)

    def apply_orientation(self):
        rotation_matrix = quaternion_to_matrix(self.orientation)
        glMultMatrixf(rotation_matrix)
        
    def draw_navball(self):
        gl_init_3d()
        setup_lighting()
        
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.navball_texture)
        glTranslatef(-0.161, -0.013, -5)
        glRotatef(1.6, 0, 1, 0)
        self.apply_orientation()
        gluSphere(self.navball, .3, 64, 64)  # radius, slices, stacks orignal radius 1.39
        glPopMatrix()
        glDisable(GL_LIGHTING)

        self.prograde_vector.draw()
        self.retrograde_vector.draw()
        
        gl_init_2d()

class ScreenAttitude:
    def __init__(self):
        self.texture_id = load_texture('Textures/StaticMask.png')
        
        self.altitude = self.surface_speed = self.orbital_velocity = self.acceleration = 0
        self.navball = NavBall()

        altitude_text = text(f"{self.altitude}", Colors.Yellow, 120, 26, 33)
        surface_speed_text = text(f"{self.surface_speed}", Colors.Yellow, 560, 26, 33)
        orbital_velocity_text = text(f"{self.orbital_velocity}", Colors.Yellow, 120, 110, 33)
        accel_text = text(f"{self.acceleration}", Colors.Yellow, 560, 110, 33)
        speedmode_text = text("SPEEDMODE:", Colors.White, 100, 153, 16)
        speedmode_select_text = text("ORB", Colors.Blue, 197, 153, 16)
        
        roll_text = text("XXX.X\u00B0", Colors.Green, 119, 228, 33)
        heading_text = text("XXX.X\u00B0", Colors.Green, 355, 68, 33)
        pitch_text = text("XXX.X\u00B0", Colors.Green, 590, 228, 33)

        self.attitude_text = [altitude_text, surface_speed_text,
                              orbital_velocity_text, accel_text, 
                              speedmode_text, roll_text, heading_text, 
                              pitch_text, speedmode_select_text]
        
        self.standby_texture = [
            (0.0, 1.0),
            (1.0, 1.0),
            (1.0, 0.0),
            (0.0, 0.0),
        ]

        self.standby_vertices = [
            (100, -3),
            (700, -3),
            (700, 597),
            (100, 597)
        ]

    def draw(self):
        self.navball.draw_navball()
        glColor3f(1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        for tex_coord, vertex in zip(self.standby_texture, self.standby_vertices):
            glTexCoord2f(*tex_coord)
            glVertex2f(*vertex)
        glEnd()

        #self.altitude += 5
        for text in self.attitude_text:
            #text.update_text(f"{self.altitude}")
            text.draw()

class TexturedQuad:
    def __init__(self, x, y, z, width, height, color, texture_path, 
                enable_mipmap, b_l = (0, 0), b_r = (0, 1), t_r = (1, 1), t_l = (1, 0), opacity = 1.0):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.color = color
        self.texture = load_texture(texture_path)
        self.b_l = b_l
        self.b_r = b_r
        self.t_r = t_r
        self.t_l = t_l
        self.opacity = opacity
        
        if (enable_mipmap):
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColor4f(*self.color.value, self.opacity)
        glBegin(GL_QUADS)
        
        glTexCoord2f(*self.b_l)
        glVertex3f(self.x, self.y, self.z)
        
        glTexCoord2f(*self.b_r)
        glVertex3f(self.x + self.width, self.y, self.z)
        
        glTexCoord2f(*self.t_r)
        glVertex3f(self.x + self.width, self.y + self.height, self.z)
        
        glTexCoord2f(*self.t_l)
        glVertex3f(self.x, self.y + self.height, self.z)
        glEnd()
               
class quad:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        glBindTexture(GL_TEXTURE_2D, 0)

        glColor3f(*self.color.value)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

class text:
    def __init__(self, text, color, x, y, scale):
        self.font = pygame.font.Font('Textures/Poppins-Light.ttf', scale)
        self.text_texture, self.text_width, self.text_height = self.create_text_texture(text, self.font)
        self.x = x
        self.y = y
        self.color = color

    def create_text_texture(self, text, font):
        # Render the text with Pygame
        text_surface = self.font.render(text, True, (255, 255, 255))  # White text
        text_data = pygame.image.tostring(text_surface, "RGBA", False)
        width, height = text_surface.get_size()

        # Generate a new texture ID and bind it
        text_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, text_texture)
    
        # Upload the text as a texture to OpenGL
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return text_texture, width, height
    
    def draw(self, target_width = None, target_height = None):
        glBindTexture(GL_TEXTURE_2D, self.text_texture)
        glColor3f(*self.color.value)

        width = target_width if target_width else self.text_width
        height = target_height if target_height else self.text_height

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(self.x, self.y)
        glTexCoord2f(1, 0); glVertex2f(self.x + width, self.y)
        glTexCoord2f(1, 1); glVertex2f(self.x + width, self.y + height)
        glTexCoord2f(0, 1); glVertex2f(self.x, self.y + height)
        glEnd()

    def update_text(self, new_text):
        glDeleteTextures(1, [self.text_texture])
        self.text_texture, self.text_width, self.text_height = self.create_text_texture(new_text, self.font)

def draw_statics():
    static_select_backround = quad(100, 0, 600, 25, Colors.Background)
    background_divider = quad(200, 0, 2, 25, Colors.White)

    static_select_backround.draw()
    static_select_backround.y = 575
    static_select_backround.draw()

    for y in range(2):
        for x in range(5):
            background_divider.draw()
            background_divider.x += 100
        
        background_divider.y = 575
        background_divider.x = 200
    background_divider.y = 0
    static_select_backround.y = 0

def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)  # Load the image with Pygame
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()

    # Generate and bind texture
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texture_id

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 600), pygame.DOUBLEBUF | pygame.OPENGL)
    clock = pygame.time.Clock()

    gl_init_2d()
    
    menu_texts = initialize_menu_text()
    
    screen_standby = Screen('Textures/nosignal.png')
    screen_attitude = ScreenAttitude()

    screen_select = [screen_standby, screen_attitude]
    screen_number = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_RIGHT:
                    screen_number += 1
                    if screen_number >= len(screen_select):  
                        screen_number = 0

                elif event.key == pygame.K_LEFT:
                    screen_number -= 1
                    if screen_number < 0: 
                        screen_number = len(screen_select) - 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            screen_attitude.navball.rotate([1, 0, 0], 1)
        if keys[pygame.K_s]:
            screen_attitude.navball.rotate([1, 0, 0], -1)
        if keys[pygame.K_a]:
            screen_attitude.navball.rotate([0, 1, 0], -1)
        if keys[pygame.K_d]:
            screen_attitude.navball.rotate([0, 1, 0], 1)
        if keys[pygame.K_q]:
            screen_attitude.navball.rotate([0, 0, 1], 1)
        if keys[pygame.K_e]:
            screen_attitude.navball.rotate([0, 0, 1], -1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        screen_select[screen_number].draw()

        draw_statics()

        for texts in menu_texts:
            texts.draw()
            
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()