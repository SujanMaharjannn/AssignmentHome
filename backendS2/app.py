#Import Flask
from flask import Flask

#Instance Creation
app = Flask(__name__)

#Route 
@app.route('/')

def home():
    return "Hello! This response is coming from the Python Flask app!"

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
