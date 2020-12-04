from ..request import Request, change_state
from global_vars import State, Tasks, Message, message_of
from storage import storage
from tasks import construct_task


class GetTask(Request):
    def __init__(self, message, client):
        super().__init__(2, message)
        self.client = client

    @change_state
    def work(self, message=None):
        if self.state == 0:
            job = storage.get_job_by_user_id(self.requester.id)
            if job:
                self.done = True
                return State.SKIP, Message(
                    content = message_of('gettask', 'A', Tasks.get_name(Tasks,job.typus)),
                    channel = self.channel)

            var = 'Aktuell gibt es folgende Dinge zu erledigen: \n' \
                + ''.join([f'[{i}] {Tasks.get_name(Tasks, task)} \n' \
                for i, task in enumerate(storage.available_tasks)])

            return State.OK, Message(
                content=message_of('gettask', self.state, var),
                channel = self.channel)

        if self.state == 1:
            try:
                task_num = int(message.content[1])
                task = storage.available_tasks[task_num]
                storage.available_tasks.remove(task)
                storage.insert_new_job(self.requester.id, task, 0)
                construct_task(task, self.requester.id, self.client)
                return State.OK, Message(
                    content=message_of('gettask', self.state, Tasks.get_name(Tasks, task)),
                    channel = self.channel)
            except Exception as e:
                print(e)
                return State.FAILED, None