import discord
import os
from dotenv import load_dotenv
import datetime

load_dotenv()  # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    emojis = ["🟦", "⭐", "🟢", "🔶", "❤️"]
    fridays = get_fridays_this_month()
    msg = f"@Players Scheduling for this month! Our play dates this time around are:\n"
    
    for i, date in enumerate(fridays):
        msg += f"{date.strftime('%B %d')} ({emojis[i]})\n"
    
    msg += "If a day doesn't work for you please react to this post with the emoji for the corresponding day to opt-out!"
    view = MyView()
    # Adding buttons with the callback
    for i, date in enumerate(fridays):
        emoji = emojis[i]
        button = discord.ui.Button(label=emoji, custom_id=emoji, style=discord.ButtonStyle.primary)
        button.callback = view.button_callback  # Assign the button callback here
        view.add_item(button)

    await ctx.respond(msg, view=view)

def get_fridays_this_month():
    today = datetime.date.today()
    # Get the first day of the current month
    first_day_of_month = today.replace(day=1)
    
    # Find the first Friday of the current month
    first_friday = first_day_of_month + datetime.timedelta(days=(4 - first_day_of_month.weekday()) % 7)
    
    # Find all Fridays of the current month
    fridays = []
    current_friday = first_friday
    while current_friday.month == today.month:
        fridays.append(current_friday)
        current_friday += datetime.timedelta(weeks=1)
    
    return fridays

async def add_reaction_to_message(message, emoji):
    await message.add_reaction(emoji)

async def get_previous_bot_message(channel):
    messages = [msg async for msg in channel.history()]
    for i in messages:
        if i.author.name == "Docent":
            return i
    return None

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # timeout of the view must be set to None
        self.current_interaction = None  # Store the interaction here

    async def button_callback(self, interaction: discord.Interaction):
        self.current_interaction = interaction
        message = await get_previous_bot_message(interaction.channel)
        if message:
            await message.add_reaction(interaction.data['custom_id'])
        await interaction.response.send_message("You have opted out for this day!", ephemeral=True)


bot.run(os.getenv('TOKEN'))  # run the bot with the token
