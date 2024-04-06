from listQueue import ListQueue
import threading
import time

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
                if item is not None:
                    print("Arrived: ", item[1])
                else:
                    print("Arrived: None")
                
            else:
                break     #죽임

        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False      #run함수에서 thread 작업을 break하도록 함. 
        self.worker.join()   # join() -> thread가 작업을 마무리하고 break할 때까지 기다렸다가 다 break되면 main도 죽음

class Consumer:
    def __init__(self, queue):
        self.__alive = True
        self.worker = threading.Thread(target = self.run)
        self.queue = queue

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                customer = self.queue.dequeue()
                print("Boarding:", customer[1])
            else: 
                break
        print("Consumer is dying.")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()

if __name__ == "__main__":

    consumer_wq = ListQueue()
    customers = []
    with open("queue/customer.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            customer = line.split()
            customers.append(customer)
            consumer_wq.enqueue(customer)

    # Priority 
    producer = Producer(customers)
    consumer = Consumer(consumer_wq)    
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()     #alive -> false -> run함수에서 break
    consumer.finish()