from UserManagementApp import db
from datasource.dto.PlantDto import PlantDto

class PyFloraPosuda(db.Model):

    __tablename__ = 'pyFloraPosuda'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'))

    @staticmethod
    def createPyPosudaFromDto(dto: PlantDto):
        pyFloraPosuda: PyFloraPosuda = PyFloraPosuda()

        pyFloraPosuda.name = dto.name
        pyFloraPosuda.plant_id = dto.plant_id

        return pyFloraPosuda



