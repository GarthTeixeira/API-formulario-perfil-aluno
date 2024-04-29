from flask import make_response

class HttpResponseUtils:
    @staticmethod
    def responseForAPIFromArrayData(arrayData):
        for data in arrayData:
            id = data.pop('_id')
            data['id'] = str(id)
    
        return make_response(arrayData)
    
    @staticmethod
    def responseForAPIFromData(data):
        id = data.pop('_id')
        data['id'] = str(id)
    
        return make_response(data)
    
    @staticmethod
    def responseForAPIFromMessage(message):
        print("MESSAGE",message)
        return make_response(message)
    
    @staticmethod
    def responseForAPIFromError(error):
        return make_response(error)
    
    @staticmethod
    def responseForAPIFromStr(str):
        return make_response(str)
    
    @staticmethod
    def reponseFromPostRequest(id):
        data= { 'id': str(id)}
        return make_response(data)