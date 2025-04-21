import discord
from discord.ext import commands
import os
import keep_alive  

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Créer un embed de bienvenue pour un nouveau membre
def create_welcome_embed(member):
    return discord.Embed(
        title=f"🎉 Bienvenue {member.name} !",
        description="On est super content de t'avoir avec nous ! Si tu as des questions, n'hésite pas.",
        color=discord.Color.blue()
    ).set_thumbnail(
        url=member.avatar.url if member.avatar else member.default_avatar.url
    ).set_footer(
        text="YARObot • Serveur by YARO 🧠"
    )

# Quand le bot est prêt
@bot.event
async def on_ready():
    print(f"{bot.user.name} est maintenant en ligne ! 🎉")

# Quand un membre rejoint, on envoie un message de bienvenue
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="🛬-welcome")
    if channel:
        await channel.send(embed=create_welcome_embed(member))

# Commande pour créer un embed personnalisé
@bot.command()
async def setupYaro(ctx):
    await ctx.send("📌 D'abord, envoie-moi le **titre** de ton embed :")
    try:
        title_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        title = title_msg.content

        await ctx.send("📝 Maintenant, envoie-moi la **description** de ton embed :")
        desc_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60)
        description = desc_msg.content

        embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
        embed.set_footer(text="YARObot • Powered by YARO 🚀")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Oups, il y a eu une erreur : {e}")

# Commande pour modifier un embed existant
@bot.command()
async def edit(ctx):
    await ctx.send("📩 Envoie-moi l'ID du message à modifier (fais un clic droit et copie l’identifiant).")
    try:
        msg_id = int((await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content)
        msg = await ctx.channel.fetch_message(msg_id)
        embed = msg.embeds[0]

        await ctx.send("🔧 Tu veux modifier quoi ? (`titre`, `description`, `footer`)")
        field = (await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content.lower()

        if field not in ["titre", "description", "footer"]:
            await ctx.send("❌ C'est une option invalide. Utilise `titre`, `description` ou `footer`.")
            return

        await ctx.send(f"✏️ Donne-moi la nouvelle valeur pour {field} :")
        new_value = (await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)).content

        if field == "titre":
            embed.title = new_value
        elif field == "description":
            embed.description = new_value
        elif field == "footer":
            embed.set_footer(text=new_value)

        await msg.edit(embed=embed)
        await ctx.send("✅ L'embed a bien été modifié !")
    except Exception as e:
        await ctx.send(f"❌ Oups, une erreur est survenue : {e}")

# Lancement du keep-alive pour garder le bot actif
keep_alive.keep_alive()

# Lancement du bot avec le token depuis les variables d'environnement
bot.run(os.getenv("DISCORD_TOKEN"))


