import discord
import os
import asyncio
import time
import random

client = discord.Client()
version = "Not found"
qntdd = int

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    token = os.environ.get('TOKEN')
else:
    import secreto
    token = secreto.token

def toint(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

@client.event
async def on_ready():
    print("=================================")
    print("Bot iniciado com sucesso!")
    print (client.user.name)
    print(f"Bot Version: {version}")
    print("=================================")
    await client.change_presence(game=discord.Game(name="!HELP", url='https://twitch.tv/TheDiretor', type=1))

@client.event
async def on_message(message):
#PING
    if message.content.lower().startswith('!ping'):
        timep = time.time()
        emb = discord.Embed(title='Aguarde', color=0xe7002f)
        pingm0 = await client.send_message(message.channel, embed=emb)
        ping = time.time() - timep
        pingm1 = discord.Embed(title='Pong!', description=':ping_pong: Ping - %.01f segundos' % ping, color=0xe7002f)
        await client.edit_message(pingm0, embed=pingm1)
#DADO
    if message.content.lower().startswith('!dado'):
        choice = random.randint(1, 6)
        embeddad = discord.Embed(title='Dado', description='🎲 Joguei o dado, o resultado é :  {}'.format(choice),colour=0xe7002f)
        await client.send_message(message.channel, embed=embeddad)
#SORTEIO
    if message.content.lower().startswith('!sorteio'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        choice = random.randint(1, 999)
        embedsorteio = discord.Embed(title='🎉 Sorteio', description='O ganhador do sorteio foi o numero {}, Parabéns! Contate algum membro da staff para receber seu premio!'.format(choice),colour=0xe7002f)
        await client.send_message(message.channel, embed=embedsorteio)
#CONVITE
    if message.content.lower().startswith('!convite'):
     invite = await client.create_invite(message.channel, max_uses=1, xkcd=True)
     await client.send_message(message.author, "Seu convite da Alpha é: {}".format(invite.url))
     await client.send_message(message.channel, "Olá {}, um convite foi enviado no seu privado!".format(message.author.mention))
#VOTAÇÃO
    elif message.content.lower().startswith('!votação'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        msg = message.content[9:2000]
        botmsg = await client.send_message(message.channel, msg)
        await client.add_reaction(botmsg, '👍')
        await client.add_reaction(botmsg, '👎')
        await client.delete_message(message)
#JOGANDO NO BOT
    if message.content.startswith('!jogando'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        game = message.content[9:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "Status de jogo alterado para: " + game + " ")
#AVATAR
    elif message.content.lower().startswith('!avatar'):
        try:
            membro = message.mentions[0]
            avatarembed = discord.Embed(
                title="",
                color=0xe7002f,
                description="**[Clique aqui](" + membro.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed.set_author(name=membro.name)
            avatarembed.set_image(url=membro.avatar_url)
            await client.send_message(message.channel, embed=avatarembed)
        except:
            avatarembed2 = discord.Embed(
                title="",
                color=0xe7002f,
                description="**[Clique aqui](" + message.author.avatar_url + ") para acessar o link do avatar!**"
            )
            avatarembed2.set_author(name=message.author.name)
            avatarembed2.set_image(url=message.author.avatar_url)
            await client.send_message(message.channel, embed=avatarembed2)
#MOEDA
    if message.content.lower().startswith('!moeda'):
        choice = random.randint(1, 2)
        if choice == 1:
         await client.add_reaction(message, '🌝')
        if choice == 2:
            await client.add_reaction(message, '👑')
#SERVERINFO
    if message.content.lower().startswith('!serverinfo'):
        server = message.server
        embedserver = discord.Embed(
            title='Informaçoes do Servidor',
            color=0xe7002f,
            descripition='Essas são as informaçoes\n')
        embedserver = discord.Embed(name="{} Server ".format(message.server.name), color=0x551A8B)
        embedserver.add_field(name="Nome", value=message.server.name, inline=True)
        embedserver.add_field(name="Dono", value=message.server.owner.mention)
        embedserver.add_field(name="ID", value=message.server.id, inline=True)
        embedserver.add_field(name="Cargos", value=len(message.server.roles), inline=True)
        embedserver.add_field(name="Membros", value=len(message.server.members), inline=True)
        embedserver.add_field(name="Criado em", value=message.server.created_at.strftime("%d %b %Y %H:%M"))
        embedserver.add_field(name="Emojis", value=f"{len(message.server.emojis)}/100")
        embedserver.add_field(name="Região", value=str(message.server.region).title())
        embedserver.set_thumbnail(url=message.server.icon_url)
        embedserver.set_footer(text="By: brunoqq")
        await client.send_message(message.channel, embed=embedserver)
#USERINFO
    if message.content.startswith('!user'):
        try:
            user = message.mentions[0]
            userjoinedat = str(user.joined_at).split('.', 1)[0]
            usercreatedat = str(user.created_at).split('.', 1)[0]

            userembed = discord.Embed(
                title="Nome",
                description=user.name,
                color=0xe7002f
            )
            userembed.set_author(
                name="Informações do usuário"
            )
            userembed.set_thumbnail(url=user.avatar_url)
            userembed.add_field(
                name="Entrou no servidor em",
                value=userjoinedat
            )
            userembed.add_field(
                name="Criou seu Discord em",
                value=usercreatedat
            )
            userembed.add_field(
                name="TAG",
                value=user.discriminator
            )
            userembed.add_field(
                name="ID",
                value=user.id
            )

            await client.send_message(message.channel, embed=userembed)
        except IndexError:
            await client.send_message(message.channel, "Usuário não encontrado!")
        except:
            await client.send_message(message.channel, "Erro, desculpe. ")
        finally:
            pass
#HELP
    if message.content.lower().startswith('!help'):
        embed = discord.Embed(
            title="",
            color=0xe7002f,
            description="Olá, eu sou o bot do Alpha, um bot muito legal com várias funções. Para ver meus comandos digite: +comandos. Caso precise de ajuda contate um staff no servidor."
        )
        embed.set_author(
            name="Alpha",
            icon_url=client.user.avatar_url
        )
        embed.set_footer(
            text="Copyright © 2018 Bruno",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/423159064533532672/424213167317712946/dsg.png"
        )

        await client.send_message(message.channel, "Olá {}, te enviei todas minhas informações no seu privado!".format(
            message.author.mention))
        await client.send_message(message.author, embed=embed)
#COMANDOSINFO
    if message.content.lower().startswith('!comandos'):
        embed = discord.Embed(
            title="Meus comandos:",
            color=0xe7002f,
            description="!serverinfo » Veja as informações do servidor\n"
                        "!user <usuário> » Veja as informações de um usuário\n"
                        "!dado » Role um dado de um número de 1 á 6\n"
                        "!moeda » Brinque de cara ou coroa\n"
                        "!avatar <usuário> » Veja o avatar seu ou de um membro\n"
                        "!help » Veja as informações do servidor Alpha\n"
                        "!convite » Gere um convite e use o mesmo para convidar todos para nossa comunidade\n"
                        "!ping » Veja o tempo de resposta do bot\n"
                        "!moderação » Veja os comandos para moderação (Somente staff tem permissão para o mesmo)"
                        "Desenvolvido pelo Bruno. Mais informações aqui: [Clique.](https://discord.gg/TuDXw)"
        )
        embed.set_author(
            name="Alpha",
            icon_url=client.user.avatar_url
        )
        embed.set_footer(
            text="Copyright © 2018 Bruno",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/423159064533532672/424213167317712946/dsg.png"
        )

        await client.send_message(message.channel, "Olá {}, te enviei todos comandos no privado!".format(
            message.author.mention))
        await client.send_message(message.author, embed=embed)
#MODERAÇÃO
    if message.content.lower().startswith('!moderação'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        embed = discord.Embed(
            title="Comandos de moderação:",
            color=0xe7002f,
            description="!apagar <1 à 999> » Apague de 1 à 999 mensagens\n"
                        "!say » Bot repete a mensagem que foi dita\n"
                        "!aviso » Bot repete a mensagem que foi dita com sistema de embed\n"
                        "!sorteio » Gera um número de 1 à 999 para o sorteio\n"
                        "!jogando » Altera o status de jogando do bot\n"
                        "!votação » Inicia uma votação com a frase e a reação de like e deslike no bot\n"
                        "Desenvolvido pelo Bruno. Mais informações aqui: [Clique.](https://discord.gg/TuDXw)"
        )
        embed.set_author(
            name="Alpha",
            icon_url=client.user.avatar_url
        )
        embed.set_footer(
            text="Copyright © 2018 Bruno",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/423159064533532672/424213167317712946/dsg.png"
        )

        await client.send_message(message.channel, "Olá {}, te enviei todos comandos no privado!".format(
            message.author.mention))
        await client.send_message(message.author, embed=embed)
#APAGAR
    if message.content.lower().startswith('!apagar'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        qntdd = message.content.strip('+apagar ')
        qntdd = toint(qntdd)
        if qntdd <= 999:
            msg_author = message.author.mention
            await client.delete_message(message)
            # await asyncio.sleep(1)
            deleted = await client.purge_from(message.channel, limit=qntdd)
            botmsgdelete = await client.send_message(message.channel,'Deletei {} mensagens de um pedido de {} para {}'.format(len(deleted), qntdd, msg_author))
            await asyncio.sleep(5)
            await client.delete_message(botmsgdelete)

        else:
            botmsgdelete = await client.send_message(message.channel, 'Utilize o comando digitando /delete <numero de 1 a 100>')
            await asyncio.sleep(5)
            await client.delete_message(message)
            await client.delete_message(botmsgdelete)
#SAY
    if message.content.lower().startswith("!say"):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        msg = message.content[5:2000]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
#AVISO
    if message.content.startswith('!aviso'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        await client.delete_message(message)
        try:
            user = message.author
            msg = message.content[7:]

            embed = discord.Embed(
                description="{}".format(msg),
                color=0xe7002f)
            await client.send_message(message.channel, embed=embed)
        finally:
            pass
#BAN
    elif message.content.lower().startswith('!ban'):
        membro = message.mentions[0]
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, "❌ {} Você nao possui permissão para executar este comando!".format(message.author.mention))
        await client.send_message(message.channel, "✔ O staff {} baniu o membro {}!".format(message.author.mention, message.mentions[0].mention))
        await client.ban(membro)
#KICK
    elif message.content.lower().startswith('!kick'):
         member = message.mentions[0]
         if not message.author.server_permissions.administrator:
             return await client.send_message(message.channel, "❌ {} Você nao possui permissão para executar este comando!".format(  message.author.mention))
         await client.send_message(message.channel, "✔ O staff {} expulsou o membro {}!".format(message.author.mention, message.mentions[0].mention))
         await client.kick(member)
#MUTE
    elif message.content.lower().startswith('!mute'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        mention = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='Mutado ❌')
        await client.add_roles(mention, cargo)
        await client.send_message(message.channel, '✔ O membro {} foi mutado com sucesso!'.format(mention))
#UNMUTE
    elif message.content.lower().startswith('!unmute'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        mention = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='Mutado ❌')
        await client.remove_roles(mention, cargo)
        await client.send_message(message.channel, '✔ O membro {} foi desmutado com sucesso!'.format(mention))
        
    if message.content.lower().startswith("!gamer"):
        embed1 = discord.Embed(
            title="Escolha seu jogo!",
            color=0x1209e0,
            description="- Gamer = 🎮\n"
                        "- Paladins =  🏆\n"
                        "- GTA = 💣\n"
                        "- League of Legends = 🔸\n"
                        "- CS GO = 🔫\n"
                        "- Minecraft = ⛏\n"
                        "- Rocket League = 🚗\n"
                        "- Pubg = ☠\n"
                        "- Fortnite = ⚔", )

        botmsg = await client.send_message(message.channel, embed=embed1)

        await client.add_reaction(botmsg, "🎮")
        await client.add_reaction(botmsg, "🏆")
        await client.add_reaction(botmsg, "💣")
        await client.add_reaction(botmsg, "🔸")
        await client.add_reaction(botmsg, "🔫")
        await client.add_reaction(botmsg, "⛏")
        await client.add_reaction(botmsg, "🚗")
        await client.add_reaction(botmsg, "☠")
        await client.add_reaction(botmsg, "⚔")

        global msg_id
        msg_id = botmsg.id
        global msg_user
        msg_user = message.author

@client.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    if reaction.emoji == "🎮" and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🎮 Gamer", msg.server.roles)
     await client.add_roles(user, role)


    if reaction.emoji == "🏆"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🏆 Paladins", msg.server.roles)
     await client.add_roles(user, role)


    if reaction.emoji == "💣"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "💣GTA", msg.server.roles)
     await client.add_roles(user, role)

    if reaction.emoji == "🔸"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🔸 League of Legends", msg.server.roles)
     await client.add_roles(user, role)

    if reaction.emoji == "🔫"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🔫 CS GO", msg.server.roles)
     await client.add_roles(user, role)

    if reaction.emoji == "⛏"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "⛏ Minecraft", msg.server.roles)
     await client.add_roles(user, role)

    if reaction.emoji == "🚗"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🚗 Rocket League", msg.server.roles)
     await client.add_roles(user, role)

    if reaction.emoji == "☠"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "☠️ Pubg", msg.server.roles)
     await client.add_roles(user, role)

    if reaction.emoji == "⚔"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "⚔️ Fortnite", msg.server.roles)
     await client.add_roles(user, role)

@client.event
async def on_reaction_remove(reaction, user):
    msg = reaction.message

    if reaction.emoji == "🎮" and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🎮 Gamer", msg.server.roles)
     await client.remove_roles(user, role)


    if reaction.emoji == "🏆"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🏆 Paladins", msg.server.roles)
     await client.remove_roles(user, role)


    if reaction.emoji == "💣"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "💣GTA", msg.server.roles)
     await client.remove_roles(user, role)

    if reaction.emoji == "🔸"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🔸 League of Legends", msg.server.roles)
     await client.remove_roles(user, role)

    if reaction.emoji == "🔫"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🔫 CS GO", msg.server.roles)
     await client.remove_roles(user, role)

    if reaction.emoji == "⛏"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "⛏ Minecraft", msg.server.roles)
     await client.remove_roles(user, role)

    if reaction.emoji == "🚗"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "🚗 Rocket League", msg.server.roles)
     await client.remove_roles(user, role)

    if reaction.emoji == "☠"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "☠️ Pubg", msg.server.roles)
     await client.remove_roles(user, role)

    if reaction.emoji == "⚔"and msg.id == msg_id: #and user == msg_user :
     role = discord.utils.find(lambda r: r.name == "⚔️ Fortnite", msg.server.roles)
     await client.remove_roles(user, role)    
#JOIN
@client.event
async def on_member_join(member):

      grupo = discord.utils.find(lambda g: g.name == "👤 Membro", member.server.roles)
      await client.add_roles(member, grupo)

      channel = client.get_channel('418916675014885376')
      serverchannel = member.server.default_channel
      embedmsg = discord.Embed(
          title="Novo membro!",
          description="Seja bem-vindo ao servidor {}!".format(member.name),
          color=0xe7002f,
      )
      embedmsg.set_thumbnail(url=member.avatar_url)

      await client.send_message(channel, embed=embedmsg)

client.run(token)
