class Validation():

    """
    Check for the empty data since DynamoDB has problem with it,
    and also check for any extra fields
    """
    @staticmethod
    def validate(keys, data):
        messages = dict()
        for k in data.keys():
            if k not in keys:
                messages[k] = 'Unknown parameter'

            if not data[k]:
                messages[k] = 'Empty parameter'

        return messages


    @staticmethod
    def create_response(error='', status_code=None, messages='', response=''):
        response = {
            'error': error,
            'statusCode': status_code,
            'message': messages,
            'response': response
        }
        return response
