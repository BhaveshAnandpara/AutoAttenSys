from flask import Flask,  request
from flask_cors import CORS
from enroll import encoding_of_enrolled_person
import os
import spreadsheet
from recognition import checkRecognition
import time

photo_folder = 'C:\\Projects\\AAS\\uploads\\photos\\'
frame_folder = 'C:\\Projects\\AAS\\uploads\\frames\\'


app = Flask("__main__")

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

app.config['photo_folder'] = photo_folder
app.config['frame_folder'] = frame_folder


@app.route('/enrollUser', methods=['POST'])
def enrollUser():
    # Recieves the data Given
    name = request.form['name']
    email = request.form['email']
    image = request.files['image']


    # Setting Name of Image as of User Name
    newimage = name.replace(' ', '_') + '.jpeg'

    # Saving Image in Folder
    image.save(os.path.join(app.config['photo_folder'], newimage))

    # Encoding the Image and Saving It
    result = encoding_of_enrolled_person(name.replace(
        ' ', '_'), photo_folder + newimage)

    if result == 'error':
        print('error')
        return { 'msg' :'error'}

    # Saving the name and email into the spreadsheet
    spreadsheet.enroll_person_to_sheet(name, email)

    return {"msg": "Enrolled Successfull", "name": name, "email": email, "image": newimage}


@app.route('/presentee', methods=['POST'])
def presentee():
    print('Frame Received')
    frame = request.files['frame']
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    newframe = current_time.replace(':' , '_') + '.jpeg'
    frame.save(os.path.join(app.config['frame_folder'], newframe))
    return checkRecognition( frame_folder + newframe)

@app.route('/check', methods=['POST'])
def check():
    return "Works"

@app.route('/stopProcess')
def stopProcess():

    for file_name in os.listdir(frame_folder):
    # construct full file path
     file = frame_folder + file_name
     if os.path.isfile(file):
        print('Deleting file:', file)
        os.remove(file)

    spreadsheet.mark_absent()
    return "Frames Deleted"




if __name__ == '__main__':
    app.run(debug=True, port=8000)
