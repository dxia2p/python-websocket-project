import servernetworkhandler

networkHandler = servernetworkhandler.ServerNetworkHandler
networkHandler.Initialize()

def onInput(message):
    print(message)

networkHandler.AddFunction("i", onInput)