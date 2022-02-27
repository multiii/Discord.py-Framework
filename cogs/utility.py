from nextcord.ext import commands
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
