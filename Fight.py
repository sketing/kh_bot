import os
import random
import asyncio
from replit import db
# 1
import discord
from discord.ext import commands

class Fight():
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
  TODO: Check if the fighter is "tired" or not
  """
  def __init__(self, ctx, bot):
    self.ctx = ctx
    self.bot = bot
    self.msg = ctx.message.content
    self.channel = ctx.message.channel
    self.challenger = ctx.author
    self.defender = ctx.message.mentions[0]
    self.score = {self.challenger: 0,
                  self.defender: 0
    }
    self.skills = {}
    self.advantage = {self.challenger: False,
                      self.defender: False
    }
    self.tactics={self.challenger: None,
                  self.defender: None
    }
    
  async def start(self):
    rounds = 5
    self.skills = self.get_fighters()
    print(self.skills, type(self.skills))
    for n in range(1,rounds+1):
      await self.accept_challenge()
      await self.round(n)
      await self.rest()
    pass

  async def accept_challenge(self):
    response = self.defender.mention + ' do you agree? \n'
    response += '👎 No \n'
    response += '👍 Yes \n'
    question = await self.channel.send(response)
    await question.add_reaction(emoji='👍')
    await question.add_reaction(emoji='👎')
    def check(reaction, user):
      """TODO: FIX msg.author to msg.mention or smth"""
      return user == self.defender and str(reaction.emoji) == '👍'
    try:
      reaction, user = await self.bot.wait_for('reaction_add', 
                                              timeout=5, 
                                              check = check)
    except asyncio.TimeoutError:
      respone = 'The Defender did not respond'
      return
    respone = self.defender.mention + 'has accepted the challenge! \n' 
    respone += 'Let the fight begin!'
    await self.ctx.reply(respone)
    
  async def round(self, n):
    response = f"Round {n}:\n"
    response += self.challenger.mention + " VS " + self.defender.mention
    await self.channel.send(response)
    await self.choose_tactics('challenger')
    await self.choose_tactics('defender')
    await self.fight()
    await self.rest()
    return

  async def fight(self):
    challenger_roll = self.roll('challenger')
    defender_roll = self.roll('defender')
    if challenger_roll > defender_roll:
      self.score[self.challenger] += 1
    elif challenger_roll < defender_roll:
      self.score[self.defender] += 1
    self.reset_advantage()

  def roll(self, who):
    fighter = self.who(who)
    advantage = self.advantage[fighter]
    tactics = self.tactics[fighter]
    print(self.skills, type(self.skills))
    skills = self.skills[fighter]
    number_of_sides = 20
    number_of_dice = 2 if advantage else 1
    roll = max([random.choice(range(1, number_of_sides + 1))for _ in range(number_of_dice)])
    print(roll, type(roll))
    return roll

  async def rest(self):
    response = f"REST PLACEHOLDER:\n"
    pass

  async def choose_tactics(self, who):
    fighter = self.who(who)
    emojis = ['🤸‍♂️', '🏋️‍♂️']
    response = fighter.mention
    response += "choose your tactic!\n"
    response += f"{emojis[0]} DEX(Acrobatics) or STR(Athletics) {emojis[1]}"
    question = await self.channel.send(response)
    await question.add_reaction(emoji=emojis[0])
    await question.add_reaction(emoji=emojis[1])
    self.tactics = {self.challenger: None,
                    self.defender: None
    }

  def get_fighters(self):
    if not self.check_fighter('challenger'):
      return 'challenger not registered'
    if not self.check_fighter('defender'):
      return 'defender not registered'
    challenger_skills = self.get_skills('challenger')
    defender_skills = self.get_skills('defender')
    skills_dict={'challenger':challenger_skills,
                 'defender':defender_skills
    }
    print('here4')
    return skills_dict

  def check_fighter(self, who):
    """
    TODO: check if fighter in DataBase
    TODO: Replace check with try
    """
    fighter = self.who(who)
    print('here4')
    if db[fighter]:
      print('here5')
      return True
    return False

  def get_skills(self, who):
    print('here2')
    """TODO: get skills from DataBase"""
    return None

  def reset_advantage(self):
    self.advantage = {self.challenger: False,
                      self.defender: False
    }

  def who(self, who):
    if who == 'challenger':
      return self.challenger
    if who == 'defender':  
      return self.defender