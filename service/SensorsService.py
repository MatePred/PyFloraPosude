import random


class SensorsPyPosuda:
    def __init__(self, name):
        self.imePyPosude = name

        self.tempData = []
        self.humidityData = []
        self.lightData = []

        # initialize data in order to have at least one value
        self.readValues()

    #gets new reading from the sensors and stores it in the list
    def readValues(self):
        temp = random.random() * 20 + 10  # [10-30]
        self.tempData.append(temp)

        humidity = random.random() * 50 + 50  # [50-100]
        self.humidityData.append(humidity)

        light = random.random() * 200 + 100  # [100-300]
        self.lightData.append(light)


class SensorsService:

    def __init__(self):
        self.lista: [SensorsPyPosuda] = []

    def AddToList(self, obj: SensorsPyPosuda):
        self.lista.append(obj)

    def RemoveFromList(self, obj: SensorsPyPosuda):
        self.lista.remove(self, obj)

    #reads new values of all sensors in a list of PyPosuda
    def SynchronizeAll(self):
        for sp in self.lista:
            sp.readValues()

    def getSensorsPyPosudaByName(self, name):
        for p in self.lista:
            if name == p.imePyPosude:
                return p

        return None
