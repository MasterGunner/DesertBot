from twisted.plugin import IPlugin
from typing import Union
from zope.interface import implementer

from desertbot.message import IRCMessage
from desertbot.moduleinterface import IModule
from desertbot.modules.commandinterface import admin, BotCommand
from desertbot.response import IRCResponse, ResponseType


@implementer(IPlugin, IModule)
class APIKeys(BotCommand):
    def __init__(self):
        BotCommand.__init__(self)
        self.loadingPriority = 10

    def triggers(self):
        return ["apikey"]

    def actions(self):
        return super(APIKeys, self).actions() + [("get-api-key", 1, self.getKey)]

    def help(self, query):
        return f"{self.bot.commandChar}apikey add/remove <name> <apikey> -- Add or remove the specified API key to the bot."

    @admin("[APIKey] Only my admins may manage API keys!")
    def execute(self, message: IRCMessage):
        if len(message.parameterList) < 3:
            return IRCResponse(ResponseType.Say, self.help(None), message.replyTo)
        command = message.parameterList[0].lower()
        key = message.parameterList.pop()
        keyname = " ".join(message.parameterList[1:])

        if command == "add":
            try:
                self.keys[keyname] = key
            except Exception:
                self.logger.exception(f"Failed to add API key {keyname}!")
                return IRCResponse(ResponseType.Say, f"Failed to add API key {keyname} to the bot!", message.replyTo)
            else:
                return IRCResponse(ResponseType.Say, f"Added the API key {keyname} to the bot.", message.replyTo)
        elif command == "remove":
            try:
                if keyname in self.keys:
                    del self.keys[keyname]
                    self.storage.save()
                else:
                    return IRCResponse(ResponseType.Say, f"There is no API key named {keyname}!", message.replyTo)
            except Exception:
                self.logger.exception(f"Failed to remove API key {keyname}!")
                return IRCResponse(ResponseType.Say, f"Failed to remove API key {keyname} from the bot!", message.replyTo)
            else:
                return IRCResponse(ResponseType.Say, f"Removed the API key {keyname} from the bot.", message.replyTo)
        else:
            return IRCResponse(ResponseType.Say, self.help(None), message.replyTo)

    def getKey(self, name: str) -> Union[str, None]:
        """
        Returns the API key with the given name, or None if it doesn't exist.
        """
        return self.storage.get(name, None)


apikeys = APIKeys()
