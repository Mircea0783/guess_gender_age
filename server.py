import datetime
import random
from datetime import datetime
from flask import Flask, render_template
import requests
import socket  #for the local network running

def get_local_ip():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external server (doesn't actually send data)
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        # Fallback to localhost if there's an error
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

app = Flask(__name__)

@app.route('/')
def home():
    year_c=datetime.now().year
    num_rd = random.randint(1,10)
    return render_template("index.html",num=num_rd,year=year_c)

@app.route("/guess/<name>")
def guess(name):

    gender_url = f"http://api.genderize.io?name={name}"

    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    gender = gender_data["gender"]

    age_url = f"https://api.agify.io?name={name}"

    age_response = requests.get(age_url)
    age_data = age_response.json()
    age = age_data["age"]

    return render_template("guess.html", person_name=name, gender=gender, age=age)

if __name__ == '__main__':
    # Get the local IP
    host_ip = get_local_ip()
    # Run the server on the local IP, port 5000
    # 0.0.0.0 makes it accessible from outside the local machine
    app.run(host='0.0.0.0', port=5000, debug=True)


