from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Get the API URL from environment variable or default to service name for Kubernetes
API_URL = os.environ.get("API_URL", "http://backend-service:5001")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        quote = request.form["quote"]
        author = request.form["author"]
        try:
            response = requests.post(
                f"{API_URL}/api/quotes", json={"quote": quote, "author": author}
            )
            if response.status_code != 201:
                print(f"Error: API returned status code {response.status_code}")
        except Exception as e:
            print(f"Error connecting to API: {str(e)}")
        return redirect(url_for("index"))
    else:
        try:
            response = requests.get(f"{API_URL}/api/quotes")
            if response.status_code == 200:
                quotes = response.json()
            else:
                quotes = []
                print(f"Error: API returned status code {response.status_code}")
        except Exception as e:
            quotes = []
            print(f"Error connecting to API: {str(e)}")
        
        return render_template("index.html", quotes=quotes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)