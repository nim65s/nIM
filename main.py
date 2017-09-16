#!/usr/bin/env python3

from datetime import datetime
import asyncio

import urwid
from matrix_client.client import MatrixClient

from settings import *


class Input(urwid.Edit):
    def __init__(self, chat):
        self.chat = chat
        super().__init__()

    def keypress(self, size, key):
        if key == 'enter':
            self.chat.cmd(self.edit_text)
            self.set_edit_text('')
        else:
            return super().keypress(size, key)


class Chat(urwid.Pile):
    def __init__(self):
        self.hist = urwid.Text("")
        self.input = Input(self)
        self.users = {}
        self.rooms = {}
        self.room_ids = []
        self.room = ''
        super().__init__([urwid.Filler(self.hist, valign='top'),
                          urwid.Filler(self.input, valign='bottom')])

    def cmd(self, text):
        if text.startswith('/'):
            if text == '/quit':
                raise urwid.ExitMainLoop
            if text == '/next':
                self.room = self.room_ids[(self.room_ids.index(self.room) + 1) % len(self.room_ids)]
                self.update()
        else:
            self.send(text)

    def send(self, text):
        now = datetime.now().strftime('%H:%M:%S ')
        self.hist.set_text(f'{self.hist.text}\n{now} {text}')


class MatrixChats(Chat):
    def __init__(self, client, main_room):
        super().__init__()
        self.client = client
        for room_id, room in self.client.get_rooms().items():
            self.rooms[room_id] = {'room': room, 'events': [], 'unread': 0, 'name': room.name, 'topic': room.topic}
            self.room_ids.append(room_id)
            room.add_listener(self.listener)
            if main_room in room.aliases:
                self.room = room_id
        self.client.start_listener_thread()
        self.update(False)

    def listener(self, room, event):
        self.rooms[room.room_id]['events'].append(event)
        if room.room_id == self.room:
            self.update()
        else:
            self.rooms[room.room_id]['unread'] += 1

    def update(self, draw=True):
        text = [self.rooms[self.room]['name']]
        for event in self.rooms[self.room]['events']:
            body = event['content']['body']
            sender_id = event['sender']
            if sender_id in self.users:
                sender = self.users[sender_id]
            else:
                sender = self.client.api.get_display_name(sender_id)
                self.users[sender_id] = sender
            dt = datetime.fromtimestamp(event['origin_server_ts'] / 1000).strftime(DT_FORMAT)
            text.append(f'{dt} <{sender}> {body}')
        self.hist.set_text('\n'.join(text))
        if draw:
            main_loop.draw_screen()

    def send(self, text):
        self.rooms[self.room]['room'].send_text(text)


if __name__ == '__main__':
    matrix_client = MatrixClient(address)
    matrix_client.login_with_password(username=login, password=passwd)

    event_loop = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
    screen = urwid.raw_display.Screen()
    chat = MatrixChats(matrix_client, chan)
    main_loop = urwid.MainLoop(chat, screen=screen, event_loop=event_loop)
    main_loop.run()
