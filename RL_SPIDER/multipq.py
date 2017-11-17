import multiprocessing
import numpy as np

class Producer():
    def __init__(self):
        pass
    def producer(self,q):
        for i in range(100):
            q.put(np.random.uniform(-1,0,1000))

class Consumer():
    def __init__(self):
        pass
    def consumer(self,q):
        while True:
            while q.empty() is False:
                print(q.get())
                
            
def Main():
    qu=multiprocessing.Queue()
    qu.put(9)
    P=Producer()
    C=Consumer()
    con=multiprocessing.Process(target=C.consumer,args=(qu,))
    prod=multiprocessing.Process(target=P.producer,args=(qu,))
    con.start()
    prod.start()

    con.join()
    prod.join()
if __name__ == '__main__':
    Main()
