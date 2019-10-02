from time import sleep
from random import randint
from threading import Lock, Thread

N = 5
THINKING = 0
HUNGRY = 1
EATING = 2
philosophers = []


class Fork():
    def __init__(self):
        self.on_table = True

    def get_taken(self):
        if self.on_table:
            self.on_table = False
            return True
        return False

    def get_returned(self):
        if not self.on_table:
            self.on_table = True


class Philosopher(Thread):

    global N, philosophers
    forks = []
    mutex = Lock()
    forks_mutex = []
    for i in range(N):
        forks.append(Fork())
        forks_mutex.append(Lock())

    def __init__(self, index):
        Thread.__init__(self)
        self.state = THINKING
        self.left_fork = self.forks[index]
        self.right_fork = self.forks[(index + 1) % N]
        self.left_fork_mutex = self.forks_mutex[index]
        self.right_fork_mutex = self.forks_mutex[(index + 1) % N]


    def set_state(self, state):
        # self.mutex.acquire()
        self.state = state
        # self.mutex.release()

    def think(self):
        # self.mutex.acquire()
        print([philosophers[0].state, philosophers[1].state, philosophers[2].state, philosophers[3].state, philosophers[4].state])
        # self.mutex.release()

    def eat(self):
       pass

    def take_forks(self):
        self.left_fork_mutex.acquire()
        self.right_fork_mutex.acquire()

        self.set_state(HUNGRY)
        if self.left_fork.get_taken() and self.right_fork.get_taken():
            self.set_state(EATING)

        self.left_fork_mutex.release()
        self.right_fork_mutex.release()

    def put_forks(self):
        self.left_fork_mutex.acquire()
        self.right_fork_mutex.acquire()

        self.left_fork.get_returned()
        self.right_fork.get_returned()
        self.set_state(THINKING)

        self.left_fork_mutex.release()
        self.right_fork_mutex.release()

    def run(self):
        while True:
            self.think()
            self.mutex.acquire()
            self.take_forks()
            self.mutex.release()
            self.eat()
            self.mutex.acquire()
            self.put_forks()
            self.mutex.release()




for i in range(N):
    philosophers.append(Philosopher(index=i))

for i in range(N):
    philosophers[i].start()

for i in range(N):
    philosophers[i].join()
