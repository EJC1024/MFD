import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from enum import Enum
from Utilities import load_texture

class Colors(Enum):
    White = (1.0, 1.0, 1.0)
    Black = (0.0, 0.0, 0.0)
    Yellow = (1.0, 1.0, 0.0)
    Red = (1.0, 0.0, 0.0)
    Green = (0.0, 1.0, 0.0)
    Blue = (0.0, 0.0, 1.0)
    Magenta = (1.0, 0.0, 1.0)
    Background = (0.01, 0.23, 0.35)

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

class DepthQuad:
    def __init__(self, x, y, z, width, height, color, texture_path, 
                enable_mipmap = False, b_l = (0, 0), b_r = (0, 1), t_r = (1, 1), t_l = (1, 0), opacity = 1.0):
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
               
class Quad:
    def __init__(self, x, y, width, height, color, opacity = 1.0, texture_path = None, 
                 b_l = (0, 0), b_r = (0, 1), t_r = (1, 0), t_l = (1, 1), enable_mipmap = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.opacity = opacity
        self.texture_path = texture_path
                
        if (texture_path != None):
            self.texture = load_texture(self.texture_path)
            self.b_l = b_l
            self.b_r = b_r
            self.t_r = t_r
            self.t_l = t_l
        
        if (enable_mipmap):
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)

    def draw(self):
        
        if (self.texture_path != None):
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glColor4f(*self.color.value, self.opacity)
            glBegin(GL_QUADS)
        
            glTexCoord2f(*self.b_l)
            glVertex2f(self.x, self.y)
        
            glTexCoord2f(*self.b_r)
            glVertex2f(self.x + self.width, self.y)
        
            glTexCoord2f(*self.t_r)
            glVertex2f(self.x + self.width, self.y + self.height)
        
            glTexCoord2f(*self.t_l)
            glVertex2f(self.x, self.y + self.height)
            glEnd()
            
        else:
            glBindTexture(GL_TEXTURE_2D, 0)
            glColor4f(*self.color.value, self.opacity)
            glBegin(GL_QUADS)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.width, self.y)
            glVertex2f(self.x + self.width, self.y + self.height)
            glVertex2f(self.x, self.y + self.height)
            glEnd()

class Text:
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