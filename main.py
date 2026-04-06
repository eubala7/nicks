import discord
from discord.ext import commands, tasks
import random
import string
import asyncio

TOKEN = 'MTQ5MDc3ODc4NTI2NjY2NzY1Mg.GPwwya.atXGRj3DfBbFfFb_ESG1YSygemqYUCCgLnbdKw'
ID_DO_CANAL = 1490779950326747327

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def gerar_nick():
    # Sorteia entre 4 ou 5 caracteres
    tamanho = random.randint(3, 4) 
    # Força a mistura de letras (abc...) e números (012...)
    caracteres = string.ascii_lowercase + string.digits 
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@bot.event
async def on_ready():
    print(f'--- SNIPER ATIVADO: {bot.user} ---')
    verificador_infinito.start()

@tasks.loop(seconds=15)
async def verificador_infinito():
    canal = bot.get_channel(ID_DO_CANAL)
    if not canal: return

    nick_teste = gerar_nick()
    # AGORA VAI APARECER NO TERMINAL TUDO O QUE ELE TESTAR:
    print(f"DEBUG: Testando agora -> {nick_teste}")

    try:
        await bot.fetch_user(nick_teste)
        # Se achou o user, o nick está ocupado
    except discord.NotFound:
        # Se NÃO achou, posta a Embed bonitona
        print(f"✅ SUCESSO: {nick_teste} parece livre!")
        embed = discord.Embed(
            title=f"✅ {nick_teste}",
            description="Está **disponível** para uso a partir do momento desta mensagem.",
            color=0x00ff00
        )
        embed.set_footer(text="Verificado via API Real-time")
        await canal.send(embed=embed)
    except discord.HTTPException as e:
        if e.status == 429:
            print("⚠️ Rate Limit! Pausando 60s...")
            await asyncio.sleep(60)
    except Exception as e:
        print(f"Erro: {e}")

bot.run(TOKEN)
