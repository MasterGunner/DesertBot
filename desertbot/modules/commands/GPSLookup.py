"""
Created on Oct 09, 2013

@author: StarlitGhost
"""
from twisted.plugin import IPlugin
from desertbot.moduleinterface import IModule
from desertbot.modules.commandinterface import BotCommand
from zope.interface import implementer

import urllib

from desertbot.message import IRCMessage
from desertbot.response import IRCResponse, ResponseType

from desertbot.utils.api_keys import load_key


@implementer(IPlugin, IModule)
class GPSLookup(BotCommand):
    def triggers(self):
        return ['gps', 'gpslookup']

    def help(self, query):
        return ("gps(lookup) <address>"
                " - Uses Microsoft's Bing Maps geocoding API to"
                " lookup GPS coordinates for the given address")

    def onLoad(self):
        self.api_key = load_key('Bing Maps')

    def execute(self, message: IRCMessage):
        if len(message.parameterList) > 0:
            if self.api_key is None:
                return IRCResponse(ResponseType.Say,
                                   "[Bing Maps API key not found]",
                                   message.replyTo)

            url = "http://dev.virtualearth.net/REST/v1/Locations"
            params = {
                'q': urllib.quote_plus(message.parameters),
                'key': self.api_key,
            }

            response = self.bot.moduleHandler.runActionUntilValue('fetch-url', url, params=params)
            j = response.json()

            if j['resourceSets'][0]['estimatedTotal'] == 0:
                self.logger.warning("Could not find GPS record for {}".format(message.parameters))
                self.logger.debug(j)
                return IRCResponse(ResponseType.Say,
                                   "Couldn't find GPS coords for '{0}', sorry!"
                                   .format(message.parameters),
                                   message.replyTo)

            coords = j['resourceSets'][0]['resources'][0]['point']['coordinates']

            return IRCResponse(ResponseType.Say,
                               "GPS coords for '{0}' are: {1},{2}"
                               .format(message.parameters, coords[0], coords[1]),
                               message.replyTo)

        else:
            return IRCResponse(ResponseType.Say,
                               "You didn't give an address to look up",
                               message.replyTo)


gpsLookup = GPSLookup()
