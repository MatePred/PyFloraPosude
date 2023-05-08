from UserManagementApp import db, app
from flask import Blueprint, request, jsonify, Response, flash,get_flashed_messages
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from service.PlantService import PlantService
import json
from wtforms.validators import DataRequired
from datasource.dto import PlantDto
from wtforms.widgets import TextArea

plants = Blueprint('plants', __name__)

#bcrypt = Bcrypt(app)

plantService = PlantService()

class PlantInfos(FlaskForm):
        name = "imeBiljke"
        photoURL = "photoURL"
        humidityValue = "humidityValue"
        tempValue = "tempValue"
        lightValue = "lightValue"

class ModifyPLantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Plant name"})
    photoURL = StringField('photoURL', validators=[DataRequired()], render_kw={"placeholder": "Photo URL"})
    humidityValue = StringField('humidityValue', validators=[DataRequired()], render_kw={"placeholder": "Humidity value"})
    tempValue = StringField('tempValue', validators=[DataRequired()], render_kw={"placeholder": "Temperature value"})
    lightValue = StringField('lightValue', validators=[DataRequired()], render_kw={"placeholder": "Light value"})

class PlantEndpoint:

    @staticmethod
    @plants.route('/')
    def listPlants():
        return render_template('listPlants.html')

    @staticmethod
    @plants.route('/plant', methods=['GET', 'POST'])
    def plant():
        #ID biljke dobijemo sa stranice "Plant list"
        selectedPlant = 1

        if request.method == 'POST':
            if 'SbmBtn_ModifyPlant' in request.form:
                flash(selectedPlant)
                return redirect(url_for('plants.modifyPlant'))

        infos = PlantInfos();

        #data = plantService.getAllPlants()
        #infos.name = data[0]['name']
        #infos.photoURL = data[0]['photoURL']

        plantDto = plantService.getPlantById(1)
        #plantDto = plantService.getPlantByName("kaktus")


        plantData = {
                        'name': 'suncokret',
                        'photoURL': '/'
                    }
        #plantService.createPlant(json.dumps(plantData))


        #plantService.deletePlantByName("suncokret")

        infos.name = plantDto['name']
        infos.photoURL = plantDto['photoURL']

        #print(json.dumps(data, indent=4))
        #infos.message = json.dumps(data, indent=4)
        return render_template('plant.html', infos=infos)


    @staticmethod
    @plants.route('/modify', methods=['GET', 'POST'])
    def modifyPlant():
        plant_ID = 1
        if len(get_flashed_messages()) > 0:
            plant_ID = get_flashed_messages()[0]
        else:
            plant_ID = 1
        plant_ID = 1


        #get plant from database by ID
        plantData = plantService.getPlantById(plant_ID)

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
                return redirect(url_for('plants.modifyPlant'))
                #print("Modify plant")
            if 'SbmBtn_DeletePlant' in request.form:
                print("Delete plant")
                #plantService.deletePlantById(plant_ID)
                return redirect(url_for('plants.listPlants'))

        return render_template('modifyPlant.html', plantName=plantData["name"],modifyPLantForm=modifyPLantForm)