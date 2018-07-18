from datetime import datetime

from matrix_client.client import MatrixClient

from settings import *


class Matrix(object):
    def __init__(self, main):
        self.main = main
        self.login = login

        self.client = MatrixClient(address, encryption=encryption)
        self.client.login(login, passwd, device_id=device_id)

        self.rooms = []
        self.room_data = {}

        for room_id, room in self.client.get_rooms().items():
            self.main.system(f'add matrix room {room_id}')
            self.rooms.append(room_id)
            self.room_data[room_id] = {
                'history': [],
                'last_read': 0,
                'name': room.name or room_id,
                'topic': room.topic or '',
            }
            for event in room.events:
                if event['type'] == 'm.room.message':
                    self.room_data[room_id]['history'].append(self.event_to_history(event))
            if chan in room.aliases:
                self.main.active_room_idx = len(self.rooms) - 1
                self.main.active_account_idx = 1
            room.add_listener(self.listener)
        self.client.start_listener_thread()

    def __str__(self):
        return f'Matrix {self.login}'

    def event_to_history(self, event):
        self.add_sender(event['sender'])
        return datetime.fromtimestamp(event['origin_server_ts'] / 1000), event['sender'], event['content']['body']

    def add_sender(self, sender):
        if sender not in self.main.users:
            self.main.users[sender] = self.client.api.get_display_name(sender)

    def listener(self, room, event):
        if event['type'] == 'm.room.message':
            history = self.room_data[room.room_id]['history']
            history.append(self.event_to_history(event))
            if self.main.account == self and room.room_id == self.main.room_id:
                self.main.update_text(history)
        else:
            self.main.system(str(event))

    def send(self, text, room_id):
        self.client.rooms[room_id].send_text(text)
