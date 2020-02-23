from services.application import create_app
from services.config import RequiredConstants
from flask_restplus import Resource, Api

import os

app = create_app()
api = Api(app)   

@api.route('/')                  
class HelloWorld(Resource):            
    def get(self):                     
        return {'hello': 'world'}

    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT_PY', '5000')))
