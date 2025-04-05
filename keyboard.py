from telebot import types
import config as cfg

def button(text):
	return types.KeyboardButton(text)
def inbutton(text, cbd):
	return types.InlineKeyboardButton(text, callback_data=cbd)
def urlbutton(text, url):
	return types.InlineKeyboardButton(text, url=url)


bbtn = inbutton('🔙 Вернуться', 'back')

main = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main.add(button('🔍 Поиск пользователя'), button('🤝 Активные сделки'))
main.add(button('🎓 Мой профиль'), button('🚀 Помощь'))
main.add(button('⭐️ Список проверенных продавцов'))

main_search = types.InlineKeyboardMarkup(row_width=1)
main_search.add(inbutton('🛰 Отзывы', 'otzivi'))

main_sdelki = types.InlineKeyboardMarkup(row_width=2)
main_sdelki.add(inbutton('🛒 Покупки', 'buys'), inbutton('🎁 Продажи', 'sells'))

main_profile = types.InlineKeyboardMarkup(row_width=2)
main_profile.add(inbutton('↪️ Пополнить', 'deposit'), inbutton('↩️ Вывести', 'outmoney'))
main_profile.add(inbutton('📲 Указать линк на форуме', 'set_link'))

main_profile_deposit = types.InlineKeyboardMarkup(row_width=2)
main_profile_deposit.add(inbutton('QIWI/CARD', 'deposit_rub'), inbutton('BITCOIN', 'btc'))

main_profile_outmoney = types.InlineKeyboardMarkup(row_width=2)
main_profile_outmoney.add(inbutton('🥝 QIWI', 'outmoney_qiwi'), inbutton('💳 CARD', 'outmoney_card'))
main_profile_outmoney.add(inbutton('BITCOIN', 'btc'))
main_profile_outmoney.add(inbutton('🔙 Вернуться', 'back_profile'))


main_help = types.InlineKeyboardMarkup(row_width=2)
main_help.add(urlbutton('Поддержка', 't.me/' + cfg.support_username), urlbutton('Наши проекты', 't.me/' + cfg.projects))
main_help.add(urlbutton('Нашли баг?', 't.me/' + cfg.bughelp))
main_help.add(inbutton('🗿 Как пользоваться ботом?', 'main_help_help'))


admin_search = types.InlineKeyboardMarkup(row_width=1)
admin_search.add(inbutton('🔍 Поиск', 'admin_search'), inbutton('✉️ Рассылка', 'admin_rass'))

none = types.InlineKeyboardMarkup(row_width=3)
none.add(inbutton('🖥 Боты автопродаж', 'none'))
none.add(inbutton('Другое', 'none'))
none.add(inbutton('🏫 Курсы', 'none'))
none.add(inbutton('◀️', 'none'), inbutton('1 из 1', 'none'), inbutton('▶️', 'none'))
none.add(inbutton('💎 Стать проверенным продавцом', 'new_seller'))

back = types.InlineKeyboardMarkup(row_width=1).add(bbtn)