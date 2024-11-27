from OpenGL.GL import *
from OpenGL.GLU import *
from Navball import NavBall
from Utilities import load_texture
from BaseClasses import Text, Colors

class ScreenAttitude:
    def __init__(self):
        self.texture_id = load_texture('Textures/StaticMask.png')
        
        self.altitude = self.surface_speed = self.orbital_velocity = self.acceleration = 0
        self.navball = NavBall()

        altitude_text = Text(f"{self.altitude}", Colors.Yellow, 120, 26, 33)
        surface_speed_text = Text(f"{self.surface_speed}", Colors.Yellow, 560, 26, 33)
        orbital_velocity_text = Text(f"{self.orbital_velocity}", Colors.Yellow, 120, 110, 33)
        accel_text = Text(f"{self.acceleration}", Colors.Yellow, 560, 110, 33)
        speedmode_text = Text("SPEEDMODE:", Colors.White, 100, 153, 16)
        speedmode_select_text = Text("ORB", Colors.Blue, 197, 153, 16)
        
        roll_text = Text("XXX.X\u00B0", Colors.Green, 119, 228, 33)
        heading_text = Text("XXX.X\u00B0", Colors.Green, 355, 68, 33)
        pitch_text = Text("XXX.X\u00B0", Colors.Green, 590, 228, 33)

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