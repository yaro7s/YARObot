import discord
from discord.ext import commands
import keep_alive  # pour garder le bot en ligne

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt !")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="🛬-welcome")
    if channel:
        embed = discord.Embed(
            title=f"🎉 welcome {member.name} !",
            description="We're so happy to have you here!\nMake yourself comfortable and don't hesitate to ask questions.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="YARObot • Serveur by YARO 🧠")
        await channel.send(embed=embed)

@bot.command()
async def setupYaro(ctx):
    await ctx.send("📌 Donne-moi le **titre** que tu veux mettre dans l'embed :")

    def check_author(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        title_msg = await bot.wait_for("message", check=check_author, timeout=60)
        title = title_msg.content

        await ctx.send("📝 Maintenant, donne-moi le **contenu** de l'embed :")
        desc_msg = await bot.wait_for("message", check=check_author, timeout=60)
        description = desc_msg.content

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        embed.set_footer(text="YARObot • Powered by YARO 🚀")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Une erreur est survenue : {e}")

@bot.command()
async def edit(ctx):
    await ctx.send("📩 Donne l'ID du message à modifier (clic droit > Copier l’identifiant)")

    def check_author(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg_id_msg = await bot.wait_for("message", check=check_author, timeout=60)
        msg_id = int(msg_id_msg.content)

        await ctx.send("🔧 Que veux-tu modifier ? (`titre`, `description`, `footer`)")
        modif_msg = await bot.wait_for("message", check=check_author, timeout=60)
        modif = modif_msg.content.lower()

        if modif not in ["titre", "description", "footer"]:
            await ctx.send("❌ Option invalide. Utilise `titre`, `description` ou `footer`.")
            return

        await ctx.send(f"✏️ Envoie la nouvelle valeur pour **{modif}** :")
        new_value_msg = await bot.wait_for("message", check=check_author, timeout=60)
        new_value = new_value_msg.content

        msg = await ctx.channel.fetch_message(msg_id)
        embed = msg.embeds[0]

        if modif == "titre":
            embed.title = new_value
        elif modif == "description":
            embed.description = new_value
        elif modif == "footer":
            embed.set_footer(text=new_value)

        await msg.edit(embed=embed)
        await ctx.send("✅ Embed modifié avec succès !")

    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")

# Lancer le keep_alive
keep_alive.keep_alive()

# Ton token ici
bot.run("MTM2MzQ2NjIyNTI5NTgyMjk2OQ.GZDrSd.zObe3iggswivGCy_IKw_SBQLO7XbLPODKG0Ahg")
