from BaseClasses import Colors, Quad
from Utilities import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

class PositionVector:
    def __init__(self):
        # Define vector properties in a list of dictionaries
        vector_data = [
            {"x": 220, "y": 345, "width": -75, "height": -75, "color": Colors.Yellow, 
             "opacity": 1.0, "texture_path": 'Textures/ManeuverVectors.png', 
             "b_l": (0, 0.66), "b_r": (0.33, 0.66), "t_r": (0.33, 1), "t_l": (0, 1), "mipmaps": True},
            
            {"x": 660, "y": 345, "width": -75, "height": -75, "color": Colors.Yellow, 
             "opacity": 1.0, "texture_path": 'Textures/ManeuverVectors.png', 
             "b_l": (0.33, 0.66), "b_r": (0.66, 0.66), "t_r": (0.66, 1), "t_l": (0.33, 1), "mipmaps": True},      
        ]
        
        self.vectors = [
            Quad(data["x"], data["y"], data["width"], data["height"], data["color"], 
                 data["opacity"], data["texture_path"], data["b_l"], data["b_r"], 
                 data["t_r"], data["t_l"], data["mipmaps"])
            for data in vector_data
        ]
        
    def translate(self, heading):
        for vector in self.vectors:
            glPushMatrix()                      
            glTranslatef(heading, 0, 0)        
            vector.draw()
            glPopMatrix() 
            
    def translate_vector(self, index, dx, dy):
        if 0 <= index < len(self.vectors):
            self.vectors[index].translate(dx, dy)

    def draw(self):
        for vector in self.vectors:
            vector.draw()
        
class NavBall:
    def __init__(self):
        self.navball_texture = load_texture('Textures/Trekky.png')
        self.navball = gluNewQuadric()
        gluQuadricTexture(self.navball, GL_TRUE)
        gluQuadricNormals(self.navball, GLU_SMOOTH)  
        
        self.position_vectors = PositionVector()

        glBindTexture(GL_TEXTURE_2D, self.navball_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        self.orientation = np.array([1, 0, 0, 0])
        
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
                
        gl_init_2d()
        #self.position_vectors.draw()
        #self.position_vectors.translate_vector(0, 0, 5)

# If starting with degrees:
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