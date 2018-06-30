from websocket import create_connection

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


send_message('turn the nanoleaf on')
