
# -*- coding: utf-8 -*-

from discord.ext import tasks
from discord.ext import commands
from datetime import *

import datetime
import discord
import asyncio

intents		= discord.Intents.default()
intents.message_content = True
intents.members = True

Token		= ""
Channel		= "1188753134676365362"

class MyBot(commands.Bot):
	
	def __init__(self, command_prefix, intent, channel="0"):
		self.VC = channel
		commands.Bot.__init__(self, command_prefix=command_prefix, intents=intent)
		
	async def on_ready(self):
		self.message1 = f"正在使用身分: {self.user}({self.user.id})"
		self.message2 = f"即將在 [{self.get_channel(int(self.VC))}]({self.get_channel(int(self.VC)).id}) 播放春日影"
		
		print(self.message1)
		print(self.message2)
		self.Player.start()
		
		self.Reflash_CharacterAI.start()

	
	async def on_message(self, message):
		#排除自己的訊息，避免陷入無限循環
		if str(message.author).find(str(self.user)) != -1:
			return

		#列印接收到的訊息
		print(f"[{Get_Time()}] Get Message from {str(message.guild)}.{str(message.channel)}.{str(message.author.display_name)}: {str(message.content)}")
		
		
	utc = datetime.timezone.utc
	times = [
		datetime.time(hour=0, tzinfo=utc)
	]
	#Reflash CharacterAI
	@tasks.loop(time=times)
	async def Reflash_CharacterAI(self):
		await self.CloseSelf()

	#播放器ですわ☆
	@tasks.loop(count=1)
	async def Player(self):
		channel = self.get_channel(int(self.VC))
		await channel.connect()
		
		voice = discord.utils.get(self.voice_clients)
		
		while True:
			PCM = discord.FFmpegPCMAudio(executable='ffmpeg/bin/ffmpeg', source='data/春日影 (MyGO!!!!! ver.).flac')
			voice.play(PCM)
			voice.source.volume = 0.2
			while voice.is_playing() or voice.is_paused():
				await asyncio.sleep(1)


def bot1():
	# Your code here
	bot = MyBot(command_prefix="/", intent=intents, channel=Channel)
	bot.run(Token)

#獲取時間
def Get_Time():
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")


bot1()