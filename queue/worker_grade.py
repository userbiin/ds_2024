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

def sort_customers(customers):
    sorted_customers = [[], [], []]  # 각 등급에 대한 리스트 초기화
    for customer in customers:
        grade = int(customer[0]) - 1  # 등급에 맞는 인덱스 계산
        sorted_customers[grade].append(customer)  # 해당 등급 리스트에 고객 추가
    return sorted_customers

if __name__ == "__main__":
    consumer_wq = ListQueue()
    customers = []
    with open("queue/customer.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            customer = line.split()
            customers.append(customer)
    sorted_customers = sort_customers(customers)

    producer = Producer(sum(sorted_customers, []))  # 등급 순서에 맞게 합친 리스트를 생성자에 전달
    consumer = Consumer(consumer_wq)    
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()
    consumer.finish()
