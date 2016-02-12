from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest
from PyQt5.QtWebKitWidgets import QWebPage
from scrapy.http import Headers


# TODO: handlers for JavaScript message boxes.


class MyErrorPageExtensionOption(QWebPage.ErrorPageExtensionOption):
    pass


class WebPage(QWebPage):
    """

    QWebPage subclass with a signal for load finished with a parameter for
    page errors.

    """

    load_finished_with_error = pyqtSignal(bool,
                                          QWebPage.ErrorPageExtensionOption)

    _dummy_error = QWebPage.ErrorPageExtensionOption()

    def __init__(self, *args, **kwargs):
        super(WebPage, self).__init__(*args, **kwargs)
        self.webview = None
        self._current_error = None
        self.loadFinished.connect(self._on_load_finished)
        self.loadStarted.connect(self.reset_curent_error)

    def setNetworkAccessManager(self, nam):
        super(WebPage, self).setNetworkAccessManager(nam)
        self.networkAccessManager().finished.connect(self._on_network_reply)

    def reset_curent_error(self):
        self._current_error = None

    def _on_network_reply(self, reply):
        if ((self._current_error is None and
             reply.error() == QNetworkReply.NoError)):
            self._current_error = MyErrorPageExtensionOption()
            self._current_error.domain = QWebPage.Http
            self._current_error.error = reply.attribute(
                QNetworkRequest.HttpStatusCodeAttribute
            )
            self._current_error.url = reply.url()
            self._current_error.errorString = reply.attribute(
                QNetworkRequest.HttpReasonPhraseAttribute
            )
            self._current_error.headers = Headers(map(partial(map, str),
                                                      reply.rawHeaderPairs()))

    def _on_load_finished(self, ok):
        self.load_finished_with_error.emit(ok, (self._current_error or
                                                self._dummy_error))
        self.reset_curent_error()

    def extension(self, extension, option=None, output=None):
        if extension == QWebPage.ErrorPageExtension:
            if self._current_error is None:
                self._current_error = option

        return False

    def supportsExtension(self, extension):
        if extension == QWebPage.ErrorPageExtension:
            return True

        return super(WebPage, self).supportsExtension(extension)