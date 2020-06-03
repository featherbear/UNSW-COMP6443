
"""
Burp Extension (Python) to proxy local-only sites through a tunnel endpoint
Built on Jython 2.7.2

# https://featherbear.cc/UNSW-COMP6443
"""

from burp import IBurpExtender, IHttpListener, IParameter
from java.net import URL

evaluateHeaders = False
HOST = "foo.example.org"   # Hostname to perform request forwarding
TUNNEL = "bar.example.org" # Forward requests through this host
# Jython doesn't support f-strings

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self.helpers = callbacks.getHelpers();
        callbacks.setExtensionName(HOST + " direct access")
        callbacks.registerHttpListener(self)

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest and evaluateHeaders and messageInfo.getComment() == HOST:
            # Jython doesn't support wildcard destructuring
            # # proxyHeader, header, body, *_ = [*self.helpers.bytesToString(messageInfo.getResponse()).split(u"\r\n\r\n", 2), None, None]
            split = self.helpers.bytesToString(messageInfo.getResponse()).split(u"\r\n\r\n", 2)
            split.append(None)
            split.append(None)

            proxyHeader = split[0]
            header = split[1] or []
            body = split[2]

            messageInfo.setResponse(self.helpers.buildHttpMessage(header.split("\r\n"), self.helpers.stringToBytes(body)))
            return

        if messageInfo.getHttpService().getHost() == HOST:
            
            data = self.helpers.toggleRequestMethod(self.helpers.buildHttpRequest(URL("https://" + TUNNEL + "/")))
            data = self.helpers.addParameter(data, self.helpers.buildParameter("request", self.helpers.bytesToString(self.helpers.urlEncode(messageInfo.getRequest())), IParameter.PARAM_BODY))

            messageInfo.setRequest(data)
            httpService = messageInfo.getHttpService()
            messageInfo.setHttpService(self.helpers.buildHttpService(TUNNEL, httpService.getPort(), httpService.getProtocol()))
            messageInfo.setComment(HOST)