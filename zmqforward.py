from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import osc_message
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.SUB)

#socket.monitor("inproc://monitor.sock", zmq.EVENT_ALL)

#monitor_socket = context.socket(zmq.PAIR)
#monitor_socket.connect("inproc://monitor.sock")

socket.connect("tcp://pong.hku.nl:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'')
localClient = udp_client.UDPClient("127.0.0.1", 8000)

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
#poller.register(monitor_socket, zmq.POLLIN)

# Loop and accept messages from both channels, acting accordingly
while True:
    # TODO: Might need to retry connection?
    socks = dict(poller.poll(1000))
    if socks:
        if socks.get(socket) == zmq.POLLIN:
            dgram = socket.recv(zmq.NOBLOCK)
            # Untested convert to osc message (from dgram)
            print("got message")
            localClient.send(osc_message.OscMessage(dgram))
    else:
        # testMessage()
        # print("error: message timeout")
        time.sleep(0.1)

