from flask import make_response, jsonify

class HttpResponseUtils:
    @staticmethod
    def responseForAPIFromArrayData(arrayData):
        for data in arrayData:
            if '_id' in data:
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
    
    def responseFromPutRequest(result):
        
        if result.modified_count == 0:
        # No document was updated
            return jsonify({'success': False, 'message': 'No document found or no new data to update.'}), 404
        else:
            # Document was successfully updated
            return jsonify({'success': True, 'message': 'Document updated successfully.'}), 200
