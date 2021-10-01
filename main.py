# bot.py
import os
import random
import asyncio
from replit import db
# 1
import discord
from discord.ext import commands
# from Fight import Fight
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')

def check(author):
    def inner_check(message): 
        if message.author != author:
            return False
        try: 
            int(message.content) 
            return True 
        except ValueError: 
            return False
    return inner_check

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


#3
@bot.command(name='signup', help='Sign up for the Fighting Pits by sharing your character data')
async def signup(ctx):
  # number_of_dice: int, number_of_sides: int
  msg = ctx.message
  channel = ctx.message.channel
  fighter = msg.author
  # abilities = ['STR','CON','DEX','INT','WIS','CHA']
  # skills = ['Athletics', 'Acrobatics', 'Sleight of Hand', 
  #           'Stealth', 'Arcana', 'History', 'Investigation', 
  #           'Nature', 'Religion', 'Animal Handling', 'Insight', 
  #           'Medicine', 'Perception', 'Survival', 'Deception','Intimidation', 'Performance', 'Persuasion']
  # skills = ['Atheltics', 'Acrobatics', 'Intimidation', 
  #           'Sleight of Hand', 'Performance']
  skills = ['Atheltics']
  # await channel.send(msg.author.mention)
  def check(m: discord.Message):
    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
  skills_dict={}
  for skill in skills:
    await channel.send(msg.author.mention
                      +' How high is your '
                      + skill + '?')
    try:
      msg = await bot.wait_for(event = 'message', check = check, timeout = 5)
    except asyncio.TimeoutError:
      await ctx.reply('Sign up timed out. Start again.')
      return
    else:
      print(msg.content)
      skills_dict[skill] = msg.content
  print(str(skills_dict))
  print(type(fighter.id), ":",fighter.id)
  # print(type(fighter), ":",fighter)
  print('fighter_'+str(fighter.id))
  db['fighter_'+str(fighter.id)] = str(skills_dict)
  response = f"Congratulationss on signing up{fighter.mention}!\n"
  response += "Here are your skills:\n"
  for skill in skills:
    response += f"**{skill}**: {skills_dict[skill]} \n"
  response += "If the skills are wrong try the ` !signup ` command again\n"
  response += "Otherwise try challenging others with the ` !fight [@user] ` command"
  await channel.send(response)


#4
@bot.command(name='fight', help='Challenge a player to a duel')
async def fight(ctx):
  """
  TODO: check if challenger is signed up
  TODO: check if defender is signed up
  TODO: add saved skills to fighting rolls
  TODO: add score tracking
  TODO: add DEX and STR Choice
  TODO: add in between rounds skill checks
  TODO: add advantage
  TODO: add feats and class check
  TODO: Create a class that handles this
  """
  msg = ctx.message.content
  channel = ctx.message.channel
  # fight = Fight(ctx, bot)
  # await fight.start()
  if len(msg.mentions) == 0:
    response = "You haven't challenged anyone"
  elif len(msg.mentions) >1:
    response = "You can challenge only one person"
  else:
    challenger = msg.author
    defender = msg.mentions[0]
    response = challenger.mention +' challenges '\
              + defender.mention + ' to a duel!'
    used_correct = True
  await channel.send(response)
  if used_correct:
    response = (defender.mention + ' do you agree? \n'+
                  ('👎 No \n'
                   '👍 Yes \n'
                  )
    )
    question = await channel.send(response)
    await question.add_reaction(emoji='👍')
    await question.add_reaction(emoji='👎')
    def check(reaction, user):
      """TODO: FIX msg.author to msg.mention or smth"""
      return user == msg.author and str(reaction.emoji) == '👍'
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout=5, check = check)
      print('here')
    except asyncio.TimeoutError:
      await ctx.reply('The Defender did not respond')
      return
    await ctx.reply(defender.mention  
                    + 'has accepted the challenge! \n' 
                    + 'Let the fight begin!'
                )
    rounds = 5
    for round_n in range(1, rounds+1):
      challenger_dice = str(random.choice(range(1, 20 + 1)))
      defender_dice = str(random.choice(range(1, 20 + 1)))
      await ctx.reply('Round ' + str(round_n) + ' results:\n'
                  + challenger.mention + ' rolled a **' + challenger_dice +'**\n'
                  + defender.mention + ' rolled a **'  + defender_dice +'**\n'
                  )
    # dice = [
    #     str(random.choice(range(1, 20 + 1)))
    #     for _ in range(5)
    # ]
    # await ctx.send(', '.join(dice))
    
      
  # msg = message.content
  # channel = message.channel

  # if msg.startswith('!fight'):
  #   challenger = message.author
  #   defender = message.mentions[-1]
  #   response = challenger.mention +' challenges '\
  #            + defender.mention + ' to a duel!'
  #   await channel.send(response)
  # if message.mentions is not None:
  #   challenger = message.author
  #   defender = message.mentions[-1]
  #   response = challenger.mention +' challenges '\
  #            + defender.mention + ' to a duel!'
  #   await channel.send(response)

  # msg = await client.wait_for('message', 
  #       check=check(ctx.author), 
  #       timeout=30)


            
# @bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
# async def nine_nine(ctx):
#     brooklyn_99_quotes = [
#         'I\'m the human form of the 💯 emoji.',
#         'Bingpot!',
#         (
#             'Cool. Cool cool cool cool cool cool cool, '
#             'no doubt no doubt no doubt no doubt.'
#         ),
#     ]

#     response = random.choice(brooklyn_99_quotes)
#     await ctx.send(response)

# @bot.command(name='roll_dice', help='Simulates rolling dice.')
# async def roll(ctx, number_of_dice: int, number_of_sides: int):
#     dice = [
#         str(random.choice(range(1, number_of_sides + 1)))
#         for _ in range(number_of_dice)
#     ]
#     await ctx.send(', '.join(dice))

# @bot.command(name='create_channel')
# @commands.has_role('admin')
# async def create_channel(ctx, channel_name='real-python'):
#     guild = ctx.guild
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel: {channel_name}')
#         await guild.create_text_channel(channel_name)

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CheckFailure):
#         await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)