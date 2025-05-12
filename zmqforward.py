from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import osc_message
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://host:5555")

localClient = udp_client.UDPClient("127.0.0.1", 8000)

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# Loop and accept messages from both channels, acting accordingly
while True:
    # TODO: Might need to retry connection?
    socks = dict(poller.poll(1000))
    if socks:
        if socks.get(socket) == zmq.POLLIN:
            dgram = socket.recv(zmq.NOBLOCK)
            # Untested convert to osc message (from dgram)
            localClient.send(osc_message.OscMessage(dgram))
            # print("got message ",message)
    else:
        # mesh template tester
        msg = osc_message_builder.OscMessageBuilder(address="/object/MeshTemplate")
        # msgType & root transform
        msg.add_arg("0")
        for i in range(0,16):
            msg.add_arg("0")

        # objects: id, type, active, name, properties (as per type)
        msg.add_arg("0")
        msg.add_arg("Mesh")
        msg.add_arg("MeshTemplate")
        msg.add_arg("0")

        # local transform
        for i in range(0,16):
            msg.add_arg("0")

        # mesh properties: modelName, visible, color (RGBA, Space), transparency
        msg.add_arg("model_name.glb")
        msg.add_arg("True")
        # Color
        for i in range(0,4):
            msg.add_arg("1")
        msg.add_arg("Linear")        
        msg.add_arg("1")
        
        builtMessage = msg.build()
        localClient.send(builtMessage)
        # print("error: message timeout")
        time.sleep(0.1)
