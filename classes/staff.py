import discord

from utils.configs import  configData
from db.mod import ausendb, desausendb
from .advertencia import adv1
from .cargos import adcrmv
from pytz import timezone
from datetime import datetime

class ban(discord.ui.View):
    
    def __init__(self, bot, membro, motivo, ctx):

        self.membro = membro

        self.bot = bot

        self.motivo = motivo

        self.ctx = ctx

        super().__init__(timeout = None)

    @discord.ui.button(label = '✅', style = discord.ButtonStyle.blurple)
    async def confirmban(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:

            l1 = self.bot.get_channel(configData['logs']['mod'])

            guild = interaction.guild

            E = discord.Embed(title = 'Ban', description = f'Pessoa banida: {self.membro.name} \nQuem baniu: {self.ctx.mention}\nAprovado por: {interaction.user.mention} \nmotivo: {self.motivo}')
            E.set_footer(text = f'id: {self.membro.id}')

            await l1.send(embed = E)

            await interaction.message.delete()

            await interaction.response.send_message(f'{self.membro.name} banido com sucesso', ephemeral = True)

            await guild.ban(user = self.membro ,reason = self.motivo)

            self.stop()

        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

    @discord.ui.button(label = '❎', style = discord.ButtonStyle.blurple)
    async def denyban(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:

            await interaction.message.delete()

            self.stop()

        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

class kick(discord.ui.View):
    
    def __init__(self, bot, membro, motivo, ctx):

        self.membro = membro

        self.bot = bot

        self.motivo = motivo

        self.ctx = ctx

        super().__init__(timeout = 180)

    @discord.ui.button(label = '✅', style = discord.ButtonStyle.blurple)
    async def confirmkick(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:
        
            l1 = self.bot.get_channel(configData['logs']['mod'])

            guild = interaction.guild

            E = discord.Embed(title = 'kick', description = f'Pessoa expulsa: {self.membro.name} \n Quem expulsou: {self.ctx.mention} \nAprovado por: {interaction.user.mention} \n motivo: {self.motivo} \n{self.membro.id}')

            await l1.send(embed = E)

            await interaction.message.delete()

            await interaction.response.send_message(f'{self.membro.name} expulso com sucesso', ephemeral = True)

            await guild.kick(user = self.membro ,reason = self.motivo)

            self.stop()

        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

    @discord.ui.button(label = '❎', style = discord.ButtonStyle.blurple)
    async def denykick(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles:
        
            await interaction.message.delete()

            await interaction.response.send_message(f'Ufa, ainda bem que não tive que expulsar o {self.membro.mention}', ephemeral = True)

            self.stop()

        else:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

class cmdstf(discord.ui.View):
    
    def __init__(self, bot):

        self.bot = bot

        super().__init__(timeout = None)

    @discord.ui.button(label = 'Ausencia', style = discord.ButtonStyle.blurple)
    async def ausente(self, button: discord.ui.Button, interaction: discord.Interaction):

        data_e_hora_atuais = datetime.now()

        fuso_horario = timezone('America/Sao_Paulo')

        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)

        dt = data_e_hora_sao_paulo.strftime('%d/%m/%Y')

        def check(m):
            return m.content and m.author.id == interaction.user.id

        try:

            role = discord.utils.get(interaction.guild.roles, id = configData['roles']['outras']['standby'])

            ausente = self.bot.get_channel(configData['chats']['ausencia'])

            channel = self.bot.get_channel(configData['chats']['cmdstf'])

            if role not in interaction.user.roles:

                await interaction.response.send_message('Escreva o motivo de estar ausente', ephemeral = True)

                msg = await self.bot.wait_for('message', check = check, timeout = 130)

                await interaction.user.add_roles(role)

                await ausente.send(f'{interaction.user.name} entrou em ausencia às {dt}\nMotivo: {msg.content}')

                await channel.send(f'Agora você está ausente {interaction.user.mention}', delete_after = 2)

                await msg.delete()

                await ausendb(interaction.user,msg.content,dt)

                return

            if role in interaction.user.roles:

                await interaction.user.remove_roles(role)

                await ausente.send(f'{interaction.user.name} Saiu da ausencia às {dt}')

                await interaction.response.send_message('Você não está mais ausente', delete_after = 2, ephemeral = True)

                await desausendb(interaction.user)

                return
        
        except Exception:

            await ausente.send(f'{interaction.user.name} clicou no ausente mas não fez nada')

    @discord.ui.button(label = 'Ban', style = discord.ButtonStyle.blurple)
    async def ban(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['staff']) not in interaction.user.roles:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

            return

        channel = self.bot.get_channel(configData['chats']['cmdstf'])

        def check(m):
            return m.content and m.author.id == interaction.user.id

        try:

            id = await channel.send('Mande o id da pessoa a banir')

            msg = await self.bot.wait_for('message', check = check, timeout = 130)

            membro = interaction.guild.get_member(int(msg.content))

            await id.delete()

            await msg.delete()

            def check2(m):
                return m.content and m.author.id == interaction.user.id

            try:

                id = await channel.send('Mande o motivo de banir o membro')

                msg2 = await self.bot.wait_for('message', check = check2, timeout = 130)

                await id.delete()

                await msg2.delete()

                e = discord.Embed(title = 'Ban')

                e.add_field(name = 'Pessoa a banir', value = f'{membro.mention}')

                e.add_field(name = 'Quem baniu', value = interaction.user.mention, inline = False)
                
                e.add_field(name = 'Motivo', value = msg2.content)

                await channel.send(embed = e, view = ban(self.bot,membro,msg2.content, interaction.user))

            except:
                print('error')

        except:
            print('error')
    
    @discord.ui.button(label = 'advertência', style = discord.ButtonStyle.blurple)
    async def advertência(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['staff']) not in interaction.user.roles:

            await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral = True)

            return

        await interaction.response.send_message('O que ira fazer?', ephemeral = True, view = adv1(self.bot))

    @discord.ui.button(label = 'cargos', style = discord.ButtonStyle.blurple)
    async def cargos(self, button: discord.ui.Button, interaction: discord.Interaction):

        if discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['admin']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['staff']['mod']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['equipes']['equipeeventos']['chefeeventos']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['equipes']['equipecall']['submod']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['equipes']['equipechat']['liderchat']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['equipes']['equipediv']['promoters']) in interaction.user.roles \
        or discord.utils.get(interaction.guild.roles, id = configData['roles']['equipes']['equipemidia']['chefemidia']) in interaction.user.roles:

            await interaction.response.send_message('Oque ira fazer?', ephemeral = True, view = adcrmv(self.bot))

        else:
        
            await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral = True)

            return