import clientcamera

class ClientEnemy:
    enemies = []
    def __init__(self, id, pos) -> None:
        self.id = id
        self.pos = pos
        ClientEnemy.enemies.append(self)

    @classmethod
    def draw_all(cls):
        """Call this every frame to draw all the enemies"""
        for enemy in cls.enemies:
            clientcamera.Camera.draw_circle(enemy.pos, 15, "red")