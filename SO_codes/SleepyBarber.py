from threading import Thread, Lock, Condition
from time import sleep

mutex = Lock()
condition = Condition(mutex)

SLEEPING = 0
AWAKE = 1
CUTTING = 2
CLIENT = 3

n_barbers = 1
barbers_states = []
n_waiting_chairs = 10

barbers = []
clients = []


class Barber(Thread):

    def __init__(self, index):
        Thread.__init__(self)
        self.index = index

    def sleep_on_chair(self):
        condition.acquire()
        if len(clients) == 0:
            barbers_states[self.index] = SLEEPING
            print("barber is sleeping cause did not found any client")
            condition.wait()
            barbers_states[self.index] = AWAKE
            print("a client has woke up the barber")
        condition.release()

    def cut_hair(self):
        condition.acquire()
        if len(clients) > 0:
            clients.pop(0)
            print("barber has found a client")
            barbers_states[self.index] = CUTTING
            print("barber is cutting")
            condition.notify()
        condition.release()

    def run(self):
        while True:
            self.sleep_on_chair()
            self.cut_hair()


# class Client(Thread):
#
#     def __init__(self):
#         Thread.__init__(self)
#
#     def awake(self):
#         condition.acquire()
#         if clients.index(object=self) == 0:
#             condition.notify()
#
#         condition.release()
#
#     def run(self):
#         while True:
#             self.awake()


class ClientGenerator(Thread):

    def __init__(self):
        Thread.__init__(self)

    def generate(self):
        condition.acquire()
        if len(clients) < n_waiting_chairs:
            clients.append(CLIENT)
            print("A client has arrived")
            condition.notify_all()

        elif len(clients) == n_waiting_chairs:
            print("A client was not able to take a chair to wait")
            condition.notify_all()
            condition.wait()
        condition.release()

    def show_info(self):
        condition.acquire()
        print("clients = ", len(clients), '/', n_waiting_chairs)
        print("barbers = ", barbers_states)
        condition.release()
        sleep(3)

    def run(self):
        while True:
            self.generate()
            self.show_info()


for i in range(n_barbers):
    barbers.append(Barber(index=i))
    barbers_states.append(SLEEPING)
client_generator = ClientGenerator()

for barber in barbers:
    barber.start()
client_generator.start()

for barber in barbers:
    barber.join()
client_generator.join()
