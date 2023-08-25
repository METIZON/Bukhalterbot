
class LangModel:
    UA = 'UA'


class Message(LangModel):
    def __init__(self) -> None:
        super().__init__()

    def welcomeMessage(self, isNew=True):
        if isNew:
            text = '''
Привет 🧮

Меня зовут БухБот 🤖
Помощник Валерия Бухгалтера!

Я создан для того чтобы Ты смог назначить задание своей Бухгалтерии📥.

Ты выбираешь задание а я моментально передаю его ответственному лицу.
И слежу за его исполнением ✅

Введи, пожалуйста, свой код клиента:
            '''
        else:
            text = '''
Привет 🧮

Меня зовут БухБот 🤖
Помощник Валерия Бухгалтера!

Я создан для того чтобы Ты смог назначить задание своей Бухгалтерии📥.

Ты выбираешь задание а я моментально передаю его ответственному лицу.
И слежу за его исполнением ✅

Выбери что ты хочешь заказать?
        '''

        return text

    def mainMenu(self):
        text = '''
Меню
        '''

        return text

    def showExpert(self, expert):
        text = f'''
{expert[0][2]}

{expert[0][3]}
Прайс - {expert[0][4]}
        '''

        return text

    def showDec(self, dec):
        text = f'''
{dec[1]}

{dec[2]}
        '''

        return text
