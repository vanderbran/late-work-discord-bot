import discord
import discord.utils
from discord.ext import commands
import os 
import time
import logging
import asyncio
from dotenv import load_dotenv



TICKET_COUNTER = 1

# bot prefix and intents

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

# class for logging information I may need 
logger = logging.getLogger(__name__)
logging.basicConfig(filename="bot.log", level=logging.INFO)
logger.info("STARTED LOGGING")

# Event: bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# # Accessor for a certain category (used for grabbing tickets) 
# async def get_category(guild, category_name):
#     for category in guild.categories:
#         if category.name == category_name:
#             return category
#     return None  # Return None if category not found

# @bot.event
# async def on_message(message):

#     # REMOVING TICKETS FOR DEBUG 
#     if(message.content == "xdd?" and message.user_id == 313472722615271427):
#         category = discord.utils.get(message.guild.categories, name="tickets")

#         for i in category.channels:
#             await i.delete()


# Prompts the user to submit work through a discord channel
async def handle_ticket(user, payload, channel, ticketNumber):

    # TODO : different class sections

    skip = False 
    message = ("Hello %s, I am ready for you to enter an assignment. " % user.mention)
    await channel.send(message)

    # # These checks waits for a message from the user who opened the ticket
    # def check1(m):
    #     type = ["lab","zybooks","program","icp"]
    #     return m.content.lower() in type and m.channel == channel and m.author == user
    
    def check2(m):
        return m.channel==channel and m.author == user
    
    # try:
    #     msg = await bot.wait_for("message", check=check1, timeout=180.0)
    #     text = msg.content.lower()

    # except asyncio.TimeoutError:
    #     skip = True 
    #     await channel.send("Oops! You took too long. Open another ticket if needed. ")
    #     # for i in range(1,10):
    #     #     time.sleep(1)
    #     # await channel.delete()

    #     
    if(not skip):
        
        await channel.send("Please enter the assignment you want to submit, no spaces. (ex: Assignment1)")
        
        try:
            msg = await bot.wait_for("message", check=check2, timeout=180.0)
            print(msg.content)
            file_save = msg.content
        except asyncio.TimeoutError:

            await channel.send("Oops! You took too long. Open another ticket if needed. ")
            for i in range(1,10):
                time.sleep(1)
            await channel.delete() 

        await channel.send("Finally, please upload your ZIP file. Make sure that it has your Tech username in it (or else I don't know who you are!)")

        attachment = "" 
        try:
            msg = await bot.wait_for("message", check=check2, timeout=180.0)
        
            if msg.attachments:
                    attachment = msg.attachments[0]

        except asyncio.TimeoutError:

            await channel.send("Oops! You took too long. Open another ticket if needed. ")
            for i in range(1,10):
                time.sleep(1)
            await channel.delete()  

        logger.info("Recieved file %s from %s in Ticket#%d" % (attachment.filename, user.name, ticketNumber))
        await attachment.save("SUBMIT/ASSIGNMENTS/"+str(file_save)+"/"+attachment.filename)


            
        # elif text == "zybooks":
        #     await channel.send("Please enter your Tech username (NOT T#) and the Zybooks you want to submit (can be multiple) (ex: bvandergriff 1,2,3)")
        #     try:
        #         msg = await bot.wait_for("message", check=check2, timeout=180.0)
        #         text = msg.content

        #     except asyncio.TimeoutError:

        #         await channel.send("Oops! You took too long. Open another ticket if needed. ")
        #         for i in range(1,10):
        #             time.sleep(1)
        #         await channel.delete() 

        #     print(text)
        #     text = text.replace(" ", "_")
        #     print(text)

        #     with open("SUBMIT/ZYBOOKS/"+str(text), "w+"):
        #         pass
        #     logger.info("Recieved file %s from %s in Ticket#%d" % (text, user, ticketNumber))

            
        # # Grab file from user, and place in ICP directory 
        # elif text == "icp": 

        #     await channel.send("Finally, please upload your file. Make sure that it has your Tech username in it (or else I don't know who you are!)")

        #     try:
        #         msg = await bot.wait_for("message", check=check2, timeout=60.0)
        #         file_save = msg.attachments[0]
        #     except asyncio.TimeoutError:

        #         await channel.send("Oops! You took too long. Open another ticket if needed. ")
        #         for i in range(1,10):
        #             time.sleep(1)
        #         await channel.delete() 
            
        #     logger.info("Recieved file %s from %s in Ticket#%d" % (file_save.filename, user, ticketNumber))
        #     await file_save.save("SUBMIT/ICPS/"+file_save.filename)

        # # Find out which program, then throw in respective directory
        # elif text == "program":
        #     await channel.send("Please enter the program you want to submit, no spaces. (ex: Program1)")
            
        #     try:
        #         msg = await bot.wait_for("message", check=check2, timeout=60.0)
        #         file_save = msg.attachments[0]
        #     except asyncio.TimeoutError:

        #         await channel.send("Oops! You took too long. Open another ticket if needed. ")
        #         for i in range(1,10):
        #             time.sleep(1)
        #         await channel.delete()  

        #     await channel.send("Finally, please upload your ZIP file. Make sure that it has your Tech username in it (or else I don't know who you are!)")

        #     try:
        #         msg = await bot.wait_for("message", check=check2, timeout=60.0)
        #     except asyncio.TimeoutError:

        #         await channel.send("Oops! You took too long. Open another ticket if needed. ")
        #         for i in range(1,10):
        #             time.sleep(1)
        #         await channel.delete()  
            
        # logger.info("Recieved file %s from %s in Ticket#%d" % (file_save.filename, user, ticketNumber))
        # await file_save.save("SUBMIT/PROGRAMS/"+str(file_save)+"/"+file_save.filename)

        # ticket is done, goodbye! 
        await channel.send("Recieved. Please take note of your ticket number, in case something goes wrong. This channel will close in 10 seconds." )
        for i in range(1,10):
            time.sleep(1)
        await channel.delete()

    # someone didn't respond to the ticket, or didn't input one of the options 
    else:
        await channel.send("Error. Please open another ticket. ")
        for i in range(1,15):
            time.sleep(1)
        await channel.delete()
        
# Creates a ticket for the user, then passes to handle_ticket() function
async def create_ticket_channel(payload): 

    # grrr global variable
    # assign to local to prevent too many processes incrementing and ruining my beautiful ticket system
    global TICKET_COUNTER
    local_counter = TICKET_COUNTER
    TICKET_COUNTER+=1

    guild = bot.get_guild(payload.guild_id)
    category = discord.utils.get(guild.categories, name="tickets")

    user = guild.get_member(payload.user_id)
    
    overwrites = { 
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True)
    }
    ticket_name = "TICKET-"+str(TICKET_COUNTER)
    channel = await guild.create_text_channel(name=ticket_name, category=category, overwrites = overwrites)
    # print(f"created {channel.name}")

    await handle_ticket(user, payload, channel, local_counter)

    return channel


# If user reacts to certain message, open ticket
@bot.event
async def on_raw_reaction_add(payload):

    if payload.message_id == 1237835387565768816: 
        await create_ticket_channel(payload)

@bot.command()
async def helpTA(ctx, args : discord.Member = None):
    # print("ATTEMPING TO CREATE THREAD " ) 
    user = ctx.author.id
    # print(user)

    thread_name = ctx.author.name+ "-help-thread"

    newThread = await ctx.channel.create_thread(name=thread_name, type = None)
    
    await newThread.add_user(ctx.author)

    if args is not None: 
        await newThread.add_user(bot.get_user(args.id))



    
if __name__ == "__main__":
    
    load_dotenv()

    TOKEN = os.getenv('TOKEN')

    bot.run(TOKEN)


