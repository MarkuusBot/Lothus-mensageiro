import discord
import os

from utils.configs import configData
from db.mod import tckdb, tckdb2, tckdb3
from discord.ui import Button
from pytz import timezone
from datetime import datetime

class adonticket2(discord.ui.View):

    def __init__(self, membro):

        self.membro = membro

        super().__init__(timeout = None)

    @discord.ui.button(label = '🔓 Abrir ticket', style = discord.ButtonStyle.blurple)
    async def abrir(self,  button: discord.ui.Button, interaction: discord.Interaction):

        member = self.membro

        guild = interaction.guild

        admin = discord.utils.get(guild.roles, id = configData['roles']['staff']['admin'])
            
        mod = discord.utils.get(guild.roles, id = configData['roles']['staff']['mod'])

        suporte = discord.utils.get(guild.roles, id = configData['roles']['staff']['suporte'])

        overwrites = {

            member: discord.PermissionOverwrite(read_messages=True),

            guild.default_role: discord.PermissionOverwrite(read_messages=False),

            admin: discord.PermissionOverwrite(read_messages=True),

            mod: discord.PermissionOverwrite(read_messages=True),

            suporte: discord.PermissionOverwrite(read_messages=True),

        }

        await interaction.channel.edit(overwrites = overwrites)

        await interaction.message.delete()

        msg = await interaction.channel.send('Ticket aberto 🔓', view = adonticket(self.membro))

        await tckdb(self.membro, msg.id)

    @discord.ui.button(label = '🛑 Deletar Ticket', style = discord.ButtonStyle.blurple)
    async def delete(self,  button: discord.ui.Button, interaction: discord.Interaction):

        await tckdb3(self.membro)

        await interaction.channel.delete()

class jumpto(Button):

    def __init__(self, url):

        super().__init__(

            label = 'Atalho para o ticket',

            style=discord.ButtonStyle.url,
        
            url = url
        )
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):

        pass

class adonticket(discord.ui.View):
    
    def __init__(self, membro):

        self.membro = membro

        super().__init__(timeout = None)

    @discord.ui.button(label = '🔒 Fechar ticket', style = discord.ButtonStyle.blurple)
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):

        member = self.membro

        guild = interaction.guild

        admin = discord.utils.get(guild.roles, id = configData['roles']['staff']['admin'])
            
        mod = discord.utils.get(guild.roles, id = configData['roles']['staff']['mod'])

        suporte = discord.utils.get(guild.roles, id = configData['roles']['staff']['suporte'])

        overwrites = {

            member: discord.PermissionOverwrite(read_messages=False),

            guild.default_role: discord.PermissionOverwrite(read_messages=False),

            admin: discord.PermissionOverwrite(read_messages=True),

            mod: discord.PermissionOverwrite(read_messages=True),

            suporte: discord.PermissionOverwrite(read_messages=True),

        }

        e = discord.Embed(description = f'🔒Ticket fechado por {interaction.user.mention} \nClique no 🔓 para abrir')

        await interaction.channel.edit(overwrites = overwrites)

        await interaction.message.delete()

        msg = await interaction.channel.send(embed = e, view = adonticket2(member))

        await tckdb2(self.membro,msg.id)

class ticket(discord.ui.View):
    
    def __init__(self):

        super().__init__(timeout = None)
        
    @discord.ui.button(label = '🛎 Criar ticket', style = discord.ButtonStyle.blurple)
    async def confirm(self,  button: discord.ui.Button, interaction: discord.Interaction):

        data_e_hora_atuais = datetime.now()

        fuso_horario = timezone('America/Sao_Paulo')

        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)

        dt = data_e_hora_sao_paulo.strftime('%d/%m/%Y')

        guild = interaction.guild

        Chat = discord.utils.get(guild.channels, name=f'ticket-{interaction.user.id}')

        if Chat is None:

            guild = interaction.guild

            ticket = f'ticket-{interaction.user.id}'

            member = interaction.user

            admin = discord.utils.get(guild.roles, id = configData['roles']['staff']['admin'])
            
            mod = discord.utils.get(guild.roles, id = configData['roles']['staff']['mod'])

            suporte = discord.utils.get(guild.roles, id = configData['roles']['staff']['suporte'])

            overwrites = {

                guild.default_role: discord.PermissionOverwrite(read_messages=False),

                member: discord.PermissionOverwrite(read_messages=True),

                admin: discord.PermissionOverwrite(read_messages=True),

                mod: discord.PermissionOverwrite(read_messages=True),

                suporte: discord.PermissionOverwrite(read_messages=True),

                }

            for file in os.listdir('./tickets'):

                if file.endswith('.txt'):

                    if file.startswith(f'{ticket}'):

                        os.remove(f"./tickets/{ticket}.txt")

            with open(f'./tickets/{ticket}.txt', 'a') as f:

                f.write(f'Ticket de {interaction.user.name} {dt}')

            channel = await guild.create_text_channel(name=ticket, 
            overwrites = overwrites, 
            category = discord.utils.get(interaction.guild.categories, id = configData['catego']['ticket']))

            await interaction.response.send_message('Ticket criado com sucesso',view = discord.ui.View(jumpto(f'https://discordapp.com/channels/{interaction.guild.id}/{channel.id}'), timeout = 180), ephemeral = True)

            msg = await channel.send(view=adonticket(member))

            await channel.send(f'{interaction.user.mention} {suporte.mention}')

            await tckdb(interaction.user, msg.id)
        
        else:

            await interaction.response.send_message('Ticket já existente, encerre o ultimo para criar outro', ephemeral = True)