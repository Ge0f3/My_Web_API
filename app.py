from flask import Flask,jsonify,request
from flask_cors import CORS,cross_origin
import pickle,json,os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib


email = "geo.geofe@gmail.com"
toaddr = "geoffrey.geofe@gmail.com"
password='Geoffrey!1994'


#including bootstrap to the application 
application = app = Flask(__name__)


# Cross Origin Server
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#load the model for prediction 
auto_mpg = pickle.load(open('./Models/auto_mpg','rb'))
# Create a URL route in our application for "/"

def send_email(form_data):
	msg = MIMEMultipart()
	new_body = '''
        <html>
            <head>
            </head>
            <body>
                <p>Email : ''' + form_data['email'] + '''</p>

                <p>Name : ''' + form_data['name'] + '''</p>

                <p>MobileNumber : ''' + form_data['mobileNumber'] + '''</p>

                <p>Message : ''' + form_data['message'] + '''</p>

            </body>

        </html>

    '''

	 
	text_part = MIMEText(new_body, _subtype="html")
	msg.attach(text_part)
	msg["To"] = toaddr
	msg["From"] = form_data['email']
	msg["Subject"] = "Enquiry from Portfolio Page from "+form_data['email']
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.connect("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(email, password)
	server.sendmail(form_data['email'], toaddr, msg.as_string())
	server.quit()
	app.logger.info("Email sent")

@app.route('/')
def home():
	"""
	This function just responds to the browser ULR
	localhost:5000/

	:return:        hello world with status 200'
	"""
	return jsonify({'result':"hello world"})

@app.route('/predict_mpg',methods=['GET','POST'])
def predict_mpg():
	if request.method   == 'POST':
		app.logger.info("The post method")
		try:
			request_data = request.get_json()
			form_data = request_data['data']
			form_data = [int(data) for data in form_data]
			try:
				prediction = auto_mpg.predict([form_data])
				app.logger.info("The form data is {}\nThe Type of form-data is {}".format(form_data,type(form_data)))
				return jsonify({'res':prediction.tolist()[0]})
			except Exception as e:
				app.logger.info(e)
				return jsonify({'res':"Prediction Failed"})
		except Exception as e:
			app.logger.info(e)
			return jsonify({'res':'Post method failed'})
	else:
		app.logger.info("Not a post method")
		return jsonify({'res':'Method Not allowed - Not a post method'})


@app.route('/enquiry',methods=['POST'])
def enquiry():
	print (request.is_json)
	if request.method   == 'POST':
		app.logger.info("The post method")
		try:
			request_data = request.get_json()
			form_data = request_data['data']
			#app.logger.info("The form data is {}\nThe Type of form-data is {}".format(form_data['name'],type(form_data)))
			send_email(form_data)
			return jsonify({'res':"Email Send"})
		except Exception as e:
			app.logger.info(e)
			return jsonify({'res':'Email Send failed'})
	else:
		app.logger.info("Not a post method")
		return jsonify({'res':'Method Not allowed - Not a post method'})	


if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)



