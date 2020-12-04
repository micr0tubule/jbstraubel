from ..request import Request, change_state 
from global_vars import Message, State

class AmongUsMaps(Request): 
    def __init__(self, message=None):
        super().__init__(1, message)
    
    def parse_message(self, message):
        splitted = message.content.split() 
        return splitted[1].lower() if len(splitted) > 1 else False


    @change_state
    def work(self, message): 
        if self.state == 0:
            parsed = self.parse_message(message)

            skeld = Message(
                    content='https://prod.cdn.earlygame.com/uploads/images/_imageBlock/SKELD_MAP-1.jpg?mtime=20201022122655&focal=none&tmtime=20201022132145',
                    channel=self.channel)

            mirahq = Message(
                    content='https://prod.cdn.earlygame.com/uploads/images/_imageBlock/3900598/Mirahq.jpg?mtime=20201022124132&focal=none&tmtime=20201022132151',
                    channel=self.channel)

            polus = Message(
                    content='https://prod.cdn.earlygame.com/uploads/images/_imageBlock/3904024/Polus.jpg?mtime=20201022125504&focal=none&tmtime=20201022132152',
                    channel=self.channel)

            lazytown = Message(
                content='https://i.ytimg.com/vi/UTdSA_zPNmM/hqdefault.jpg',
                channel=self.channel)
                
            msg = {
                'skeld': skeld,
                'mirahq': mirahq,
                'polus': polus,
                'nuttensohn': lazytown
            }.get(parsed, [skeld, mirahq, polus])
            print(msg)
            return State.OK, msg