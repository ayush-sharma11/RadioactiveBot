from discord.ext.commands import Bot as BotBase, CommandNotFound
from discord import Intents, Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import version

from ..db import db

PREFIX = "rb "
OWNER_IDS  = [622126341344460812]
VERSION = version.VERSION

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave()

        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents = Intents.all(),
                         )
    
    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as token:
            self.TOKEN = token.read()
        
        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            await args[0].send("Something went wrong.")
            # passes this string on command error
            # first element of the args will be the one we can send message back to
        
        debug_channel = self.get_channel(1146436184181051452)
        await debug_channel.send("An error occured.")

        raise
        # it re raises the error

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, CommandNotFound):
            # checks whether the first argument is an instance of the second argument
            pass
        
        elif hasattr(exception, "original"):
            # checks if exception has an attribute called original
            raise exception.original

        else:
            raise exception

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            # self.guild = self.get_guild(guild_number) only is single server bot

            self.scheduler.start()

            debug_channel = self.get_channel(1146436184181051452)
            embed = Embed(
                title = "Start Message",
                description = "Radiactive Bot is online!",
                color = 0xFFFF00,
                timestamp = datetime.utcnow()
            )

            fields = [("Enjoy using the bot!", "Remember to adhere to Discord rules!", False)] # it wont be inline
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline  = inline)

            file = File("radioactive.png")

            embed.set_author(
                name = "Radioactive Bot",
                icon_url = "attachment://radioactive.png"  # bot cover image
            )

            embed.set_footer(text=f"Radioactive Bot | version {VERSION}")

            embed.set_thumbnail(url="attachment://radioactive.png")
            
            await debug_channel.send(file=file, embed=embed)

            print("bot ready")
        
        else:
            print("bot reconnected")

    async def on_message(self, message):
        pass

bot = Bot()
