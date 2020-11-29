import random



salary_threshold = 1

class Role:
    TRAINEE = 0
    ENGINEER = 1
    COINMASTER = 2
    HRMITGLIED = 3
    DIRECTOR = 4
    CHAIRMEN_OF_THE_BOARD_OF_DIRECTORS = 5
    CHIEF_STRATEGY_OFFICER = 6
    CHIEF_MARKETING_OFFICER = 7
    CHIEF_DESIGN_OFFICER = 8
    CHIEF_COMMERCIAL_OFFICER = 9
    CHIEF_HUMAN_RESOURCES_OFFICER = 10
    CHIEF_DIGITAL_OFFICER = 11
    CHIEF_INFORMATION_OFFICER = 12
    CHIEF_LEGAL_OFFICER = 13
    CHIEF_TECHNOLOGY_OFFICER = 14
    CHIEF_BUSINESS_DEVELOPMENT_OFFICER = 15
    CHIEF_OPERATING_OFFICER = 16
    CHIEF_OPERATING_OFFICER = 17 
    CHIEF_EXECUTIVE_OFFICER = 18

class Message(): 
    def __init__(self, content, channel): 
        self.content = content
        self.channel = channel


class Tasks:
    MESSAGE = 1 
    POST_MEME = 2
    COFFEE = 3
    BLOWJOB = 4
    def get_random(self, name=False):
        return random.choice(range(4)) + 1

    def get_name(self, task):
        return {
            self.MESSAGE: 'Nachricht',
            self.POST_MEME: 'Meme',
            self.COFFEE: 'Kaffee',
            self.BLOWJOB: 'Blowjob'
        }.get(task)

def role(name):
    return { 
        'Praktikant': Role.TRAINEE,
        'Engineer': Role.ENGINEER, 
        'Coinmaster': Role.COINMASTER, 
        'HR-Mitglied': Role.HRMITGLIED,
        'Director': Role.DIRECTOR,
        'Chairmen of the Board of Directors': Role.CHAIRMEN_OF_THE_BOARD_OF_DIRECTORS,
        'Chief Strategy Officer': Role.CHIEF_STRATEGY_OFFICER,
        'Chief Marketing Officer': Role.CHIEF_MARKETING_OFFICER,
        'Chief Design Officer': Role.CHIEF_DESIGN_OFFICER,
        'Chief Marketing Officer': Role.CHIEF_MARKETING_OFFICER,
        'Chief Commercial Officer': Role.CHIEF_COMMERCIAL_OFFICER, 
        'Chief Human Resources Officer': Role.CHIEF_HUMAN_RESOURCES_OFFICER,
        'Chief Digital Officer': Role.CHIEF_DIGITAL_OFFICER,
        'Chief Information Officer': Role.CHIEF_INFORMATION_OFFICER,
        'Chief Legal Officer': Role.CHIEF_LEGAL_OFFICER,
        'Chief Technology Officer': Role.CHIEF_TECHNOLOGY_OFFICER,
        'Chief Business Development Officer': Role.CHIEF_BUSINESS_DEVELOPMENT_OFFICER,
        'Chief Operating Officer': Role.CHIEF_OPERATING_OFFICER,
        'Chief Executive Officer': Role.CHIEF_EXECUTIVE_OFFICER
    }.get(name, Role.TRAINEE)

def salary_of(role): 
    return {
        Role.TRAINEE: 1000, 
        Role.ENGINEER: 1500, 
        Role.COINMASTER: 2000, 
        Role.HRMITGLIED: 2500, 
        Role.DIRECTOR: 3000,
        Role.CHAIRMEN_OF_THE_BOARD_OF_DIRECTORS: 3500,
        Role.CHIEF_STRATEGY_OFFICER: 4000,
        Role.CHIEF_MARKETING_OFFICER: 4000,
        Role.CHIEF_MARKETING_OFFICER: 4500,
        Role.CHIEF_DESIGN_OFFICER: 5000,
        Role.CHIEF_COMMERCIAL_OFFICER: 5000,
        Role.CHIEF_HUMAN_RESOURCES_OFFICER: 5000,
        Role.CHIEF_DIGITAL_OFFICER: 5000,
        Role.CHIEF_INFORMATION_OFFICER: 5500,
        Role.CHIEF_LEGAL_OFFICER: 6000,
        Role.CHIEF_TECHNOLOGY_OFFICER: 6500,
        Role.CHIEF_BUSINESS_DEVELOPMENT_OFFICER: 7000,
        Role.CHIEF_OPERATING_OFFICER: 12000,
        Role.CHIEF_EXECUTIVE_OFFICER: 20000 
    }.get(role, 1000)

params = { 
    'starting xp': 0, 
    'starting money': 10,
    'starting workdone': 0
}

LOG_TIME = 5
AVAILABLE_TASKS_NUM = 5

NEWS_TIME = 100

def message_of(request, state, var):
    return {
        'salary': [f'```Ihr Gehalt betraegt {var}$.```'],
        'balance': [f'```Aktuell befinden sich {var}$ in ihrem Besitz.```'],
        'workdone': [f'```Du hast {var}/{10} von deiner Arbeit geschafft.```'],
        'gettask': {
            0:f'```{var}```', 
            1:f'```du hast {var} gewaehlt.```', 
            'A':f'```u hast bereits eine laufende Aufgabe: {var}```'
            }
    }.get(request)[state]



class State:
    OK = 1
    NO_UPDATE = 2
    FAILED = 3

class ItemCats: 
    FOOD = 1

class Food: 
    CORN_DOG = 1
    KEBAP = 2
    HAMBURGER = 3
    CRAZY_HAMBURGER = 4
    BANANA = 5
    HOTDOG = 6

