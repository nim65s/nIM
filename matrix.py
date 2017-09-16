from datetime import datetime

from matrix_client.client import MatrixClient

from settings import *


class Matrix(object):
    def __init__(self, main):
        self.main = main
        self.login = login

        self.client = MatrixClient(address)
        self.client.login_with_password(username=login, password=passwd)

        self.rooms = []
        self.room_data = {}

        for room_id, room in self.client.get_rooms().items():
            self.rooms.append(room_id)
            self.room_data[room_id] = {
                'history': [],
                'last_read': 0,
                'name': room.name or room_id,
                'topic': room.topic or '',
            }
            self.main.system(f'add matrix room {room_id}')

            room.add_listener(self.listener)
        self.client.start_listener_thread()

    def __str__(self):
        return f'Matrix {self.login}'

    def listener(self, room, event):
        if event['type'] == 'm.room.message':
            history = self.room_data[room.room_id]['history']
            dt = datetime.fromtimestamp(event['origin_server_ts'] / 1000)
            history.append((dt, event['sender'], event['content']['body']))
            if event['sender'] not in self.main.users:
                self.main.users[event['sender']] = self.client.api.get_display_name(event['sender'])
            if self.main.account == self and room.room_id == self.main.room_id:
                self.main.update_text(history)
        else:
            self.main.system(str(event))

    def send(self, text, room_id):
        self.client.api.send_message(room_id, text)