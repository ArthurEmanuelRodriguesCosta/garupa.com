import unittest
import sys

sys.path.append('../../')
sys.path.append('../')

from core.src.User import User
from core.src.Ride import Ride
from core.src.Address import Address

from datetime import datetime
from time import time

class RideTest(unittest.TestCase):

    def setUp(self):

        self.user1 = User('User1', 'user1@gmail.com', '(83)91234-56789', '114110478', '123456789')
        self.user2 = User('User2', 'user2@gmail.com', '(83)91234-56789', '114110478')

        self.ride1 = Ride(self.user1, 2)
        self.ride2 = Ride(self.user2, 5)

        self.address = Address('Rua da minha casa', 'Meu bairro')

    def test_constructor(self):

        ride = Ride(self.user1, 2)

        self.assertEqual(ride.getDriver(), self.user1)
        self.assertEqual(ride.getNumberOfVacancies(), 2)
        self.assertEqual(ride.isWeekly(), False)
        self.assertEquals(ride.getReadableDate(), datetime.fromtimestamp(int(time())).strftime('%Y-%m-%d'))
        self.assertEqual(ride.isFull(), False)
        self.assertEqual(ride.getNumberOfPassengers(), 0)

        #  Test UID

        self.assertEqual(self.ride1.getUid(), 4)
        self.assertEqual(self.ride2.getUid(), 5)
        self.assertEqual(ride.getUid(), 6)


    def test_addPassenger(self):

        self.assertEqual(self.ride1.isFull(), False)
        self.assertEqual(self.ride1.getNumberOfPassengers(), 0)

        self.ride1.addPassenger(self.user1, self.address)

        self.assertEqual(self.ride1.isFull(), False)
        self.assertEqual(self.ride1.getNumberOfPassengers(), 0)

        self.ride1.addPassenger(self.user2, self.address)

        self.assertEqual(self.ride1.isFull(), False)
        self.assertEqual(self.ride1.getNumberOfPassengers(), 1)

    def test_removePassenger(self):

        self.assertEqual(self.ride1.isFull(), False)
        self.assertEqual(self.ride1.getNumberOfPassengers(), 0)

        self.ride1.addPassenger(self.user1, self.address)

        self.assertEqual(self.ride1.isFull(), False)
        self.assertEqual(self.ride1.getNumberOfPassengers(), 0)

        self.ride1.addPassenger(self.user2, self.address)

        self.assertEqual(self.ride1.isFull(), False)
        self.assertEqual(self.ride1.getNumberOfPassengers(), 1)

        self.ride1.removePassenger(self.user2)

        self.assertEqual(self.ride1.isFull(), False)
        self.assertEqual(self.ride1.getNumberOfPassengers(), 0)

if __name__ == '__main__':
    unittest.main()
