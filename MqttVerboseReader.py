import paho.mqtt.client as mqtt  # import the client1
import time
import argparse

global dataFlag
dataFlag = False

# Printing Received Data Function


def on_message(client, userdata, message):

    global dataFlag

    if message.topic == "data/formatted/datalog_on-off": # reading datalog switch state from MQTT
        dataFlag = message.payload

    if dataFlag == "True":   # If datalog switch is on, dataFlag will be true and the datalog will save data
        dataLogFile = open("dataLog.txt", "a")
        dataLogFile.write('\n')
        dataLogFile.write(message.topic)
        dataLogFile.write(" said: ")
        dataLogFile.write(str(message.payload.decode("utf-8")))
        dataLogFile.close()
    if args.verbose:
        print(message.topic, "says: ", str(message.payload.decode("utf-8")))
        

########################################


print("creating new instance")


client = mqtt.Client("VerboseReader") 
client.on_message = on_message  # attach function to callback

print("connecting to broker")
client.connect("localhost")  # connect to broker
dataLogFile = open("dataLog.txt", "a")
dataLogFile.write("\n")
dataLogFile.write("started new session")
dataLogFile.close()


# SUBSCRIPTIONS

# to subscribe just type:
# client.subscribe("data/formatted/ <formatted data Channel-name> ")

print("Subscribing to topic","formatted/gear")
print("Subscribing to topic","formatted/auto_acc_flag")
print("Subscribing to topic","formatted/debug_mode")
print("Subscribing to topic","formatted/datalog_on-off")
print("Subscribing to topic","formatted/telemetria_on-off")
client.subscribe("data/formatted/gear")  # subscribing to gear Channel
client.subscribe("data/formatted/auto_acc_flag")
client.subscribe("data/formatted/debug_mode")
client.subscribe("data/formatted/datalog_on-off")
client.subscribe("data/formatted/telemetria_on-off")


# code to handle verbose mode
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="shows output", action="store_true");
args = parser.parse_args()
###############################################

client.loop_forever()  # start the loop
