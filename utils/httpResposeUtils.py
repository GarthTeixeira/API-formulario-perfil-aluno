from flask import make_response

class HttpResponseUtils:
    @staticmethod
    def responseForAPIFromArrayData(arrayData):
        for data in arrayData:
            id = data.pop('_id')
            data['id'] = str(id)
    
        return make_response(arrayData)