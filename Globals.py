from Attitude import ScreenAttitude
from BaseClasses import Colors, Screen, Text

screen_select = None
menu_texts = None

def init_screens():
    global screen_select
    screen_standby = Screen('Textures/nosignal.png')
    screen_attitude = ScreenAttitude()

    screen_select = [screen_standby, screen_attitude]


def init_menu_text():
    global menu_texts
    attitude_text = Text("ATTITUDE", Colors.White, 105, 0, 20)
    target_text = Text("TARGET", Colors.White, 216, 0, 20)
    nav_text = Text("NAV 1/2", Colors.White, 316, 0, 20)
    astrogator_text = Text("ASTR.", Colors.White, 425, 0, 20)
    graphs_text = Text("GRPH. 1/2", Colors.White, 508, 0, 20)
    vslview_text = Text("VESL.VIEW", Colors.White, 605, 0, 20)

    flight_text = Text("FLIGHT", Colors.White, 119, 575, 20)
    orbit_text = Text("ORB/DISP", Colors.White, 207, 575, 20)
    docking_text = Text("DOCKING", Colors.White, 307, 575, 20)
    log_text = Text("SHIP/LOG", Colors.White, 407, 575, 20)
    crew_text = Text("CREW", Colors.White, 523, 575, 20)
    sci_text = Text("SCI/COM", Colors.White, 610, 575, 20)

    menu_texts = [attitude_text, target_text, nav_text, 
                  astrogator_text, graphs_text, vslview_text,
                  flight_text, orbit_text, docking_text,
                  log_text, crew_text, sci_text]

