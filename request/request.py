from storage import storage
from global_vars import State

class Request:
    '''
    ATTRIBUTES 
    state: current state of process of the request 
    complete: at what sate the request is finished 
    done: state == complete 
    '''
    def __init__(self, complete, message=None): 
        print(message)
        self.state = 0
        self.complete = complete
        self.done = False
        if message: 
            self.channel = message.channel
            self.requester = message.author

    def attach_payload(self, payload):
        self.payload = payload 

def change_state(function):
    def wrapper(self, message):
        state, payload = function(self, message)
        if state == State.SKIP: 
            return False, payload
        if state == State.OK:
            self.state += 1
            print('added 1 to state of ', type(self), self.state)
            self.done = self.state == self.complete
        elif state == State.FAILED:
            self.done = True
        return True, payload
    return wrapper
