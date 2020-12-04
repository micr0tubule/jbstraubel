from ..request import Request, change_state
from storage import storage
from global_vars import message_of, salary_of, Message


class Salary(Request): 
    '''
    state 0: user just made the !salary restquest
    '''
    def __init__(self, message):
        super().__init__(1, message) 

    @change_state
    def work(self, message=None):
        for u in storage.users: 
            if u.id.val == self.requester.id:
                return True, Message(
                    content=message_of('salary', self.state, salary_of(u.role.val)), 
                    channel=self.channel)
    

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