# -*- coding: UTF-8 -*-
__author__ = 'lijie'
import path
from response import *
from template import render


@path.route(path='/', method=['GET'])
def index(request):
    return render(request, "首页模板.html")


@path.route(path='/redir/', method=['GET'])
def index(request):
    return HttpResponseRedirect("http://www.baidu.com")


@path.route(path='/json/', method=['GET'])
def index(request):
    return {'id': 111, "name": "杭州"}


@path.route(path='/print/<str:msg>/<int:id>', method=['GET', 'POST'])
def index(request, msg, id):
    return msg + str(id)


"""
    JS 测试代码:
    var ws = new WebSocket("ws://localhost:8000/live/");
    ws.onopen = function(evt) {
        console.log("Connection open ...");
        ws.send('1234');
    };
    ws.onclose = function(evt){
        console.log("connection closed...")
    };
"""


class WebSocketEcho(HttpResponseWebSocket):
    def __init__(self, request):
        super().__init__(request)

    def on_text_frame(self, data):
        """
            called while receive a text frame
            return None
        """
        self.send_text(data)

    def on_bin_frame(self, data):
        """
            called while receive a binary frame
            return None
        """
        self.send_bin(data)

    def on_close_frame(self, data):
        """
            called while receive a close frame
            return None
        """
        self.close()

    def on_connection_down(self, request):
        """
            called while the connection is lost
            return None
        """
        print(request.path, "websocket is down.")


@path.route(path='/live/', method=['GET'])
def live(request):
    try:
        if request.headers['Upgrade'] != 'websocket':
            raise TypeError
        if request.headers['Connection'] != 'Upgrade':
            raise TypeError
    except:
        return HttpResponseBadRequest()

    return WebSocketEcho(request)
