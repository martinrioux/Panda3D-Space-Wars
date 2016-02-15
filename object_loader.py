
from panda3d.core import LPoint3

from panda3d.core import TransparencyAttrib, LineSegs, GeomTristrips, Geom, GeomVertexArrayFormat, GeomVertexFormat
from panda3d.core import GeomVertexData, GeomVertexWriter, GeomTriangles, GeomNode, NodePath, Point3
import defines
from Box2D import b2PolygonShape, b2_pi, b2FixtureDef, b2CircleShape
from direct.gui.DirectGui import DirectFrame, DGG, DirectButton, DirectCheckButton, DirectRadioButton

def loadObject(tex=None, pos=LPoint3(0, 0), depth=defines.SPRITE_POS, scale=1,
               transparency=True, model="models/plane"):
    # Every object uses the plane model and is parented to the camera
    # so that it faces the screen.
    obj = loader.loadModel(model)
    obj.reparentTo(camera)

    # Set the initial position and scale.
    obj.setPos(pos.getX(), depth, pos.getY())
    obj.setScale(scale)

    # This tells Panda not to worry about the order that things are drawn in
    # (ie. disable Z-testing).  This prevents an effect known as Z-fighting.
    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)

    if transparency:
        # Enable transparency blending.
        obj.setTransparency(TransparencyAttrib.MAlpha)

    if tex:
        # Load and set the requested texture.
        tex = loader.loadTexture("textures/" + tex)
        obj.setTexture(tex, 1)

    return obj

def new_physic_object(shape='box', scale=1, 
                        is_a_bullet=False, pos=(0, 0), 
                        angular_dampning=0, linear_dampning=0,
                        category_bits=0x0001, mask_bits=(0x0001 | 0x0002 | 0x0003),
                        den=2.0):

    debug_graphic = loader.loadModel("models/physic_square")
    debug_graphic.reparentTo(camera)
    if shape == 'circle':
        tex = loader.loadTexture("textures/round.png")
    else:
        tex = loader.loadTexture("textures/physic_texture.png")
    debug_graphic.setTexture(tex, 1)
    debug_graphic.setBin("unsorted", 0)
    debug_graphic.setDepthTest(False)
    if shape == 'box':
        new_shape = b2PolygonShape(box=(scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO, scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO))
    elif shape == 'circle':
        new_shape= b2CircleShape(radius=(scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO))
    else:
        new_shape = b2PolygonShape(box=(scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO, scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO))
        
    
    body = defines.world.CreateDynamicBody(
            position=pos,
            angle=0,
            angularDamping=angular_dampning,
            linearDamping=linear_dampning,  
            shapes=new_shape,
            bullet=is_a_bullet,
            shapeFixture=b2FixtureDef(density=den,
                                    categoryBits=category_bits,
                                maskBits=mask_bits)
        )

    return debug_graphic, body

def replace_body(old_body, new_position, scale, shape='box',
                  category_bits=0x0001, mask_bits=(0x0001 | 0x0002 | 0x0003)):
    if shape == 'box':
        new_shape = b2PolygonShape(box=(scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO, scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO))
    elif shape == 'circle':
        new_shape= b2CircleShape(radius=(scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO))
    else:
        new_shape= b2PolygonShape(box=(scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO, scale * defines.GRAPHIC_TO_PHYSIC_SCALE_RATIO))
    
    new_body = defines.world.CreateDynamicBody(
            position=new_position,
            angle=old_body.angle,
            angularDamping=old_body.angularDamping,
            linearDamping=old_body.linearDamping,  
            shapes=new_shape,
            bullet=old_body.bullet,
            shapeFixture=b2FixtureDef(density=2.0,
                            categoryBits=category_bits,
                            maskBits=mask_bits  )
        )

    return new_body

def add_button(self, text, label_id, pos_x, pos_y, width=0.0, hight=0.1):
    if width == 0.0:
        for c in range(len(text)/2):
            width += 0.08
    ls = LineSegs("lines")
    ls.setColor(0,1,0,1)
    ls.drawTo(-width/2, 0, hight/2)
    ls.drawTo(width/2, 0, hight/2)
    ls.drawTo(width/2, 0,-hight/2)
    ls.drawTo(-width/2, 0,-hight/2)
    ls.drawTo(-width/2, 0, hight/2)
    border = ls.create(False)
    border.setTag('back_ground', '1')
    
    array = GeomVertexArrayFormat()
    array.addColumn("vertex", 4, Geom.NTFloat32, Geom.CPoint)
    arr_format = GeomVertexFormat()
    arr_format.addArray(array)
    arr_format = GeomVertexFormat.registerFormat(arr_format)

    vdata = GeomVertexData('fill', arr_format, Geom.UHStatic)
    vdata.setNumRows(4)
    vertex = GeomVertexWriter(vdata, 'vertex')

    vertex.addData3f(-width/2, 0, hight/2)
    vertex.addData3f(width/2, 0, hight/2)
    vertex.addData3f(-width/2, 0,-hight/2)
    vertex.addData3f(width/2, 0,-hight/2)

    prim = GeomTristrips(Geom.UHStatic)
    prim.addVertex(0)
    prim.addVertex(1)
    prim.addVertex(2)
    prim.addVertex(3)

    geom = Geom(vdata)
    geom.addPrimitive(prim)
    node = GeomNode('gnode')
    node.addGeom(geom)
    nodePath = NodePath("button")
    nodePath.attachNewNode(node)
    nodePath.setPos(0,0,0)
    nodePath.setTag('button', '1')
    nodePath.setBin("unsorted", 0)
    nodePath.setDepthTest(False)
    nodePath.setColor(0,0,0,1)
    nodePath.attachNewNode(border)

    nodePath1 = NodePath("button")
    nodePath1.attachNewNode(node)
    nodePath1.setPos(0,0,0)
    nodePath1.setTag('button1', '1')
    nodePath1.setBin("unsorted", 0)
    nodePath1.setDepthTest(False)
    nodePath1.setColor(0,1,0,1)
    nodePath1.attachNewNode(border)


    button=DirectFrame( 
                        enableEdit=1,                      
                        text=text,
                        geom=nodePath,
                        text_scale=0.05,
                        text_fg=(0,1,0,1),
                        borderWidth=(1,1), 
                        relief = None,
                        text_pos=(0,-0.01,0),
                        textMayChange=1,
                        state=DGG.NORMAL,
                        parent=aspect2d
                        )
    button.setPos(pos_x,0,pos_y)
    button.bind(DGG.B1PRESS, button_click, [button])
    button.bind(DGG.WITHIN, button_hover, [button])
    button.bind(DGG.WITHOUT, button_no_hover, [button])
    # button.resetFrameSize()
    # self.button.bind(DGG.WITHIN, self.onMouseHoverInFunction, [button, some_value1])

    defines.ENTITIES[defines.ENTITY_ID] = {'CATEGORY':'button', 'BUTTON':button, 'NODE':nodePath, 'LABEL':label_id,'STATUS': 0}
    defines.ENTITY_ID += 1

def button_click(self, button):
    sound = base.loader.loadSfx("sounds/click.ogg")
    sound.play()
    for entity_id, entity in defines.ENTITIES.items():
        if entity['BUTTON'] == self and entity['STATUS'] == 0:
            entity['STATUS'] = 1
            self["text_fg"] = (0,0,0,1)
            self["geom"] = None
            entity['NODE'].setColor(0,1,0,1)
            self["geom"] = entity['NODE']

        elif entity['BUTTON'] == self:
            entity['STATUS'] = 0
            self["text_fg"] = (0,1,0,1)
            self["geom"] = None
            entity['NODE'].setColor(0,0,0,1)
            self["geom"] = entity['NODE']

def button_hover(self, button):
    sound = base.loader.loadSfx("sounds/rollover.ogg")
    sound.play()
    for entity_id, entity in defines.ENTITIES.items():
        if entity['BUTTON'] == self and entity['STATUS'] == 0:
            self["text_fg"] = (0,0,0,1)
            self["geom"] = None
            entity['NODE'].setColor(0,1,0,1)
            self["geom"] = entity['NODE']

def button_no_hover(self, button): 
    for entity_id, entity in defines.ENTITIES.items():
        if entity['BUTTON'] == self and entity['STATUS'] == 0:
            self["text_fg"] = (0,1,0,1)
            self["geom"] = None
            entity['NODE'].setColor(0,0,0,1)
            self["geom"] = entity['NODE']