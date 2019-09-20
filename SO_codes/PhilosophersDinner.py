from threading import Lock, Condition, Thread
from time import sleep

mutex = Lock()
condition = Condition(mutex)

def think(name):
    mutex.acquire()
    print("philosopher ", name, " is thinking")
    mutex.release()

def eat(name):
    mutex.acquire()
    print("philosopher ", name, " is eating")
    mutex.release()

def take_forks(name, left_fork, right_fork):
    mutex.acquire()
    print("philosopher ", name, " is taking forks = ", [left_fork, right_fork])
    mutex.release()

def put_forks(name, left_fork, right_fork):
    mutex.acquire()
    print("philosopher ", name, " is putting forks = ", [left_fork, right_fork])
    mutex.release()

def philosopher(name, left_fork, right_fork):
    print("philosopher ", name, " its in place")
    think(name)
    take_forks(name, left_fork, right_fork)
    eat(name)
    put_forks(name, left_fork, right_fork)

N = 5
names = ["Antonio", "Erick", "Isaque", "Ailson", "Stefano"]
philosophers = []

for i in range(N):
    name = names[i]
    left_fork = (i + N - 1) % N
    right_fork = (i + 1) % N
    philosopherX = Thread(target=philosopher, args=[name, left_fork, right_fork])
    philosophers.append(philosopherX)