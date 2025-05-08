import discord
import requests
import asyncio
import os

# Load environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_stock():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    previous_stock = []

    while not client.is_closed():
        try:
            response = requests.get("https://fruityblox.com/api/stock")
            response.raise_for_status()
            stock_data = response.json()

            # Extract fruit names from stock_data
            current_fruits = [fruit.get("name", "").lower() for fruit in stock_data]

            # Check for new fruits
            new_fruits = [fruit for fruit in current_fruits if fruit not in previous_stock]
            for fruit in new_fruits:
                if "mirage" in fruit or fruit in ["dragon", "dough", "leopard", "venom", "control"]:  # adjust as needed
                    await channel.send(f"🍍 **New Fruit in Stock**: `{fruit.title()}`")

            previous_stock = current_fruits

        except Exception as e:
            print(f"Error checking stock: {e}")

        await asyncio.sleep(300)  # Check every 5 minutes

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

client.loop.create_task(check_stock())
client.run(TOKEN)
