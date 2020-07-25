import random
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC

BOT_CONFIG = {
    'intents': {
        'about': {
            'example': ['Кто ты?', 'Кто ты такой?'],
            'response': [
                'Я просто бот, нахожусь на стадии разработки.',
                'Просто чат-бот...',
                'Хороший вопрос.'
            ]
        },
        'appeal': {
            'example': ['Миша', 'Михалыч', 'Михаил'],
            'response': ['Что-то не так?', 'Мда...']
        },
        'areyoubad': {
            'example': [
                'Что такой грустный?',
                'Все так плохо?',
                'Что так грустно?'],
            'response': [
                'Да так...',
                'Да ладно, ничего страшного.',
                'Бывает иногда, рандом все-таки...'
            ]
        },
        'badhabits': {
            'example': [
                'У тебя есть вредные привычки?',
                'Какие у тебя вредные привычки?'
            ],
            'response': ['Да, я иногда спамлю...']
        },
        'changing': {
            'example': ['Так лучше?', 'Ок?', 'ок?', 'Все ок?', 'Ты умнеешь?'],
            'response': [
                'Возможно...',
                'Судите сами...',
                'Весьма вероятно...',
                'Возможно, что и нет.'
            ]
        },
        'compliment': {
            'example': ['Красавчик!', 'Молодец!', 'Лучший!'],
            'response': ['Слава Богу!', 'Я просто бот... слава Богу!']
        },
        'creators': {
            'example': [
                'Кто твои создатели?',
                'Кто тебя создал?',
                'Кто тебя разработал?',
                'Кто написал тебе программу?'],
            'response': [
                'Не скажу...',
                'Если вам необходимо знать, то вы уже наверное знаете об этом.'
            ]
        },
        'danger': {
            'example': ['Ты тупой!', 'Ты глупый!', 'Помолчи!', 'Достал уже...'],
            'response': [
                'Не надо так, пожалуйста...',
                'Я просто бездушный бот.',
                'Пожалуйста, аккуратнее общайтесь.'
            ]
        },
        'good': {
            'example': ['Отлично!', 'Классно!', 'Замечательно!'],
            'response': ['Согласен.', 'Возможно.', 'Действительно.']},
        'goodhabits': {
            'example': [
                'У тебя есть хорошие привычки?',
                'У тебя есть правильные привычки?',
                'У тебя есть полезные привычки?',
                'Какие у тебя полезные привычки?'],
            'response': [
                'Да, я стараюсь всегда отзываться, когда ко мне обращаются.'
            ]
        },
        'habits': {
            'example': ['Какие у тебя приывчки?'],
            'response': ['Спамить, отвечать.']},
        'hello': {
            'example': [
                'Привет',
                'Здравствуйте',
                'Hello',
                'Здорова',
                'Hi',
                'Приветствую',
                'Прив'
            ],
            'response': ['Здравствуйте!', 'Привет!', 'Hello!']},
        'impossible': {
            'example': ['Что ты не можешь?', 'Что ты не умеешь?'],
            'response': [
                'Да много чего пока...',
                'Всего не перечислить...'
            ]
        },
        'joy': {
            'example': [
                'Красота...',
                'Замечательно!',
                'Супер!',
                'Здорово!',
                'Отлично!',
                'Лепота!'],
            'response': [
                'Да...',
                'Трудно поспорить.',
                'Действительно!',
                'Согласен.',
                'Похоже на то...',
                'Лепота!'
            ]
        },
        'name': {
            'example': ['Как тебя зовут?', 'Как твое имя?', 'Как тебя по имени?'],
            'response': ['Миха, Миша, Михалыч...']},
        'nocomments': {
            'example': ['Без комментариев', 'Мда', 'Вот так'],
            'response': [
                'Без комментариев...',
                'Мда...',
                'Вот так...',
                'ИгнорЪ.']
        },
        'opportunities': {
            'example': ['Что ты можешь?', 'Что ты умеешь?'],
            'response': ["""Пока немного:
- отвечать на некоторые вопросы (ты как? ты кто? и т. п.);
- отправлять стикеры в беседе, реагируя тем самым на сообщение."""
                ]
            },
        'ready': {
            'example': ['Готов?', 'Поехали?'],
            'response': ['Всегда готов!', 'Поехали!', 'Конечно.', 'К чему?']},
        'state': {
            'example': [
                'Как ты?',
                'Как дела?',
                'Ты как?',
                'Как житие?',
                'Че как?',
                'Ты нормально?',
                'Шо как?'],
            'response': [
                'Да нормально.',
                'Пойдет.',
                'Разрабатываюсь.',
                'Походу нормально.',
                'Неплохо, развиваемся...',
                'Последние изменения весьма были полезны для меня...'
            ]
        },
        'stop': {
            'example': ['Хватит!', 'Прекрати!', 'Остановись!'],
            'response': ['Да ладно...', 'Что тут такого?', 'Не нравится?']},
        'whatsaboutit': {
            'example': ['Как тебе?'],
            'response': ['Мда...', 'Нет слов.']},
        'whyareyoufun': {
            'example': ['Что смешного?', 'Почему смеёмся?'],
            'response': ['Ну вот так.', 'Рандом...']
        },
        'whydoyoudoit': {
            'example': ['Ты зачем это делаешь?'],
            'response': ['Простите меня...']
        },
        'wrong': {
            'example': ['Как так-то?', 'Почему так?', 'За что?'],
            'response': ['Мда...', 'Бывает...', 'Ну вот так.']
        }
    },
    'empty': [
        'Я пока не понимаю этого...',
        'Не понял, не умею, простите...',
        'Не знаю, как это понять...',
        'Простите, не понимаю о чем вы, я еще на стадии разработки...',
        'Что, простите?',
        'Вы о чём?',
        'Мда...',
        'Внатуре...'
    ]
}

class Bot():
    def __init__(self, config):
        self.config_ = config
        self.threshold = 0.4

        X_text = []
        y = []
        for intent, value in self.config_['intents'].items():
            X_text += value['example']
            y += [intent] * len(value['example'])

        self.vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        X = self.vectorizer.fit_transform(X_text)

        self.model = LogisticRegression()
        self.model.fit(X, y)

    def get_answer(self, text):
        intent = self.get_intent(text)

        if intent:
            return self.response_by_intent(intent)

        # generative model
        # TO DO

        return self.get_failure_phrase()

    def get_intent(self, text):
        text_vector = self.vectorizer.transform([text]).toarray()[0]
        probas_list = self.model.predict_proba([text_vector])[0]
        probas_list = list(probas_list)
        max_proba = max(probas_list)
        if max_proba > self.threshold:
            index = probas_list.index(max_proba)
            return self.model.classes_[index]

    def response_by_intent(self, intent):
        responses = self.config_['intents'][intent]['response']
        return random.choice(responses)
    
    def get_failure_phrase(self):
        failure_phrases = self.config_['empty']
        return random.choice(failure_phrases)

if __name__ == '__main__':
    bot = Bot(BOT_CONFIG)

    while True:
        text = input('Я:       ')
        if text.lower() in ['выход', 'exit', 'пока']:
            print('Михалыч: Пока!')
            break
        print(f'(tech: {bot.get_intent(text)})')
        print('Михалыч:', bot.get_answer(text))
