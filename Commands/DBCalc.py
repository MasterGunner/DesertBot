import math

from CommandInterface import CommandInterface
from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType


class Command(CommandInterface):
    triggers = ['dbcalc']
    help = 'dbcalc (hours <hours> / money <money>) - tells you how much money is required for a given number of hours, ' \
           'or how many hours will be bussed for a given amount of money'

    def execute(self, message=IRCMessage):
        if len(message.ParameterList) < 2:
            return IRCResponse(ResponseType.Say, self.help, message.ReplyTo)

        if message.ParameterList[0].lower() == 'hours':
            return IRCResponse(ResponseType.Say, self.hours(message.ParameterList[1]), message.ReplyTo)
        elif message.ParameterList[0].lower() == 'money':
            return IRCResponse(ResponseType.Say, self.money(message.ParameterList[1]), message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, self.help, message.ReplyTo)

    @staticmethod
    def hours(hours):

        try:
            f_hours = float(hours)
        except ValueError:
            return "Sorry, I don't recognize '{0}' as a number".format(hours)

        try:
            money = (1-(1.07**f_hours))/(-0.07)
        except OverflowError:
            return "The amount of money you would need for that many hours is higher than I can calculate!"

        return "For {0:,} hour(s), the team needs a total of ${1:,.2f}".format(f_hours, money)

    @staticmethod
    def money(money):

        try:
            f_money = float(money)
        except ValueError:
            return "Sorry, I don't recognize '{0}' as a number".format(money)

        try:
            hours = math.log((7*f_money)/100 + 1)/math.log(1.07)
        except OverflowError:
            return "???"

        return "With ${0:,.2f}, the team will bus for {1:,.2f} hour(s)".format(f_money, hours)
