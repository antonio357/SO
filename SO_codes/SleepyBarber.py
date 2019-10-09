from threading import Thread, Lock, Condition
from time import sleep
from random import randint

mutex = Lock()
condition = Condition(mutex)
condition1 = Condition(mutex)

SLEEPING = "zzz"
AWAKE = "\o/"
CUTTING = "><><"
CLIENT = "$"

n_barbers = 2
barbers_states = []
n_waiting_chairs = 14

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
            print("barber", self.index, "sleeping")
            print("barbers = ", barbers_states)
            print("clients waiting = ", len(clients), '/', n_waiting_chairs)
            condition.wait()  # for this thread wait until generator generate

            barbers_states[self.index] = AWAKE
            print("barber", self.index, "woke up")
            print("barbers = ", barbers_states)

        if len(clients) > 0:
            clients.pop(0)
            barbers_states[self.index] = CUTTING
            print("barber", self.index, "cutting")
            print("barbers = ", barbers_states)
            print("clients waiting = ", len(clients), '/', n_waiting_chairs)
            condition1.notify()  # for generator wake up

        condition.release()

    def cut_hair(self):
        condition.acquire()

        if len(clients) > 0:
            clients.pop(0)
            barbers_states[self.index] = CUTTING
            print("barber", self.index, "cutting")
            print("barbers = ", barbers_states)
            print("clients waiting = ", len(clients), '/', n_waiting_chairs)
            condition1.notify()  # for generator wake up

        if len(clients) == 0:
            barbers_states[self.index] = SLEEPING
            print("barber", self.index, "sleeping")
            print("barbers = ", barbers_states)
            print("clients waiting = ", len(clients), '/', n_waiting_chairs)
            condition.wait()  # for this thread wait until generator generate

        condition.release()

    def run(self):
        while True:
            self.sleep_on_chair()
            self.cut_hair()
            # sleep(randint(0, 3))


class ClientGenerator(Thread):

    def __init__(self):
        Thread.__init__(self)

    def generate(self):
        condition.acquire()
        if len(clients) < n_waiting_chairs:
            clients.append(CLIENT)
            print("new client")
            print("clients waiting = ", len(clients), '/', n_waiting_chairs)
            condition.notify()  # to wake the sleepy barbers

        elif len(clients) == n_waiting_chairs:
            print("barber shop full")
            condition1.wait()  # for generator sleep until barber cut hair
        condition.release()

    def run(self):
        while True:
            self.generate()
            # sleep(randint(0, 3))


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
