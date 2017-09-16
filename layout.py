#!/usr/bin/env python3

from datetime import datetime
import asyncio

import urwid
from matrix_client.client import MatrixClient

from settings import *


class Input(urwid.Edit):
    def __init__(self, main):
        self.main = main
        super().__init__()

    def keypress(self, size, key):
        if key == 'enter':
            if self.edit_text:
                self.main.cmd(self.edit_text)
                self.set_edit_text('')
        else:
            return super().keypress(size, key)


class Main(urwid.Frame):
    def __init__(self):
        self.accounts = [Nim(self)]
        self.active_account_idx = 0
        self.active_room_idx = 0
        self.users = {'system': 'system', 'you': 'you'}

        self.header = urwid.Text('header')
        self.rooms = urwid.Text('rooms')
        self.text = urwid.Text('text')
        self.input = Input(self)
        self.body = urwid.Columns([(ROOM_LIST_WIDTH, urwid.Filler(self.rooms, valign='top')),
                                   urwid.Filler(self.text, valign='top')])

        super().__init__(self.body, header=self.header, footer=self.input, focus_part='footer')

    def cmd(self, text):
        if text.startswith('/'):
            if text == '/quit':
                raise urwid.ExitMainLoop
            if text == '/next':
                self.next()
            else:
                self.accounts[0].send(f'unknown command: {text}', 0, 'system')
        else:
            self.send(text)

    def send(self, text):
        self.accounts[self.active_account_idx].send(text, self.active_room_idx)

    def update_text(self, data):
        text = []
        for dt, sender, body in data['history']:
            dt = dt.strftime(DT_FORMAT)
            text.append(f'{dt} <{sender}> {body}')
        self.text.set_text('\n'.join(text))


class Nim(object):
    def __init__(self, main):
        self.main = main
        self.rooms = ['main']
        self.room_data = {'main': {
            'history': [(datetime.now(), 'system', 'hello')],
            'last_read': 1,
            'topic': 'nIM log',
        }}

    def send(self, text, room_idx, sender='you'):
        data = self.room_data[self.rooms[room_idx]]
        data['history'].append((datetime.now(), sender, text))
        self.main.update_text(data)


if __name__ == '__main__':
    event_loop = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
    screen = urwid.raw_display.Screen()
    main_loop = urwid.MainLoop(Main(), screen=screen, event_loop=event_loop)
    main_loop.run()
