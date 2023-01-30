import socket

import sys
sys.path.append('../')

from engine.headers import Turn, Coordinates
from engine.board import Board
from gui.game import Game

import asyncio
        

class SocketClient(asyncio.Protocol, Board):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

        Board.__init__(self)
        self.set_defautl_board()
        game = Game(self)
        game.start_game()

    def connection_made(self, transport):
        self.transport = transport
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def drag_figure(self, figure, new_coordinate: Coordinates, is_castling=False):
        super().drag_figure(figure, new_coordinate, is_castling)
        self.write_data(figure.name.encode())

    def write_data(self, message):
        self.transport.write(message)

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)

    def send_move(self, figure, new_coordinate: Coordinates):
        self.socket.sendall(f'move\n{self.figure.type_}\n{figure.name}\nx={figure.position.x} y={figure.position.y}\nx={new_coordinate.x} y={new_coordinate.y}')

async def start_client():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'H'

    transport, protocol = await loop.create_connection(
        lambda: SocketClient(message, on_con_lost),
        '127.0.0.1', 15555)

    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()
    
def init_client():
    asyncio.run(start_client())

