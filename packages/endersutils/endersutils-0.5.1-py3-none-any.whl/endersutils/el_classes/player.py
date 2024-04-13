import math
from .gameobjects import GameObject

class Player:
    def __init__(self, x, y, z, facing, fov):
        """
        The player to act certain functions on
        :param x: The x position of the player
        :param y: The x position of the player
        :param z: The x position of the player
        :param facing: The direction the player is facing
        :param fov: The feild of veiw of the player
        """
        self.x = x
        self.y = y
        self.z = z
        self.facing = facing
        self.fov = fov

    def isColliding(self, obj: GameObject):
        """
        Tests if the player is colliding with an object
        :param obj: The object to test
        :return: Returns true if collision is true
        """
        objData = obj.formatData()
        objScale = obj.getScale()
        isColliding: bool = False
        if obj.getCollider() and obj.getActive():
            for i in range(3):
                objScale[i] = objScale[i] / 2
            if obj.x - objScale[0] <= self.x <= obj.x + objScale[0]:
                if obj.y - objScale[1] <= self.y <= obj.y + objScale[1]:
                    if obj.z - objScale[2] <= self.z <= obj.z + objScale[2]:
                        isColliding = True
        return isColliding

    def canSee(self, obj: GameObject):
        """
        Tests if the player can see an object. It also checks this using math.atan2(y, x), the most underrated and also best function in python.
        :param obj: The object to test
        :return: Returns true if player can see the object
        """
        if not obj.getInvis() and obj.getActive():
            if self.isColliding(obj):
                return True  # If they're in the block, they can probably see it

            x = obj.x - self.x
            y = obj.x - self.x

            t = math.atan2(y, x)  # BEST FUNCTION IN PYTHON

            t = t * (180 / math.pi)
            if t < 0:
                t = 360 + t

            halfFOV = self.fov / 2

            if self.facing - halfFOV <= t <= self.facing + halfFOV and self.z - halfFOV <= obj.z <= self.z + halfFOV:
                return True
            return False

    def move(self, d: float):
        """
        Moves d units in the players direction, uses cool trig ;)
        :param d: The distance to move
        """
        o = self.facing * (math.pi / 180)
        x = d * math.cos(o)
        y = d * math.sin(o)
        self.x = self.x + round(x, 2)
        self.y = self.y + round(y, 2)

    def turn(self, deg: float):
        """
        Changes the direction of the player in degrees(even though radians are superior)
        :param deg: The degrees to turn
        """
        if deg > 360:
            raise ValueError("Turning degrees cannot be over 360!")
        f = self.facing + deg
        if f > 360:
            f = f - 360
        if f < 0:
            f = f + 360
        self.facing = f