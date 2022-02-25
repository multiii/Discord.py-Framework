from tinydb import TinyDB, Query

from .storage import YAMLStorage

User = Query()

db = TinyDB("database.yaml", storage=YAMLStorage)

pr = db.table("prefix")

def get_prefix(bot, message):
  if not message.guild:
    return "?"
    
  if not bool(pr.get(User.id == message.guild.id)):
    return "?"

  return pr.get(User.id == message.guild.id)["prefix"]

def clean_none(arg, datatype: type=str) -> str:
  match = {str: "", int: 0, bool: False}

  if arg is None:
    return match[datatype]
  return arg