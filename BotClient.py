import socketio
import time

sio = socketio.Client()
#logger.info('Created socketio client')


@sio.event
def connect():
    s = input("Enter Name : ")
    sio.emit('connected_bot', s)


@sio.event
def start_self(data):
    time.sleep(5)
    sio.emit('start_self_ok', data)
    time.sleep(5)
    sio.emit('task_completed', data)


@sio.event
def disconnect():
    print("disconnected")
    #logger.info('disconnected from server')


sio.connect('https://betasam-socket.herokuapp.com')
sio.wait()
