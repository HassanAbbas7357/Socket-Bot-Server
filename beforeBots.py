from pymongo import MongoClient
import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    s = "beforeBots"
    sio.emit('connected_bot', s)
    print("Connected to Server")

with open('credentials/mongo_pass.txt', 'r') as f:
    conn_string = f.read()

# client = MongoClient()
client = MongoClient(username='transviti',
                    password=conn_string,
                    authSource='admin',
                    authMechanism='SCRAM-SHA-256')
db = client.betasam_updated

todo = db.todo

def firstStep():
    # clean kardein todo ko aur uskay andar sab bots ke todos ko
    db.todo1.delete_many({})
    db.todo1e.delete_many({})
    db.todo2.delete_many({})
    db.todo2e.delete_many({})
    db.todo3.delete_many({})
    db.todo3e.delete_many({})
    db.todo4.delete_many({})
    db.todo4e.delete_many({})
    db.todo5.delete_many({})
    db.todo5e.delete_many({})
    db.todo6.delete_many({})
    db.todo6e.delete_many({})
    db.todo7.delete_many({})
    db.todo7e.delete_many({})
    db.todo8.delete_many({})
    db.todo8e.delete_many({})
    db.todo9.delete_many({})
    db.todo9e.delete_many({})
    db.todo10.delete_many({})
    db.todo10e.delete_many({})
    db.todo11.delete_many({})
    db.todo11e.delete_many({})
    db.todo12.delete_many({})
    db.todo12e.delete_many({})
    db.todo13.delete_many({})
    db.todo13e.delete_many({})
    db.todo14.delete_many({})
    db.todo14e.delete_many({})
    db.todo15.delete_many({})
    db.todo15e.delete_many({})
    db.todo16.delete_many({})
    db.todo16e.delete_many({})

    db.todo.delete_many({'status': True})

def secondStep():
    # latest se utha kar, todo mein phenkana hai
    # # Run the below code only once
    for record in db.latest.find( {}, batch_size=50 ):
        db.todo.insert_one(record)

def thirdStep():
    # clean kareinge
    issue = list()
    for record in todo.find( {}, batch_size=500 ):
        sol = record['sol']
        if sol:
            rcount = todo.count_documents({'sol': sol})
            if rcount == 2:
                status = list()
                for r in todo.find({'sol': sol}):
                    status.append(record['status'])
                if status[0] == status[1]: # both true or both false
                    todo.delete_one({'sol': sol}) # delete one
                else: # one is true and one is false
                    todo.delete_one({'sol': sol, 'status': False}) # delete one with the False
            if rcount > 2:
                todo.delete_many({'sol': sol}) # saari instances delete kardo
                todo.insert_one({'sol': sol, 'status': False}) # baad mein aik khud se insert kardo

def fourthStep():
    # baateinge distributed bots ko
    query = {"status":False}
    totalCount = todo.count_documents(query)
    print(f"There are {totalCount} documents.")

    iteration = {
        1: db.todo1,
        2: db.todo1e,
        3: db.todo2,
        4: db.todo2e,
        5: db.todo3,
        6: db.todo3e,
        7: db.todo4,
        8: db.todo4e,
        9: db.todo5,
        10: db.todo5e,
        11: db.todo6,
        12: db.todo6e,
        13: db.todo7,
        14: db.todo7e,
        15: db.todo8,
        16: db.todo8e,
        17: db.todo9,
        18: db.todo9e,
        19: db.todo10,
        20: db.todo10e,
        21: db.todo11,
        22: db.todo11e,
        23: db.todo12,
        24: db.todo12e,
        25: db.todo13,
        26: db.todo13e,
        27: db.todo14,
        28: db.todo14e,
        29: db.todo15,
        30: db.todo15e,
        31: db.todo16,
        32: db.todo16e,
    }

    breakPoint = totalCount / 32
    breakPoint = int(breakPoint)
    print(breakPoint)

    count = 0
    itr = 1
    for record in todo.find( query, batch_size=1000 ):
        if count % breakPoint == 0 and count != 0:
            itr += 1
        if itr == 33:
            itr = 1
        print(record, itr, count)
        iteration[itr].insert_one(record)
        count = count + 1

def fifthStep():
    # latest ko saaf kareinge
    db.latest.delete_many({})

def mainDistribution():
    firstStep()
    secondStep()
    thirdStep()
    fourthStep()
    fifthStep()


@sio.event
def beforeBotsStart():
    # mainDistribution()
    print("Running Before Bots Setup")
    time.sleep(4)
    sio.emit('beforeBotsStartCompleted')
    print("Completed Before Bots Setup")


@sio.event
def disconnect():
    print("disconnected")
    #logger.info('disconnected from server')


sio.connect('https://betasam-socket.herokuapp.com')
sio.wait()
