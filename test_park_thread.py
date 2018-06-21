import threading
import park_unpark
import time


def park_test_one():
    park_unpark.park("compact_car",True)


def park_test_two():
    park_unpark.park("compact_car", False)


def park_test_three():
    park_unpark.park("compact_car", False)


def park_test_four():
    for i in range(1,21):
        park_unpark.park("large_car", True)


def park_test_five():
        park_unpark.park("compact_car", True)
        time.sleep(3)
        amnt = park_unpark.unpark((1,2,5))
        print "****** Unpark (1,2,5) ******"
        print "Total Amount: ",amnt
        park_unpark.printlevel()
        time.sleep(3)
        space = park_unpark.park("compact_car", True)
        print "****** Park",space,"******"
        park_unpark.printlevel()


if __name__ == "__main__":
    t1 = threading.Thread(target=park_test_one, name='t1')
    t2 = threading.Thread(target=park_test_two, name='t2')
    t3 = threading.Thread(target=park_test_three, name='t3')
    t4 = threading.Thread(target=park_test_four, name='t4')
    t5 = threading.Thread(target=park_test_five, name='t5')



    park_unpark.init()

    # starting threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    park_unpark.printlevel()
