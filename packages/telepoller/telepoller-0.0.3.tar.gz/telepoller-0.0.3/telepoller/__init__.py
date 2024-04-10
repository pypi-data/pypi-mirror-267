import types
from telebot.types import ReplyKeyboardMarkup

class Poller:
    def __init__(self, bot, questions: dict, filters, buttons, answers, logger=None):
        """
        Этот класс будет использоваться для определения порядка отправки сообщений. Также будут указываться,
        кнопки для отправки сообщений и фильтры для приёмки сообщений.
        """
        if logger is None:
            import loguru
            self.logger = loguru.logger
        else:
            self.logger = logger

        self.bot = bot
        self.questions = questions
        self.filters = filters
        self.buttons = buttons
        self.bot_answers = answers
        self.user_answers = []
        self.counter = 1

    def create_keyboard(self):
        questions = self.buttons.get(self.counter)
        if questions is None:
            return False

        keyboard = ReplyKeyboardMarkup(True, True)
        for row in questions:
            keyboard.row(*row)
        return keyboard

    def start_poll(self, msg):
        """
        Этот метод будет запускать опрос.
        """
        if self.counter > len(self.questions):
            return
        if self.questions.get(self.counter) is None:
            return

        text = self.questions[self.counter]
        self.bot.send_message(msg.from_user.id, text, reply_markup=self.create_keyboard())
        self.bot.register_next_step_handler(msg, self.next_step)

    def next_step(self, msg):
        """
        Этот метод будет обрабатывать ответы пользователей.
        """
        if self.counter > len(self.questions):
            return

        if self.buttons.get(self.counter):
            filters = []
            for row in self.buttons[self.counter]:
                for button in row:
                    filters.append(button)
        elif self.filters.get(self.counter):
            filters = self.filters.get(self.counter)
        else:
            self.bot.send_message(msg.from_user.id, self.bot_answers.get(self.counter))
            self.user_answers.append(msg.text)
            self.counter += 1
            self.start_poll(msg)
            self.logger.info(f"Фильтры не найдены для ответа {self.counter}")
            return

        self.logger.debug(f"Найденные фильтры: {filters}")

        if isinstance(filters, types.FunctionType):
            # Значит это фильтр с функцией
            filters = filters(msg.text)

        elif msg.text in filters:
            # Значит это фильтр со списком ответов
            filters = True
        else:
            filters = False

        if filters:
            self.user_answers.append(msg.text)
            if self.bot_answers.get(self.counter):
                self.bot.send_message(msg.from_user.id, self.bot_answers.get(self.counter).format(msg.text))
            self.counter += 1
            self.start_poll(msg)
        else:
            self.logger.warning(f"Пользователь ошибся на вопросе №{self.counter}")
            self.start_poll(msg)