import json


def loadModel(jsonModel):
    try:
        return json.loads(jsonModel)
    except Exception as e:
        print(e)

    return jsonModel

class JSONSerializator:

    def serialize(self, jsonModel, ignoreProperties=True):
        model = loadModel(jsonModel)
        for key in model.keys():
            if ignoreProperties:
                setattr(self, key, model.get(key))
            else:
                if hasattr(self, key):
                    setattr(self, key, model.get(key))

        return self

    def dumpModel(self):
        return json.dumps(self.__dict__, indent=4)


    def __repr__(self):
        return str(self.__dict__)

