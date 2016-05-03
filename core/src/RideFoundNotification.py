from datetime import datetime
from Notification import Notification

class RideFoundNotification(Notification):

    def __init__(self, nid, ride):
        Notification.__init__(self, nid)

        self._ride = ride
        self._message = "Uma carona surgiu"

    def getRide(self):
    	return self._ride

    def getType(self):
        return 'RIDE_FOUND'

    def getData(self):
        result = {}

        result['nid'] = self.getNid()
        result['status'] = self.getSeen()
        result['type'] = self.getType()
        result['date'] = self.getReadableDate()
        result['message'] = self.getMessage()
        result['ride'] = ride.getView()
        result['associatedUser'] = self.ride.getDriver().getPublicView()

        return result
