import vk
import random

class vkAPI(vk.API):
    def __init__(self, session, token, *args, **kwargs):
        super().__init__(session, *args, **kwargs)
        self.token = token
    
    def send(self, peer_id, *args, **kwargs):
        ans = self.messages.send(
            access_token=self.token,
            peer_id=str(peer_id),
            random_id=random.randint(0, 18446744073709551615),
            *args,
            **kwargs
        )
        return ans

    def sendMessage(self, peer_id, message):
        ans = self.send(peer_id=peer_id, message=str(message))
        return ans

    def sendSticker(self, peer_id, sticker_id):
        ans = self.send(peer_id=peer_id, sticker_id=sticker_id)
        return ans

    def getSelfInfo(self):
        ans = self.groups.getById(
            access_token=self.token
        )
        return ans

    def markAsRead(self, peer_id):
        ans = api.messages.markAsRead(
            access_token=self.token,
            peer_id=str(peer_id),
            mark_conversation_as_read=1
        )
        return ans
    
    def setActivity(self, peer_id):
        api.messages.setActivity(
            access_token=self.token,
            peer_id=str(peer_id),
            type='typing'
        )
    

    def getConversationsById(self, peer_id):
        api.messages.getConversationsById(
            access_token=self.token,
            peer_ids=peer_id
        )

token = "f855540f5998bf973ebad153eae7df2af6106301da411e78ae77c471c48c1131f7f81ad6820c57b6d34a3"
session = vk.Session()
api = vkAPI(session, token, v="5.122")
api.sendMessage(245725904, "Привет.")
api.sendSticker(245725904, 9037)
print(api.getSelfInfo()[0]['name'])
