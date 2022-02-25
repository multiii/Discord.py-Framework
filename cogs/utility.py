import discord
from discord.ext import check, commands
from tinydb import TinyDB, Query

from utils import resources
from utils.storage import YAMLStorage

User = Query()

db = TinyDB("database.yaml", storage=YAMLStorage)

pr = db.table("prefix")

class Utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    name="adduser",
    brief="adds users to the database!"
  )
  @check.has_user_id_in([511728748647677973, 283451159593615361, 394320584089010179])
  async def _adduser(self, ctx, user: discord.User, channel: discord.TextChannel):
    await resources.default.embed(
      msg=ctx.message,
      title="Added User!",
      description=f"The user {user.mention} was added to the database!\n\nChannel: {channel.mention}"
    )

    row = self.bot.economy.find_one({'user_id': user.id})

    if row is None:
      return self.bot.economy.insert_one({
        "user_id": str(user.id),
        "channel_id": str(channel.id)
      })

    self.bot.economy.update_one(
      {"user_id": str(user.id)},
      {"$set": {"channel_id": str(channel.id)}}
    )

  @commands.command(
    name="createroom",
    brief="create a room for a user (channels and roles)!"
  )
  @check.has_user_id_in([511728748647677973, 283451159593615361, 394320584089010179])
  async def _createroom(self, ctx, *, name):
    cat = await ctx.guild.create_category_channel(name=f"💎 ~ {name}’s Private Room")

    text_names = ["about-me", "menus-and-more", "admin-chat", "content", "chat", "public-chat"]

    for text_name in text_names:
      await cat.create_text_channel(
        name=text_name,
        overwrites={
          ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
      )

    await cat.create_voice_channel(
      name="Going Live",
      overwrites={
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
      }
    )

    await ctx.guild.create_role(name=f"{name} Verified Model")
    await ctx.guild.create_role(name=f"{name} Buyer")
    

  @commands.command(
    name="prefix",
    brief="used to change the bot's prefix"
  )
  @commands.has_permissions(manage_guild=True)
  async def _prefix(self, ctx, *, prefix):
    if len(prefix) > 3:
      return await resources.error.embed(
        msg=ctx.message,
        title="Prefix exceeded 3 characters!",
        description=f"Your bot prefix, for the server `{ctx.guild.name}` cannot exceeed 3 characters. Please retry the command"
      )

    await resources.default.embed(
      msg=ctx.message,
      title="Prefix successfully changed!",
      description=f"Your bot prefix, for the server `{ctx.guild.name}` was successfully changed to {prefix}"
    )

    pr.upsert({"id": ctx.guild.id, "prefix": prefix})

def setup(bot):
  bot.add_cog(Utility(bot))