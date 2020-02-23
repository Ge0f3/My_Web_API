from flask import render_template,jsonify,request,Flask
import connexion
from flask_cors import CORS,cross_origin

# Create the application instance
app = Flask(__name__)
app = connexion.App(__name__, specification_dir="./")

# read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

# Cross Origin Server
# CORS(app, resources={r"/*": {"origins": "*"}}) 

# Create a URL route in our application for "/"
@app.route('/')
def home():
	"""
	This function just responds to the browser ULR
	localhost:5000/

	:return:        the rendered template 'home.html'
	"""
	return jsonify({'result':"hello world"})

@app.route('/predict_mpg',methods=['GET','POST'])
def predict_mpg():
	if request.method   == 'POST':
		app.logger.info("The post method")
		try:
			form_data = request.get_json()
			app.logger.info(form_data)
			
			app.logger.info("The form data is {}\nThe Type of form-data is {}".format(form_data,type(form_data)))
			return jsonify({'res':"Form data recieved"})
		except:
			return jsonify({'res':"Form data Error"})
	else:
		app.logger.info("Not a post method")
		return jsonify({'res':'Method Not allowed - Not a post method'})
	



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
