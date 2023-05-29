from datasource.dto.PlantDto import PlantDto
from datasource.entity.Plant import Plant
from utils.DBUtils import DBUtils
from datasource.dto.PyFloraPosudaDto import PyFloraPosudaDto
from datasource.entity.PyFloraPosuda import PyFloraPosuda


class PyFloraPosudeService:

    def __init__(self):
        pass

    def createPyPosuda(self, pyPosudaData):
        print(pyPosudaData)
        pyFloraPosudaDto = PyFloraPosudaDto().serialize(pyPosudaData, ignoreProperties=False)
        print(pyFloraPosudaDto)
        posuda = PyFloraPosuda.createPyPosudaFromDto(pyFloraPosudaDto)
        posuda = DBUtils.insert(posuda)
        if posuda is not None:
            newPosudaDto = PyFloraPosudaDto.createFromEntity(posuda)
            # userType = userTypeService.getUserTypeByType(1)
            # newUserDto.userType = userType.name
            return newPosudaDto.getJson()

        return None

    #radi
    def getAllPyPosuda(self):
        pyPosudaDtoList = []
        pyFloraPosuda = DBUtils.findAll(PyFloraPosuda)
        for p in pyFloraPosuda:
            pyPosudaDtoList.append(PyFloraPosudaDto.createFromEntity(p).getJson())
        return pyPosudaDtoList

    def getAllPyPosuda2(self):
        pyFloraPosuda = DBUtils.findAll(PyFloraPosuda)
        return pyFloraPosuda

    def getAllPyPosudeNames(self):
        pyPosudeDtoList = []
        pyPosude = DBUtils.findAll(PyFloraPosuda)
        for p in pyPosude:
            pyPosudeDtoList.append(PyFloraPosudaDto.createFromEntity(p).name)
        return pyPosudeDtoList


    def getPyPosudaById(self, id):
        pyFloraPosuda = DBUtils.findById(PyFloraPosuda, id)
        if pyFloraPosuda is not None:
            return PyFloraPosudaDto.createFromEntity(pyFloraPosuda).getJson()

        return None

    def getPyPosudaByName(self, name):
        pyPosuda = PyFloraPosuda.query.filter_by(name=name).first()
        if pyPosuda is not None:
            return PyFloraPosudaDto.createFromEntity(pyPosuda).getJson()

        return None

    def deletePlantById(self, id):
        return DBUtils.deleteById(Plant, id)

    def deletePlantByName(self, name):
        return DBUtils.deleteByName(Plant, name)

    def updatePlant(self, userData, id):
        plantDto: PlantDto = PlantDto().serialize(userData, ignoreProperties=False)
        plant: Plant = DBUtils.findById(Plant, id)

        updated = False
        if plant is not None:

            if plantDto.name is not None and plant.name != plantDto.name:
                plant.name = plantDto.name
                updated = True

            if plantDto.photoURL is not None and plant.photoURL != plantDto.photoURL:
                plant.photoURL = plantDto.photoURL
                updated = True

            if plantDto.humidityValue is not None and plant.humidityValue != plantDto.humidityValue:
                plant.humidityValue = plantDto.humidityValue
                updated = True

            if plantDto.tempValue is not None and plant.tempValue != plantDto.tempValue:
                plant.tempValue = plantDto.tempValue
                updated = True

            if plantDto.lightValue is not None and plant.lightValue != plantDto.lightValue:
                plant.lightValue = plantDto.lightValue
                updated = True

            if updated:
                DBUtils.commit()
                newPlantDto = PlantDto.createFromEntity(plant)
                return updated, newPlantDto.getJson()

            return updated, PlantDto.createFromEntity(plant).getJson()

        return False, None


