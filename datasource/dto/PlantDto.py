from utils.JSONSerializator import JSONSerializator


class PlantDto(JSONSerializator):

    def __init__(self):
        self.id = None
        self.name = None
        self.photoURL = None
        self.humidityValue = None
        self.tempValue = None
        self.lightValue = None

    @staticmethod
    def createFromEntity(e):
        dto = PlantDto()
        dto.id = e.id
        dto.name = e.name
        dto.photoURL = e.photoURL
        dto.humidityValue = e.humidityValue
        dto.tempValue = e.tempValue
        dto.lightValue = e.lightValue
        return dto

    def getJson(self):
        model = {
            "id": self.id,
            "name": self.name,
            "photoURL": self.photoURL,
            "humidityValue": self.humidityValue,
            "tempValue": self.tempValue,
            "lightValue": self.lightValue
        }
        return model
