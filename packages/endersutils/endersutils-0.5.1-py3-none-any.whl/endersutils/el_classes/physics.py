import json
from ..el_funcs.getobjectsbyclass import getObjectByClass
import random

class Physics:
    def __init__(self, x: float, y: float, z: float, g: float, b: float, bl: int, s: float, st: float, gr: float, m: float):
        """
        Defines a physics object that will move and change based on physics updates
        :param x: The starting x of the object
        :param y: The starting y of the object
        :param z: The starting z of the object
        :param g: The gravity of the object
        :param b: The bounciness of the object
        :param bl: The loss of bounciness per bounce, random from `bl to 3bl
        :param s: The chance of the object breaking on impact
        :param st: The z value required to shatter, will not shatter if the distance from the original z to the ground
        :param gr: The z level of the ground
        :param m: The mass of the object
        """
        self.x = x
        self.y = y
        self.z = z
        self.g = g * 9.87  # count of earths gravity, g is a constant of earths gravity
        self.b = b * 9.87  # proportionalise b to match g
        self.bl = bl * 9.87  # same with bl
        self.s = s
        self.st = st
        self.gr = gr
        self.m = m
        self.a = 0

def updatePhysics():
    global pLastFrame
    pLastFrame = []
    physics = getObjectByClass(Physics)
    delp = True

    for p in physics:
        sz = p.z
        if p.gr != p.z:
            p.a = p.a + p.g * abs(((p.m * p.g) / (p.z - p.gr) ** 2))
            p.z = p.z - p.g - p.a
            if p.z < p.gr:
                p.z = p.gr
            p.g = round(p.g, 3)
            p.b = round(p.b, 3)
            p.z = round(p.z, 3)
        else:
            p.a = 0
            shatter = round(random.random(), 2)
            if shatter < p.s / 100 and sz - p.gr >= p.st:
                delp = False
                print(f"[GOOFPY PHYSICS]: Object shattered - {p}")

            if p.b > p.g and delp:
                p.z += p.b - p.g
                p.g = round(p.g, 3)
                p.b = round(p.b, 3)
                p.z = round(p.z, 3)
                l = int(p.bl)
                try:
                    p.b -= round(random.randrange(l, l * 3), 3)
                except ValueError:
                    raise TypeError("Bounce loss must be an integer")
                if p.b < 0:
                    p.b = 0
            else:
                p.b = 0
        p.g = round(p.g, 3)
        p.b = round(p.b, 3)
        p.z = round(p.z, 3) # Prevents precision loss
        pLastFrame = [p.b, p.g, p.z]
        if not delp:
            del p
def savePhysicsToJson(data: list):
    jsond = "[{"
    for i in range(len(data)):
        jsond = jsond + data[i]
        if i != len(data) - 1:
            jsond = jsond + "},{"
    jsond = jsond + "}]"
    f = open("physicsJSON.json", "w")
    jsond.replace('\\\"', '"')
    f.write(jsond)
    f.close()