import discord
import asyncio

from datetime import datetime
from pytz import timezone
from utils.configs import configData
from db.mod import advdb, rmvadvdb

class adcadv(discord.ui.View):

    def __init__(self, bot, membro, motivo, ctx):

        self.motivo = motivo

        self.membro = membro

        self.bot = bot

        self.ctx = ctx

        super().__init__(timeout = None)

    @discord.ui.button(label = '✅'  , style = discord.ButtonStyle.blurple)
    async def adv(self, button: discord.ui.Button, interaction: discord.Interaction):

        data_e_hora_atuais = datetime.now()

        fuso_horario = timezone('America/Sao_Paulo')

        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
        
        dt = data_e_hora_sao_paulo.strftime('%H:%M %d/%m/%Y')

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:

            role1 = discord.utils.get(interaction.guild.roles, id = configData['roles']['adv']['adv1'])

            role2 = discord.utils.get(interaction.guild.roles, id = configData['roles']['adv']['adv2'])

            role3 = discord.utils.get(interaction.guild.roles, id = configData['roles']['adv']['adv3'])

            mute2 = discord.utils.get(interaction.guild.roles, id = configData['roles']['outras']['mute'])

            channel = self.bot.get_channel(configData['logs']['mod'])

            if role3 in self.membro.roles:

                E = discord.Embed(title = 'Ban', description = f'Pessoa banida: {self.membro.name} \n Quem baniu: {interaction.user.mention} \n motivo: Acumulo de adv')

                await channel.send(embed = E)

                await self.membro.ban(reason = 'Acumulo de advertencia')

                await interaction.message.delete()

                await interaction.response.send_message(f'{self.membro.name} advertido com sucesso e banido devido o acumulo de adv', ephemeral = True)

            if role2 in self.membro.roles:

                e = discord.Embed(title = 'Advertencia 3', description = f'{self.membro.mention} foi advertido por {self.ctx.mention} e aprovado por {interaction.user.mention}\nMotivo:{self.motivo}')
                
                await advdb(self.membro,3,f'{self.motivo} {dt}')

                await self.membro.add_roles(role3, reason = self.motivo)
                await self.membro.add_roles(mute2, reason = 'Adv3')

                await interaction.message.delete()

                await channel.send(embed = e)

                await asyncio.sleep(86400)

                await self.membro.remove_roles(mute2)

                return

            if role1 in self.membro.roles:

                e = discord.Embed(title = 'Advertencia 2', description = f'{self.membro.mention} foi advertido por {self.ctx.mention} e aprovado por {interaction.user.mention}\nMotivo:{self.motivo}')
                
                await advdb(self.membro,2,f'{self.motivo} {dt}')

                await self.membro.add_roles(role2, reason = self.motivo)
                await self.membro.add_roles(mute2, reason = 'Adv2')

                await interaction.message.delete()

                await channel.send(embed = e)

                await interaction.response.send_message(f'{self.membro} advertido com sucesso', ephemeral = True)

                await asyncio.sleep(10800)

                await self.membro.remove_roles(mute2)

                return

            if role1 not in self.membro.roles:

                e = discord.Embed(title = 'Advertencia 1', description = f'{self.membro.mention} foi advertido por {self.ctx.mention} e aprovado por {interaction.user.mention}\nMotivo:{self.motivo}')

                await advdb(self.membro,3,'None')

                await advdb(self.membro,2,'None')

                await advdb(self.membro,1,f'{self.motivo} {dt}')
                
                await self.membro.add_roles(role1, reason = self.motivo)

                await self.membro.add_roles(mute2, reason = 'Adv1')

                await interaction.message.delete()

                await channel.send(embed = e)

                await interaction.response.send_message(f'{self.membro} advertido com sucesso', ephemeral = True)

                await asyncio.sleep(3600)

                await self.membro.remove_roles(mute2)

                return
        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

    @discord.ui.button(label = '❎', style = discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:

            await interaction.message.delete()

            self.stop()

        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

class rmvadv(discord.ui.View):

    def __init__(self, bot, membro):

        self.membro = membro

        self.bot = bot

        super().__init__(timeout = None)

    @discord.ui.button(label = '✅'  , style = discord.ButtonStyle.blurple)
    async def rmvadv(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:

            await interaction.message.delete()

            membro = self.membro

            role1 = discord.utils.get(interaction.guild.roles, id = configData['roles']['adv']['adv1'])

            role2 = discord.utils.get(interaction.guild.roles, id = configData['roles']['adv']['adv2'])

            role3 = discord.utils.get(interaction.guild.roles, id = configData['roles']['adv']['adv3'])

            channel = self.bot.get_channel(configData['logs']['mod'])

            mute = discord.utils.get(interaction.guild.roles, id = configData['roles']['outras']['mute'])

            e = discord.Embed(title = 'Remoção adv', description = f'{interaction.user.mention} removeu uma advertencia de {membro.mention}')

            if role3 in membro.roles:
                
                await rmvadvdb(membro,3, 'None')

                await membro.remove_roles(role3)

                await channel.send(embed = e)

                await interaction.response.send_message('Advertência removida com sucesso', ephemeral = True)

                await self.membro.remove_roles(mute)

                return

            elif role2 in membro.roles:
                
                await rmvadvdb(membro,2,'None')

                await membro.remove_roles(role2)

                await channel.send(embed = e)

                await interaction.response.send_message('Advertência removida com sucesso', ephemeral = True)

                await self.membro.remove_roles(mute)

                return

            elif role1 in membro.roles:

                await rmvadvdb(membro,1,'None')
                
                await membro.remove_roles(role1)

                await channel.send(embed = e)

                await interaction.response.send_message('Advertência removida com sucesso', ephemeral = True)

                await self.membro.remove_roles(mute)

                return

            elif discord.utils.get(interaction.guild.roles, id = configData['roles']['adv']['adv1']) not in membro.roles:

                await interaction.response.send_message('Esse membro não possue advertencias', delete_after = 3)

                return
        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

    @discord.ui.button(label = '❎', style = discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:
        
            await interaction.message.delete()

            self.stop()

        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

class adv1(discord.ui.View):

    def __init__(self, bot, timeout = 300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
    placeholder = "Advivertencia",
    options = [
        discord.SelectOption(
            label = 'Adicionar',
            description = 'Adiciona uma advertencia'
        ),
        discord.SelectOption(
            label = 'Remover',
            description = 'Remove uma advertencia'
        )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        channel = self.bot.get_channel(configData['chats']['cmdstf'])

        if select.values[0] == 'Adicionar':

            def check(m):
                return m.content and m.author.id == interaction.user.id

            try:

                await interaction.response.send_message('Mande o id da pessoa a adverter', ephemeral = True)

                msg = await self.bot.wait_for('message', check = check, timeout = 130)

                membro = interaction.guild.get_member(int(msg.content))

                await msg.delete()

                def check2(m):
                    return m.content and m.author.id == interaction.user.id

                try:

                    id = await channel.send('Mande o motivo de adverter o membro')

                    msg2 = await self.bot.wait_for('message', check = check2, timeout = 130)

                    await id.delete()

                    await msg2.delete()

                    e = discord.Embed(title = 'Advertencia')

                    e.add_field(name = 'Pessoa a adverter', value = f'{membro.mention}')
                    e.add_field(name = 'Quem adverteu', value = interaction.user.mention, inline = False)
                    e.add_field(name = 'Motivo', value = msg2.content)

                    await channel.send(embed = e, view = adcadv(self.bot,membro,msg2.content, interaction.user))

                    self.stop()

                except:
                    print('error')

            except:
                print('error')

        elif select.values[0] == 'Remover':

            def check50(m):
                return m.content and m.author.id == interaction.user.id

            try:

                await interaction.response.send_message('Mande o id da pessoa a remover a advertencia', ephemeral = True)

                msg50 = await self.bot.wait_for('message', check = check50, timeout = 130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                e = discord.Embed(title = 'Advertencia')

                e.add_field(name = 'Remover advertencia de ', value = f'{membro.mention}')
                e.add_field(name = 'Quem removeu ', value = interaction.user.mention, inline = False)

                await channel.send(embed = e, view = rmvadv(self.bot,membro))

                self.stop()

            except:

                print('error')