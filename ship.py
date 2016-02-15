

import defines
from weapons import weapon
from object_loader import loadObject, new_physic_object
from panda3d.core import LVector3, TextureStage
from panda3d.core import LPoint2


def init_ship(self, ship_model_path, player2=False):
    if player2 == True:
        pos = LPoint2(12,-8)
        category_bits = 0x0003
        mask_bits = (0x0001 | 0x0002)
    else:
        pos = LPoint2(-12,8)
        category_bits = 0x0002
        mask_bits = (0x0001 | 0x0003)

    new_ship = loadObject(ship_model_path, scale=0.5)
    physic_debug, physic_body  = new_physic_object(shape='box', scale=0.5, 
                        angular_dampning=5, linear_dampning=0.1, pos=pos, 
                        category_bits=category_bits, mask_bits=mask_bits)
    new_ship.reparentTo(render)
    new_ship.setTexRotate(TextureStage.getDefault(), 90)

    new_weapon = weapon();
    if player2 == True:
        shipname = "ship2"
        self.life_bar2 = loadObject(scale=0.5)
        self.life_bar2.setPos(-0.1,0, 0.12)
        self.life_bar2.reparentTo(base.a2dBottomRight)
        self.life_bar2.setSz(0.005)
        self.energy_bar2 = loadObject(scale=0.5)
        self.energy_bar2.setPos(-0.1,0, 0.215)
        self.energy_bar2.reparentTo(base.a2dBottomRight)
        self.energy_bar2.setSz(0.005)
    else:
        shipname = "ship" 
        self.life_bar = loadObject(scale=0.5)
        self.life_bar.setPos(-0.1,0,0.12)
        self.life_bar.reparentTo(base.a2dBottomLeft)
        self.life_bar.setSz(0.005)
        self.energy_bar = loadObject(scale=0.5)
        self.energy_bar.setPos(-1,0,0.215)
        self.energy_bar.reparentTo(base.a2dBottomLeft)
        self.energy_bar.setSz(0.005)

    defines.ENTITIES[defines.ENTITY_ID] = {'CATEGORY':shipname,'E_FIELD_ENABLED': False, 'NODE':new_ship, 'PHYSIC_NODE':physic_debug, 'BODY':physic_body, 'SHIELD':100.0, 'ENERGY':100.0, 'WEAPON':new_weapon}
    defines.ENTITY_ID += 1

def add_shield(self, entity_id):
    pos = defines.ENTITIES[entity_id]['BODY'].position
    if defines.ENTITIES[entity_id]['CATEGORY'] == 'ship':
        category_bits = 0x0002
        mask_bits = (0x0001 | 0x0003)
    else:
        category_bits = 0x0003
        mask_bits = (0x0001 | 0x0002)
    physic_debug, physic_body  = new_physic_object(shape='circle', scale=1, 
                        angular_dampning=0, linear_dampning=0, pos=pos, 
                        category_bits=category_bits, mask_bits=mask_bits, den=0.0)
    # help(defines.world)
    defines.world.CreateRevoluteJoint(
            bodyA=defines.ENTITIES[entity_id]['BODY'],
            bodyB=physic_body
        )
    new_shield = loadObject('shield.png', scale=1)
    physic_body.linearVelocity.Set(defines.ENTITIES[entity_id]['BODY'].linearVelocity.x, defines.ENTITIES[entity_id]['BODY'].linearVelocity.y)
    physic_body.angularVelocity = defines.ENTITIES[entity_id]['BODY'].angularVelocity

    defines.ENTITIES[entity_id]['E_FIELD_BODY'] = physic_body
    defines.ENTITIES[entity_id]['E_FIELD_DEBUG_NODE'] = physic_debug
    defines.ENTITIES[entity_id]['E_FIELD_NODE'] = new_shield
    # CreateFixture
    # CreateFixturesFromShapes


def update_ship(self):
    for entity_id, entity in defines.ENTITIES.items(): 
        if entity['CATEGORY'] == "ship":
            self.life_bar.setSx(entity['SHIELD']/250)
            self.life_bar.setX(0.45 + entity['SHIELD']/250)
            self.energy_bar.setSx(entity['ENERGY']/250)
            self.energy_bar.setX(0.45 + entity['ENERGY']/250)
            if entity['ENERGY'] < 100:
                entity['ENERGY'] += 0.1
            if self.keys["turnRight"]:
                entity['BODY'].ApplyTorque(-5, True)
            elif self.keys["turnLeft"]:
                entity['BODY'].ApplyTorque(5, True)
            if self.keys["accel"]:
                f = entity['BODY'].GetWorldVector(localVector=(5.0, 0.0))
                p = entity['BODY'].GetWorldPoint(localPoint=(0.0, 0))
                entity['BODY'].ApplyForce(f, p, True)
            if self.keys["fire"] and entity['ENERGY'] >= 20:
                entity['WEAPON'].fire(self, entity_id)
            if self.keys["laser"] and entity['ENERGY'] >= 10:
                entity['WEAPON'].fire_laser(self, entity_id)
            if self.keys["e_to_s"] and entity['ENERGY'] >= 5 and entity['SHIELD'] < 100:
                entity['ENERGY'] -= 2
                entity['SHIELD'] += 1
            if self.keys["s_to_e"] and entity['SHIELD'] >= 5 and entity['ENERGY'] < 100:
                entity['ENERGY'] += 2
                entity['SHIELD'] -= 1
            if self.keys["cloak"] and entity['ENERGY'] > 5 :
                entity['NODE'].detachNode()
                entity['ENERGY'] -= 0.2
            else:
                entity['NODE'].reparentTo(render)
            if self.keys["e_field"] == 1 and ((entity['ENERGY'] > 5 and entity['E_FIELD_ENABLED'] == True) or (entity['ENERGY'] > 20)):
                if entity['E_FIELD_ENABLED'] == False:
                    entity['ENERGY'] -= 3
                    add_shield(self, entity_id)
                    entity['E_FIELD_ENABLED'] = True
                entity['ENERGY'] -= 0.3
            elif entity['E_FIELD_ENABLED'] == True:
                defines.world.DestroyBody(entity['E_FIELD_BODY'])
                entity['E_FIELD_DEBUG_NODE'].removeNode()
                entity['E_FIELD_NODE'].removeNode()
                entity['E_FIELD_ENABLED'] = False

        if entity['CATEGORY'] == "ship2":
            self.life_bar2.setSx(entity['SHIELD']/250)
            self.life_bar2.setX(-0.95 + entity['SHIELD']/250 )
            self.energy_bar2.setSx(entity['ENERGY']/250)
            self.energy_bar2.setX(-0.95 + entity['ENERGY']/250)
            if entity['ENERGY'] < 100:
                entity['ENERGY'] += 0.1
            if self.keys["p2turnRight"]:
                entity['BODY'].ApplyTorque(-5, True)
            elif self.keys["p2turnLeft"]:
                entity['BODY'].ApplyTorque(5, True)
            if self.keys["p2accel"]:
                f = entity['BODY'].GetWorldVector(localVector=(5.0, 0.0))
                p = entity['BODY'].GetWorldPoint(localPoint=(0.0, 0))
                entity['BODY'].ApplyForce(f, p, True)
            if self.keys["p2fire"] and entity['ENERGY'] >= 20:
                entity['WEAPON'].fire(self, entity_id)
            if self.keys["p2laser"] and entity['ENERGY'] >= 5:
                entity['WEAPON'].fire_laser(self, entity_id)
            if self.keys["e_to_s2"] and entity['ENERGY'] >= 5 and entity['SHIELD'] < 100:
                entity['ENERGY'] -= 2
                entity['SHIELD'] += 1
            if self.keys["s_to_e2"] and entity['SHIELD'] >= 5 and entity['ENERGY'] < 100:
                entity['ENERGY'] += 2
                entity['SHIELD'] -= 1
            if self.keys["cloak2"] and entity['ENERGY'] > 5 :
                entity['NODE'].detachNode()
                entity['ENERGY'] -= 0.2
            else:
                entity['NODE'].reparentTo(render)
            if self.keys["e_field2"] == 1 and ((entity['ENERGY'] > 5 and entity['E_FIELD_ENABLED'] == True) or (entity['ENERGY'] > 20)):
                if entity['E_FIELD_ENABLED'] == False:
                    entity['ENERGY'] -= 3
                    add_shield(self, entity_id)
                    entity['E_FIELD_ENABLED'] = True
                entity['ENERGY'] -= 0.3
            elif entity['E_FIELD_ENABLED'] == True:
                defines.world.DestroyBody(entity['E_FIELD_BODY'])
                entity['E_FIELD_DEBUG_NODE'].removeNode()
                entity['E_FIELD_NODE'].removeNode()
                entity['E_FIELD_ENABLED'] = False

