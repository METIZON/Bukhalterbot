import telebot


class Inline():
    def mainMenu(self, role):
        if role == 'newbie':
            btns = [
                telebot.types.InlineKeyboardButton(text='Консультация', callback_data='newbie_consultation'),
                telebot.types.InlineKeyboardButton(text='Бухгалтерия ИП', callback_data='newbie_buhgalteria'),
            ]
        elif role == 'veteran':
            btns = [
                telebot.types.InlineKeyboardButton(text='Консультация бухгалтера', callback_data='veteran_consultation'),
                telebot.types.InlineKeyboardButton(text='Заказать документы', callback_data='veteran_orderDocs'),
                telebot.types.InlineKeyboardButton(text='Изменения в реестре', callback_data='veteran_changeRecords'),
                telebot.types.InlineKeyboardButton(text='Регистрационные действия', callback_data='veteran_registryDeals'),
                telebot.types.InlineKeyboardButton(text='Написать менеджеру', url='https://t.me/bukhalterpoland'),
                telebot.types.InlineKeyboardButton(text='Я новенький', callback_data='veteran_newbie'),
            ]

        mainMenu = telebot.types.InlineKeyboardMarkup(row_width=1)
        mainMenu.add(*btns)

        return mainMenu

    def showExpert(self, experts):
        btns = []

        for expert in experts:
            btns.append(telebot.types.InlineKeyboardButton(text=expert[2], callback_data=f'newbie_showExpert_{expert[0]}'))

        showExpert = telebot.types.InlineKeyboardMarkup(row_width=1)
        showExpert.add(*btns)

        return showExpert

    def acceptExpert(self, id_):
        btns = [
            telebot.types.InlineKeyboardButton(text='🔙', callback_data='newbie_consultation'),
            telebot.types.InlineKeyboardButton(text='✅', callback_data=f'newbie_acceptExpert_{id_}'),
        ]

        acceptExpert = telebot.types.InlineKeyboardMarkup(row_width=2)
        acceptExpert.add(*btns)

        return acceptExpert

    def acceptCredentials(self, id_):
        btns = [
            telebot.types.InlineKeyboardButton(text='➡️', callback_data=f'newbie_skipPay_{id_}')
        ]

        acceptCredentials = telebot.types.InlineKeyboardMarkup(row_width=1)
        acceptCredentials.add(*btns)

        return acceptCredentials

    def chooseDate(self, id_):
        btns = [
            telebot.types.InlineKeyboardButton(text='skip', callback_data=f'newbie_skipDate_{id_}')
        ]

        chooseDate = telebot.types.InlineKeyboardMarkup(row_width=1)
        chooseDate.add(*btns)

        return chooseDate

    def haveUsrIp(self):
        btns = [
            telebot.types.InlineKeyboardButton(text='Есть', callback_data=f'newbie_hasIp'),
            telebot.types.InlineKeyboardButton(text='Нету', callback_data=f'newbie_noIp'),
        ]

        haveUsrIp = telebot.types.InlineKeyboardMarkup(row_width=1)
        haveUsrIp.add(*btns)

        return haveUsrIp

    def showDec(self, decList, page):
        btns = []

        for doc in decList:
            btns.append(telebot.types.InlineKeyboardButton(text=doc[1], callback_data=f'veteran_showDec_{doc[0]}_{page}'))

        showDec = telebot.types.InlineKeyboardMarkup(row_width=1)
        showDec.add(*btns)

        if page == 0:
            showDec.row(telebot.types.InlineKeyboardButton(text='🔙', callback_data=f'veteran_mainMenu'),
                        telebot.types.InlineKeyboardButton(text='➡️', callback_data=f'veteran_showDecPage_{page + 1}'))
        else:
            showDec.row(telebot.types.InlineKeyboardButton(text='⬅️', callback_data=f'veteran_showDecPage_{page - 1}'),
                        telebot.types.InlineKeyboardButton(text='➡️', callback_data=f'veteran_showDecPage_{page + 1}'))
            showDec.row(telebot.types.InlineKeyboardButton(text='🔙', callback_data=f'veteran_mainMenu'))

        return showDec

    def decMenu(self, decID, page):
        btns = [
            telebot.types.InlineKeyboardButton(text='✅', callback_data=f'veteran_acceptDec_{decID}'),
            telebot.types.InlineKeyboardButton(text='🔙', callback_data=f'veteran_showDecPage_{page}')
        ]

        decMenu = telebot.types.InlineKeyboardMarkup(row_width=1)
        decMenu.add(*btns)

        return decMenu

    def selectDate(self, year, month, day, user, mode):
        btns = [
            telebot.types.InlineKeyboardButton(text=year, callback_data=f'{user}_changeYear_{year}_{month}_{day}_{mode}'),
            telebot.types.InlineKeyboardButton(text=month, callback_data=f'{user}_changeMonth_{year}_{month}_{day}_{mode}'),
            telebot.types.InlineKeyboardButton(text=day, callback_data=f'{user}_changeDay_{year}_{month}_{day}_{mode}'),
            telebot.types.InlineKeyboardButton(text='🔙', callback_data=f'{user}_mainMenu'),
            telebot.types.InlineKeyboardButton(text='✅', callback_data=f'{user}_acceptDate_{year}_{month}_{day}_{mode}')
        ]

        selectDate = telebot.types.InlineKeyboardMarkup(row_width=3)
        selectDate.add(*btns)

        return selectDate

    def chooseDateCompound(self, array, mode, period, day, month, year, user):
        btns = []

        for element in array:
            if period == 'Month':
                print(element[1], f'{user}_setDate_{year}_{element[0]}_{day}_{mode}')
                btns.append(telebot.types.InlineKeyboardButton(text=element[1], callback_data=f'{user}_setDate_{year}_{element[0]}_{day}_{mode}'))
            elif period == 'Day':
                if element == '*':
                    btns.append(telebot.types.InlineKeyboardButton(text=element, callback_data=f'*'))
                else:
                    btns.append(telebot.types.InlineKeyboardButton(text=element, callback_data=f'{user}_setDate_{year}_{month}_{element}_{mode}'))
            else:
                btns.append(telebot.types.InlineKeyboardButton(text=element, callback_data=f'{user}_setDate_{element}_{month}_{day}_{mode}'))

        if period == 'Day':
            chooseDateCompound = telebot.types.InlineKeyboardMarkup(row_width=7)
        else:
            chooseDateCompound = telebot.types.InlineKeyboardMarkup(row_width=3)
        chooseDateCompound.add(*btns)
        chooseDateCompound.row(telebot.types.InlineKeyboardButton('🔙', callback_data=f'{user}_setDate_{year}_{month}_{day}_{mode}'))

        return chooseDateCompound

    def chooseFreeHour(self, hoursSet, user, mode, year, month, day):
        btns = []

        for hour in hoursSet:
            btns.append(telebot.types.InlineKeyboardButton(text=hour, callback_data=f'{user}_showHour_{hour}_{year}_{month}_{day}_{mode}'))

        chooseFreeHour = telebot.types.InlineKeyboardMarkup(row_width=3)
        chooseFreeHour.add(*btns)
        chooseFreeHour.add(telebot.types.InlineKeyboardButton(text='🔙', callback_data=f'{user}_{mode}'))

        return chooseFreeHour

    def selectTimePeriod(self, periodsArr, user, mode, year, month, day):
        btns = []

        for period in periodsArr:
            btns.append(telebot.types.InlineKeyboardButton(text=f'{period[0].time()} - {period[1].time()}', callback_data=f'{user}_selectPeriod_{period[0].time()}_{period[1].time()}_{year}_{month}_{day}_{mode}'))

        selectTimePeriod = telebot.types.InlineKeyboardMarkup(row_width=1)
        selectTimePeriod.add(*btns)
        selectTimePeriod.add(telebot.types.InlineKeyboardButton(text='🔙', callback_data=f'{user}_acceptDate_{year}_{month}_{day}_{mode}'))

        return selectTimePeriod

    def docTypes(self, docID):
        btns = [
            telebot.types.InlineKeyboardButton(text='Отдел ЗУС', callback_data=f'admin_addoc_ZUS_{docID}'),
            telebot.types.InlineKeyboardButton(text='Отдел НАЛОГИ', callback_data=f'admin_addoc_taxes_{docID}'),
            telebot.types.InlineKeyboardButton(text='ОФОРМИТЬ/УВОЛИТЬ СОТРУДНИКА', callback_data=f'admin_addoc_employer_{docID}')
        ]

        docTypes = telebot.types.InlineKeyboardMarkup(row_width=1)
        docTypes.add(*btns)

        return docTypes


class Reply():
    NotImplemented
