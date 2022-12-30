from flask import Flask,  request
from enroll import encoding_of_enrolled_person
import os
import spreadsheet
from recognition import checkRecognition
import time

photo_folder = 'C:\\Projects\\AAS\\uploads\\photos\\'
frame_folder = 'C:\\Projects\\AAS\\uploads\\frames\\'


app = Flask("__main__")
app.config['photo_folder'] = photo_folder
app.config['frame_folder'] = frame_folder


@app.route('/enrollUser', methods=['POST'])
def enrollUser():
    # Recieves the data Given
    name = request.form['name']
    email = request.form['email']
    image = request.files['image']

    # Setting Name of Image as of User Name
    newimage = name.replace(' ', '_') + "."+(image.filename.split('.')[-1])

    # Saving Image in Folder
    image.save(os.path.join(app.config['photo_folder'], newimage))

    # Encoding the Image and Saving It
    encoding_of_enrolled_person(name.replace(
        ' ', '_'), photo_folder + newimage)

    # Saving the name and email into the spreadsheet
    spreadsheet.enroll_person_to_sheet(name, email)

    return {"msg": "Enrolled Successfull", "name": name, "email": email, "image": newimage}


@app.route('/presentee', methods=['POST'])
def presentee():
    frame = request.files['frame']
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    newframe = current_time.replace(':' , '_') + '.jpeg'
    frame.save(os.path.join(app.config['frame_folder'], newframe))
    checkRecognition( frame_folder + newframe)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
