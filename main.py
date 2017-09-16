#!/usr/bin/env python3

from datetime import datetime
import asyncio

import urwid

from settings import *
from matrix import Matrix
from system import System


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
        self.users = {}
        self.active_account_idx = 0
        self.active_room_idx = 0

        self.header = urwid.Text('header')
        self.rooms = urwid.Text('rooms')
        self.text = urwid.Text('text')
        self.input = Input(self)
        self.body = urwid.Columns([(ROOM_LIST_WIDTH, urwid.Filler(self.rooms, valign='top')),
                                   urwid.Filler(self.text, valign='top')])

        self.accounts = [System(self)]
        self.accounts.append(Matrix(self))
        self.update_header()
        self.update_rooms()
        super().__init__(self.body, header=self.header, footer=self.input, focus_part='footer')

    def cmd(self, text):
        if text.startswith(CMD_PREFIX):
            text = text[1:]
            if text.startswith(CMD_PREFIX):
                self.account.send(text, self.room_id)
            elif text.startswith('q'):
                raise urwid.ExitMainLoop
            elif text.startswith('n'):
                self.next()
            elif text.startswith('s'):
                self.active_room_idx = self.active_account_idx = 0
                self.update_rooms()
            else:
                self.system(f'unknown command: {text}')
            self.update_text()
            self.update_header()
        else:
            self.account.send(text, self.room_id)

    def system(self, text, sender='system'):
        self.accounts[0].send(text, 'main', 'system')

    def update_header(self, header=None):
        if header is None:
            header = self.room_data['topic']
        self.header.set_text(header + '\n')

    def update_text(self, history=None, draw=True):
        text = []
        if history is None:
            history = self.room_data['history']
        for dt, sender, body in history:
            dt = dt.strftime(DT_FORMAT)
            sender = self.users[sender]
            text.append(f'{dt} <{sender}> {body}')
        self.text.set_text('\n'.join(text))
        if draw:
            main_loop.draw_screen()

    def update_rooms(self):
        rooms = []
        for account in self.accounts:
            fill = '=' * (ROOM_LIST_WIDTH - 4 - len(str(account)))
            rooms.append(f'= {account} {fill}')
            for i, room_id in enumerate(account.rooms):
                name = account.room_data[room_id]['name']
                active = '*' if account == self.account and i == self.active_room_idx else ' '
                rooms.append(f' {active} {name}'[:ROOM_LIST_WIDTH - 1])
        self.rooms.set_text('\n'.join(rooms))


    def next(self):
        self.active_room_idx += 1
        if self.active_room_idx >= len(self.account.rooms):
            self.active_account_idx = (self.active_account_idx + 1) % len(self.accounts)
            self.active_room_idx = 0
        self.update_rooms()

    @property
    def account(self):
        return self.accounts[self.active_account_idx]

    @property
    def room_id(self):
        return self.account.rooms[self.active_room_idx]

    @property
    def room_data(self):
        return self.account.room_data[self.room_id]


if __name__ == '__main__':
    event_loop = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
    screen = urwid.raw_display.Screen()
    main_loop = urwid.MainLoop(Main(), screen=screen, event_loop=event_loop)
    main_loop.run()
