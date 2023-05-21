from flask import Blueprint, request, session, render_template
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from service.PlantService import PlantService
from datasource.dto.PlantDto import PlantDto
from service.PyFloraPosudeService import PyFloraPosudeService
import json
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

plants = Blueprint('plants', __name__)

#bcrypt = Bcrypt(app)

plantService = PlantService()

class PlantInfos(FlaskForm):
        id = 0
        name = "imeBiljke"
        photoURL = "photoURL"
        humidityValue = "humidityValue"
        tempValue = "tempValue"
        lightValue = "lightValue"

        def createFromDto(self):
            pass

class ModifyPLantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Plant name"})
    photoURL = StringField('photoURL', validators=[DataRequired()], render_kw={"placeholder": "Photo URL"})
    humidityValue = StringField('humidityValue', validators=[DataRequired()], render_kw={"placeholder": "Humidity value"})
    tempValue = StringField('tempValue', validators=[DataRequired()], render_kw={"placeholder": "Temperature value"})
    lightValue = StringField('lightValue', validators=[DataRequired()], render_kw={"placeholder": "Light value"})


class PlantEndpoint:

    @staticmethod
    @plants.route('/',methods=['GET', 'POST'])
    @login_required
    def listPlants():
        plantsList = plantService.getAllPlants2()
        plantsListNames = plantService.getAllPlantNames()
        if request.method == 'POST':
            if 'SbmBtn_AddPlant' in request.form:
                return redirect(url_for('plants.createPlant'))

            #if some of the other buttons pressed
            keys = request.form.keys()
            k = next(iter(keys))
            if k in plantsListNames:
                p:PlantDto = plantService.getPlantByName(k)
                PlantEndpoint.sharedVar = p['id']
                return redirect(url_for('plants.plant'))

            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

        pyPosudaData = {
            "name": "dsads",
            "plant_id": 1
        }

        #testiranje
        pyFloraPosudeService = PyFloraPosudeService()
        pyFloraPosudeService.createPyPosuda(pyPosudaData)
        print(pyFloraPosudeService.getAllPyPosuda())

        return render_template('PlantTemplates/listPlants.html', plantsList=plantsList,current_user=current_user.username)

    @staticmethod
    @plants.route('/createPlant',methods=['GET', 'POST'])
    @login_required
    def createPlant():
        modifyPLantForm: ModifyPLantForm = ModifyPLantForm()

        if request.method == 'POST':
            if 'SbmBtn_CreatePlant' in request.form:
                #modify plant and update db
                plantData = {
                    "name": request.form['name'],
                    "photoURL": request.form['photoURL'],
                    "humidityValue": request.form['humidityValue'],
                    "tempValue": request.form['tempValue'],
                    "lightValue": request.form['lightValue']
                }
                plantService.createPlant(json.dumps(plantData))
                #after plant creation get back to the plant list
                return redirect(url_for('plants.listPlants'))

            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

        return render_template('PlantTemplates/createPlant.html',modifyPLantForm=modifyPLantForm,current_user=current_user.username)

    @staticmethod
    @plants.route('/plant', methods=['GET', 'POST'])
    @login_required
    def plant():
        #ID biljke dobijemo sa stranice "Plant list"
        # sglobal variable
        selectedPlant = PlantEndpoint.sharedVar

        infos = PlantInfos();

        plantDto = plantService.getPlantById(selectedPlant)
        infos.id = selectedPlant
        infos.name = plantDto['name']
        infos.photoURL = plantDto['photoURL']
        infos.humidityValue = plantDto['humidityValue']
        infos.tempValue = plantDto['tempValue']
        infos.lightValue = plantDto['lightValue']

        if request.method == 'POST':
            if 'SbmBtn_ModifyPlant' in request.form:
                PlantEndpoint.selectedPlantToMod = infos.id
                return redirect(url_for('plants.modifyPlant'))

            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

        return render_template('PlantTemplates/plant.html', infos=infos,current_user=current_user.username)


    @staticmethod
    @plants.route('/modify', methods=['GET', 'POST'])
    @login_required
    def modifyPlant():

        #sglobal variable
        plant_ID = PlantEndpoint.selectedPlantToMod

        #get plant from database by ID
        plantData = plantService.getPlantById(int(plant_ID))

        modifyPLantForm: ModifyPLantForm = ModifyPLantForm();
        modifyPLantForm.name.data = plantData["name"]
        modifyPLantForm.photoURL.data = plantData["photoURL"]
        modifyPLantForm.humidityValue.data = plantData["humidityValue"]
        modifyPLantForm.tempValue.data = plantData["tempValue"]
        modifyPLantForm.lightValue.data = plantData["lightValue"]

        if request.method == 'POST':
            if 'SbmBtn_ModifyPlant' in request.form:
                #modify plant and update db
                plant_data = {
                    "name": request.form['name'],
                    "photoURL": request.form['photoURL'],
                    "humidityValue": request.form['humidityValue'],
                    "tempValue": request.form['tempValue'],
                    "lightValue": request.form['lightValue']
                }
                plantService.updatePlant(json.dumps(plant_data), plant_ID)
                return redirect(url_for('plants.listPlants'))

            if 'SbmBtn_DeletePlant' in request.form:
                plantService.deletePlantById(plant_ID)
                return redirect(url_for('plants.listPlants'))

            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

        return render_template('PlantTemplates/modifyPlant.html', plantName=plantData["name"],modifyPLantForm=modifyPLantForm,current_user=current_user.username)
