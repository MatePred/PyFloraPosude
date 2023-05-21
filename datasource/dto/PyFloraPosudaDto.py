from utils.JSONSerializator import JSONSerializator


class PyFloraPosudaDto(JSONSerializator):

    def __init__(self):
        self.id = None
        self.name = None
        self.plant_id = None

    @staticmethod
    def createFromEntity(e):
        dto = PyFloraPosudaDto()
        dto.id = e.id
        dto.name = e.name
        dto.plant_id = e.plant_id

        return dto

    def getJson(self):
        model = {
            "id": self.id,
            "name": self.name,
            "plant_id": self.plant_id,
        }
        return model
