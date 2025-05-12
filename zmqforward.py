from flask import Flask, render_template
from flask_sock import Sock
from pythonosc import osc_message_builder
import zmq
import pythonosc
import time

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://pong.hku.nl:5555")

localClient = context.socket(zmq.RADIO)
localClient.connect("udp://127.0.0.1:8000")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# Loop and accept messages from both channels, acting accordingly
while True:
    socks = dict(poller.poll(1000))
    if socks:
        if socks.get(socket) == zmq.POLLIN:
            message = socket.recv(zmq.NOBLOCK)
            localClient.send(message)
            print("got message ",message)
    else:
        msg = osc_message_builder.OscMessageBuilder(address="/hello")
        msg.add_arg("Hello World!")
        builtMessage = msg.build()
        localClient.send(builtMessage.dgram)
        print("error: message timeout")
        time.sleep(0.1)