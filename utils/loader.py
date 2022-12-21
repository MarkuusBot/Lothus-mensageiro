import discord
import os

from discord.ext.commands import Bot as BotBase
from utils.verify import ticketloader, bottonstaffloader, verifyticket

class loadcogs():

    def __init__(self, bot):

        for filename in os.listdir('./plugins'):

            if filename.endswith('.py') and not filename.startswith('__'):

                bot.load_extension('plugins.{0}'.format(filename[:-3]))

class client(BotBase):

    def __init__(self, prefix, token):

        self.token = token

        super().__init__(

            command_prefix = prefix,

            intents = discord.Intents.all(),

            help_command = None,

            case_insensitive = True
            
        )

    async def on_ready(self):

        await self.change_presence(status = discord.Status.idle)

        await ticketloader(self)

        await bottonstaffloader(self)

        await verifyticket(self)

        print(f'Eu entrei como {self.user}')
    
    def __start__(self):

        loadcogs(self)

        self.run(self.token)