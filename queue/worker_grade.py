from listQueue import ListQueue
import threading
import time

class Producer: 
    def __init__(self, items):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.worker = threading.Thread(target=self.run)

    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item 
        else: 
            return None 
        
    def run(self):
        while True: 
            time.sleep(0.2)
            if self.__alive:
                item = self.get_item()
                if item is not None:
                    print("Arrived: ", item[1])
                else:
                    print("Arrived: None")
            else:
                break

        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()

class Consumer:
    def __init__(self, queue):
        self.__alive = True
        self.worker = threading.Thread(target=self.run)
        self.queue = queue

    def sort_customer(self):
        self.queue.sort_queue()

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
    consumer.sort_customer()  
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()     #alive -> false -> run함수에서 break
    consumer.finish()
