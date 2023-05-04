from UserManagementApp import db, app
from flask import Blueprint, request, jsonify, Response
from flask import Flask, render_template, url_for, redirect
from service.UserService import UserService
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from service.PlantService import PlantService
import json
from datasource.dto import PlantDto
plants = Blueprint('plants', __name__)

#bcrypt = Bcrypt(app)

plantService = PlantService()

class PlantInfos(FlaskForm):
        name = "imeBiljke"
        photoURL = "/"
        message = TextAreaField('Message')


class PlantEndpoint:

    @staticmethod
    @plants.route('/')
    def listPlants():
        return render_template('listPlants.html')

    @staticmethod
    @plants.route('/plant')
    def plant():
        #učitaj sve o biljci iz DBa
        #prenesi podatke html stranici, prikazi na ekranu
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