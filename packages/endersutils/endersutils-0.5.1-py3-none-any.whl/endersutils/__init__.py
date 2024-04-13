from .el_funcs import getallindir, getobjectsbyclass
from .el_globs import globs
from .el_classes import component, game, gameobjects, physics, player
from urllib.request import urlopen
import json

url = urlopen("https://raw.githubusercontent.com/endert1099/EndersUtils/main/versions.json")
versions = json.loads(url.read())

class EndersUtils():
    def getVersion():
        return globs.LIBVERSION
    def getNumVersion():
        return globs.LIBNUMVERSION
    def __init__(self):
        self.components = component.Components
        self.game = game.Game
        self.getAllInDir = getallindir.getFilesInDir
        self.getObjectsByClass = getobjectsbyclass.getObjectByClass
        self.gameobjects = gameobjects.GameObject
        self.physics = physics.Physics
        self.player = player.Player

# The main class used, although other instances can be made!
eu = EndersUtils()

if eu.intversion not in versions:
    raise ImportError(f"EndersUtils - Version {eu.getNumVersion()} is not up to date! Please use any of the following versions: {versions}")
