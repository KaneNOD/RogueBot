from constants import *

name = 'Зеркало'

hp = 1
element = NONE
damage_range =  ( 0, 0 )

coins = 200

loot = [ ]

def enter(user, reply):
	msg = (
		'Ты видишь какого-то странного, грязного и страшного человека'
	)
	reply(msg)

	user.set_room_temp('hp', user.hp)

	ch = user.get_charisma()

	if ch < 0:
		reply('Оно треснуло')
		user.won(reply)
	elif ch > 10:
		reply('Такой красивый. Иди с миром ;)')
		user.won(reply)

def make_damage(user, reply, dmg):
	hp = user.get_room_temp('hp', 0)
	hp -= dmg

	reply('Ты нанес сам себе урон, равный *{0}*'.format(dmg))
	user.make_damage(dmg, dmg, reply)

	if hp <= 0:
		user.won(reply)
	else:
		user.set_room_temp('hp', hp)