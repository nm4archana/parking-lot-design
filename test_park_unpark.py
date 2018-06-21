import unittest
import park_unpark


class TestParkUnpark(unittest.TestCase):

    # Test cases to check 'handicapped' parking
    def test_park_handicapped(self):

        park_unpark.init()
        for i in range(1,22):
            result = park_unpark.park("compact_car", True)
        self.assertEqual(result, (1, 3, 1))
        print "Parking Handicapped Compact Car at Space (1, 3, 1)"
        park_unpark.printlevel()

        park_unpark.init()
        for i in range(1,22):
            result = park_unpark.park("large_car", True)
        self.assertEqual(result, (2, 5, 1))
        print "Parking Handicapped Large Car at Space (2, 5, 1)"
        park_unpark.printlevel()

        park_unpark.init()
        for i in range(1, 142):
            result = park_unpark.park("compact_car", True)
        self.assertEqual(result, (2, 5, 1))
        print "Parking Handicapped Compact Car at Space  (2, 5, 1)"
        park_unpark.printlevel()

        park_unpark.init()
        for i in range(1, 222):
            result = park_unpark.park("compact_car", True)
        self.assertEqual(result, (-1,-1,-1))
        print "Parking Handicapped Compact Car at Space (-1,-1,-1)"
        park_unpark.printlevel()

    # Test cases to check 'compact_car' parking
    def test_park_compact_car(self):

        park_unpark.init()
        for i in range(1,2):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (1, 3, 1))
        print "Parking Compact Car at Space (1, 3, 1)"
        park_unpark.printlevel()


        park_unpark.init()
        for i in range(1,42):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (2, 1, 1))
        print "Parking Compact Car at Space (2, 1, 1)"
        park_unpark.printlevel()


        park_unpark.init()
        for i in range(1, 82):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (3, 1, 1))
        print "Parking Compact Car at Space (3, 1, 1)"
        park_unpark.printlevel()


        park_unpark.init()
        for i in range(1, 202):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (-1,-1,-1))
        print "Parking Compact Car at Space (-1,-1,-1)"
        park_unpark.printlevel()

    # Test cases to check 'large_car' parking
    def test_park_large_car(self):
        park_unpark.init()
        for i in range(1,2):
            result = park_unpark.park("large_car", False)
        self.assertEqual(result, (2, 5, 1))
        print "Parking Large Car at Space (2, 5, 1)"
        park_unpark.printlevel()

        park_unpark.init()
        for i in range(1,42):
            result = park_unpark.park("large_car", False)
        self.assertEqual(result, (3, 5, 1))
        print "Parking Large Car at Space (3, 5, 1)"
        park_unpark.printlevel()

        park_unpark.init()
        for i in range(1, 82):
            result = park_unpark.park("large_car", False)
        self.assertEqual(result, (-1,-1,-1))
        print "Parking Large Car at Space (-1,-1,-1)"
        park_unpark.printlevel()

    # Test cases to check 'compact_car','large_car' and 'handicapped' parking
    def test_park_car(self):
        park_unpark.init()

        for i in range(1,22):
            result = park_unpark.park("compact_car", True)
        self.assertEqual(result, (1, 3, 1))
        print "Parking Handicapped Compact Car at Space (1, 3, 1)"
        park_unpark.printlevel()

        for i in range(1,2):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (1, 3, 2))
        print "Parking Compact Car at Space (1, 3, 2)"
        park_unpark.printlevel()

        for i in range(1, 2):
            result = park_unpark.park("large_car", False)
        self.assertEqual(result, (2, 5, 1))
        print "Parking Large Car at Space (2, 5, 1)"
        park_unpark.printlevel()

        for i in range(1,2):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (1, 3, 3))
        print "Parking Compact Car at Space (1, 3, 3)"
        park_unpark.printlevel()

        for i in range(1,2):
            result = park_unpark.park("compact_car", True)
        self.assertEqual(result, (1, 3, 4))
        print "Parking Handicapped Compact Car at Space (1, 3, 4)"
        park_unpark.printlevel()

    # Test cases to check un-parking
    def test_unpark_car(self):
        park_unpark.init()

        for i in range(1, 22):
            result = park_unpark.park("compact_car", True)
        self.assertEqual(result, (1, 3, 1))
        print "Parking Handicapped Compact Car at Space (1, 3, 1)"
        park_unpark.printlevel()

        for i in range(1, 2):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (1, 3, 2))
        print "Parking Compact Car at Space (1, 3, 2)"
        park_unpark.printlevel()

        for i in range(1, 2):
            result = park_unpark.park("large_car", False)
        self.assertEqual(result, (2, 5, 1))
        print "Parking Large Car at Space (2, 5, 1)"
        park_unpark.printlevel()

        for i in range(1, 2):
            result = park_unpark.park("compact_car", False)
        self.assertEqual(result, (1, 3, 3))
        print "Parking Compact Car at Space (1, 3, 3)"
        park_unpark.printlevel()

        amnt = park_unpark.unpark((1, 3, 3))
        print "Unparking Handicapped Compact car from Space (1, 3, 3) "
        print "Total Amount: ",amnt
        park_unpark.printlevel()

        for i in range(1, 2):
            result = park_unpark.park("compact_car", True)
        self.assertEqual(result, (1, 3, 3))
        print "Unparking Handicapped Compact car from Space(1, 3, 3) after Unparking"
        park_unpark.printlevel()

        amnt = park_unpark.unpark( (1, 3, 1))
        print "Total Amount: ", amnt
        print "Unparking Handicapped Compact Car from Space (1,3,1)"
        park_unpark.printlevel()

        amnt = park_unpark.unpark((1, 3, 2))
        print "Total Amount: ", amnt
        print "Unparking Compact Car from Space (1, 3, 2) "
        park_unpark.printlevel()

        amnt = park_unpark.unpark((2, 5, 1))
        print "Total Amount: ", amnt
        print "Unparking Large Car from Space  (2, 5, 1) "
        park_unpark.printlevel()

        amnt = park_unpark.unpark((1, 1, 1))
        print "Total Amount: ", amnt
        print "Unparking Handicapped Compact car from Apace (1, 1, 1) "
        park_unpark.printlevel()

        park_unpark.park("compact_car",True)
        print "Parking Handicapped Compact car at space (1, 1, 1) after unparking"
        park_unpark.printlevel()
