import numpy
from flask import Blueprint, request, jsonify, render_template
from flask import Flask, render_template, url_for, redirect
from service.PlantService import PlantService
from datasource.dto.PlantDto import PlantDto
from service.PyFloraPosudeService import PyFloraPosudeService
from datasource.entity.PyFloraPosuda import PyFloraPosuda
import json
from forms.CreatePyPosudaForm import CreatePyPosudaForm
from service.SensorsService import SensorsPyPosuda, SensorsService
import numpy as np
import random
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

pyPosude = Blueprint('pyPosude', __name__)

# bcrypt = Bcrypt(app)

plantService = PlantService()
pyPosudeService = PyFloraPosudeService()
sensorsService = SensorsService()


class PyPosudaInfo():
    def __init__(self):
        self.name = None
        self.status = None
        self.biljkaDto: PlantDto = PlantDto()
        self.currTemp = None
        self.currHum = None
        self.currLight = None

    def updateSensorsValues(self, currTemp, currHum, currLight):
        self.currTemp = currTemp
        self.currHum = currHum
        self.currLight = currLight

    def updateStatus(self, currTemp, currHum, currLight):
        self.updateSensorsValues(currTemp, currHum, currLight)

        text = ""
        if self.biljkaDto is None:
            text = "nema biljke"
        else:
            if currTemp < self.biljkaDto['tempValue']:
                text = text + "Grijati \n"
            else:
                text = "Temp ok \n"
            if currLight < self.biljkaDto['lightValue']:
                text = text + "Osvijetliti \n"
            else:
                text = text + "Svijetlo ok \n"
            if currHum < self.biljkaDto['humidityValue']:
                text = text + "Zaliti"
            else:
                text = text + "Vlaga ok"

        self.status = text



class PyPosudeEndpoint:
    showAllPosude = False
    SbmBtn_ListAllPosudaState = "+"

    @staticmethod
    @pyPosude.route('/', methods=['GET', 'POST'])
    @login_required
    def listPyPosude():
        # variable to swith between full and empty PyPosuda list

        pyPosudeList: PyFloraPosuda = pyPosudeService.getAllPyPosuda2()

        # ucitati sve posude i stvoriti svakoj od njih senzor objekt,
        # na sync button pozivati svaku zasebno
        # MOZDA BI BILO BOLJE IMATI LOKALNU LISTU, TAKO CE SE LAKSE
        # MODIFIKACIJE PROCITATI
        # ili jednostavno nakon modifikacije izbrisati pa dodatai ponovno u listu
        for pyPosuda in pyPosudeList:
            if sensorsService.getSensorsPyPosudaByName(pyPosuda.name) is None:
                sensorsPyPosuda = SensorsPyPosuda(pyPosuda.name)
                sensorsService.AddToList(sensorsPyPosuda)

        pyPosudaInfoList = []
        for p in pyPosudeList:
            pPinfo = PyPosudaInfo()
            pPinfo.name = p.name
            pPinfo.biljkaDto = plantService.getPlantById(p.plant_id)

            tempData = sensorsService.getSensorsPyPosudaByName(p.name).tempData[:]
            humidityData = sensorsService.getSensorsPyPosudaByName(p.name).humidityData[:]
            lightData = sensorsService.getSensorsPyPosudaByName(p.name).lightData[:]
            pPinfo.updateStatus(tempData[-1], humidityData[-1], lightData[-1])

            if PyPosudeEndpoint.showAllPosude is False:
                if pPinfo.biljkaDto is not None:
                    pyPosudaInfoList.append(pPinfo)
            else:
                pyPosudaInfoList.append(pPinfo)

        pyPosudeListNames = pyPosudeService.getAllPyPosudeNames()

        if request.method == 'POST':
            # add new pyPosuda
            if 'SbmBtn_AddPosuda' in request.form:
                return redirect(url_for('pyPosude.createPyPosuda'))

            if 'SbmBtn_Sync' in request.form:
                sensorsService.SynchronizeAll()
                return redirect(url_for('pyPosude.listPyPosude'))

            if 'SbmBtn_PyPosude' in request.form:
                sensorsService.SynchronizeAll()
                return redirect(url_for('pyPosude.listPyPosude'))

            if 'SbmBtn_Biljke' in request.form:
                return redirect(url_for('plants.listPlants'))

            if 'SbmBtn_ListAllPosuda' in request.form:
                PyPosudeEndpoint.showAllPosude = not PyPosudeEndpoint.showAllPosude
                if PyPosudeEndpoint.showAllPosude:
                    PyPosudeEndpoint.SbmBtn_ListAllPosudaState = "-"
                else:
                    PyPosudeEndpoint.SbmBtn_ListAllPosudaState = "+"
                return redirect(url_for('pyPosude.listPyPosude'))

            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

            # if some of the "+" buttons in PyPosuda are pressed, go to the PyPosuda page
            keys = request.form.keys()
            k = next(iter(keys))
            if k in pyPosudeListNames:
                py = pyPosudeService.getPyPosudaByName(k)
                PyPosudeEndpoint.selectedPyPosuda = py['id']
                return redirect(url_for('pyPosude.pyPosuda'))

        return render_template('PyPosudeTemplates/listPyPosude.html', pyPosudaInfoList=pyPosudaInfoList,
                               SbmBtn_ListAllPosudaState=PyPosudeEndpoint.SbmBtn_ListAllPosudaState,
                               current_user=current_user.username)

    @staticmethod
    @pyPosude.route('/createPyPosuda', methods=['GET', 'POST'])
    @login_required
    def createPyPosuda():
        createPyPosudaForm: CreatePyPosudaForm = CreatePyPosudaForm()
        plant_names = plantService.getAllPlantNames()
        plant_names.insert(0, "None")
        createPyPosudaForm.plant_name.choices = [(plant_name, plant_name) for plant_name in plant_names]

        if request.method == 'POST':
            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

            if 'SbmBtn_PyPosude' in request.form:
                sensorsService.SynchronizeAll()
                return redirect(url_for('pyPosude.listPyPosude'))

            if 'SbmBtn_Biljke' in request.form:
                return redirect(url_for('plants.listPlants'))

            if 'SbmBtn_CreatePyPosuda' in request.form:
                # create PyPosuda and update db
                selected_plant_name = createPyPosudaForm.plant_name.data
                data = plantService.getPlantByName(selected_plant_name)
                # dumps the json object into an element
                json_str = json.dumps(data)
                # load the json to a string
                resp = json.loads(json_str)
                selected_plant_id = resp['id']

                pyPosudaData = {
                    "name": request.form['name'],
                    "plant_id": selected_plant_id
                }

                # write to DB
                pyPosudeService.createPyPosuda(pyPosudaData)

                return redirect(url_for('pyPosude.listPyPosude'))

        return render_template('PyPosudeTemplates/createPyPosuda.html', createPyPosudaForm=createPyPosudaForm,
                               current_user=current_user.username)

    @staticmethod
    @pyPosude.route('/pyPosuda', methods=['GET', 'POST'])
    @login_required
    def pyPosuda():
        # ID pyPosude dobijemo sa stranice "PyPosuda list"
        # sglobal variable
        selectedPyPosuda = PyPosudeEndpoint.selectedPyPosuda

        infos = PyPosudaInfo()
        pyPosudaDto = pyPosudeService.getPyPosudaById(selectedPyPosuda)
        plantDto = plantService.getPlantById(pyPosudaDto['plant_id'])

        infos.name = pyPosudaDto['name']
        # infos.status = plantDto['id']
        infos.biljkaDto: PlantDto = plantDto

        tempData = sensorsService.getSensorsPyPosudaByName(infos.name).tempData[:]
        humidityData = sensorsService.getSensorsPyPosudaByName(infos.name).humidityData[:]
        lightData = sensorsService.getSensorsPyPosudaByName(infos.name).lightData[:]

        infos.currTemp = tempData[-1]
        infos.currHum = humidityData[-1]
        infos.currLight = lightData[-1]



        lightPieChart = create_pie_chart_data(lightData, infos.biljkaDto['lightValue'], 'Svijetlo')
        lightPieChart_json = json.dumps(lightPieChart)

        tempPieChart = create_pie_chart_data(tempData, infos.biljkaDto['tempValue'], 'Temperatura')
        tempPieChart_json = json.dumps(tempPieChart)

        humPieChart = create_pie_chart_data(humidityData, infos.biljkaDto['humidityValue'], 'Vlažnost')
        humPieChart_json = json.dumps(humPieChart)

        chart_data = create_chart_data(tempData, lightData, humidityData,infos.biljkaDto['tempValue'],infos.biljkaDto['lightValue'],infos.biljkaDto['humidityValue'])
        chart_data_json = json.dumps(chart_data)

        maxVal = numpy.ceil(max(max(tempData),max(humidityData),max(lightData)))
        histogramChartData = createHistogramData(0,maxVal,2,tempData, lightData, humidityData,infos.biljkaDto['tempValue'],infos.biljkaDto['lightValue'],infos.biljkaDto['humidityValue'])
        histogramChartData_json = json.dumps(histogramChartData)





        if request.method == 'POST':
            if 'SbmBtn_PyPosude' in request.form:
                sensorsService.SynchronizeAll()
                return redirect(url_for('pyPosude.listPyPosude'))

            if 'SbmBtn_Sync' in request.form:
                sensorsService.SynchronizeAll()
                return redirect(url_for('pyPosude.pyPosuda'))

            if 'SbmBtn_Biljke' in request.form:
                return redirect(url_for('plants.listPlants'))

            if 'SbmBtn_ModifyPlant' in request.form:
                PyPosudeEndpoint.selectedPlantToMod = infos.id
                return redirect(url_for('plants.modifyPlant'))

            if 'SbmBtn_UserProfile' in request.form:
                return redirect(url_for('users.modifyProfile'))

        return render_template('PyPosudeTemplates/pyPosuda.html', infos=infos, current_user=current_user.username, chart_data=chart_data_json,
                               histogramChartData_json=histogramChartData_json, tempPieChart_json=tempPieChart_json,lightPieChart_json=lightPieChart_json,
                               humPieChart_json=humPieChart_json)


def create_chart_data(tempData,lightData,humData, tempThresh,lightTresh,humTresh):

    label = list(range(1, len(tempData)+1))
    humDataTresh = [humTresh] * len(humData)
    tempDataTresh = [tempThresh] * len(tempData)
    lightDataTresh = [lightTresh] * len(lightData)

    # Prepare the datasets as a dictionary
    chart_data = {
        'labels': label,
        'datasets': [
            {'label': 'Temperatura', 'data': tempData, 'borderColor': 'red', 'fill': False,'tension': 0.3},
            {'label': 'T_Threshold', 'data': tempDataTresh, 'borderColor': 'red', 'fill': False},
            {'label': 'Svijetlost', 'data': lightData, 'borderColor': 'blue', 'fill': False,'tension': 0.3},
            {'label': 'S_Threshold', 'data': lightDataTresh, 'borderColor': 'blue', 'fill': False},
            {'label': 'Vlažnost', 'data': humData, 'borderColor': 'green', 'fill': False,'tension': 0.3},
            {'label': 'V_Threshold', 'data': humDataTresh, 'borderColor': 'green', 'fill': False}
        ]
    }
    return chart_data

def createHistogramData(start_value, end_value, step_size, tempData,lightData, humData ,tempThresh,lightTresh,humTresh):

    maxData = max(len(humData),len(tempData),len(lightData))
    humDataTresh = [humTresh] * maxData
    tempDataTresh = [tempThresh] * maxData
    lightDataTresh = [lightTresh] * maxData
    datasets = [tempData,tempDataTresh, humData,humDataTresh, lightData,lightDataTresh]

    # Calculate the bin edges for the histogram
    bins = np.arange(start_value, end_value + step_size, step_size)

    # Create the histograms for each dataset
    histograms = []
    for dataset in datasets:
        hist, _ = np.histogram(dataset, bins=bins)
        histograms.append(hist.tolist())

    # Prepare the data for the histogram chart
    labels = [f'{bins[i]}-{bins[i + 1]}' for i in range(len(bins) - 1)]

    histogram_data = {
        'labels': labels,
        'datasets': [
            {'label': 'Temperatura', 'data': histograms[0],'backgroundColor': 'red'},
            {'label': 'T_Threshold', 'data': histograms[1],'backgroundColor': 'red'},
            {'label': 'Svijetlost', 'data': histograms[4], 'backgroundColor': 'blue'},
            {'label': 'S_Threshold', 'data': histograms[5], 'backgroundColor': 'blue'},
            {'label': 'Vlažnost', 'data': histograms[2], 'backgroundColor': 'green'},
            {'label': 'V_Threshold', 'data': histograms[3], 'backgroundColor': 'green'}
        ]
    }

    return histogram_data


#create Bar chart to represent average value, compared to the threshold.
def create_pie_chart_data(data,dataThresh, label):

    labels = ['Samples bellow threshold', 'Samples above threshold']
    countBlwThresh = 0
    countAbvThresh = 0
    for i in data:
        if i < dataThresh:
            countBlwThresh +=1
        else:
            countAbvThresh +=1

    sendData = [countBlwThresh, countAbvThresh]

    # Prepare the datasets as a dictionary
    chart_data = {
        'labels': labels,
        'datasets': [
            {
                'data': sendData,
                'backgroundColor': ['red', 'green'],
                'label': label
            }
        ]
    }
    return chart_data

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
