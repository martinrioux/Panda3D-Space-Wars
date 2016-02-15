
import defines
from Box2D import b2World, b2RayCastCallback, b2Vec2
from planet import planet_gravity

def init_physics():
    defines.world = b2World(gravity=(0,0), doSleep=True)  # default gravity is (0,-10) and doSleep is True
    defines.world.using_contacts = True

def bullet_contact(entity_id, bullet_entity_id, impact):
    now = globalClock.getRealTime()
    if now - (defines.ENTITIES[bullet_entity_id]['EXPIRE'] - 3) > 0.09:
        defines.ENTITIES[bullet_entity_id]['NODE'].removeNode()
        defines.ENTITIES[bullet_entity_id]['PHYSIC_NODE'].removeNode()
        defines.world.DestroyBody(defines.ENTITIES[bullet_entity_id]['BODY'])
        del defines.ENTITIES[bullet_entity_id]
        defines.ENTITIES[entity_id]['SHIELD'] -= 10
        #print defines.ENTITIES[entity_id]['SHIELD']

def update_physics(dt):
    vel_iters, pos_iters = 6, 2
    planet_gravity()
    defines.world.Step(dt, vel_iters, pos_iters)

def add_contacts_to_list(entity_id, contacts):
    for c in contacts:
        impact = 0
        for d in c.contact.manifold.points:
            if d.normalImpulse > impact:
                impact = d.normalImpulse
        for entity_2_id, entity in defines.ENTITIES.items():
            if entity['BODY'] == c.other and c.contact.touching == True:
                defines.CONTACT_LIST += [[entity_id, entity_2_id, impact]]

def get_contacts_list():
    for entity_id, entity in defines.ENTITIES.items():
        if defines.ENTITIES[entity_id]['CATEGORY'] == 'asteroid':
            next
        contacts = defines.ENTITIES[entity_id]['BODY'].contacts

        if contacts == []:
            next
        add_contacts_to_list(entity_id, contacts)


def manage_contacts():
    i = 0
    for contact in defines.CONTACT_LIST:
        try:
            defines.ENTITIES[contact[0]]['BODY']
            defines.ENTITIES[contact[1]]['BODY']
            #print ("Entity: " + str(defines.ENTITIES[contact[0]]['CATEGORY']) + " -- In contact with: " + str(defines.ENTITIES[contact[1]]['CATEGORY']) + " -- At: " + str(contact[2]))
            #ASTEROID-SHIP
            if defines.ENTITIES[contact[0]]['CATEGORY'] == "ship" and defines.ENTITIES[contact[1]]['CATEGORY'] == "asteroid":
                defines.ENTITIES[contact[0]]['SHIELD'] -= contact[2]

            if defines.ENTITIES[contact[1]]['CATEGORY'] == "ship" and defines.ENTITIES[contact[0]]['CATEGORY'] == "asteroid":
                defines.ENTITIES[contact[1]]['SHIELD'] -= contact[2]

            #ASTEROID-SHIP2
            if defines.ENTITIES[contact[0]]['CATEGORY'] == "ship2" and defines.ENTITIES[contact[1]]['CATEGORY'] == "asteroid":
                defines.ENTITIES[contact[0]]['SHIELD'] -= contact[2]

            if defines.ENTITIES[contact[1]]['CATEGORY'] == "ship2" and defines.ENTITIES[contact[0]]['CATEGORY'] == "asteroid":
                defines.ENTITIES[contact[1]]['SHIELD'] -= contact[2]

            # PLANET-SHIP
            # if defines.ENTITIES[contact[0]]['CATEGORY'] == "ship" and defines.ENTITIES[contact[1]]['CATEGORY'] == "planet":
            #     defines.ENTITIES[contact[0]]['SHIELD'] -= contact[2]

            # if defines.ENTITIES[contact[1]]['CATEGORY'] == "ship" and defines.ENTITIES[contact[0]]['CATEGORY'] == "planet":
            #     defines.ENTITIES[contact[1]]['SHIELD'] -= contact[2]

            # #PLANET-SHIP2
            # if defines.ENTITIES[contact[0]]['CATEGORY'] == "ship2" and defines.ENTITIES[contact[1]]['CATEGORY'] == "planet":
            #     defines.ENTITIES[contact[0]]['SHIELD'] -= contact[2]

            # if defines.ENTITIES[contact[1]]['CATEGORY'] == "ship2" and defines.ENTITIES[contact[0]]['CATEGORY'] == "planet":
            #     defines.ENTITIES[contact[1]]['SHIELD'] -= contact[2]
     
     
            #ASTEROID-BULLET
            if defines.ENTITIES[contact[0]]['CATEGORY'] == "asteroid" and defines.ENTITIES[contact[1]]['CATEGORY'] == "bullet":
                bullet_contact(contact[0], contact[1], contact[2])
            if defines.ENTITIES[contact[1]]['CATEGORY'] == "asteroid" and defines.ENTITIES[contact[0]]['CATEGORY'] == "bullet":
                bullet_contact(contact[1], contact[0], contact[2])

            # #ASTEROID-ASTEROID
            # if defines.ENTITIES[contact[0]]['CATEGORY'] == "asteroid" and defines.ENTITIES[contact[1]]['CATEGORY'] == "asteroid":
            #     defines.ENTITIES[contact[0]]['SHIELD'] -= contact[2]*5
            #     defines.ENTITIES[contact[1]]['SHIELD'] -= contact[2]*5

            #SHIP-BULLET
            if defines.ENTITIES[contact[0]]['CATEGORY'] == "ship" and defines.ENTITIES[contact[1]]['CATEGORY'] == "bullet":
                bullet_contact(contact[0], contact[1], contact[2])
            if defines.ENTITIES[contact[1]]['CATEGORY'] == "ship" and defines.ENTITIES[contact[0]]['CATEGORY'] == "bullet":
                bullet_contact(contact[1], contact[0], contact[2])

            if defines.ENTITIES[contact[0]]['CATEGORY'] == "ship2" and defines.ENTITIES[contact[1]]['CATEGORY'] == "bullet":
                bullet_contact(contact[0], contact[1], contact[2])
            if defines.ENTITIES[contact[1]]['CATEGORY'] == "ship2" and defines.ENTITIES[contact[0]]['CATEGORY'] == "bullet":
                bullet_contact(contact[1], contact[0], contact[2]) 


        except:
            a = 2#print "entity deleted"
        del defines.CONTACT_LIST[i]
        i += 1


def test_laser_collision(start_x, start_y, end_x, end_y):
    point1 = b2Vec2(start_x, start_y)
    point2 = b2Vec2(end_x, end_y)
    callback = RayCastAnyCallback()
    defines.world.RayCast(callback, point1, point2)
    return callback

class RayCastAnyCallback(b2RayCastCallback):
    """This callback finds any hit"""

    def __repr__(self):
        return 'Any hit'

    def __init__(self, **kwargs):
        b2RayCastCallback.__init__(self, **kwargs)
        self.fixture = None
        self.hit = False

    def ReportFixture(self, fixture, point, normal, fraction):
        self.hit = True
        self.fixture = fixture
        self.point = b2Vec2(point)
        self.normal = b2Vec2(normal)
        return 0.0