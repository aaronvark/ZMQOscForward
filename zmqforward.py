from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import osc_message
import zmq
import sys
import time

oscdest = (b"127.0.0.1:8000",)

context = zmq.Context()
subsocket = context.socket(zmq.SUB)
subsocket.connect("tcp://pong.hku.nl:5555")
subsocket.setsockopt(zmq.SUBSCRIBE, b'')

oscsend = None
if zmq.DRAFT_API:
    oscsend = context.socket(zmq.DGRAM)
    oscsend.bind("udp://*:6789")
else:
    oscsend = udp_client.UDPClient("127.0.0.1", 8000)

poller = zmq.Poller()
poller.register(subsocket, zmq.POLLIN)

def testMessage():
    # mesh template tester
    msg = osc_message_builder.OscMessageBuilder(address="/object/MeshTemplate")
    # msgType & root transform
    msg.add_arg("0")
    for i in range(0,16):
        msg.add_arg("0")

    # objects: id, type, active, name
    msg.add_arg("0")
    msg.add_arg("Mesh")
    msg.add_arg("True")
    msg.add_arg("MeshTemplate")

    # local transform
    for i in range(0,16):
        msg.add_arg("0")

    # wildcard properties: bool, float
    msg.add_arg("True")
    msg.add_arg("1.0")

    # mesh properties: modelName, visible, color (RGBA, Space), transparency
    msg.add_arg("model_name.glb")
    msg.add_arg("True")
    # Color
    for i in range(0,4):
        msg.add_arg("1")
    msg.add_arg("Linear")        
    msg.add_arg("1")
    
    builtMessage = msg.build()
    if zmq.DRAFT_API:
        for d in oscdest:
            oscsend.send_multipart(d, builtMessage)
    else:
        oscsend.send(builtMessage)

# Loop and accept messages from both channels, acting accordingly
while True:
    # TODO: Might need to retry connection?
    socks = dict(poller.poll(1000))
    if socks:
        if socks.get(subsocket) == zmq.POLLIN:
            dgrams = subsocket.recv_multipart(copy=False)
            # Untested convert to osc message (from dgram)
            if zmq.DRAFT_API:
                for dgram in dgrams:
                    for d in oscdest:
                        oscsend.send_multipart((d, dgram), copy=False)
                sys.stdout.write('█')
                sys.stdout.flush()
            else:
                oscsend.send(osc_message.OscMessage(dgram))
                # print("got message ",message)
    else:
        # testMessage()
        # print("error: message timeout")
        print("idle iter")

