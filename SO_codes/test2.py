N = 5
lis = []

first_execution = True

for i in range(N):
    left = i
    right = (i + 1) % N
    lis.append([left, right])

print(lis)

from threading import Lock

mutex = Lock()

print(mutex.acquire(False))
print(mutex.acquire(False))
print(mutex.acquire(False))
print(mutex.acquire(False))