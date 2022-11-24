
from paho.mqtt import client as mqtt_client
import sqlite3
import numpy as np

conn = sqlite3.connect('MQTTNew.db')



def create_table():
    c_cur = conn.cursor()
    c_cur.execute("CREATE TABLE IF NOT EXISTS CH0(ID INTEGER PRIMARY KEY AUTOINCREMENT,Channel0 INT)")  # <<<<<<<<<< CHANGED
    c_cur.execute("CREATE TABLE IF NOT EXISTS CH4(ID INTEGER PRIMARY KEY AUTOINCREMENT,Channel4 INT)")
    c_cur.execute("CREATE TABLE IF NOT EXISTS CH3(ID INTEGER PRIMARY KEY AUTOINCREMENT,Channel3 INT)")  # <<<<<<<<<< CHANGED
    c_cur.execute("CREATE TABLE IF NOT EXISTS CH5(ID INTEGER PRIMARY KEY AUTOINCREMENT,Channel5 INT)")
    c_cur.execute("CREATE TABLE IF NOT EXISTS CH6(ID INTEGER PRIMARY KEY AUTOINCREMENT,Channel6 INT)")  # <<<<<<<<<< CHANGED
    c_cur.execute("CREATE TABLE IF NOT EXISTS CH7(ID INTEGER PRIMARY KEY AUTOINCREMENT,Channel7 INT)")
    c_cur.close()
create_table()



broker = '192.168.222.4'
port = 1883
topic = "Data"
client_id = ''
username = 'Reinstated'
password = 'whatthehell'





x0 = []
i = 0
x1 = []
x2 = []
x3=[]
x4=[]
x4t=[]
x5=[]
x6=[]
x7=[]
x9=[]


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    conn = sqlite3.connect('MQTTNew.db')
    def on_message(client, userdata, msg):




        a = ((msg.payload))
        print("Payload Recieved:")
        print(a)
        print("Length of Payload:")
        print(len((msg.payload)))
        #y = np.transpose(x)
        intermediate = (msg.payload);

        hexA = intermediate.hex()

        print("Length of converted hexadecimal payload:")
        print(len(hexA))
        print("Hexadecimal Converted Payload:")
        print(hexA)
        b = int(hexA[2:6], 16)
        print("A single data extracted from Packet:")
        print(b)
        print("Channel no:")
        print(int(b)>>12)
        print("Converted Decimal form of the Data:")
        print((int(b) & 0x0FFF))
        c = int(hexA[0:2], 16)
        print(c)
        hst = 2
        hend = 6
        for m in range(int(len((msg.payload))/8)-2):
            c_cur = conn.cursor()
            hextoint = (int(hexA[hst:hend], 16))
            channel = int (hextoint) >> 12
            tmp = int(int(hextoint) & 0x0FFF)

            #print(type(tmp))
            if ((int(hextoint) & 0x0FFF) < 4097):
                if (channel == 0):
                    f0 = []
                    if (len(x0) == 0 or m == 0 or m == int(len((msg.payload)) / 8) - 3):
                        f0.append((int(hextoint) & 0x0FFF))
                        # x4.append((int(hextoint) & 0x0FFF))
                        # print((int(hextoint) & 0x0FFF))

                    else:
                        hextointpreditor = (int(hexA[hst - 8:hend - 8], 16)) & 0x0FFF
                        hextointadvance = (int(hexA[hst + 8:hend + 8], 16)) & 0x0FFF
                        # diff=int(x4[m-1])-(int(hextoint) & 0x0FFF)
                        # if (diff > 140 and diff <300 ):
                        dist = hextointadvance - (int(hextoint) & 0x0FFF)
                        # diff = int(x4[m - 1]) - (int(hextoint) & 0x0FFF)
                        if (dist == 256):
                            f0.append((int(hextoint) & 0x0FFF) + 256)
                            # x4.append((int(hextoint) & 0x0FFF) + 256)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -256):
                            f0.append((int(hextoint) & 0x0FFF) - 256)
                            # x4.append((int(hextoint) & 0x0FFF) - 256)
                        # print((int(hextoint) & 0x0FFF) - 256)
                        elif (dist == 512):
                            f0.append((int(hextoint) & 0x0FFF) + 512)
                            # x4.append((int(hextoint) & 0x0FFF) + 512)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -512):
                            f0.append((int(hextoint) & 0x0FFF) - 512)
                            # x4.append((int(hextoint) & 0x0FFF) - 512)
                        else:
                            f0.append((int(hextoint) & 0x0FFF))
                            # x4.append((int(hextoint) & 0x0FFF))
                            # print((int(hextoint) & 0x0FFF))
                    x0.append(tuple(f0))
                    f0.clear()
                #    c_cur.execute("INSERT INTO CH0 (Channel0) VALUES (?)", (tmp,))

                if (channel == 3):
                    f3 = []
                    if (len(x3) == 0 or m == 0 or m == int(len((msg.payload)) / 8) - 3):
                        f3.append((int(hextoint) & 0x0FFF))
                        # x4.append((int(hextoint) & 0x0FFF))
                        # print((int(hextoint) & 0x0FFF))

                    else:
                        hextointpreditor = (int(hexA[hst - 8:hend - 8], 16)) & 0x0FFF
                        hextointadvance = (int(hexA[hst + 8:hend + 8], 16)) & 0x0FFF
                        # diff=int(x4[m-1])-(int(hextoint) & 0x0FFF)
                        # if (diff > 140 and diff <300 ):
                        dist = hextointadvance - (int(hextoint) & 0x0FFF)
                        # diff = int(x4[m - 1]) - (int(hextoint) & 0x0FFF)
                        if (dist == 256):
                            f3.append((int(hextoint) & 0x0FFF) + 256)
                            # x4.append((int(hextoint) & 0x0FFF) + 256)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -256):
                            f3.append((int(hextoint) & 0x0FFF) - 256)
                            # x4.append((int(hextoint) & 0x0FFF) - 256)
                        # print((int(hextoint) & 0x0FFF) - 256)
                        elif (dist == 512):
                            f3.append((int(hextoint) & 0x0FFF) + 512)
                            # x4.append((int(hextoint) & 0x0FFF) + 512)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -512):
                            f3.append((int(hextoint) & 0x0FFF) - 512)
                            # x4.append((int(hextoint) & 0x0FFF) - 512)
                        else:
                            f3.append((int(hextoint) & 0x0FFF))
                            # x4.append((int(hextoint) & 0x0FFF))
                            # print((int(hextoint) & 0x0FFF))
                    x3.append(tuple(f3))
                    f3.clear()
                 #   c_cur.execute("INSERT INTO CH3 (Channel3) VALUES (?)", (tmp,))

                if (channel == 4):
                    f4=[]
                    if (len(x4) == 0 or m==0 or m==int(len((msg.payload))/8)-3):
                        f4.append((int(hextoint) & 0x0FFF))
                        #x4.append((int(hextoint) & 0x0FFF))
                        # print((int(hextoint) & 0x0FFF))

                    else:
                        hextointpreditor = (int(hexA[hst - 8:hend - 8], 16)) & 0x0FFF
                        hextointadvance = (int(hexA[hst + 8:hend + 8], 16)) & 0x0FFF
                        # diff=int(x4[m-1])-(int(hextoint) & 0x0FFF)
                        # if (diff > 140 and diff <300 ):
                        dist = hextointadvance - (int(hextoint) & 0x0FFF)
                        #diff = int(x4[m - 1]) - (int(hextoint) & 0x0FFF)
                        if (dist==256):
                            f4.append((int(hextoint) & 0x0FFF) + 256)
                            #x4.append((int(hextoint) & 0x0FFF) + 256)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist==-256):
                            f4.append((int(hextoint) & 0x0FFF) - 256)
                            #x4.append((int(hextoint) & 0x0FFF) - 256)
                        # print((int(hextoint) & 0x0FFF) - 256)
                        elif (dist==512):
                            f4.append((int(hextoint) & 0x0FFF) + 512)
                            #x4.append((int(hextoint) & 0x0FFF) + 512)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist==-512):
                            f4.append((int(hextoint) & 0x0FFF) - 512)
                            #x4.append((int(hextoint) & 0x0FFF) - 512)
                        else:
                            f4.append((int(hextoint) & 0x0FFF))
                            #x4.append((int(hextoint) & 0x0FFF))
                            # print((int(hextoint) & 0x0FFF))
                    x4.append(tuple(f4))
                    f4.clear()
                    #c_cur.execute("INSERT INTO CH4 (Channel4) VALUES (?)", (tmp,))

                    #conn.close()
                if (channel == 5):
                    f5 = []
                    if (len(x5) == 0 or m == 0 or m == int(len((msg.payload)) / 8) - 3):
                        f5.append((int(hextoint) & 0x0FFF))
                        # x4.append((int(hextoint) & 0x0FFF))
                        # print((int(hextoint) & 0x0FFF))

                    else:
                        hextointpreditor = (int(hexA[hst - 8:hend - 8], 16)) & 0x0FFF
                        hextointadvance = (int(hexA[hst + 8:hend + 8], 16)) & 0x0FFF
                        # diff=int(x4[m-1])-(int(hextoint) & 0x0FFF)
                        # if (diff > 140 and diff <300 ):
                        dist = hextointadvance - (int(hextoint) & 0x0FFF)
                        # diff = int(x4[m - 1]) - (int(hextoint) & 0x0FFF)
                        if (dist == 256):
                            f5.append((int(hextoint) & 0x0FFF) + 256)
                            # x4.append((int(hextoint) & 0x0FFF) + 256)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -256):
                            f5.append((int(hextoint) & 0x0FFF) - 256)
                            # x4.append((int(hextoint) & 0x0FFF) - 256)
                        # print((int(hextoint) & 0x0FFF) - 256)
                        elif (dist == 512):
                            f5.append((int(hextoint) & 0x0FFF) + 512)
                            # x4.append((int(hextoint) & 0x0FFF) + 512)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -512):
                            f5.append((int(hextoint) & 0x0FFF) - 512)
                            # x4.append((int(hextoint) & 0x0FFF) - 512)
                        else:
                            f5.append((int(hextoint) & 0x0FFF))
                            # x4.append((int(hextoint) & 0x0FFF))
                            # print((int(hextoint) & 0x0FFF))
                    x5.append(tuple(f5))
                    f5.clear()
                 #   c_cur.execute("INSERT INTO CH5 (Channel5) VALUES (?)", (tmp,))

                elif (channel == 6):
                    f6 = []
                    if (len(x6) == 0 or m == 0 or m == int(len((msg.payload)) / 8) - 3):
                        f6.append((int(hextoint) & 0x0FFF))
                        # x4.append((int(hextoint) & 0x0FFF))
                        # print((int(hextoint) & 0x0FFF))

                    else:
                        hextointpreditor = (int(hexA[hst - 8:hend - 8], 16)) & 0x0FFF
                        hextointadvance = (int(hexA[hst + 8:hend + 8], 16)) & 0x0FFF
                        # diff=int(x4[m-1])-(int(hextoint) & 0x0FFF)
                        # if (diff > 140 and diff <300 ):
                        dist = hextointadvance - (int(hextoint) & 0x0FFF)
                        # diff = int(x4[m - 1]) - (int(hextoint) & 0x0FFF)
                        if (dist == 256):
                            f6.append((int(hextoint) & 0x0FFF) + 256)
                            # x4.append((int(hextoint) & 0x0FFF) + 256)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -256):
                            f6.append((int(hextoint) & 0x0FFF) - 256)
                            # x4.append((int(hextoint) & 0x0FFF) - 256)
                        # print((int(hextoint) & 0x0FFF) - 256)
                        elif (dist == 512):
                            f6.append((int(hextoint) & 0x0FFF) + 512)
                            # x4.append((int(hextoint) & 0x0FFF) + 512)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -512):
                            f6.append((int(hextoint) & 0x0FFF) - 512)
                            # x4.append((int(hextoint) & 0x0FFF) - 512)
                        else:
                            f6.append((int(hextoint) & 0x0FFF))
                            # x4.append((int(hextoint) & 0x0FFF))
                            # print((int(hextoint) & 0x0FFF))
                    x6.append(tuple(f6))
                    f6.clear()
               #     c_cur.execute("INSERT INTO CH6 (Channel6) VALUES (?)", (tmp,))

                elif (channel == 7):
                    f7 = []
                    if (len(x7) == 0 or m == 0 or m == int(len((msg.payload)) / 8) - 3):
                        f7.append((int(hextoint) & 0x0FFF))
                        # x4.append((int(hextoint) & 0x0FFF))
                        # print((int(hextoint) & 0x0FFF))

                    else:
                        hextointpreditor = (int(hexA[hst - 8:hend - 8], 16)) & 0x0FFF
                        hextointadvance = (int(hexA[hst + 8:hend + 8], 16)) & 0x0FFF
                        # diff=int(x4[m-1])-(int(hextoint) & 0x0FFF)
                        # if (diff > 140 and diff <300 ):
                        dist = hextointadvance - (int(hextoint) & 0x0FFF)
                        # diff = int(x4[m - 1]) - (int(hextoint) & 0x0FFF)
                        if (dist == 256):
                            f7.append((int(hextoint) & 0x0FFF) + 256)
                            # x4.append((int(hextoint) & 0x0FFF) + 256)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -256):
                            f7.append((int(hextoint) & 0x0FFF) - 256)
                            # x4.append((int(hextoint) & 0x0FFF) - 256)
                        # print((int(hextoint) & 0x0FFF) - 256)
                        elif (dist == 512):
                            f7.append((int(hextoint) & 0x0FFF) + 512)
                            # x4.append((int(hextoint) & 0x0FFF) + 512)
                            # print((int(hextoint) & 0x0FFF)+256)
                        elif (dist == -512):
                            f7.append((int(hextoint) & 0x0FFF) - 512)
                            # x4.append((int(hextoint) & 0x0FFF) - 512)
                        else:
                            f7.append((int(hextoint) & 0x0FFF))
                            # x4.append((int(hextoint) & 0x0FFF))
                            # print((int(hextoint) & 0x0FFF))
                    x7.append(tuple(f7))
                    f7.clear()
                #    c_cur.execute("INSERT INTO CH7 (Channel7) VALUES (?)", (tmp,))


            #print(len(x4))
            #print(x7)


            x9.append(int(hextoint) & 0x0FFF)
            hst = hst + 8
            hend = hend + 8

        x4t.clear()
       # print(len(x4))

        def enter_data():
            c_cur.executemany("INSERT INTO CH0 (Channel0) VALUES (?)", (x0))
            c_cur.executemany("INSERT INTO CH4 (Channel4) VALUES (?)", (x4))
            c_cur.executemany("INSERT INTO CH3 (Channel3) VALUES (?)", (x3))
            c_cur.executemany("INSERT INTO CH5 (Channel5) VALUES (?)", (x5))
            c_cur.executemany("INSERT INTO CH6 (Channel6) VALUES (?)", (x6))
            c_cur.executemany("INSERT INTO CH7 (Channel7) VALUES (?)", (x7))

        enter_data()
        conn.commit()
        c_cur.close()

        x0.clear()
        x3.clear()
        x4.clear()
        x4t.clear()
        #print(len(x4))
        x5.clear()
        x6.clear()
        x7.clear()
        x9.clear()


    client.subscribe(topic)
    client.on_message = on_message
conn.close()


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
