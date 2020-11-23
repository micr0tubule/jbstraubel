import os 
import pandas as pd 
from global_vars import Role, params
import random

userframe = pd.read_csv('data/users.csv')
jobframe = pd.read_csv('data/jobs.csv')
inventoryframe = pd.read_csv('data/inventory.csv')

class val(object):
    def __init__(self, val, name, pos, dataframe): 
        self.__dict__['val'] = val
        self.__dict__['name'] = name
        self.__dict__['pos'] = pos
        self.__dict__['dataframe'] = dataframe

    def __call__(self, val):
        self.__dict__['val'] = val
        self.dataframe[self.name][self.pos] = val


class User(object): 
    def __init__(self, id, experience, money, role, work_done, pos): 
        self.id = val(id, 'id', pos, userframe)
        self.experience = val(experience, 'experience', pos, userframe)
        self.money = val(money, 'money', pos, userframe) 
        self.role = val(role, 'role', pos, userframe)
        self.work_done = val(work_done, 'work_done', pos, userframe)

    def __getattribute__(self, attr):
        return object.__getattribute__(self, attr)


class Job(object):
    def __init__(self, typus, user_id, state, pos):
        self.user_id = val(user_id, 'user_id', pos, jobframe)
        self.state = val(state, 'state', pos, jobframe)
        self.typus = typus
    
    def __getattribute__(self, attr):
        return object.__getattribute__(self, attr)


class Item(object): 
    def __init__(self, user_id, category, subcategory, pos):
        self.user_id = val(user_id, 'user_id', pos, inventoryframe)
        self.category = val(category, 'category', pos, inventoryframe)
        self.subcategory = val(subcategory, 'subcategory', pos, inventoryframe)
    
    def __getattribute__(self, attr): 
        return object.__getattribute__(self, attr)

    
class Storage: 
    def __init__(self):
        self.users = self.construct_users()
        self.jobs = self.construct_jobs()
        self.items = self.construct_items()
        self.available_tasks = []
        
    def save_df(self, df, filename):
        df.to_csv(filename, index=False)

        
    def construct_users(self):
        return [
            User(
                userframe['id'][i], 
                userframe['experience'][i], 
                userframe['money'][i], 
                userframe['role'][i], 
                userframe['work_done'][i], i
                ) for i in userframe.index]


    def construct_jobs(self):
        return [
            Job(
                jobframe['user_id'][i],
                jobframe['typus'][i],
                jobframe['state'][i], i
            ) for i in jobframe.index
        ]
    
    def construct_items(self): 

        for i in inventoryframe.index:
            print(i)

        return [
            Item(
                inventoryframe['user_id'][i], 
                inventoryframe['category'][i],
                inventoryframe['subcategory'][i], i
            ) for i in inventoryframe.index
        ]


    def insert_new_user(self, id): 
        global userframe
        row = [
            id, 
            params['starting xp'], 
            params['starting money'],
            Role.TRAINEE,
            params['starting workdone']
        ]
        row_df = pd.DataFrame([row], columns=['id', 'experience', 'money', 'role', 'work_done'])
        userframe = pd.concat([row_df, userframe], ignore_index=True)
        self.users = self.construct_users()

    
    def insert_new_job(self, typus, user_id, state):
        global jobframe
        row = [
            user_id, 
            typus,
            state
        ]
        row_df = pd.DataFrame([row], columns=['user_id', 'typus', 'state'])
        jobframe = pd.concat([row_df, jobframe], ignore_index=True)
        self.save_df(jobframe, 'data/jobs.csv')
        self.jobs = self.construct_jobs()
    

    def insert_new_item(self, user_id, category, subcategory): 
        global inventoryframe
        row = [
            user_id,
            category,
            subcategory
        ]
        row_df = pd.DataFrame([row], columns=['user_id', 'category', 'subcategory'])
        inventoryframe = pd.concat([row_df, inventoryframe], ignore_index=True)
        self.save_df(inventoryframe, 'data/inventory.csv')
        self.items = self.construct_items()


    def get_job_by_user_id(self, user_id):
        for job in self.jobs:
            if job.user_id.val == user_id:
                return job

    def get_items_by_user_id(self, user_id):
        return [item for item in self.items if item.user_id.val == user_id]  

    def del_job(self, job): 
        global jobframe
        try:
            jobframe = jobframe.drop([job.user_id.pos])
            self.save_df(jobframe, 'data/jobs.csv')
            self.jobs.remove(job)
            del(job)
        except Exception as e:
            print(e)

    def get_user(self, id):
        for user in self.users:
            if user.id.val == id:
                return user 

    def get_random_user(self):
        return random.choice(self.users)
        
    
    def update_users(self, ids): 
        for id in ids:
            if id not in [user.id.val for user in self.users]: 
                self.insert_new_user(id)
        self.save_df(userframe, 'data/users.csv')
    
    
    def update_jobs(self):
        self.save_df(jobframe, 'data/jobs.csv')

storage = Storage()
