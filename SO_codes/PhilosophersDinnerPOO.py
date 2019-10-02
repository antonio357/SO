from time import sleep
from random import randint
from threading import Lock, Thread

N = 5
THINKING = 0
HUNGRY = 1
EATING = 2
philosophers = []


class Philosopher(Thread):

    global N
    forks = []
    mutex = Lock()
    lis = []
    for i in range(N):
        forks.append(Lock())

    def __init__(self, index):
        Thread.__init__(self)
        self.state = THINKING
        self.left_fork = self.forks[index]
        self.right_fork = self.forks[(index + 1) % N]

    def think(self):
        self.mutex.acquire()
        self.lis.clear()
        for i in range(N):
            self.lis.append(philosophers[i].state)
        print(self.lis)
        for i in self.lis:
            left = (i + N - 1) % N
            right = (i + 1) % N
            if self.lis[left] + self.lis[i] == EATING * 2 or self.lis[right] + self.lis[i] == EATING * 2:
                while True:
                    print("bug = ", self.lis)
        self.mutex.release()

    def eat(self):
        # sleep(randint(0, 3))
        pass

    def take_forks(self):
        self.state = HUNGRY
        self.mutex.acquire()
        self.left_fork.acquire()
        self.right_fork.acquire()
        self.state = EATING
        # else:
        #     if not self.left_fork.acquire(blocking=False):
        #         self.left_fork.release()
        #     if not self.right_fork.acquire(blocking=False):
        #         self.right_fork.release()
        self.mutex.release()

    def put_forks(self):
        self.mutex.acquire()
        if self.state == EATING:
            self.left_fork.release()
            self.right_fork.release()
            self.state = THINKING
        self.mutex.release()

    def run(self):
        while True:
            self.think()
            self.take_forks()
            self.eat()
            self.put_forks()


for i in range(N):
    philosophers.append(Philosopher(index=i))

for i in range(N):
    philosophers[i].start()

for i in range(N):
    philosophers[i].join()
