# MY Web API's

Service that handles My portfolio API requests and responses

Flask application, install requirements in requirements.txt and run with 'python manage.py'

# Working with Docker

Build docker using ` docker build -t name:version .  `

After deploy the app using ` docker run -d -p 5000:5000 name `

In your browser navigate to: **http://localhost:5000** (or whatever port you have mention in the docker build) to see the app up and running

# Working without docker

I highly recommend the use of docker as it is far simpler to get started than to run all of the following manually.

To Deploy manually Assure you have Python. installed.

Navigate inside the directory

Install pip dependencies: `pip install -r requirements.txt`

Run `python manage.py` to see the app up and running on port **5000** (will watch files and restart server on port 5000 on change)
