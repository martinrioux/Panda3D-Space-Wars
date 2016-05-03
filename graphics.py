
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import defines
from panda3d.core import LVector3, LineSegs
from math import pi
from Box2D import b2Transform, b2Vec2
from object_loader import replace_body
from ship import add_shield

def genLabelText(text, i):
    return OnscreenText(text=text, parent=base.a2dTopLeft, pos=(0.07, -.06 * i - 0.1),
                        fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5), scale=.05)

def init_labels(self):
    self.energy1 = OnscreenText(text="Energy",
                      parent=base.a2dBottomLeft, scale=.05,
                      align=TextNode.ARight, pos=(0.4, 0.2),
                      fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
    self.shield1 = OnscreenText(text="Shield",
                      parent=base.a2dBottomLeft, scale=.05,
                      align=TextNode.ARight, pos=(0.4, 0.11),
                      fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
    self.energy2 = OnscreenText(text="Energy",
                      parent=base.a2dBottomRight, scale=.05,
                      align=TextNode.ARight, pos=(-1, 0.2),
                      fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
    self.shield2 = OnscreenText(text="Shield",
                      parent=base.a2dBottomRight, scale=.05,
                      align=TextNode.ARight, pos=(-1, 0.11),
                      fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
def player_win(self, player):
    if defines.GAME_WON == 0:
      defines.GAME_WON = 1
      sound = base.loader.loadSfx("sounds/endgame.ogg")
      sound.setVolume(0.5)
      sound.play()
      if player == 'ship':
        self.winner = OnscreenText(text="Player 2 win", scale=0.1, pos=(0, 0),
                        fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
      else:
        self.winner = OnscreenText(text="Player 1 win", scale=0.1, pos=(0, 0),
                        fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))

      task = taskMgr.doMethodLater(5, self.reset_game, 'reset game')

def update_graphics(self):
    width = (base.win.getXSize() + 0.0) / (base.win.getYSize() + 0.0)
    height = 1

    X_MAX_LOCATION = width * 15
    X_RETURN_LOCATION = width * 15
    Y_MAX_LOCATION = height * 15
    Y_RETURN_LOCATION = height * 15

    if self.keys["toggle_debug"] ==  1:
            if defines.DISPLAY_PHYSIC_DEBUG == 1:
                defines.DISPLAY_PHYSIC_DEBUG = 0
            else:
                defines.DISPLAY_PHYSIC_DEBUG = 1
    for entity_id, entity in defines.ENTITIES.items():

        if self.keys["toggle_debug"] ==  1:
            if defines.DISPLAY_PHYSIC_DEBUG == 1:
                entity['PHYSIC_NODE'].detachNode()
            else:
                entity['PHYSIC_NODE'].reparentTo(entity['NODE'])
        entity['NODE'].setR(-entity['BODY'].angle*180/pi%360)
        pos = entity['BODY'].position
        x_pos = pos.x
        y_pos = pos.y
        replace = 0
        if x_pos > X_MAX_LOCATION:
            x_pos = -X_RETURN_LOCATION
            replace = 1
        if x_pos < -X_MAX_LOCATION:
            x_pos = X_RETURN_LOCATION
            replace = 1
        if y_pos > Y_MAX_LOCATION:
            y_pos = -Y_RETURN_LOCATION
            replace = 1
        if y_pos < -Y_MAX_LOCATION:
            y_pos = Y_RETURN_LOCATION
            replace = 1
        if replace == 1:
          if entity['CATEGORY'] == 'ship':
            category_bits = 0x0002
            mask_bits = (0x0001 | 0x0003)
          elif entity['CATEGORY'] == 'ship2':
            category_bits = 0x0003
            mask_bits = (0x0001 | 0x0002)
          else:
            category_bits = 0x0001
            mask_bits = (0x0001 | 0x0002 | 0x0003)
          shape = 'box'
          if entity['CATEGORY'] == 'asteroid':
            shape = 'circle'
          new_body = replace_body(entity['BODY'], b2Vec2(x_pos, y_pos), entity['NODE'].getScale().x, category_bits=category_bits, mask_bits=mask_bits, shape=shape)
          new_body.linearVelocity.Set(entity['BODY'].linearVelocity.x, entity['BODY'].linearVelocity.y)
          new_body.angularVelocity = entity['BODY'].angularVelocity
          defines.world.DestroyBody(entity['BODY'])
          entity['BODY'] = new_body

          if (entity['CATEGORY'] == 'ship' or entity['CATEGORY'] == 'ship2') and entity['E_FIELD_ENABLED'] == True:
              defines.world.DestroyBody(entity['E_FIELD_BODY'])
              entity['E_FIELD_DEBUG_NODE'].removeNode()
              entity['E_FIELD_NODE'].removeNode()
              add_shield(self, entity_id)
        if (entity['CATEGORY'] == 'ship' or entity['CATEGORY'] == 'ship2') and entity['E_FIELD_ENABLED'] == True:
          entity['E_FIELD_NODE'].setPos(entity['E_FIELD_BODY'].position.x, 55, entity['E_FIELD_BODY'].position.y)

        entity['NODE'].setPos(LVector3(pos.x, 55, pos.y))

    self.keys["toggle_debug"] = 0

