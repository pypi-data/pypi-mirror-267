import sys
sys.path.append("../mqi-api")
from api.v1 import MQI 

m = MQI("ws://mqicontroller.local", "8080")
m.connect()

# Will set current of channel 1 to 0
m.getBias("0");
