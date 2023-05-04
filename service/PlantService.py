from datasource.dto.PlantDto import PlantDto
from datasource.entity.Plant import Plant
from UserManagementApp import db
from utils.DBUtils import DBUtils
import uuid


class PlantService:

    def __init__(self):
        pass

    def createPlant(self, plantData):
        print(plantData)
        plantDto = PlantDto().serialize(plantData, ignoreProperties=False)
        print(plantDto)
        plant = Plant.createPlantFromDto(plantDto)
        plant = DBUtils.insert(plant)
        if plant is not None:
            newPantDto = PlantDto.createFromEntity(plant)
            # userType = userTypeService.getUserTypeByType(1)
            # newUserDto.userType = userType.name
            return newPantDto.getJson()

        return None


    def getAllPlants(self):
        plantDtoList = []
        plants = DBUtils.findAll(Plant)
        for p in plants:
            plantDtoList.append(PlantDto.createFromEntity(p).getJson())
        return plantDtoList

    def getAllPlantNames(self):
        plantDtoList = []
        plants = DBUtils.findAll(Plant)
        for p in plants:
            plantDtoList.append(PlantDto.createFromEntity(p).username)
        return plantDtoList


    def getPlantById(self, id):
        plant = DBUtils.findById(Plant, id)
        if plant is not None:
            return PlantDto.createFromEntity(plant).getJson()

        return None

    def getPlantByName(self, name):
        plant = Plant.query.filter_by(name=name).first()
        if plant is not None:
            return PlantDto.createFromEntity(plant).getJson()

        return None

    def deletePlantById(self, id):
        return DBUtils.deleteById(Plant, id)

    def deletePlantByName(self, name):
        return DBUtils.deleteByName(Plant, name)


    def updateUser(self, userData, id):
        plantDto: PlantDto = PlantDto().serialize(userData, ignoreProperties=False)
        plant: Plant = DBUtils.findById(Plant, id)
        # dohvatite token po value-u
        # provjerite toke.user_id == id

        updated = False
        if plant is not None:
            if PlantDto.name is not None and plant.name != PlantDto.name:
                plant.name = PlantDto.name
                updated = True

            if PlantDto.pwd is not None and plant.pwd != PlantDto.pwd:
                plant.pwd = PlantDto.pwd
                updated = True

            if updated:
                DBUtils.commit()
                newPlantDto = PlantDto.createFromEntity(plant)
                return updated, newPlantDto.getJson()

            return updated, PlantDto.createFromEntity(plant).getJson()

        return False, None


