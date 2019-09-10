from random import randint
import threading
from time import sleep
from sys import exit

BUFFER_SIZE = 10

buffer = []

"""
to solve this problem it is needed a Condition Object to be associated to a Lock Object
"""
mutex = threading.Lock()
threading.Condition(mutex)


def fill_buffer():

    while True:
        mutex.acquire()

        if len(buffer) < BUFFER_SIZE:
            value = randint(0, 9)
            buffer.append(value)
            sleep(2)
            print("Produced ", value, ", len(buffer) = ", len(buffer))

        mutex.release()


def consume_buffer():

    while True:
        mutex.acquire()

        if len(buffer) > 0:
            value = buffer.pop(0)
            sleep(2)
            print("Consumed ", value, ", len(buffer) = ", len(buffer))

        mutex.release()


producer = threading.Thread(target=fill_buffer)
consumer = threading.Thread(target=consume_buffer)


"""
its necessary to .start() all the threads before .join() any of threads, otherwise it does not execute the threads in 
parallel
"""
producer.start()
consumer.start()
producer.join()
consumer.join()
