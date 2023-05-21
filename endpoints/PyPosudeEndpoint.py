from flask import Blueprint, request, session, render_template
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from service.PlantService import PlantService
from datasource.dto.PlantDto import PlantDto
from service.PyFloraPosudeService import PyFloraPosudeService
from datasource.entity.PyFloraPosuda import PyFloraPosuda
import json
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

pyPosude = Blueprint('pyPosude', __name__)

#bcrypt = Bcrypt(app)

plantService = PlantService()
pyPosudeService = PyFloraPosudeService()


class PyPosudaInfo():
    name = None
    status = None
    biljkaDto: PlantDto = PlantDto()


class PyPosudeEndpoint:

    @staticmethod
    @pyPosude.route('/',methods=['GET', 'POST'])
    #@login_required
    def listPyPosude():
        pyPosudeList:PyFloraPosuda = pyPosudeService.getAllPyPosuda2()


        pyPosudaInfoList = []
        for p in pyPosudeList:
            pPinfo = PyPosudaInfo()
            pPinfo.name = p.name
            pPinfo.biljkaDto = plantService.getPlantById(p.plant_id)
            pyPosudaInfoList.append(pPinfo)

        pyPosudeListNames = pyPosudeService.getAllPyPosudeNames()

        if request.method == 'POST':
            #add new pyPosuda
            if 'SbmBtn_AddPosuda' in request.form:
                return redirect(url_for('plants.createPlant'))

            #if some of the other buttons pressed
            keys = request.form.keys()
            k = next(iter(keys))
            if k in pyPosudeListNames:
                p:PlantDto = pyPosudeService.getPyPosudaByName(k)
                PyPosudeEndpoint.sharedVar = p['id']
                return redirect(url_for('plants.plant'))

            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

        # # testiranje
        # pyPosudaData = {
        #     "name": "dsads",
        #     "plant_id": 1
        # }
        #
        #
        # pyFloraPosudeService = PyFloraPosudeService()
        # pyFloraPosudeService.createPyPosuda(pyPosudaData)
        # print(pyFloraPosudeService.getAllPyPosuda())

        return render_template('PyPosudeTemplates/listPyPosude.html', pyPosudaInfoList=pyPosudaInfoList)
    #
    # @staticmethod
    # @pyPosude.route('/createPlant',methods=['GET', 'POST'])
    # @login_required
    # def createPlant():
    #     modifyPLantForm: ModifyPLantForm = ModifyPLantForm()
    #
    #     if request.method == 'POST':
    #         if 'SbmBtn_CreatePlant' in request.form:
    #             #modify plant and update db
    #             plantData = {
    #                 "name": request.form['name'],
    #                 "photoURL": request.form['photoURL'],
    #                 "humidityValue": request.form['humidityValue'],
    #                 "tempValue": request.form['tempValue'],
    #                 "lightValue": request.form['lightValue']
    #             }
    #             plantService.createPlant(json.dumps(plantData))
    #             #after plant creation get back to the plant list
    #             return redirect(url_for('plants.listPlants'))
    #
    #         if 'SbmBtn_UserProfile' in request.form:
    #             return redirect(url_for('users.modifyProfile'))
    #
    #     return render_template('PlantTemplates/createPlant.html',modifyPLantForm=modifyPLantForm,current_user=current_user.username)
    #
    # @staticmethod
    # @pyPosude.route('/plant', methods=['GET', 'POST'])
    # @login_required
    # def plant():
    #     #ID biljke dobijemo sa stranice "Plant list"
    #     # sglobal variable
    #     selectedPlant = PlantEndpoint.sharedVar
    #
    #     infos = PlantInfos();
    #
    #     plantDto = plantService.getPlantById(selectedPlant)
    #     infos.id = selectedPlant
    #     infos.name = plantDto['name']
    #     infos.photoURL = plantDto['photoURL']
    #     infos.humidityValue = plantDto['humidityValue']
    #     infos.tempValue = plantDto['tempValue']
    #     infos.lightValue = plantDto['lightValue']
    #
    #     if request.method == 'POST':
    #         if 'SbmBtn_ModifyPlant' in request.form:
    #             PlantEndpoint.selectedPlantToMod = infos.id
    #             return redirect(url_for('plants.modifyPlant'))
    #
    #         if 'SbmBtn_UserProfile' in request.form:
    #             return redirect(url_for('users.modifyProfile'))
    #
    #     return render_template('PlantTemplates/plant.html', infos=infos,current_user=current_user.username)
    #
    #
    # @staticmethod
    # @pyPosude.route('/modify', methods=['GET', 'POST'])
    # @login_required
    # def modifyPlant():
    #
    #     #sglobal variable
    #     plant_ID = PlantEndpoint.selectedPlantToMod
    #
    #     #get plant from database by ID
    #     plantData = plantService.getPlantById(int(plant_ID))
    #
    #     modifyPLantForm: ModifyPLantForm = ModifyPLantForm();
    #     modifyPLantForm.name.data = plantData["name"]
    #     modifyPLantForm.photoURL.data = plantData["photoURL"]
    #     modifyPLantForm.humidityValue.data = plantData["humidityValue"]
    #     modifyPLantForm.tempValue.data = plantData["tempValue"]
    #     modifyPLantForm.lightValue.data = plantData["lightValue"]
    #
    #     if request.method == 'POST':
    #         if 'SbmBtn_ModifyPlant' in request.form:
    #             #modify plant and update db
    #             plant_data = {
    #                 "name": request.form['name'],
    #                 "photoURL": request.form['photoURL'],
    #                 "humidityValue": request.form['humidityValue'],
    #                 "tempValue": request.form['tempValue'],
    #                 "lightValue": request.form['lightValue']
    #             }
    #             plantService.updatePlant(json.dumps(plant_data), plant_ID)
    #             return redirect(url_for('plants.listPlants'))
    #
    #         if 'SbmBtn_DeletePlant' in request.form:
    #             plantService.deletePlantById(plant_ID)
    #             return redirect(url_for('plants.listPlants'))
    #
    #         if 'SbmBtn_UserProfile' in request.form:
    #             return redirect(url_for('users.modifyProfile'))
    #
    #     return render_template('PlantTemplates/modifyPlant.html', plantName=plantData["name"],modifyPLantForm=modifyPLantForm,current_user=current_user.username)
