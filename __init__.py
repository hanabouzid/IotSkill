from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
import pyrebase
import RPi.GPIO as GPIO
import time
import json

#declaration
config = {
  "apiKey": "AIzaSyBIcKApBiLDHvRKMobq_wmEMqxeWXGG5no",
  "authDomain": "smart-assistant-box-274114.firebaseapp.com",
  "databaseURL": "https://smart-assistant-box-274114.firebaseio.com",
  "storageBucket": "smart-assistant-box-274114.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
GPIO.setmode(GPIO.BOARD)
class IotSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(IotSkill, self).__init__(name="IotSkill")
        self.dict ={"london meeting room":"lampe_1","tokyo meeting room":"lampe_2"}
        self.lampe_1 = 3
        self.lampe_2 = 5
        #self.lampe_3 = 12

    def allume_Lampe(self,pin_lampe):
        GPIO.setup(pin_lampe)
        GPIO.output(pin_lampe,1)
        print("allume", pin_lampe)

    def eteindre_Lampe(self,pin_lampe):
        GPIO.setup(pin_lampe)
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
                #db.child(cle).child(valeur).get().val() = "ON"
                db.child(cle).child(valeur).setValue("ON")
                self.speak_dialog("On")

    @intent_handler(IntentBuilder("lights_off_intent").require("Off").optionally('room').build())
    def light_off(self, message):
        utt = message.data.get("utterance", None)
        list = utt.split(" in ")
        room = list[1]
        for cle, valeur in self.dict.items():
            if cle == room:
                self.eteindre_Lampe(valeur)
                db.child(cle).child(valeur).setValue("OFF")
                self.speak_dialog("Off")

    @intent_handler(IntentBuilder("").require("displaylights"))
    def affich_lightsOn(self, message):
        roomlist =[]
        for key,value in self.dict.items():
            if db.child(key).child(value).get().val() == "ON":
                roomlist.append(key)
        if roomlist!=[]:
            s = ",".join(roomlist)
            self.speak_dialog("roomsOn", data={"s": s})
        else:
            self.speak_dialog("roomsOff")

def create_skill():
    return IotSkill()