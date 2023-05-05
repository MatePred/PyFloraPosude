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
        photoURL = TextAreaField('/')
        humidityValue = TextAreaField('Message')
        tempValue = TextAreaField('Message')
        lightValue = TextAreaField('Message')
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
        selectedPlant = "kaktus"

        if request.method == 'POST':
            if 'SbmBtn_ModifyPlant' in request.form:
                flash(selectedPlant)
                return redirect(url_for('plants.modifyPlant'))

        data = plantService.getAllPlants()
        infos = PlantInfos();

        infos.name = data[0]['name']
        infos.message = data[0]['name'] + "\n" + \
                        data[0]['photoURL']

        plantDto = plantService.getPlantById(1)
        plantDto = plantService.getPlantByName("kaktus")
        plantData = {
                        'name': 'suncokret',
                        'photoURL': '/'
                    }
        #plantService.createPlant(json.dumps(plantData))
        #plantService.deletePlantById(2)
        plantService.deletePlantByName("suncokret")
        infos.name = plantDto['name']
        infos.photoURL = plantDto['photoURL']

        print(json.dumps(data, indent=4))
        #infos.message = json.dumps(data, indent=4)
        return render_template('plant.html', infos=infos)


    @staticmethod
    @plants.route('/modify', methods=['GET', 'POST'])
    def modifyPlant():
        plant_ID = 0
        if len(get_flashed_messages()) > 0:
            plant_ID = get_flashed_messages()[0]
        #get plant from database by ID
        modifyPLantForm: ModifyPLantForm = ModifyPLantForm();
        modifyPLantForm.name.data = "Kaktus"

        if request.method == 'POST':
            if 'SbmBtn_ModifyPlant' in request.form:
                #modify plant and update db
                print("Modify plant")
            if 'SbmBtn_DeletePlant' in request.form:
                print("Delete plant")
                return redirect(url_for('plants.listPlants'))

        return render_template('modifyPlant.html', plantName=plant_ID,modifyPLantForm=modifyPLantForm)