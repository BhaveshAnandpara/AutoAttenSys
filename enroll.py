
import face_recognition,cv2,pickle
import os
# import spreadsheet

photo_folder = 'C:\\Projects\\AAS\\uploads\\photos\\'
facial_encodings_folder = 'C:\\Projects\\AAS\\uploads\\encodings\\'


def encoding_of_enrolled_person(name,image):
	enroll_encoding=[]

	enroll_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(image))[0])
	f=open(facial_encodings_folder+name+'.txt','w+')
	
	with open(facial_encodings_folder+name+'.txt','wb') as fp:
		pickle.dump(enroll_encoding,fp)
	f.close


