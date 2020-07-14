import pyrebase
import RPi.GPIO as GPIO
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
import json
#declaration
config = {
  "apiKey": "AIzaSyBIcKApBiLDHvRKMobq_wmEMqxeWXGG5no",
  "authDomain": "smart-assistant-box-274114.firebaseapp.com",
  "databaseURL": "https://smart-assistant-box-274114.firebaseio.com",
  "storageBucket": "smart-assistant-box-274114.appspot.com",
    "serviceAccount": "/opt/mycroft/skills/iotskill.hanabouzid/smart-assistant-box.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
GPIO.setmode(GPIO.BOARD)
class IotSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(IotSkill, self).__init__(name="IotSkill")
        self.lampe_1 = 3
        self.lampe_2 = 5
        self.lampe_3 = 12
        self.dict ={"london meeting room":self.lampe_1,"paris meeting room":self.lampe_2,"tokyo meeting room":self.lampe_3}


    def allume_Lampe(self,pin_lampe):
        GPIO.setup(pin_lampe,GPIO.OUT)
        GPIO.output(pin_lampe,1)
        print("allume", pin_lampe)

    def eteindre_Lampe(self,pin_lampe):
        GPIO.setup(pin_lampe,GPIO.OUT)
        GPIO.output(pin_lampe,0)
        print("eteindre", pin_lampe)

    @intent_handler(IntentBuilder("lights_on_intent").require("On").optionally('room').build())
    def light_on(self, message):
        utt = message.data.get("utterance", None)
        list = utt.split(" in ")
        room =list[1]
        for cle, valeur in self.dict.items():
            if cle == room:
                self.allume_Lampe(valeur)
                dict2 = {cle: "ON"}
                db.update(dict2)
                self.speak_dialog("On")

    @intent_handler(IntentBuilder("lights_off_intent").require("Off").optionally('room').build())
    def light_off(self, message):
        utt = message.data.get("utterance", None)
        list = utt.split(" in ")
        room = list[1]
        for cle, valeur in self.dict.items():
            if cle == room:
                self.eteindre_Lampe(valeur)
                dict3 = {cle: "OFF"}
                db.update(dict3)
                self.speak_dialog("Off")

    @intent_handler(IntentBuilder("").require("displaylights"))
    def affich_lightsOn(self, message):
        roomlist =[]
        for key,value in self.dict.items():
            if db.child(key).get().val() == "ON":
                roomlist.append(key)
        if roomlist!=[]:
            s = ",".join(roomlist)
            self.speak_dialog("roomsOn", data={"s": s})
        else:
            self.speak_dialog("roomsOff")

    @intent_handler(IntentBuilder("").require("all_light_soff"))
    def all_lights_off(self, message):
        for key, value in dict.items():
            if db.child(key).get().val() == "ON":
                self.eteindre_Lampe(value)
                dict4 = {key: "OFF"}
                db.update(dict4)
        self.speak_dialog("roomsOff")
def create_skill():
    return IotSkill()
