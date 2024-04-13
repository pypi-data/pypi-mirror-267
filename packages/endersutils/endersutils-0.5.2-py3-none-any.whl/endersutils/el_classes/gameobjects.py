class GameObject:
    def __init__(self, gid, x, y, z, data, gtype, zIndex=0):
        """
        GameObjects to be used in games
        :param gid: The ID of the object
        :param x: The x position of the new object
        :param y: The y position of the new object
        :param z: The z position of the new object
        :param data: The data to be sent to the object, see the GameObject.formatData documentation for more info
        :param gtype: The type of the object, 2D or 3D
        :param zIndex: Optional, the Z index instead of 2D objects
        """
        self.gid = gid
        self.x = x
        self.y = y
        self.z = z
        self.data = data
        self.gtype = gtype
        self.zIndex = zIndex

    def formatData(self):
        """
        Formats data in this order:
        ['scalex', val, 'scaley', val, 'scalez', val, 'collider', val, 'isActive', val, 'isInvis', val].
        Data should be an array with the above syntax, all of those 6 values in any order, but following a ['var', val] structure.
        Also filters out any incorrect values.
        Might break if one of the 6 is missing.
        :return: Returns the formatted list
        """
        nextc = 0
        data = []
        for i in self.data:
            if nextc > 0:
                data.insert(nextc - 1, i)
                nextc = 0

            if i == "scalex":
                nextc = 1
            elif i == "scaley":
                nextc = 2
            elif i == "scalez":
                nextc = 3
            elif i == "collider":
                nextc = 4
            elif i == "isActive":
                nextc = 5
            elif i == "isInvis":
                nextc = 6
        return data

    def getScale(self):
        """
        Gets the scale of the current object, x, y, and z, in that order
        :return: The x, y, and z scale, in an array
        """
        data = self.formatData()
        return data[0:3]

    def getCollider(self):
        """
        Gets whether the current object is a collider.
        :return: Returns if it is a collider
        """
        data = self.formatData()
        return data[3]

    def getActive(self):
        """
            Gets whether the current object is active.
            :return: Returns if it is active
        """
        data = self.formatData()
        return data[4]

    def getInvis(self):
        """
            Gets whether the current object is invisible.
            :return: Returns if it is invisible
        """
        data = self.formatData()
        return data[5]


# External functions that relate to GameObjects
def readFormattedData(data: list, valueID):
    """
    Gets formatted data and reads a value
    Useless lmao
    :param data: The formatted data
    :param valueID: The ID of the value
    :return: The proper value
    """
    return data[valueID - 1]