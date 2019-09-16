from threading import Lock, Condition
from time import sleep

FORKS = [0, 1, 2, 3, 4]

mutex = Lock()
condition = Condition(mutex)

class Philosopher():

    def __init__(self, name, left_fork, right_fork):
        self. name = name
        self.state = "hungry"
        self.left_fork = left_fork
        self.right_fork = right_fork

    def take_forks(self):
        FORKS.remove(self.left_fork)
        FORKS.remove(self.right_fork)

    def put_forks(self):
        FORKS.insert(index=self.left_fork, object=self.left_fork)
        FORKS.insert(index=self.left_fork, object=self.left_fork)

    def think(self):
        self.state = "thinking"
        print("philosopher ", self.name,  " its thinking")

    def eat(self):
        self.state = "eating"
        print("philosopher ", self.name,  " its eating, with forks = ", tuple(self.left_fork, self.right_fork))

    def hungry(self):
        self.state = "hungry"
        print("philosopher ", self.name,  " its hungry")

    def philosopher(self):
        self.think()
        self.take_forks()
        self.eat()
        self.put_forks()

name_lis = ["Antonio", "Erick", "Isaque", "Ailson", "Stefano"]
