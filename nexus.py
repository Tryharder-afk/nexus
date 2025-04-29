import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

# -----------------------------
# CARREGANDO VARIÁVEIS DE AMBIENTE
# -----------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# -----------------------------
# CONFIGURAÇÃO INICIAL
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# -----------------------------
# LISTA DE CREEPYPASTAS
# -----------------------------
creepypastas = [
    "Você está deitado na sua cama e ouve um barulho vindo do corredor. Quando você vai ver, descobre que todos os membros da sua família desapareceram, mas as luzes estão ligadas em cada cômodo.",
    "Enquanto você estava indo dormir, sentiu um arrepio no pescoço. Quando olhou para o espelho, viu uma sombra estranha atrás de você, mas não havia ninguém na sala.",
    "Você acorda e percebe que sua mãe está ao seu lado, dizendo: 'Eu nunca te deixei sair da cama durante a noite'. Você começa a chorar, pois sua mãe já faleceu há muitos anos.",
    "Você entra em um site antigo e descobre uma foto sua tirada enquanto você estava dormindo. A legenda diz: 'Eu vi você'."
]

# -----------------------------
# EVENTOS
# -----------------------------
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="tryharder"), status=discord.Status.dnd)

# -----------------------------
# COMANDOS
# -----------------------------
@bot.command()
async def oi(ctx):
    await ctx.send('Oi! Eu estou online.')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='userinfo')
async def userinfo(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    embed = discord.Embed(title=f'Informações de {user.name}', color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name='ID do usuário', value=user.id, inline=False)
    embed.add_field(name='Nome de usuário', value=user.name, inline=False)
    embed.add_field(name='Tag', value=user.discriminator, inline=False)
    embed.add_field(name='Cargos', value=", ".join([role.name for role in user.roles[1:]]), inline=False)
    embed.add_field(name='Entrou no servidor em', value=user.joined_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
    embed.add_field(name='Criado em', value=user.created_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)

    await ctx.send(embed=embed)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade: int):
    if quantidade > 100:
        await ctx.send('Você só pode apagar até 100 mensagens por vez.')
        return
    await ctx.channel.purge(limit=quantidade + 1)
    mensagem = await ctx.send(f'O chat teve {quantidade} mensagens apagadas por {ctx.author.mention}')
    await mensagem.delete(delay=10)

@bot.command(name='creepypasta')
async def creepypasta(ctx, user: discord.Member):
    creepypasta = random.choice(creepypastas)
    try:
        await user.send(f"Uma creepypasta para você: {creepypasta}")
        await ctx.send(f"Enviei a creepypasta na DM do {user.mention} kkkkkk")
    except discord.Forbidden:
        await ctx.send(f"Não consegui enviar a creepypasta para {user.mention}, provavelmente ele está com DM desabilitada.")

@bot.command(name='nuke')
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    canal_atual = ctx.channel

    if isinstance(canal_atual, discord.TextChannel):
        nome_canal = canal_atual.name
        categoria_canal = canal_atual.category
        guild = ctx.guild

        await canal_atual.delete()
        novo_canal = await guild.create_text_channel(nome_canal, category=categoria_canal)
        await novo_canal.send(f'O canal foi **nukado** por {ctx.author.mention}.')
    else:
        await ctx.send('Esse comando só pode ser usado em canais de texto!')

@bot.command(name='serverinfo')
async def serverinfo(ctx):
    guild = ctx.guild
    dono = guild.owner.mention if guild.owner else "Desconhecido"
    icon_url = guild.icon.url if guild.icon else None

    embed = discord.Embed(
        title=guild.name,
        description="Informações sobre este servidor:",
        color=discord.Color.blurple()
    )

    if icon_url:
        embed.set_thumbnail(url=icon_url)

    embed.add_field(name="Nome do servidor", value=guild.name, inline=False)
    embed.add_field(name="ID do servidor", value=guild.id, inline=False)
    embed.add_field(name="Dono", value=dono, inline=False)
    embed.add_field(name="Membros", value=guild.member_count, inline=False)
    embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)

    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="Lista de Comandos",
        description="Aqui estão os comandos disponíveis:",
        color=discord.Color.green()
    )
    embed.add_field(name="!oi", value="O bot responde com um 'Oi!'", inline=False)
    embed.add_field(name="!ping", value="Testa a latência do bot (Pong!)", inline=False)
    embed.add_field(name="!userinfo [usuário]", value="Mostra informações de um usuário", inline=False)
    embed.add_field(name="!clear [quantidade]", value="Limpa uma quantidade de mensagens do chat", inline=False)
    embed.add_field(name="!creepypasta [usuário]", value="Manda uma creepypasta aleatória na DM do usuário", inline=False)
    embed.add_field(name="!nuke", value="Apaga e recria o canal atual", inline=False)
    embed.add_field(name="!serverinfo", value="Mostra informações do servidor", inline=False)
    embed.set_footer(text="Use os comandos com responsabilidade!")

    await ctx.send(embed=embed)

# -----------------------------
# TRATAMENTO DE ERROS
# -----------------------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para usar esse comando.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Você esqueceu de colocar o número de mensagens. Exemplo: !clear 5')
    else:
        print(f'Erro encontrado: {error}')

# -----------------------------
# EXECUÇÃO DO BOT
# -----------------------------
bot.run(TOKEN)
