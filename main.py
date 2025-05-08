import discord
import requests
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()

class MyBot(discord.Client):
    async def setup_hook(self):
        # Start background task when the bot is ready
        self.bg_task = self.loop.create_task(self.check_stock())

    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

    async def check_stock(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)
        if channel is None:
            print("❌ Channel not found.")
            return

        previous_fruits = []

        while not self.is_closed():
            try:
                response = requests.get("https://fruityblox.com/api/stock")
                response.raise_for_status()
                stock_data = response.json()

                current_fruits = [fruit.get("name", "").lower() for fruit in stock_data]

                new_fruits = [fruit for fruit in current_fruits if fruit not in previous_fruits]
                for fruit in new_fruits:
                    if "mirage" in fruit or fruit in ["dragon", "dough", "leopard", "venom", "control"]:
                        await channel.send(f"🍍 **New Fruit in Stock**: `{fruit.title()}`")

                previous_fruits = current_fruits

            except Exception as e:
                print(f"❌ Error fetching stock: {e}")

            await asyncio.sleep(300)  # Check every 5 minutes

# Run bot
client = MyBot(intents=intents)
client.run(TOKEN)
