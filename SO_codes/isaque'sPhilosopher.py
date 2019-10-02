import threading
import random
import time


class Philosopher(threading.Thread):
    running = False

    def __init__(self, name, forkLeft, forkRight):
        threading.Thread.__init__(self)  # super method constructor
        self.name = name
        self.forkLeft = forkLeft
        self.forkRight = forkRight

    def run(self):
        while (Philosopher.running):
            print(self.name, "is thinking.")
            time.sleep(random.randint(0, 2))  # thinking
            print(self.name, "want to eat")
            self.eat()

    def eat(self):
        forkL, forkR = self.forkLeft, self.forkRight
        while (self.running):
            forkL.acquire(True)
            locked = forkR.acquire(False)  # don't block
            if locked: break
            forkL.release()
            print(f"{self.name} swaps forks")
            forkL, forkR = forkR, forkL
        else:
            return

        self.eating()
        forkR.release()
        forkL.release()

    def eating(self):
        print(f"{self.name} is eating..")
        time.sleep(random.randint(0, 2))
        print(f"{self.name} is done eating..")


forks = [threading.Lock() for n in range(3)]
philosopher_names = ('Aristotle', 'Kant', 'Buddha')

philosophers = [Philosopher(philosopher_names[i], forks[i % 3], forks[(i + 1) % 3]) \
                for i in range(3)]

random.seed(507129)
Philosopher.running = True
for p in philosophers: p.start()
time.sleep(100)
Philosopher.running = False
print("Now we're finishing.")