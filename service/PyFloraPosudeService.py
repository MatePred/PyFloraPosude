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

    def deletePyPosudaById(self, id):
        return DBUtils.deleteById(PyFloraPosuda, id)

    def deletePyPosudaByName(self, name):
        return DBUtils.deleteByName(PyFloraPosuda, name)

    def updatePyPosuda(self, userData, id):
        pyPosudaDto: PyFloraPosudaDto = PyFloraPosudaDto().serialize(userData, ignoreProperties=False)
        pyFloraPosuda: PyFloraPosuda = DBUtils.findById(PyFloraPosuda, id)

        updated = False
        if pyFloraPosuda is not None:

            if pyPosudaDto.name is not None and pyFloraPosuda.name != pyPosudaDto.name:
                pyFloraPosuda.name = pyPosudaDto.name
                updated = True

            if pyPosudaDto.plant_id is not None and pyFloraPosuda.plant_id != pyPosudaDto.plant_id:
                pyFloraPosuda.plant_id = pyPosudaDto.plant_id
                updated = True

            if updated:
                DBUtils.commit()
                newPyPosudaDto = pyPosudaDto.createFromEntity(pyFloraPosuda)
                return updated, newPyPosudaDto.getJson()

            return updated, PlantDto.createFromEntity(pyFloraPosuda).getJson()

        return False, None


