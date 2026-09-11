# Line 1: Import the Flask tool into Python
from flask import Flask

# Line 2: Create our web app instance
app = Flask(__name__)

# Line 3: Define the Web Route (The URL)
@app.route('/')
# Line 4: The function that runs when someone visits '/'
def home():
    # Line 5: The answer sent back to the browser
    return "Hello! This response is coming from the Python Flask app!"

# Line 6: Check if this file is being executed directly
if __name__ == '__main__':
    # Line 7: Tell Flask to start listening on network port 5000
    app.run(host='0.0.0.0', port=5000)
