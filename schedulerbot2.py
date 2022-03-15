import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.commands import Option
from dotenv import load_dotenv
import os
import re

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.emojis_and_stickers = True
bot = commands.Bot(command_prefix='!', intents=intents)
raidicons = ['<:vog:953003822366736424>', '<:lw:953002957027291167>', '<:dsc:953003247864545280>', '<:votd:953002604600893470>', '<:gos:953002644920758342>', '<:raid:952994000959336518>', '<:camp:953012764174065744>', '<:patrol:953012764228612157>', '<:contact:953012764115341372>', '<:seraph:953012764228603964>', '<:strike:953012764316688524>', '<:dungeon:953012766363516928>']
bipid = [759362928276537410]
TOKEN = os.environ.get('TOKEN')

class SchedulerButton(Button):
    def __init__(self, emoji, view, thread, threadinteraction):
        super().__init__(label=',', emoji=emoji)
        self.messagepointer = view
        self.thread = thread
        self.threadinteraction = threadinteraction
    async def callback(self, interaction):
        attendees = ""
        joined = False
        if self.label == '':
            self.label = ','
        userlist = re.split(',',self.label)
        i = 0
        while i < len(userlist):
            if userlist[i]==interaction.user.name:
                joined = True
                i += 1
            elif not userlist[i]=='':
                if attendees == '':
                    attendees =  userlist[i]
                else:
                    attendees =  userlist[i] + ',' + attendees
                i += 1
            else:
                i += 1
        
        if joined == False and attendees == '':
            attendees = interaction.user.name 
        elif joined == True and attendees == '':
            attendees = ','
        elif joined == False:
            attendees = attendees + ',' + interaction.user.name
        self.label = attendees
        if self.threadinteraction == True:
            await self.thread.add_user(interaction.user)
        else:
            await self.thread.remove_user(interaction.user)
        await interaction.response.edit_message(view=self.messagepointer)
        

@bot.event
async def on_ready():
  print('{0.user} is logged in'.format(bot))

RAIDS = ['Vault of Glass', 'Master Vault of Glass', 'Vow of the Disciple', 'Master Vow of the Disciple', 'Last Wish', 'Garden of Salvation', 'Deep Stone Crypt']
TIMES = ['Tänään', 'Huomenna', 'Ennen resettiä', 'Tällä viikolla']

async def get_raids(ctx: discord.AutocompleteContext):
    return [place for place in RAIDS if place.startswith(ctx.value.lower())]

async def get_times(ctx: discord.AutocompleteContext):
    return [place for place in TIMES if place.startswith(ctx.value.lower())]

@bot.slash_command(guild_ids=bipid, name="lfg", description="Etsitään seuraa tositarkoituksella")
async def lfg(ctx,
                activity: Option(str, "Which activity do you fancy?", required=True, autocomplete=get_raids),
                time: Option(str, "When shall you be going, sir?", required=True, autocomplete=get_times),
                description: Option(str,
                              "Would you like to add some infomration to that?",
                              required=False,
                              default='-')
                ):
    #await ctx.respond(f"Scorn Walker walking the Scorn walk from {activity} to {time} at a speed of {description}")
    view = View(timeout=None)
    thread = await createThread(ctx, activity, time, description)
    await initTimes(view, thread)
    await ctx.respond("", view=view)

async def initTimes(view, thread):
    jointhread = True
    leavethread = False
    buttonskip = SchedulerButton("🚫", view, thread, leavethread)
    button09 = SchedulerButton("<:09:948168884463222854>", view, thread, jointhread)
    button10 = SchedulerButton("<:10:952989679169470504>", view, thread, jointhread)
    button11 = SchedulerButton("<:11:948168884429672488>", view, thread, jointhread)
    button12 = SchedulerButton("<:12:948168884085739581>", view, thread, jointhread)
    button13 = SchedulerButton("<:13:948168884421275658>", view, thread, jointhread)
    button14 = SchedulerButton("<:14:948168884404510720>", view, thread, jointhread)
    button15 = SchedulerButton("<:15:948168884475809812>", view, thread, jointhread)
    button16 = SchedulerButton("<:16:948168884064763905>", view, thread, jointhread)
    button17 = SchedulerButton("<:17:948168884282880021>", view, thread, jointhread)
    button18 = SchedulerButton("<:18:948168884408696862>", view, thread, jointhread)
    button19 = SchedulerButton("<:19:948168884492595230>", view, thread, jointhread)
    button20 = SchedulerButton("<:20:948168884505178162>", view, thread, jointhread)
    button21 = SchedulerButton("<:21:948168884186394635>", view, thread, jointhread)
    button22 = SchedulerButton("<:22:948168884089937981>", view, thread, jointhread)
    button23 = SchedulerButton("<:23:948168884438065182>", view, thread, jointhread)
    button00 = SchedulerButton("<:00:948168884438069288>", view, thread, jointhread)
    view.add_item(buttonskip)
    view.add_item(button09)
    view.add_item(button10)
    view.add_item(button11)
    view.add_item(button12)
    view.add_item(button13)
    view.add_item(button14)
    view.add_item(button15)
    view.add_item(button16)
    view.add_item(button17)
    view.add_item(button18)
    view.add_item(button19)
    view.add_item(button20)
    view.add_item(button21)
    view.add_item(button22)
    view.add_item(button23)
    view.add_item(button00)

async def createThread(ctx, activity, time, description):
    
    view = View(timeout=None)
    msg = discord.Embed(title=activity, description=description, color=0x0ff0e3)
    
    msg.add_field(name="Ajankohta", value=time, inline=False)
    msg.add_field(name="<:raid:952994000959336518>: " + activity, value='.')
    
    # i = 2
    # while i < len(info):
    #   msg.add_field(name=raidicons[i-2] + ": " + info[i], value='.')
    #   i += 1
    post = await ctx.channel.send(embed=msg)
    thread = await post.create_thread(name=activity)
    
    # i = 2
    # while i < len(info):
    choicebutton = SchedulerButton("<:raid:952994000959336518>", view, thread, True)
    #choicebutton = Button(emoji=raidicons[0])
    view.add_item(choicebutton)
    #   i += 1
    
    await ctx.send("", view=view)
    return thread

bot.run(TOKEN)