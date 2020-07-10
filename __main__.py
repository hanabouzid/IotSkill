import pyrebase
import RPi.GPIO as GPIO
import json
config = {
    "apiKey": "AIzaSyBIcKApBiLDHvRKMobq_wmEMqxeWXGG5no",
    "authDomain": "smart-assistant-box-274114.firebaseapp.com",
    "databaseURL": "https://smart-assistant-box-274114.firebaseio.com",
    "storageBucket": "smart-assistant-box-274114.appspot.com",
    "serviceAccount": "/opt/mycroft/skills/iotskill/smart-assistant-box.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
GPIO.setmode(GPIO.BOARD)
dict = {"london meeting room": "lampe_1", "paris meeting room": "lampe_2", "tokyo meeting room": "lampe_3"}
lampe_1 = 3
lampe_2 = 5
lampe_3 = 12
def allume_Lampe(pin_lampe):
    GPIO.setup(pin_lampe,GPIO.OUT)
    GPIO.output(pin_lampe,1)
    print("allume",pin_lampe)
def eteindre_Lampe(pin_lampe):
    GPIO.setup(pin_lampe,GPIO.OUT)
    GPIO.output(pin_lampe,0)
    print ("eteindre",pin_lampe)
#eteindre lampe
utt = input("request off")
list = utt.split(" in ")
room = list[1]
for cle, valeur in dict.items():
    if cle == room:
        eteindre_Lampe(valeur)
        db.child(cle).child(valeur).setValue("OFF")
        print("off")

#allumer lampe
utt = input("request on")
list = utt.split(" in ")
room =list[1]
for cle, valeur in dict.items():
    if cle == room:
        allume_Lampe(valeur)
        db.child(cle).child(valeur).setValue("ON")
        print("On")
#rooms with lights on
roomlist =[]
for key,value in dict.items():
    if db.child(key).child(value).get().val() == "ON":
        roomlist.append(key)
if roomlist!=[]:
    s = ",".join(roomlist)
    print("roomsOn"+s)
else:
    print("roomsOff")
#all lights off
for key, value in dict.items():
    if db.child(key).child(value).get().val() == "ON":
        eteindre_Lampe(value)
        db.child(key).child(value).setValue("OFF")
print("roomsOff")