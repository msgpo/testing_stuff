import uuid

def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac

guid =  uuid.uuid4()
print(guid)
print(get_mac_address())