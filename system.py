from datetime import datetime

class System(object):
    def __init__(self, main):
        self.main = main
        self.rooms = ['main']
        self.room_data = {'main': {
            'history': [(datetime.now(), 'system', 'hello')],
            'last_read': 1,
            'name': 'system',
            'topic': 'nIM log',
        }}
        self.main.users['system'] = 'system'
        self.main.users['you'] = 'you'

    def __str__(self):
        return 'system'

    def send(self, text, room_id, sender='you'):
        history = self.room_data[room_id]['history']
        history.append((datetime.now(), sender, text))
        if self.main.account == self:
            self.main.update_text(history, draw=False)
