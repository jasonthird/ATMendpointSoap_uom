from ladon.ladonizer import ladonize
from ladon.server.wsgi import LadonWSGIApplication
from ladon.types.ladontype import LadonType

from clientLib import Atm

host = "localhost"
port = 5672


class AuthResponse(LadonType):
    success = bool
    token = str


class BalanceResponse(LadonType):
    success = bool
    balance = str


class DepositResponse(LadonType):
    deposited = str


class WithdrawResponse(LadonType):
    withdrawn = str


class AtmEndpoint(object):

    @ladonize(str, str, rtype=AuthResponse)
    def Auth(self, username, pin):
        atm = Atm(host, port)
        response = atm.auth(username, pin)
        toReturn = AuthResponse()
        if response == "False":
            toReturn.success = False
            toReturn.token = ""
        else:
            toReturn.success = True
            toReturn.token = response

        return toReturn

    @ladonize(str, rtype=BalanceResponse)
    def Balance(self, token):
        atm = Atm(host, port)
        response = atm.balance(token)
        toReturn = BalanceResponse()
        if response == "False":
            toReturn.success = False
            toReturn.balance = 0
        else:
            toReturn.success = True
            toReturn.balance = response

        return toReturn

    @ladonize(str, str, rtype=DepositResponse)
    def Deposit(self, token, amount):
        atm = Atm(host, port)
        response = atm.deposit(token, amount)
        toReturn = DepositResponse()
        if response == "False":
            toReturn.deposited = 0
        elif response == "Invalid message":
            toReturn.deposited = 0
        else:
            toReturn.deposited = response

        return toReturn

    @ladonize(str, str, rtype=WithdrawResponse)
    def Withdraw(self, token, amount):
        atm = Atm(host, port)
        response = atm.withdraw(token, amount)
        toReturn = WithdrawResponse()
        if response == "False":
            toReturn.withdrawn = 0
        elif response == "Invalid message":
            toReturn.withdrawn = 0
        else:
            toReturn.withdrawn = response

        return toReturn


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    import logging

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('ladon').setLevel(logging.DEBUG)

    application = LadonWSGIApplication(["main"])
    server = make_server('localhost', 8081, application)
    server.serve_forever()
