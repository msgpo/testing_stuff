from websocket import create_connection
import json
import time

URL_TEMPLATE = "{scheme}://{host}:{port}{path}"


def send_message(message, host="192.168.0.41", port=8181, path="/core", scheme="ws"):
    payload = json.dumps({
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

# mute Command
send_message('please be silent')
print('silent now')
time.sleep(1)

send_message('turn the room lights on')
time.sleep(0.5)
send_message('turn the wall lights on')
time.sleep(10)
send_message('set the room lights to 10 percent')
time.sleep(10)
send_message('turn the room lights off')
send_message('set the wall lights to orange')
time.sleep(10)
send_message('set the wall lights to 2 percent')
time.sleep(15)

# un-mute Command
send_message('you can speak now')
print('no longer silent')
time.sleep(1)


