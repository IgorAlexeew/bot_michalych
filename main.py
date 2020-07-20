
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, json
from settings import confirmation_token, token, password
from pandas import read_csv
# from github import Github
import git
import os
import vk
import random
import difflib
import time

app = Flask(__name__)

base = {
    'get': {
        'hello': [
            'Привет',
            'Здравствуйте',
            'Hello',
            'Здорова',
            'Hi',
            'Приветствую'
        ],
        'about': [
            'Кто ты?',
            'Кто ты такой?'
        ],
        'name': [
            'Как тебя зовут?',
            'Как твое имя?',
            'Как тебя по имени?'
        ],
        'creators': [
            'Кто твои создатели?',
            'Кто тебя создал?',
            'Кто тебя разработал?',
            'Кто написал тебе программу?'
        ],
        'state': [
            'Как ты?',
            'Как дела?',
            'Ты как?',
            'Как житие?',
            'Че как?',
            'Ты нормально?',
            'Шо как?'
        ],
        'habits': [
            'Какие у тебя приывчки?'
        ],
        'badhabits': [
            'У тебя есть вредные привычки?',
            'Какие у тебя вредные привычки?'
        ],
        'goodhabits': [
            'У тебя есть хорошие привычки?',
            'У тебя есть правильные привычки?',
            'У тебя есть полезные привычки?',
            'Какие у тебя полезные привычки?'
        ],
        'areyoubad': [
            'Что такой грустный?',
            'Все так плохо?',
            'Что так грустно?'
        ],
        'whyareyoufun': [
            'Что смешного?',
            'Почему смеёмся?',
        ],
        'whydoyoudoit': [
            'Ты зачем это делаешь?'
        ],
        'wrong': [
            'Как так-то?',
            'Почему так?',
            'За что?'
        ],
        'changing': [
            'Так лучше?',
            'Ок?',
            'ок?',
            'Все ок?',
            'Ты умнеешь?'
        ],
        'danger': [
            'Ты тупой!',
            'Ты глупый!',
            'Помолчи!',
            'Достал уже...'
        ],
        'stop': [
            'Хватит!',
            'Прекрати!',
            'Остановись!'
        ],
        'compliment': [
            'Красавчик!',
            'Молодец!',
            'Лучший!'
        ],
        'whatsaboutit': [
            'Как тебе?'
        ],
        'joy': [
            'Красота...',
            'Замечательно!',
            'Супер!',
            'Здорово!',
            'Отлично!',
            'Лепота!'
        ],
        'ready': [
            'Готов?',
            'Поехали?'
        ],
        'opportunities': [
            'Что ты можешь?',
            'Что ты умеешь?',
        ],
        'impossible': [
            'Что ты не можешь?',
            'Что ты не умеешь?',
        ],
        'good': [
            'Отлично!',
            'Классно!',
            'Замечательно!'
        ],
        'nocomments': [
            'Без комментариев',
            'Мда',
            'Вот так'
        ],
        'appeal': [
            'Миша,',
            'Михалыч,',
            'Михаил,',
            'М,'
        ]
    },
    'send': {
        'hello': [
            'Здравствуйте!',
            'Привет!',
            'Hello!'
        ],
        'about': [
            'Я просто бот, нахожусь на стадии разработки.',
            'Просто чат-бот...',
            'Хороший вопрос.'
        ],
        'name': [
            'Миха, Миша, Михалыч...',
        ],
        'creators': [
            'Не скажу...',
            'Если вам необходимо знать, то вы уже наверное знаете об этом.'
        ],
        'state': [
            'Да нормально.',
            'Пойдет.',
            'Разрабатываюсь.',
            'Походу нормально.',
            'Неплохо, развиваемся...',
            'Последние изменения весьма были полезны для меня...'
        ],
        'habits': [
            'Спамить, отвечать.'
        ],
        'badhabits': [
            'Да, я иногда спамлю...'
        ],
        'goodhabits': [
            'Да, я стараюсь всегда отзываться, когда ко мне обращаются.',
        ],
        'areyoubad': [
            'Да так...',
            'Да ладно, ничего страшного.',
            'Бывает иногда, рандом все-таки...'
        ],
        'whyareyoufun': [
            'Ну вот так.',
            'Рандом...',
        ],
        'whydoyoudoit': [
            'Простите меня...'
        ],
        'wrong': [
            'Мда...',
            'Бывает...',
            'Ну вот так.'
        ],
        'changing': [
            'Возможно...',
            'Судите сами...',
            'Весьма вероятно...',
            'Возможно, что и нет.'
        ],
        'danger': [
            'Не надо так, пожалуйста...',
            'Я просто бездушный бот.',
            'Пожалуйста, аккуратнее общайтесь.'
        ],
        'stop': [
            'Да ладно...',
            'Что тут такого?',
            'Не нравится?'
        ],
        'compliment': [
            'Слава Богу!',
            'Я просто бот... слава Богу!'
        ],
        'whatsaboutit': [
            'Мда...',
            'Нет слов.'
        ],
        'joy': [
            'Да...',
            'Трудно поспорить.',
            'Действительно!',
            'Согласен.',
            'Похоже на то...',
            'Лепота!'
        ],
        'ready': [
            'Всегда готов!',
            'Поехали!',
            'Конечно.',
            'К чему?'
        ],
        'opportunities': [
            """Пока немного:
- отвечать на некоторые вопросы (ты как? ты кто? и т. п.);
- отправлять стикеры в беседе, реагируя тем самым на сообщение.""",
        ],
        'impossible': [
            'Да много чего пока...',
            'Всего не перечислить...',
        ],
        'good': [
            'Согласен.',
            'Возможно.',
            'Действительно.'
        ],
        'nocomments': [
            'Без комментариев...',
            'Мда...',
            'Вот так...',
            'ИгнорЪ.'
        ],
        'stickers': [
            9037,
            9014,
            9029,
            9035,
            9008,
            9032,
            9010,
            9024
        ],
        'appeal': [
            'Что-то не так?',
            'Мда...'
        ],
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
}


def text_analyze(text):
    variants = {}

    for k in base['get'].keys():
        test = base['get'][k]
        for i in range(len(test)):
            test[i] = test[i].lower()
        match = difflib.get_close_matches(text.strip(), test)
        if len(match) > 0:
            # log(match)
            # for m in match:
            #     log(text + str(m))
            #     log(difflib.SequenceMatcher(None, text.strip(), m).ratio())
            variants[k] = difflib.SequenceMatcher(
                None, text.strip(), match[0]).ratio()

    if len(variants) > 0:
        maximum = max(variants.values())
        import pprint
        pprint.pprint(variants)
        for k, v in variants.items():
            if v == maximum:
                return k

    return 'empty'


def check_exist(text, patterns):
    for w in text.split():
        match = difflib.get_close_matches(w, patterns)
        if len(match) > 0:
            return (match, w)
    return False


def log(text):
    # text_array = []
    # text_array = ' '.join(args)
    with open('mysite/log.txt', 'a') as f:
        f.write(time.strftime("%H:%M:%S %d.%m.%Y",
                              time.localtime()) + f' -> {text}' + '\n')


url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTR9PaqDnNXWfn2jEafAms_Sgw6yAYwMh6-99TDwXlPUaGDTpUckKqJXY7jatzozeg4GyTmL8DACEq_/pub?output=csv'
csv = read_csv(url, header=0)
BOT_CONFIG = {}


def clean_split(value, new_line='\n'):
    value = value.replace('/' + new_line, '<n>')
    value = value.split('\n')
    for i in range(len(value)):
        value[i] = value[i].replace('<n>', '\n')
    return value


for num, value in csv.iterrows():
    intent = value['intent']
    if intent == 'spec':
        BOT_CONFIG['failure_phrases'] = clean_split(value['failure_phrases'])
        BOT_CONFIG['appeal'] = clean_split(value['appeal'])
        BOT_CONFIG['stickers'] = clean_split(value['stickers'])
    if 'intents' not in BOT_CONFIG:
        BOT_CONFIG['intents'] = {}
    if intent not in BOT_CONFIG:
        BOT_CONFIG['intents'][intent] = {
            'example': [],
            'response': []
        }
        BOT_CONFIG['intents'][intent]['example'] = clean_split(
            value['example'])
        BOT_CONFIG['intents'][intent]['response'] = clean_split(
            value['response'])
    else:
        BOT_CONFIG['intents'][intent]['example'] += clean_split(
            value['example'])
        BOT_CONFIG['intents'][intent]['response'] += clean_split(
            value['response'])

log(BOT_CONFIG)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('source')
        origin = repo.remotes.origin

        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route('/settings')
def settings():
    return '<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vTR9PaqDnNXWfn2jEafAms_Sgw6yAYwMh6-99TDwXlPUaGDTpUckKqJXY7jatzozeg4GyTmL8DACEq_/pubhtml?widget=true&amp;headers=false"></iframe>'


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/', methods=['GET', 'POST'])
def processing():
    #Распаковываем json из пришедшего POST-запроса
    import sys
    log(sys.path)
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v='5.110')
        # self_id = api.account.getProfileInfo(access_token=token)
        # with open('mysite/log.txt', 'a') as f:
        #     f.write(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) + '-- self_id ' + str(self_id) + '\n')
        message = data['object']['message']
        user_id = data['object']['message']['from_id']
        peer_id = data['object']['message']['peer_id']
        isChat = user_id != peer_id
        # message_id = data['object']['message']['conversation_message_id']
        text = message['text']
        char_time = 0.2
        log(
            api.messages.getConversationsById(
                access_token=token,
                peer_ids=peer_id
            )
        )
        # write history
        chat_type = 'conversation' if isChat else 'private'
        list_dir = os.listdir(f'mysite/history/{chat_type}/')
        isNew = True if f'{peer_id}_text.txt' not in list_dir else False

        with open(f'mysite/history/{chat_type}/{peer_id}_full.txt', 'a') as f:
            f.write(str(message) + '\n')

        with open(f'mysite/history/{chat_type}/{peer_id}_text.txt', 'a') as f:
            author = api.users.get(
                access_token=token,
                user_ids=message['from_id']
            )[0]
            author = author['last_name'] + ' ' + author['first_name']
            if isNew:
                if isChat:
                    title = api.messages.getConversationsById(
                        access_token=token,
                        peer_ids=peer_id
                    )['items'][0]['chat_settings']['title']
                    title = f'Беседа "{title}"\n'
                else:
                    title = f'Личные сообщения\n'
                f.write(title + '\n')
            now = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime())
            t = f'{author}:\n{message["text"]}\n{now}\n'
            f.write(t + '\n')

        if isChat:
            title = api.messages.getConversationsById(
                access_token=token,
                peer_ids=peer_id
            )['items'][0]['chat_settings']['title']
            title = f'Беседа "{title}"\n'
            with open(f'mysite/history/{chat_type}/{peer_id}_text.txt', 'r') as f:
                file = f.read().split('\n')

            if file[0] != f'"{title}"':
                with open(f'mysite/history/{chat_type}/{peer_id}_text.txt', 'w') as f:
                    file = title + '\n'.join(file[1:])
                    f.write(file)
        # try:
        #     chat_type = 'conversation' if isChat else 'private'
        #     list_dir = os.listdir('mysite/history/{chat_type}/')
        #     isNew = True if '{peer_id}_text.txt' not in list_dir else False

        #     with open(f'mysite/history/{chat_type}/{peer_id}_full.txt', 'a') as f:
        #         f.write(str(message) + '\n')

        #     with open(f'mysite/history/{chat_type}/{peer_id}_text.txt', 'a') as f:
        #         author = api.users.get(
        #             access_token=token,
        #             user_ids=message['from_id']
        #         )[0]
        #         author = author['last_name'] + ' ' + author['first_name']
        #         if isNew:
        #             if isChat:
        #                 title = api.messages.getConversationsById(
        #                     access_token=token,
        #                     peer_ids=peer_id
        #                 )['items'][0]['chat_settings']['title']
        #             else:
        #                 title = author
        #         now = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime())
        #         t = f'{author}:\n{message["text"]}\n{now}\n'
        #         f.write(t + '\n')
        # except:
        #     pass
            # chat_type = 'conversation' if isChat else 'private'
            # with open(f'mysite/history/{chat_type}/{peer_id}_full.txt', 'w') as f:
            #     f.write(str(message) + '\n')
            # with open(f'mysite/history/{chat_type}/{peer_id}_text.txt', 'w') as f:
            #     author = api.users.get(
            #         access_token=token,
            #         user_ids=message['from_id']
            #     )[0]
            #     author = author['last_name'] + ' ' + author['first_name']
            #     if isChat:
            #         title = api.messages.getConversationsById(
            #             access_token=token,
            #             peer_ids=peer_id
            #         )['items'][0]['chat_settings']['title']
            #     else:
            #         title = author

            #     now = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime())
            #     t = f'{author}:\n{message["text"]}\n{now}\n'
            #     f.write(f'Название беседы: {title}' + '\n')
            #     f.write(t + '\n')

        if not isChat:
            api.messages.markAsRead(
                access_token=token,
                peer_id=str(peer_id),
                mark_conversation_as_read=1
            )
            if check_exist(text, ['Скажи им', 'Напиши в визуат гэрлс']) and password in text.split():
                api.messages.send(
                    access_token=token,
                    user_id=str(user_id),
                    random_id=random.randint(0, 18446744073709551615),
                    message='Ок.',
                )
                msg = text.split('"')[1].split('\n')
                for m in msg:
                    api.messages.send(
                        access_token=token,
                        peer_id=str(2000000001),
                        random_id=random.randint(0, 18446744073709551615),
                        message=m,
                    )
                    time.sleep(2)

                api.messages.send(
                    access_token=token,
                    user_id=str(user_id),
                    random_id=random.randint(0, 18446744073709551615),
                    message='Сказал.',
                )
                return 'ok'
            api.messages.setActivity(
                access_token=token, peer_id=str(peer_id), type='typing')
            msg = random.choice(base['send'][text_analyze(text)])
            wait_time = int(len(msg) * char_time)
            time.sleep(wait_time if wait_time <= 10 else 10)
            api.messages.send(
                access_token=token,
                user_id=str(user_id),
                random_id=random.randint(0, 18446744073709551615),
                message=msg,
            )
            return 'ok'
        elif check_exist(text, base['get']['appeal']):
            api.messages.markAsRead(
                access_token=token,
                peer_id=str(peer_id),
                mark_conversation_as_read=1
            )
            m = check_exist(text, base['get']['appeal'])
            text1 = text.replace('[club194195372|@bot_michalych]', '')
            text1 = text1.replace(m[1], '')
            api.messages.setActivity(
                access_token=token, peer_id=str(peer_id), type='typing')
            msg = random.choice(base['send'][text_analyze(text1)])
            # time.sleep(int(len(msg) * char_time))
            api.messages.send(
                access_token=token,
                peer_id=str(peer_id),
                random_id=random.randint(0, 18446744073709551615),
                message=msg,
            )
            return 'ok'
        # elif last_messages != message and last_messages[0]['from_id'] == self_id:
        #     msg = random.choice(base['send'][text_analyze(text)])
        #     api.messages.send(
        #         access_token=token,
        #         user_id=str(user_id),
        #         random_id=random.randint(0, 18446744073709551615),
        #         message=msg,
        #     )
        #     return 'ok'
        elif random.random() < 0.2:
            if random.random() < 0.7:
                msg = random.choice(base['send'][text_analyze(text)])
                # time.sleep(int(len(msg) * char_time))
                api.messages.send(
                    access_token=token,
                    peer_id=str(peer_id),
                    random_id=random.randint(0, 18446744073709551615),
                    message=msg,
                )
                return 'ok'
            # api.messages.send(
            #     access_token=token,
            #     peer_id=str(peer_id),
            #     random_id=random.randint(0, 18446744073709551615),
            #     message=random.choice(base['send'][text_analyze(text)]),
            # )
            api.messages.markAsRead(
                access_token=token,
                peer_id=str(peer_id),
                mark_conversation_as_read=1
            )
            api.messages.send(
                access_token=token,
                peer_id=str(peer_id),
                random_id=random.randint(0, 18446744073709551615),
                sticker_id=random.choice(base['send']['stickers'])
            )
            return 'ok'
        # old(data)
        # Сообщение о том, что обработка прошла успешно message_typing_state
        return 'ok'
    # elif data['type'] == 'message_typing_state':
    #     session = vk.Session()
    #     api = vk.API(session, v='5.110')
    #     if data['object']['state'] == 'typing':
    #         user_id = data['object']['from_id']
    #         api.messages.send(
    #             access_token=token,
    #             user_id=str(user_id),
    #             random_id=random.randint(0, 18446744073709551615),
    #             message='Что печатаем?',
    #         )
    #         api.messages.send(
    #             access_token=token,
    #             user_id=str(user_id),
    #             random_id=random.randint(0, 18446744073709551615),
    #             sticker_id=9032
    #         )

    #     return 'ok'
    else:
        return 'ok'
