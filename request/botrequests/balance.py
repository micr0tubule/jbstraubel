from ..request import Request, change_state
from global_vars import State, Message, message_of
from storage import storage

class Balance(Request):
    def __init__(self, message):
        super().__init__(1, message)

    @change_state
    def work(self, message=None):
        for u in storage.users:
            if u.id.val == self.requester.id:
                return True, Message(
                    content=message_of('balance', self.state, u.money.val),
                    channel=self.channel)
