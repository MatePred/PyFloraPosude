from utils.JSONSerializator import JSONSerializator

class UserDto(JSONSerializator):

    def __init__(self):
        self.id = None
        #self.name = None
        #self.surname = None
        #self.email = None
        self.username = None
        self.pwd = None
        self.userType = None

    @staticmethod
    def createFromEntity(e):
        dto = UserDto()
        dto.id = e.id
        #dto.name = e.name
        #dto.surname = e.surname
        #dto.email = e.email
        dto.username = e.username
        dto.pwd = e.pwd
        dto.userType = e.user_type
        return dto


    def getJson(self):
       model = {
           "id": self.id,
           "username": self.username,
           "pwd": self.pwd,
           "userType": self.userType
       }
       return model