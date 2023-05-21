from UserManagementApp import db
from datasource.dto.PlantDto import PlantDto

class Plant(db.Model):

    __tablename__ = 'plant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    photoURL = db.Column(db.String(80), nullable=False)
    humidityValue = db.Column(db.Integer, nullable=True)
    tempValue = db.Column(db.Integer, nullable=True)
    lightValue = db.Column(db.Integer, nullable=True)

    @staticmethod
    def createPlantFromDto(dto: PlantDto):
        plant: Plant = Plant()

        plant.name = dto.name
        plant.photoURL = dto.photoURL
        plant.humidityValue = dto.humidityValue
        plant.tempValue = dto.tempValue
        plant.lightValue = dto.lightValue
        return plant



