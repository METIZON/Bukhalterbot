from telebot.async_telebot import AsyncTeleBot
import asyncio
import datetime

import config
import text_messages as txt
import keyboards
import database
import dateManager as dManager
import googleCalendarApi as gcalAPI


bot = AsyncTeleBot(config.token)  # '5385126708:AAHLVLLs708YePNRDYvk6dswfd0v-qkMG84'


# TXT TEMPLATES
txtMenu = txt.Message()

# INLINE MARKUPS
markup = keyboards.Inline()

# REPLY MARKUPS
kb = keyboards.Reply()

# GOOGLE CALENDAR
gCalendar = gcalAPI.GoogleCalendar()


async def tables():
    users_dic = {
        'chatid': "integer",
        'name': "text",
        'username': "text",
        'code': "text",
        'role': "text",
        'input': "text"
    }
    codes_dic = {
        'chatid': "integer",
        'code': "text"
    }
    experts_dic = {
        'chatid': "integer",
        'name': "text",
        'desc': "text",
        'price': "text"
    }
    documents_dic = {
        'docName': "text",
        'docDesc': "text",
        'docType': "text",
        'endpoint': "text",
        'status': "text"
    }

    # await database.create_table('users', users_dic)
    # await database.create_table('codes', codes_dic)
    # await database.create_table('experts', experts_dic)
    await database.create_table('documents', documents_dic)


@bot.message_handler(commands=['addc'])
async def addc_msg(message):
    codeInform = await database.select_value_by_key('codes', 'code', message.text)
    if not len(codeInform):
        await database.insert_code(message.text)
        await bot.send_message(message.chat.id, 'Код зарегистрирован!')
    else:
        await bot.send_message(message.chat.id, 'Код уже зарегистрирован!')


@bot.message_handler(commands=['addoc'])
async def addoc_msg(message):
    await database.update_values('users', message.from_user.id, {'input': "new_doc"})
    await bot.send_message(message.chat.id, 'Введите название документа')


@bot.message_handler(commands=['start'])
async def start_msg(message):
    is_usr_reg = await database.select_values('users', message.from_user.id)
    if not len(is_usr_reg):
        input_users_dic = {
            'name': message.from_user.first_name,
            'username': message.from_user.username,
            'input': "code"
        }
        await database.insert_values('users', message.from_user.id, input_users_dic)
        await bot.send_message(message.chat.id, txtMenu.welcomeMessage())
        return
    await bot.send_message(message.chat.id, txtMenu.welcomeMessage(isNew=False), reply_markup=markup.mainMenu(role=is_usr_reg[0][5]))


@bot.message_handler(content_types=['text'])
async def txt_msg(message):
    if message.text == '...':
        ...
    else:
        msint = await database.select_values('users', message.from_user.id)
        if msint[0][-1] is None:
            ...
        elif msint[0][-1] == 'code':
            codeInfo = await database.select_value_by_key('codes', 'code', message.text)
            if not len(codeInfo):
                await database.update_values('users', message.from_user.id, {'role': "newbie"})
                await bot.send_message(message.chat.id, txtMenu.mainMenu(), reply_markup=markup.mainMenu(role='newbie'))
            else:
                await database.update_values('users', message.from_user.id, {'role': "veteran"})
                await bot.send_message(message.chat.id, txtMenu.mainMenu(), reply_markup=markup.mainMenu(role='veteran'))
        elif msint[0][-1] == 'new_doc':
            await database.insert_doc(message.text)
            docID = await database.select_all_values('documents')
            await database.update_values('users', message.from_user.id, {'input': f"docDesc_{docID[-1][0]}"})
            await bot.send_message(message.chat.id, "Введите описание для документа")
        elif msint[0][-1].startswith('docDesc_'):
            docID = msint[0][-1].split('_')[1]
            await database.update_values_wkey('documents', {'id': docID}, {'docDesc': message.text})
            await bot.send_message(message.chat.id, 'Выберите тип документа:', reply_markup=markup.docTypes(docID=docID))


@bot.callback_query_handler(func=lambda call: True)
async def query_handler(call):
    print(call.data)
    if call.data == '':
        ...
    else:
        scall = call.data.split('_')
        if scall[0] == 'newbie':
            if scall[1] == 'consultation':
                expertsList = await database.select_all_values('experts')
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите эксперта', reply_markup=markup.showExpert(expertsList))
            elif scall[1] == 'buhgalteria':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='У вас есть Ип или хотите открыть?', reply_markup=markup.haveUsrIp())
            elif scall[1] == 'hasIp':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='need admin token')
            elif scall[1] == 'noIp':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="прайс")
                await bot.send_message(call.message.chat.id, "Предложить записаться на услугу открытия ИП или взять консультацию")
                await bot.send_message(call.message.chat.id, 'payment credentials', reply_markup=markup.acceptCredentials(0))
            elif scall[1] == 'showExpert':
                expertInf = await database.select_value_by_key('experts', 'id', scall[2])
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=txtMenu.showExpert(expertInf), reply_markup=markup.acceptExpert(scall[2]))
            elif scall[1] == 'acceptExpert':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='payment credentials', reply_markup=markup.acceptCredentials(scall[2]))
            elif scall[1] == 'skipPay':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите дату', reply_markup=markup.chooseDate(scall[2]))
            elif scall[1] == 'skipDate':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='success', reply_markup=markup.mainMenu(role='newbie'))
        elif scall[0] == 'veteran':
            if scall[1] == 'mainMenu':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=txtMenu.welcomeMessage(isNew=False), reply_markup=markup.mainMenu(role='veteran'))
            elif scall[1] == 'consultation':
                cur_time = datetime.datetime.now()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите дату', reply_markup=markup.selectDate(year=cur_time.year, month=cur_time.month, day=cur_time.day, user='veteran', mode='consultation'))
            elif scall[1] == 'changeYear':
                '''veteran_changeYear_2023_8_23_consultation'''
                yearArray = dManager.get_upcoming_years(2)
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите год:', reply_markup=markup.chooseDateCompound(array=yearArray, mode=scall[5], period='Year', day=scall[4], month=scall[3], year=scall[2], user='veteran'))
            elif scall[1] == 'changeMonth':
                chosen_year = int(scall[2])
                current_month = datetime.datetime.now().month
                monthsArray = dManager.get_enumerated_months_in_following_year(chosen_year, current_month)
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите месяц:', reply_markup=markup.chooseDateCompound(array=monthsArray, mode=scall[5], period='Month', day=scall[4], month=scall[3], year=scall[2], user='veteran'))
            elif scall[1] == 'changeDay':
                daysArray = dManager.get_days_in_following_month(int(scall[2]), int(scall[3]))
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите день:', reply_markup=markup.chooseDateCompound(array=daysArray, mode=scall[5], period='Day', day=scall[4], month=scall[3], year=scall[2], user='veteran'))
            elif scall[1] == 'setDate':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите дату', reply_markup=markup.selectDate(year=scall[2], month=scall[3], day=scall[4], user=scall[0], mode=scall[5]))
            elif scall[1] == 'orderDocs':
                dec1List = await database.select_value_by_key('documents', 'docType', 'ZUS')
                dec2List = await database.select_value_by_key('documents', 'docType', 'taxes')
                decList = dec1List + dec2List
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите тип документов', reply_markup=markup.showDec(decList=decList, page=0))
            elif scall[1] == 'showDec':
                decList = await database.select_value_by_key('documents', 'id', scall[2])
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=txtMenu.showDec(decList[0]), reply_markup=markup.decMenu(scall[2], int(scall[3])))
            elif scall[1] == 'showDecPage':
                decList = await database.select_value_by_key('documents', 'docType', 'declaration')
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите тип документов', reply_markup=markup.showDec(decList=decList, page=int(scall[2])))
            elif scall[1] == 'acceptDec':
                docInfo = await database.select_value_by_key('documents', 'id', scall[2])
                cur_time = datetime.datetime.now()
                target_date = datetime.date(cur_time.year, cur_time.month, cur_time.day)
                if docInfo[0][3] == 'ZUS':
                    calendarID = config.ZUS_calendar
                else:
                    calendarID = config.BUHGALTERY_calendar
                free_slots = gCalendar.get_free_time_slots(calendarID, target_date)
                result_periods = gCalendar.save_10min_periods(free_slots)
                hour_set = gCalendar.extract_hours(result_periods)
                print(next(iter(hour_set)))
                free_per = gCalendar.get_time_periods_by_hour(next(iter(hour_set)), result_periods)
                try:
                    # Create a new event
                    userInfo = await database.select_values('users', call.from_user.id)
                    new_event = {
                        'summary': f'{userInfo[0][4]} {docInfo[0][1]}',
                        'start': {'dateTime': f'{cur_time.year}-{cur_time.month}-{cur_time.day}T{free_per[0][0].time()}', 'timeZone': 'UTC+2'},
                        'end': {'dateTime': f'{cur_time.year}-{cur_time.month}-{cur_time.day}T{free_per[0][1].time()}', 'timeZone': 'UTC+2'}
                    }
                    print(f'{cur_time.year}-{cur_time.month}-{cur_time.day}T{free_per[0][0].time()}')
                    print(f'{cur_time.year}-{cur_time.month}-{cur_time.day}T{free_per[0][1].time()}')
                    created_event = gCalendar.create_event(new_event, calendarID)
                    if created_event:
                        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                    text="Ваш запрос отправлен на нашу почту! Ожидайте звонка менеджера", reply_markup=markup.mainMenu(role='veteran'))
                    else:
                        await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте в другое время!')
                except Exception:
                    await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте в другое время!')
            elif scall[1] == 'acceptDate':
                target_date = datetime.date(int(scall[2]), int(scall[3]), int(scall[4]))
                if scall[-1] == 'consultation':
                    free_slots = gCalendar.get_free_time_slots(config.V20OFFICE_calendar, target_date)
                    result_periods = gCalendar.save_10min_periods(free_slots)
                    hour_set = gCalendar.extract_hours(result_periods)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Выберите примерный час для записи', reply_markup=markup.chooseFreeHour(hoursSet=hour_set, user='veteran', mode=scall[-1], year=int(scall[2]), month=int(scall[3]), day=int(scall[4])))
                elif scall[-1] == 'changeRecords':
                    free_slots = gCalendar.get_free_time_slots(config.EDWARD_calendar, target_date)
                    result_periods = gCalendar.save_10min_periods(free_slots)
                    hour_set = gCalendar.extract_hours(result_periods)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Выберите примерный час для записи', reply_markup=markup.chooseFreeHour(hoursSet=hour_set, user='veteran', mode=scall[-1], year=int(scall[2]), month=int(scall[3]), day=int(scall[4])))
                elif scall[-1] == 'registryDeals':
                    free_slots = gCalendar.get_free_time_slots(config.EDWARD_calendar, target_date)
                    result_periods = gCalendar.save_10min_periods(free_slots)
                    hour_set = gCalendar.extract_hours(result_periods)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Выберите примерный час для записи', reply_markup=markup.chooseFreeHour(hoursSet=hour_set, user='veteran', mode=scall[-1], year=int(scall[2]), month=int(scall[3]), day=int(scall[4])))
            elif scall[1] == 'showHour':
                target_date = datetime.date(int(scall[3]), int(scall[4]), int(scall[5]))
                if scall[-1] == 'consultation':
                    free_slots = gCalendar.get_free_time_slots(config.V20OFFICE_calendar, target_date)
                    result_periods = gCalendar.save_10min_periods(free_slots)
                    free_per = gCalendar.get_time_periods_by_hour(int(scall[2]), result_periods)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Выберите свободный промежуток времени:', reply_markup=markup.selectTimePeriod(periodsArr=free_per, user='veteran', mode=scall[-1], year=int(scall[3]), month=int(scall[4]), day=int(scall[5])))
                elif scall[-1] == 'changeRecords':
                    free_slots = gCalendar.get_free_time_slots(config.EDWARD_calendar, target_date)
                    result_periods = gCalendar.save_10min_periods(free_slots)
                    free_per = gCalendar.get_time_periods_by_hour(int(scall[2]), result_periods)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Выберите свободный промежуток времени:', reply_markup=markup.selectTimePeriod(periodsArr=free_per, user='veteran', mode=scall[-1], year=int(scall[3]), month=int(scall[4]), day=int(scall[5])))
                elif scall[-1] == 'registryDeals':
                    free_slots = gCalendar.get_free_time_slots(config.EDWARD_calendar, target_date)
                    result_periods = gCalendar.save_10min_periods(free_slots)
                    free_per = gCalendar.get_time_periods_by_hour(int(scall[2]), result_periods)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='Выберите свободный промежуток времени:', reply_markup=markup.selectTimePeriod(periodsArr=free_per, user='veteran', mode=scall[-1], year=int(scall[3]), month=int(scall[4]), day=int(scall[5])))
            elif scall[1] == 'selectPeriod':
                if scall[-1] == 'consultation':
                    try:
                        # Create a new event
                        userInfo = await database.select_values('users', call.from_user.id)
                        new_event = {
                            'summary': f'{userInfo[0][4]} Консультация',
                            'start': {'dateTime': f'{scall[4]}-{scall[5]}-{scall[6]}T{scall[2]}', 'timeZone': 'UTC+2'},
                            'end': {'dateTime': f'{scall[4]}-{scall[5]}-{scall[6]}T{scall[3]}', 'timeZone': 'UTC+2'}
                        }
                        created_event = gCalendar.create_event(new_event, config.V20OFFICE_calendar)
                        if created_event:
                            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                        text="Ваш запрос отправлен на нашу почту! Ожидайте звонка менеджера", reply_markup=markup.mainMenu(role='veteran'))
                        else:
                            await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте выбрать другое время!')
                    except Exception:
                        await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте выбрать другое время!')
                elif scall[-1] == 'changeRecords':
                    try:
                        # Create a new event
                        userInfo = await database.select_values('users', call.from_user.id)
                        new_event = {
                            'summary': f'{userInfo[0][4]} Изменения в реестре',
                            'start': {'dateTime': f'{scall[4]}-{scall[5]}-{scall[6]}T{scall[2]}', 'timeZone': 'UTC+2'},
                            'end': {'dateTime': f'{scall[4]}-{scall[5]}-{scall[6]}T{scall[3]}', 'timeZone': 'UTC+2'}
                        }
                        created_event = gCalendar.create_event(new_event, config.EDWARD_calendar)
                        if created_event:
                            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                        text="Ваш запрос отправлен на нашу почту! Ожидайте звонка менеджера", reply_markup=markup.mainMenu(role='veteran'))
                        else:
                            await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте выбрать другое время!')
                    except Exception:
                        await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте выбрать другое время!')
                elif scall[-1] == 'registryDeals':
                    try:
                        # Create a new event
                        userInfo = await database.select_values('users', call.from_user.id)
                        new_event = {
                            'summary': f'{userInfo[0][4]} Регистрационные действия',
                            'start': {'dateTime': f'{scall[4]}-{scall[5]}-{scall[6]}T{scall[2]}', 'timeZone': 'UTC+2'},
                            'end': {'dateTime': f'{scall[4]}-{scall[5]}-{scall[6]}T{scall[3]}', 'timeZone': 'UTC+2'}
                        }
                        created_event = gCalendar.create_event(new_event, config.EDWARD_calendar)
                        if created_event:
                            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                        text="Ваш запрос отправлен на нашу почту! Ожидайте звонка менеджера", reply_markup=markup.mainMenu(role='veteran'))
                        else:
                            await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте выбрать другое время!')
                    except Exception:
                        await bot.answer_callback_query(callback_query_id=call.id, text='Ууупс... Что-то пошло не так, попробуйте выбрать другое время!')
            elif scall[1] == 'changeRecords':
                cur_time = datetime.datetime.now()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите дату', reply_markup=markup.selectDate(year=cur_time.year, month=cur_time.month, day=cur_time.day, user='veteran', mode='changeRecords'))
            elif scall[1] == 'registryDeals':
                cur_time = datetime.datetime.now()
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Выберите дату', reply_markup=markup.selectDate(year=cur_time.year, month=cur_time.month, day=cur_time.day, user='veteran', mode='registryDeals'))
            elif scall[1] == 'newbie':
                ...
        elif scall[0] == 'admin':
            if scall[1] == 'addoc':
                await database.update_values_wkey('documents', {'id': scall[3]}, {'docType': scall[2]})
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Док успешно добавлен!')


if __name__ == '__main__':
    try:
        asyncio.run(tables())
        print('[200] - tables ')
    except Exception:
        print('[400] - tables')
    finally:
        asyncio.run(bot.infinity_polling())
