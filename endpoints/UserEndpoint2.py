from flask import Blueprint, request, jsonify, Response
#from service.UserService import UserService
import json


users = Blueprint('users', __name__)

#userService = UserService()


@users.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return jsonify("OK GET")
    elif request.method == 'POST':
        print(request.json)
        return jsonify(request.json)


@users.route("/test-params/<int:id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def testParams(id):
    print(request.headers)
    token = request.headers["token"]
    if (token == "qwertz12345"):
        if request.method == 'GET':
            print(f"Dohvati kontakt po id-u: {id}")

        elif request.method == 'PUT':
            print(request.args)

        return jsonify("OK")
    else:
        response = {
            "Data": "Unauthorized"
        }
        return Response(json.dumps(response), status=401)

# @POST localhost:5555/users/ -> createUser
# @GET localhost:5555/users/ -> get all users

class UserEndpoint:

    @staticmethod
    @users.route("/", methods=['POST'])
    def createUser():
        userData = userService.createUser(request.json)
        if userData is not None:
            return json.dumps(userData)
        else:
            resp = {
                "message": "Something went wrong."
            }
            return Response(json.dumps(resp), status=500)


    @staticmethod
    @users.route("/", methods=['GET'])
    def getAllUsers():
        return json.dumps(userService.getAllUsers())


    @staticmethod
    @users.route("/<int:id>", methods=['GET'])
    def getUserById(id):
        userDto = userService.getUserById(id)
        if userDto is not None:
            return json.dumps(userDto)
        else:
            resp = {
                "message": f"User with ID:{id} not found."
            }
            return Response(json.dumps(resp), status=404)


    @staticmethod
    @users.route("/<int:id>", methods=['DELETE'])
    def deleteUserById(id):
        result = userService.deleteUserById(id)
        if result:
            message = "User successfully deleted"
            code = 204
        else:
            message = f"User with ID: {id} not found."
            code = 404

        resp = {
            "message": message
        }
        return Response(json.dumps(resp), status=code)


    @staticmethod
    @users.route("/<int:id>", methods=['PUT'])
    def updateUser(id):
        # provjera i dohvat tokena iz headera
        updated, userData = userService.updateUser(request.json, id, token)
        if userData is not None:
            if not updated:
                return Response(json.dumps(userData), status=304)
            else:
                return json.dumps(userData)
        else:
            resp = {
                "message": f"User with ID: {id} not found."
            }
            return Response(json.dumps(resp), status=404)


    # POST endpoint - login()
    """
    body = {
        "username": "----",
        "password": "-----"
    }
    
    response ako je login OK - 
    {
        "token": "asdofiuasd98f7as8d7f6a"
    }
    
    zanemarite expiresAt
    """
