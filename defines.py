
from math import pi


def init_defines():

    global ENTITY_ID
    ENTITY_ID = 0
    global GAME_ONGOING
    GAME_ONGOING = 0
    global GAME_WON
    GAME_WON = 0
    global ENTITIES
    ENTITIES  = {}
    global SPRITE_POS
    SPRITE_POS = 55     # At default field of view and a depth of 55, the screen dimensions is 40x30 units
    global SCREEN_X
    SCREEN_X = 20       # Screen goes from -20 to 20 on X
    global SCREEN_Y
    SCREEN_Y = 15       # Screen goes from -15 to 15 on Y
    global TURN_RATE
    TURN_RATE = 360     # Degrees ship can turn in 1 second
    global ACCELERATION
    ACCELERATION = 10   # Ship acceleration in units/sec/sec
    global MAX_VEL
    MAX_VEL = 6         # Maximum ship velocity in units/sec
    global MAX_VEL_SQ
    MAX_VEL_SQ = MAX_VEL ** 2  # Square of the ship velocity
    global DEG_TO_RAD
    DEG_TO_RAD = pi / 180  # translates degrees to radians for sin and cos
    global BULLET_LIFE
    BULLET_LIFE = 2     # How long bullets stay on screen before removed
    global BULLET_REPEAT
    BULLET_REPEAT = .2  # How often bullets can be fired
    global BULLET_SPEED
    BULLET_SPEED = 10   # Speed bullets move
    global GRAPHIC_TO_PHYSIC_SCALE_RATIO
    GRAPHIC_TO_PHYSIC_SCALE_RATIO = 1
    global AST_INIT_VEL
    AST_INIT_VEL = 1    # Velocity of the largest asteroids
    global AST_INIT_SCALE
    AST_INIT_SCALE = 1.5  # Initial asteroid scale
    global AST_VEL_SCALE
    AST_VEL_SCALE = 2.2  # How much asteroid speed multiplies when broken up
    global AST_SIZE_SCALE
    AST_SIZE_SCALE = .6  # How much asteroid scale changes when broken up
    global AST_MIN_SCALE
    AST_MIN_SCALE = 1.1  # If and asteroid is smaller than this and is hit,
    global world        #physic world
    global X_MAX_LOCATION    
    X_MAX_LOCATION = 28            
    global X_RETURN_LOCATION  
    X_RETURN_LOCATION = 28          
    global Y_MAX_LOCATION    
    Y_MAX_LOCATION = 16         
    global Y_RETURN_LOCATION     
    Y_RETURN_LOCATION = 16    
    global DISPLAY_PHYSIC_DEBUG        
    DISPLAY_PHYSIC_DEBUG = 0
    global CONTACT_LIST        
    CONTACT_LIST = []
    global PLANET_ON        
    PLANET_ON = 0
        
        
