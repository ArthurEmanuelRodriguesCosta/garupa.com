#coding: utf-8

from datetime import datetime
from Notification import Notification

class FriendRequestNotification(Notification):

    def __init__(self, nid, associatedUser):
        Notification.__init__(self, nid)

        self._associatedUser = associatedUser
        self._message = "enviou uma solicitação de amizade"

    def getAssociatedUser(self):
    	return self._associatedUser

    def getType(self):
        return 'FRIEND_REQUEST'

    def getData(self):
        result = {}

        result['nid'] = self.getNid()
        result['status'] = self.getSeen()
        result['type'] = self.getType()
        result['date'] = self.getReadableDate()
        result['message'] = self.getMessage()
        result['ride'] = ""
        result['associatedUser'] = self.getAssociatedUser().getPublicView()

        return result
