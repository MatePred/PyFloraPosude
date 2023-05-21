from flask_wtf import FlaskForm

class PlantInfos(FlaskForm):
    id = 0
    name = "imeBiljke"
    photoURL = "photoURL"
    humidityValue = "humidityValue"
    tempValue = "tempValue"
    lightValue = "lightValue"

    def createFromDto(self):
        pass