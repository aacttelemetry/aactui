import sys

from PyQt5 import QtCore, QtWebSockets, QtNetwork
from PyQt5.QtCore import QUrl, QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication

#from: https://stackoverflow.com/questions/48709399/pyqt5-connect-to-websocket-wait-for-signal-from-server

class Client(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)

        self.client =  QtWebSockets.QWebSocket("",QtWebSockets.QWebSocketProtocol.Version13,None)
        self.client.error.connect(self.error)

        self.client.open(QUrl("wss://echo.websocket.org"))
        self.client.pong.connect(self.onPong)

        self.client.textMessageReceived.connect(self.ontextmsgreceived)

    def do_ping(self):
        print("client: do_ping")
        self.client.ping(b"foo")

    def send_message(self):
        print("client: send_message")
        self.client.sendTextMessage("asd")

    def onPong(self, elapsedTime, payload):
        print("onPong - time: {} ; payload: {}".format(elapsedTime, payload))

    def error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    def close(self):
        self.client.close()

    def ontextmsgreceived(self, message):
        print("Text MSG received", message)

def quit_app():
    print("timer timeout - exiting")
    QCoreApplication.quit()

def ping():
    client.do_ping()

def send_message():
    client.send_message()

if __name__ == '__main__':
    global client
    app = QApplication(sys.argv)

    QTimer.singleShot(2000, ping)
    QTimer.singleShot(3000, send_message)
    QTimer.singleShot(5000, quit_app)

    client = Client(app)

    app.exec_()
