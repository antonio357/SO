from threading import Semaphore, Lock, Thread
from time import sleep
from random import randint

N = 5
THINKING = 0
HUNGRY = 1
EATING = 2
mutex = Lock()
semaphores = []
states = []

for i in range(N):
    semaphores.append(Semaphore(0))
    states.append(THINKING)


def test(i, LEFT, RIGHT):
    if states[i] == HUNGRY and states[LEFT] != EATING and states[RIGHT] != EATING:
        states[i] = EATING
        semaphores[i].release()

def verify():
    for i in range(N):
        left = (i + N - 1) % N
        right = (i + 1) % N
        left_sum = states[i] + states[left]
        right_sum = states[i] + states[right]
        if left_sum == EATING * 2 or right_sum == EATING * 2:
            return False
        return True

def think():
    mutex.acquire()
    if verify() is False:
        print(states)
        while True:
            print("deu treta")
    print(states)
    mutex.release()
    # sleep(3)


def eat():
    mutex.acquire()
    print(states)
    mutex.release()
    # sleep(3)


def take_forks(i, LEFT, RIGHT):
    mutex.acquire()
    states[i] = HUNGRY
    test(i, LEFT, RIGHT)
    mutex.release()
    semaphores[i].acquire()


def put_forks(i, LEFT, RIGHT):
    mutex.acquire()
    states[i] = THINKING
    test(LEFT, LEFT, RIGHT)
    test(RIGHT, LEFT, RIGHT)
    mutex.release()


def philosopher(i, LEFT, RIGHT):
    while True:
        think()
        take_forks(i, LEFT, RIGHT)
        eat()
        put_forks(i, LEFT, RIGHT)

threads = []
for i in range(N):
    left = (i + N - 1) % N
    right = (i + 1) % N
    name = i
    threads.append(Thread(target=philosopher, args=[name, left, right]))

for i in range(N):
    threads[i].start()

for i in range(N):
    threads[i].join()
