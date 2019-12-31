from threading import Thread
import time

def func1():
  while True:
    print 'Working 1'
    time.sleep(1)

def func2():
  while True:
    print 'Working 2'
    time.sleep(2)

Thread(target = func1).start()
Thread(target = func2).start()