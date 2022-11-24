from flask import request
from flask import Flask,render_template
import requests
'''meta tag追跡用'''




app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        DocNo = request.form.get('doc')
        DocNo = str(DocNo)
        DocURL = requests.get("https://daccess-ods.un.org/access.nsf/Get?OpenAgent&DS="+DocNo+"&Lang=E").url
        
    else:
        DocNo = "none"
    button = "on"
    print(DocURL)
    return render_template('index.html', DocNo=DocNo, DocURL=DocURL, button=button) 

@app.route('/download/<DocURL>')
def download(DocURL):
    return render_template("download.html", DocURL=DocURL,
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)