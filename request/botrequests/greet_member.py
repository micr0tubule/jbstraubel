import discord
from ..request import Request, change_state
from global_vars import State, Message

class GreetMember(Request): 
    def __init__(self, member, client): 
        super().__init__(1)
        self.member = member
        self.channel = discord.utils.get(client.guilds[0].channels, id=782953651978633246)

    @change_state
    def work(self, message=None): 
        return State.OK, Message(
            content=f'```@{self.member.name} Willkommen bei Mesla Totors!```',
            channel=self.channel)