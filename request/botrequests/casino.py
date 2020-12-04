from ..request import Request, change_state
import random 
from global_vars import Message
import discord 
from functools import singledispatch
from storage import storage
from global_vars import State

class Hand: 
    def __init__(self, player=None): 
        self.player = player
        self.cards = []
        self.commitment = None

class Casino(Request):
    def __init__(self, message, client):
        super().__init__(5, message)
        self.client_reference = client
        self.channel = discord.utils.get(client.guilds[0].channels, id=783111605289353257)         
        self.hands = []
        self.dealer_hand = self.givecards(Hand())
        self.pointer = 0
        print('heloo')


    def givecards(self, hand):
        for i in range(2):  
            card = (random.randint(2, 11), random.randint(1, 4))
            hand.cards.append(card)
        return hand
    
    def givecard(self, hand): 
        card = (random.randint(2, 11), random.randint(1, 4))
        hand.cards.append(card)

    def commitcommitment(self, hand, commitment): 
        hand.commitment = commitment
        hand.player.money(hand.player.money.val - commitment) 

    def getimage(self, card):
        if card[1] == 1: 
            return self.diamonds(card[0])
        elif card[1] == 2: 
            return self.clubs(card[0])
        elif card[1] == 3: 
            return self.hearts(card[0])
        else: 
            return self.spades(card[0])

    def diamonds(self, value): 
        return {
            2: '🃂 (2D)', 3: '🃃 (3D)', 4: '🃄 (4D)',
            5: '🃅 (5D)', 6: '🃆 (6D)', 7: '🃇 (7D)',
            8: '🃈 (8D)', 9: '🃉 (9D)', 10: '🃊 (10D)',
            'B': '🃋 (BD)', 'Q': '🃍 (QD)',
            'K': '🃎 (KD)', 'A': '🃑 (AD)'
        }.get(value)
    
    def clubs(self, value): 
        return {
            2: '🃒 (2C)', 3: '🃓 (3C)', 4: '🃔 (4C)',
            5: '🃕 (5C)', 6: '🃖 (6C)', 7: '🃗 (7C)',
            8: '🃘 (8C)', 9: '🃙 (9C)', 10: '🃚 (10C)',
            'B': '🃛 (BC)', 'Q': '🃝 (BC)',
            'K': '🃞 (KC)', 'A': '🃑 (AC)'
        }.get(value)

    def hearts(self, value): 
        return {
            2: '🂲 (2H)', 3: '🂳 (3H)', 4: '🂴 (4H)',
            5: '🂵 (5H)', 6: '🂶 (6H)', 7: '🂷 (7H)',
            8: '🂸 (8H)', 9: '🂹 (9H)', 10: '🂺 (10H)',
            'B': '🂻 (BH)', 'Q': '🂽 (QH)',
            'K': '🂾 (KH)', 'A': '🂱 (AH)'
        }.get(value)

    def spades(self, value): 
        return {
            2: '🂢 (2S)', 3: '🂣 (3S)', 4: '🂤 (4S)',
            5: '🂥 (5S)', 6: '🂦 (6S)', 7: '🂧 (7S)',
            8: '🂨 (8S)', 9: '🂩 (9S)', 10: '🂪 (10S)',
            'B': '🂫 (BS)', 'Q': '🂭 (QS)',
            'K': '🂮 (KS)', 'A': '🂡 (AS)'
        }.get(value)

    def validate_join(self, player): 
        for hand in self.hands: 
            if hand.player == player: 
                return False, (State.NO_UPDATE, Message(
                    content='du bist bereits in der Runde',
                    channel=self.channel))
        if len(self.hands) == 5: 
            return False, (State.NO_UPDATE, Message(
                content='die Runde ist bereits voll',
                channel=self.channel))
        return True, (None, None)
    
    def validate_hand(self, hand): 
        if sum([card[0] for card in hand.cards]) > 21: 
            return False
        else: 
            return True
    
    def construct_hands_display(self): 
        pass 



    @change_state
    def work(self, message): 
        if self.state == 0:
            if message.content == '!blackjack': 
                return State.NO_UPDATE, Message(
                    content='waiting for players', 
                    channel=self.channel)
            if message.content == '!join': 
                player = storage.get_user(message.author.id)
                join_validation, payload = self.validate_join(player)
                if join_validation: 
                    self.hands.append(Hand(player))
                    return State.NO_UPDATE, Message(
                        content=f'{len(self.hands)}/5 Spieler!',
                        channel=self.channel)
                else: 
                    return State.NO_UPDATE, payload

            elif message.content == '!start' and len(self.hands) >= 1:
                first = self.client_reference.guilds[0].get_member(self.hands[self.pointer].player.id.val).name
                self.pointer += 1
                return State.OK, [
                Message(
                    content='initialisiere Spiel..',
                    channel=self.channel),
                Message(
                    content=f'@{first} was setzen Sie?',
                    channel=self.channel) 
                ]
            else: 
                return State.SKIP, None
                    
        elif self.state == 1:
            try: 
                commitment = int(message.content[1:])
                if commitment > self.hands[self.pointer-1].player.money.val: 
                    return State.NO_UPDATE, Message(
                        content=f'dein Geld reicht nicht aus',
                        channel=self.channel) 
                else: 
                    self.commitcommitment(self.hands[self.pointer-1], commitment)
                if len(self.hands) == self.pointer:
                    msg = ''
                    for hand in self.hands: 
                        name = self.client_reference.guilds[0].get_member(hand.player.id.val).name
                        self.givecards(hand)
                        card_string = ' '.join([self.getimage(card) for card in hand.cards])
                        msg += f'{name}: {card_string} \n'
                    dealer_string = ' '.join([self.getimage(card) for card in self.dealer_hand.cards])
                    msg += f'dealer hand: {dealer_string}'

                    self.pointer = 0
                    first = self.client_reference.guilds[0].get_member(self.hands[self.pointer].player.id.val).name

                    return State.OK, [
                        Message(
                            content=f'```{msg}```',
                            channel=self.channel), 
                        Message(
                            content=f'@{first} haetten Sie gerne noch eine Karte?',
                            channel=self.channel
                    )]
                    
                name = self.client_reference.guilds[0].get_member(self.hands[self.pointer].player.id.val).name
                self.pointer += 1
                return State.NO_UPDATE, Message(
                    content=f'@{name} was setzen Sie?',
                    channel=self.channel
                )
            except ValueError as e:  
                print(e)
                return State.NO_UPDATE, None
            pointer +=1
        elif self.state == 2: 
            if message.content[1:] == 'ja': 
                self.givecard(self.hands[self.pointer])
                msg = ''
                for hand in self.hands: 
                    name = self.client_reference.guilds[0].get_member(hand.player.id.val).name
                    card_string = ' '.join([self.getimage(card) for card in hand.cards])
                    msg += f'{name}: {card_string} \n'
                dealer_string = ' '.join([self.getimage(card) for card in self.dealer_hand.cards])
                msg += f'dealer hand: {dealer_string}'

                if self.validate_hand(self.hands[self.pointer]): 
                    name = self.client_reference.guilds[0].get_member(self.hands[self.pointer].player.id.val).name
                    return State.NO_UPDATE, [
                        Message(
                            content=f'```{msg}```',
                            channel=self.channel),
                        Message(
                            content=f'@{name} haetten Sie gerne noch eine Karte?',
                            channel=self.channel)]
                else: 
                    self.hands.remove(self.hands[self.pointer])
                    self.pointer += 1
                    name = self.client_reference.guilds[0].get_member(self.hands[self.pointer].player.id.val).name
                    return State.NO_UPDATE, [
                        Message(
                            content='schade!',
                            channel=self.channel),
                        Message(
                            content=f'```{msg}```',
                            channel=self.channel), 
                        Message(
                            content=f'@{name} haetten Sie gerne noch eine Karte?',
                            channel=self.channel)]

            else: 
                self.pointer += 1
                name = self.client_reference.guilds[0].get_member(self.hands[self.pointer].player.id.val).name
                return Message(
                    content=f'{name} haetten Sie gerne noch eine Karte?',
                    channel=self.channel
                )    

        







