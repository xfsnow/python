from datetime import datetime
import json
import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    dt = datetime.now()
    timeNow = dt.strftime('%Y-%m-%d, %H:%M:%S')
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    if name:
        message = 'Hello, '+name+'! Welcome to Azure Function!'
    else:
        message = 'Missing name parameter.'
    output = json.dumps({
        'message': message,
        'timestamp': timeNow
    })
    return func.HttpResponse(output)
