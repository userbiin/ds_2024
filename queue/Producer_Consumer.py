from listQueue import ListQueue
import threading
import time 

import sys
print(sys.path)

class Producer: 
    def __init__(self, items):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.worker = threading.Thread(target = self.run)  #thread는 시킬 일을 인자로 지정해줘야 함. 

    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item 
        else: 
            return None 
        
    def run(self):  #thread에게 해당 작업을 계속 시키냐 죽이냐 
        while True: 
            time.sleep(0.2)
            if self.__alive:       #계속 시킴
                item = self.get_item()
                print("Arrived: ", item)
            else:
                break     #죽임

        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False      #run함수에서 thread 작업을 break하도록 함. 
        self.worker.join()   # join() -> thread가 작업을 마무리하고 break할 때까지 기다렸다가 다 break되면 main도 죽음

class Consumer:
    def __init__(self):
        self.__alive = True
        self.worker = threading.Thread(target = self.run)

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                print("Boarding:")
            else: 
                break
        print("Consumer is dying.")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()
    