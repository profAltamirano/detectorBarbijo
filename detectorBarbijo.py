import cv2
import os
#import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import serial


BAUD = 9600
#usar el puerto serie que ocupe su arduino! IMPORTANTE... EN MI CASO FUE COM3 !
ser = serial.Serial("COM3", BAUD)

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_alt2.xml')
model = load_model("mask_recog.h5")
 
video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         #minSize=(120, 120),
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
    faces_list=[]
    preds=[]
    for (x, y, w, h) in faces:
        face_frame = frame[y:y+h,x:x+w]
        face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
        face_frame = cv2.resize(face_frame, (224, 224))
        face_frame = img_to_array(face_frame)
        face_frame = np.expand_dims(face_frame, axis=0)
        face_frame =  preprocess_input(face_frame)
        face_important = 'Prof Altamirano Alejandro Ivan, conect to https://prof.altamirano.xyz/'
        faces_list.append(face_frame)
        if len(faces_list)>0:
            preds = model.predict(faces_list)
        for pred in preds:
            (mask, withoutMask) = pred
        label = "Tiene Barbijo" if mask > withoutMask else "No tiene Barbijo"
        color = (0, 255, 0) if label == "Tiene Barbijo" else (0, 0, 255)
        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
        #ser.write(b'2')
        
        ser.write(b"a\n") if mask < withoutMask else ser.write(b"b\n")
        cv2.putText(frame, label, (x-40, y-30),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.3, color, 2)
 
        cv2.rectangle(frame, (x, y), (x + w, y + h),color, 2)
        

        # Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == 27:
        ser.close()
        break
video_capture.release()
cv2.destroyAllWindows()