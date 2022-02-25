import requests
import itertools

from moviepy.config import change_settings
from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip

change_settings({"IMAGEMAGICK_BINARY": r"/usr/bin/convert"})

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

class Listeners(commands.Cog):
  def __init__(self, bot):
    self.bot = bot  

  async def send_image(self, msg, channel_id):
    guild_name = "<Server Name>"

    image = msg.attachments[0]
    image_data = requests.get(image.url).content


    with open("./images/image.png", "wb") as handler:
      handler.write(image_data)

    image = Image.open("./images/image.png")

    width, height = image.size
    font = ImageFont.truetype('./fonts/RobotoSlab-Regular.ttf', width // 10)

    with image.convert("RGBA") as base:

      txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
      d = ImageDraw.Draw(txt)

      text = f"{msg.author.name}#{msg.author.discriminator}"

      x = (width - (len(text) * width * 0.05)) // 2
      y = height // 2

      for i, j in itertools.product((-3, 0, -3), (-3, 0, -3)):
        d.text((x + i, y + j), text, font=font, fill=(128, 128, 128, 125))

      d.text((x, y), text, font=font, fill=(255, 255, 255, 125))

      text = guild_name

      x = (width - (len(text) * width * 0.05)) // 2
      y = (height // 2) - (height // 4)

      for i, j in itertools.product((-3, 0, -3), (-3, 0, -3)):
        d.text((x + i, y + j), text, font=font, fill=(128, 128, 128, 125))

      d.text((x, y), text, font=font, fill=(255, 255, 255, 125))

      image = Image.alpha_composite(base, txt)
    
    image.save("./images/w_image.png")

    image = Image.open('./images/w_image.png')

    # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    
    image_without_exif.save('./images/w_image.png')

    await self.bot.get_channel(channel_id).send(file=discord.File("./images/w_image.png"))

  async def send_video(self, msg, channel_id):
    video = msg.attachments[0]
    video_data = requests.get(video.url).content

    with open("./videos/video.mp4", "wb") as handler:
      handler.write(video_data)

    video = VideoFileClip("./videos/video.mp4", audio=True)

    width, height = video.size

    text = TextClip(
      txt=f"{msg.author.name}#{msg.author.discriminator}",
      font="./fonts/RobotoSlab-Regular.ttf", color="white",
      fontsize=width // 10
    )

    txt_col = text.on_color(pos=(6, "center"), col_opacity=0.6)

    final = CompositeVideoClip([video, txt_col])

    final.subclip(0).write_videofile(
      "./videos/w_video.mp4",
      fps=24,
      codec="libx264"
    )

    await self.bot.get_channel(channel_id).send(file=discord.File("./videos/w_video.png"))

  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.guild:
      return

    row = self.bot.economy.find_one({'user_id': str(msg.author.id)})

    if row is None:
      return

    if len(msg.attachments) == 0:
      return

    if msg.attachments[0].content_type.split("/")[0] == "image":
      await self.send_image(msg, row["channel_id"])

    else:
      await self.send_video(msg, row["channel_id"])

def setup(bot):
  bot.add_cog(Listeners(bot))