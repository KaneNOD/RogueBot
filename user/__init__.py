import random
from datetime import datetime

import logging
from constants import *
from utils.names import names

from collections import Counter
from localizations import locale_manager
import usermanager
import databasemanager as dbmanager

logger = logging.getLogger('rg')

class User(object):
	def __init__(self, uid):
		super(User, self).__init__()

		self.uid = uid

		self.name = 'none'
		self.hp = 100
		self.mp = 100
		self.gold = 200
		self.race = HUMAN

		self.max_hp = 150
		self.max_mp = 150

		self.state = 'name'

		self.items = [ ]
		self.active_items = [ ]
		self.inventory_page = 0

		self.gods = [ locale_manager.get('BUDDHA'), locale_manager.get('JESUS'), locale_manager.get('ALLAH'), locale_manager.get('AUTHOR') ]
		self.gods_level = [ 0 for g in self.gods ]
		self.last_god = ''
		self.prayed = False

		self.damage = 10
		self.defence = 1
		self.charisma = 0
		self.mana_damage = 0

		self.visited_shop = False
		self.shop_items = [ ]
		self.shop_names = [ ]

		self.tags = [ ]

		self.room = ('', '')
		self.room_temp = { }

		self.reborn_answer = None
		self.dead = False

		self.last_message = datetime.now()
		self.rooms_count = 0
		self.monsters_killed = 0

		self.subject = None

		self.race = 'human'
		self.pet = None

		self.variables = dict()
		self.missions = list()
		self.buffs = list()

		self.new_mission('main')
		self.new_mission('caravan', path_len=20)

	def message(self, reply, text):
		self.last_message = datetime.now()
		logger.info('msg from {0}'.format(self.uid))

		if self.dead:
			reply(locale_manager.get('DEAD_MESSAGE_AGAIN'), [ '/start' ])
		elif self.state == 'name':
			self.name_given(reply, text)
		elif self.state == 'name_confirm':
			self.name_confirm(reply, text)
		elif self.state == 'first_msg':
			self.first(reply, text)
		elif self.state == 'corridor':
			self.corridor(reply, text)
		elif self.state == 'pray':
			self.pray(reply, text)
		elif self.state == 'shop':
			self.shop(reply, text)
		elif self.state == 'inventory':
			self.inventory(reply, text)
		elif self.state == 'room':
			self.in_room(reply, text)
		elif self.state == 'dice':
			self.dice(reply, text)
		elif self.state.startswith('pet'):
			self.on_pet(reply, text)
		elif self.state == 'rebornd':
			reply(self.reborn_answer, [ '/start' ])
			
	from user.corridor_defenition import open_corridor, corridor
	from user.death_defenition import update_leaderbord, death, reborn
	from user.fight_defenition import get_fight_actions, fight_dice, fight_action, fight_answer, escape, won
	from user.gods_defenition import evilgod, god_love, prayto, pray, divine_intervention
	from user.inventory_defenition import open_inventory, inventory
	from user.items_defenition import remove_item, remove_items_with_tag, deactivate_item_by_name
	from user.items_defenition import remove_item_by_name, get_item_by_name, get_items, get_active_items
	from user.items_defenition import add_item, get_active_slots_len, has_item
	from user.meet_defenition import name_confirm, name_given, first
	from user.money_defenition import paid, steal, give_gold
	from user.room_defenition import make_damage, set_room_temp, get_room_temp, open_room, in_room
	from user.room_defenition import throw_dice, get_dice_bonus, dice, leave
	from user.save_defenition import save, recover
	from user.shop_defenition import open_shop, buy, shop
	from user.stats_defenition import debug_info, get_damage, get_damage_bonus, get_defence, get_charisma, get_gold_bonus
	from user.stats_defenition import get_mana_damage, has_aura, heal, mana, get_stats, add_tag, has_tag, remove_tag
	from user.stats_defenition import show_characteristics, set_variable, get_variable, new_buff
	from user.pets_defenition import new_pet, on_pet, get_pet, pet_gone
	from user.missions_defenition import new_mission, get_last_mission, pop_mission
	
