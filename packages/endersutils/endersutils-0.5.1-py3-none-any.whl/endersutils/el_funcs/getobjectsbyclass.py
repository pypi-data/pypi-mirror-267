import gc

def getObjectByClass(c):
    """
    Gets all the objects in a certain class
    :param c: The class to take the objects from
    :return: Returns an array of all instances of `c` class
    """
    objs = []
    for obj in gc.get_objects():
        if isinstance(obj, c):
            objs.append(obj)
    return objs