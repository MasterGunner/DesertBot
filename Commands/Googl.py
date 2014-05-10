from CommandInterface import CommandInterface
from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
import WebUtils


class Command(CommandInterface):
    triggers = ['googl', 'shorten', 'goo.gl']
    help = "googl/shorten <url> - Gives you a shortened version of a url, via Goo.gl"
    
    def execute(self, message=IRCMessage):
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "You didn't give a URL to shorten!", message.ReplyTo)
        
        url = WebUtils.shortenGoogl(message.Parameters)
        
        return IRCResponse(ResponseType.Say, url, message.ReplyTo)
