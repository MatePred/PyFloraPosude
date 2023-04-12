from utils.JSONSerializator import JSONSerializator

class UserDto(JSONSerializator):

    def __init__(self):
        self.id = None
        #self.name = None
        #self.surname = None
        #self.email = None
        self.username = None
        self.password = None
        self.userType = None

    @staticmethod
    def createFromEntity(e):
        dto = UserDto()
        dto.id = e.id
        #dto.name = e.name
        #dto.surname = e.surname
        #dto.email = e.email
        dto.username = e.username
        dto.password = e.pwd
        dto.userType = e.user_type
        return dto


    def getJson(self):
       model = {
           "id": self.id,
           "name": self.name,
           "surname": self.surname,
           "email": self.email,
           "username": self.username,
           "userType": self.userType
       }
       return model