from UserManagementApp import app
from service.InitializeService import InitializeService

if __name__ == '__main__':
    InitializeService()
    app.run(host="0.0.0.0", port=5555)
