    from multiprocessing import Process

    import serial
    import time


    class MySerialManager(Process):
        def __init__(self, serial_port, baudrate=115200, timeout=1):
            super(MySerialManager, self).__init__(target=self.loop_iterator,args=(serial_port, baudrate, timeout))
            # As soon as you uncomment this, you'll get an error.
            # self.ser = serial.Serial(serial_port, baudrate=baudrate, timeout=timeout)

        def loop_iterator(self,serial_port, baudrate,timeout):
            ser = serial.Serial(serial_port, baudrate=baudrate, timeout=timeout)
            self.loop(ser)

        def loop(self,ser):
            # Just some simple action for simplicity.
            #you can use ser here
            for i in range(3):
                print("hi")
                time.sleep(1)


    if __name__ == "__main__":
        msm = MySerialManager("COM4")
        try:
            msm.start()
        except KeyboardInterrupt:
            print("caught in main")
        finally:
            msm.join()