from flask import Flask, request, send_from_directory
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

def get_integer(name):
    try:

        return int(name.split(".")[0].split("-")[-1])
    except:
        return 0

@app.route('/get_latest_twelve', methods=['GET'])
def get_latest_twelve():
    image_type = request.args.get('type')  # Get the image type from the query parameter
    
    if image_type not in ['NG', 'SG']:
        return 'Invalid image type. Allowed types are NG and SG.'

    files = os.listdir('files')  # List all files in the 'files' directory
    files = [file for file in files if file.startswith(image_type+"-") and "LINK" not in file]  # Filter files based on image type
    files = sorted(files, key=lambda x: get_integer(x), reverse=True)  # Sort files by timestamp
    
    latest_twelve = files[:12]  # Get the latest 12 files

    latest_twelve = sorted(latest_twelve, key=lambda x: get_integer(x), reverse=False)
    
    return ','.join(latest_twelve)  # Return the filenames as a comma-separated string

@app.route("/", methods=['GET'])
def return_main():
    #return "Hello"
    return send_from_directory("doc", "index2.html")

if __name__ == '__main__':
    app.run()
