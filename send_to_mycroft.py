import sys
import pickle
from websocket import create_connection
import json
import time
import asyncio

URL_TEMPLATE = "{scheme}://{host}:{port}{path}"


socket_host = "192.168.0.41" #this should be the ip address of the mycroft device on the local network
socket_port = 8181 #this port should match the client port
hyperion_host = "192.168.0.32" #this should be the ip address of the mycroft device on the local network
hyperion_port = 19444 #this port should match the client port



def send_message(message, host=socket_host, port=socket_port, path="/core", scheme="tcp"):
    payload = pickle.dumps({
        "type": "recognizer_loop:utterance",
        "context": "",
        "data": {
            "utterances": [message]
        }
    })
    url = URL_TEMPLATE.format(scheme=scheme, host=host, port=str(port), path=path)
    ws = create_connection(url)
    ws.send(payload)
    ws.close()


def send_hyperion(host=hyperion_host, port=hyperion_port, path="/core", scheme="ws"):
    # payload = '{"command": "color", "priority": 50, "color": [255,255,255], "duration": 14400000}'
    payload = '{"command":"serverinfo"}'

    url = URL_TEMPLATE.format(scheme=scheme, host=host, port=str(port), path=path)
    ws = create_connection(url)
    ws.send(payload)
    greeting = await ws.recv()
    print(f"< {greeting}")
    ws.close()


send_hyperion()

#send_message(socket_msg)
#time.sleep(1)




# mute Command
# send_message('please be silent')
# time.sleep(1)
# send_message('turn the wall lights on')
# time.sleep(10)
# send_message('set the room lights to 10 percent')
# time.sleep(10)
# send_message('turn the room lights off')
# send_message('set the wall lights to orange')
# time.sleep(10)
# send_message('set the wall lights to 2 percent')
# time.sleep(15)

# un-mute Command
# send_message('you can speak now')
# print('no longer silent')
# time.sleep(1)


