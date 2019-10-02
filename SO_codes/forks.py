from threading import Lock, Thread
from time import sleep
from random import randint

N = 0
THINKING = 0
HUNGRY = 1
EATING = 2

philosophers_state = [0, 0, 0, 0, 0]
mutex = Lock()


def think(index):
    mutex.acquire()
    philosophers_state[index] = HUNGRY
    mutex.release()


def eat():
    sleep(randint(0, 3))
    mutex.acquire()
    print(philosophers_state)
    mutex.release()


def take_forks(index, left, right):
    mutex.acquire()
    if philosophers_state[left] != EATING and philosophers_state[right] != EATING:
        philosophers_state[index] = EATING
    mutex.release()


def put_forks(index):
    mutex.acquire()
    philosophers_state[index] = THINKING
    mutex.release()


def philosopher(index, left, right):
    while True:
        # think(index)
        # take_forks(index, left, right)
        # eat()
        # put_forks(index)
        mutex.acquire()
        print("ok")
        mutex.release()


threads = []
for i in range(N):
    left = (i + N - 1) % N
    right = (i + 1) % N
    threads.append(Thread(target=philosopher, args=[i, left, right]))

for i in range(N):
    threads[i].start()

for i in range(N):
    threads[i].join()
