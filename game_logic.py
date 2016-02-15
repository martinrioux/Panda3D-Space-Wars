import defines
from ship import update_ship
from asteroids import break_asteroid
from graphics import player_win

def update_game_logic(self):
    update_ship(self)
    for entity_id, entity in defines.ENTITIES.items():
        if entity['CATEGORY'] == 'bullet' and globalClock.getRealTime() > entity['EXPIRE']:
            entity['NODE'].removeNode()
            entity['PHYSIC_NODE'].removeNode()
            defines.world.DestroyBody(entity['BODY'])
            del defines.ENTITIES[entity_id]
            continue

        if entity['CATEGORY'] == 'asteroid':
            if entity['SHIELD'] <= 0:
                entity['NODE'].removeNode()
                entity['PHYSIC_NODE'].removeNode()
                defines.world.DestroyBody(entity['BODY'])
                del defines.ENTITIES[entity_id]
            elif entity['SHIELD'] > 30 and entity['SHIELD'] <= 50:
                break_asteroid(self, entity_id)
                entity['NODE'].removeNode()
                entity['PHYSIC_NODE'].removeNode()
                defines.world.DestroyBody(entity['BODY'])
                del defines.ENTITIES[entity_id]

        if entity['CATEGORY'] == 'ship':
            if entity['SHIELD'] <= 0:
                entity['NODE'].removeNode()
                entity['PHYSIC_NODE'].removeNode()
                defines.world.DestroyBody(entity['BODY'])
                del defines.ENTITIES[entity_id]
                player_win(self, "ship")

        if entity['CATEGORY'] == 'ship2':
            if entity['SHIELD'] <= 0:
                entity['NODE'].removeNode()
                entity['PHYSIC_NODE'].removeNode()
                defines.world.DestroyBody(entity['BODY'])
                if entity['E_FIELD_ENABLED'] == True:
                    defines.world.DestroyBody(entity['E_FIELD_BODY'])
                    entity['E_FIELD_DEBUG_NODE'].removeNode()
                    entity['E_FIELD_NODE'].removeNode()
                del defines.ENTITIES[entity_id]
                player_win(self, "ship2")




                
