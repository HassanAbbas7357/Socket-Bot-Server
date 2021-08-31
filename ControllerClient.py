import socketio
import time
sio = socketio.Client()


@sio.event
def connect():
    s = input("Enter Name : ")
    sio.emit('connected_controllerClient', s)
    time.sleep(5)
    sio.emit('start_bots')



@sio.event
def TasksCompletedSuccess(bots):
    print("All Bots Completed their tasks",bots)


@sio.event
def disconnect():
    print("disconnected")


sio.connect('http://localhost:3000/')
sio.wait()
