
class LangModel:
    UA = 'UA'


class Message(LangModel):
    def __init__(self) -> None:
        super().__init__()

    def welcomeMessage(self, isNew=True):
        if isNew:
            text = '''
Input code
            '''
        else:
            text = '''
Main menu:
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
