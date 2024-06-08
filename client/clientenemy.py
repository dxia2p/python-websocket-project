import clientcamera

class ClientEnemy:
    enemies = {}

    @classmethod
    def destroy_at_id(cls, id):
        cls.enemies.pop(id)

    def __init__(self, id, pos) -> None:
        self.id = id
        self.pos = pos
        ClientEnemy.enemies[id] = self

    @classmethod
    def draw_all(cls):
        """Call this every frame to draw all the enemies"""
        for enemy_id in cls.enemies:
            enemy = cls.enemies[enemy_id]
            clientcamera.Camera.draw_circle(enemy.pos, 20, "red")