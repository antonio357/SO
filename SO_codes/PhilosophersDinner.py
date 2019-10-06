from threading import Lock, Condition, Thread
from time import sleep

EATING = 2
HUNGRY = 1
THINKING = 0

N = 5
philosophers_states = []
philosophers_threads = []

mutex = Lock()
condition = Condition(mutex)


def think(index):
    condition.acquire()
    philosophers_states[index] = HUNGRY
    condition.release()


def eat():
    condition.acquire()
    print(philosophers_states)
    sleep(1)
    condition.release()


def take_forks(index, left_index, right_index):
    condition.acquire()
    while philosophers_states[left_index] == EATING or philosophers_states[right_index] == EATING:
        condition.wait()
    philosophers_states[index] = EATING
    condition.release()


def put_forks(index):
    condition.acquire()
    philosophers_states[index] = THINKING
    condition.notify_all()
    condition.release()


def philosopher_run(index, left_index, right_index):
    while True:
        think(index)
        take_forks(index, left_index, right_index)
        eat()
        put_forks(index)


for i in range(N):
    left_index = (i + N - 1) % N
    right_index = (i + 1) % N
    philosophers_threads.append(Thread(target=philosopher_run, args=[i, left_index, right_index]))
    philosophers_states.append(THINKING)

for philosopher in philosophers_threads:
    philosopher.start()

for philosopher in philosophers_threads:
    philosopher.join()
