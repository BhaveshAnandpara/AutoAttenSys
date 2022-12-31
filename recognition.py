
import face_recognition
import cv2
import os
import pickle
import numpy as np
import spreadsheet

known_face_encodings = []
known_face_names = []

photo_folder = "C:\\Projects\\AAS\\uploads\\photos\\"
facial_encodings_folder = "C:\\Projects\\AAS\\uploads\\encodings\\"


def load_facial_encodings_and_names_from_memory():
    for filename in os.listdir(facial_encodings_folder):
        known_face_names.append(filename[:-4])
        with open(facial_encodings_folder+filename, 'rb') as fp:
            known_face_encodings.append(pickle.load(fp)[0])


def checkRecognition(imgSrc):

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    load_facial_encodings_and_names_from_memory()

    frame = cv2.imread(
        imgSrc)


    while True:

        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        except Exception as e:
            print(e)

        # Resize frame of video to 1/4 size for faster face recognition processing

#     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

             # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                    spreadsheet.write_to_sheet(face_names[0].replace('_', ' '))
                    process_this_frame = not process_this_frame
                    return face_names       


