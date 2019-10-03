from threading import Lock, Thread, Condition
from time import sleep
from random import randint

N = 5
THINKING = 0
HUNGRY = 1
EATING = 2

philosophers_state = [0, 0, 0, 0, 0]
mutex = Lock()
condition = Condition(mutex)


def think(index):
    condition.acquire()
    philosophers_state[index] = HUNGRY
    condition.release()


def eat():
    condition.acquire()
    print(philosophers_state)
    condition.release()
    sleep(randint(0, 3))


def take_forks(index, left, right):
    condition.acquire()
    while not (philosophers_state[left] != EATING and philosophers_state[right] != EATING):
        condition.wait()
    philosophers_state[index] = EATING
    condition.release()


def put_forks(index):
    condition.acquire()
    philosophers_state[index] = THINKING
    condition.notify()
    condition.release()


def philosopher(index, left, right):
    while True:
        think(index)
        take_forks(index, left, right)
        eat()
        put_forks(index)


threads = []
for i in range(N):
    left = (i + N - 1) % N
    right = (i + 1) % N
    threads.append(Thread(target=philosopher, args=[i, left, right]))

for i in range(N):
    threads[i].start()

for i in range(N):
    threads[i].join()
