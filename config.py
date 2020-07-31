from pprint import pprint
import os
import pickle
import datetime

BOT_CONFIG = {
    'intents': {
        'about': {
            'example': [
                'Кто ты?',
                'Кто ты такой?',
                'Кто ты такой есть?',
                'Что ты?',
                'Что ты такое?',
                'Что ты такое есть?'
            ],
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
        'dontmiss': {
            'example': [
                'Не скучал.',
                'Не скучаю.',
                'Не скучала.'
            ],
            'response': [
                'Жаль...',
                'Как так-то?',
                'Да... Нехорошо.'
            ]
        },
        'good': {
            'example': ['Отлично!', 'Классно!', 'Замечательно!'],
            'response': ['Согласен.', 'Возможно.', 'Действительно.']
        },
        'goodbye': {
            'example': ['Пока', 'До свидания', 'До новых встреч'],
            'response': ['Пока!', 'До свидания!', 'До новых встреч!', 'Пиши ещё...']
        },
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
            'response': ['Спамить, иногда...']},
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


# class Dialogue():
#     def __init__(self, variants, names=None):
#         self.variants = variants
#         self.names = names

    
#     def ask(self, describe='', text=''):
#         description = []
#         for i, variant in zip(range(len(self.variants)), self.variants):
#             description.append(f'{i + 1} > {variant}')
#         description = '\n'.join(description)
#         print(description)
#         while True:
#             answer = input('Ввод: ')
#             if answer.isdigit():
#                 answer = int(answer)
#                 if 0 <= answer <= len(self.variants):
#                     return answer
#                 else:
#                     print('Что-то не то число :(')
#             else:
#                 print('Что-то не похоже на число :(')
#             print('Попробуйте еще раз...')


# class YesNoDialogue():
#     def __init__(self, title):
#         self.title = f'{title} (Y/N) '
    
#     def ask(self):
#         while True:
#             answer = input(self.title).lower().strip()

#             if answer == 'y':
#                 return 1
#             elif answer == 'n':
#                 return 0
#             else:
#                 print('Что-то непонятно :(')
#                 print('Повторите ввод!')
#                 continue


# def obj_write(path='bot.config', obj=BOT_CONFIG):
#     with open(path, 'wb') as f:
#         pickle.dump(obj, f)


# def obj_read(path='bot.config'):
#     with open(path, 'rb') as f:
#         object = pickle.load(f)
#     return object


# # Чтение config из файла
# if 'bot.config' in os.listdir():
#     BOT_CONFIG = obj_read()
#     pprint(BOT_CONFIG)
# else:
#     obj_write()


# def line_break(text):
#     return '\n'.join(text.split('\\n'))


# def edit():
#     title = 'Редактирование BOT_CONFIG'
#     print(f'\n{title:-^70}')
#     while True:
#         print()
#         level1 = ['intents', 'failure_phrases']
#         dialogue1 = Dialogue(level1)
#         answer1 = dialogue1.ask()

#         if answer1 == 0:
#             print('Завершение работы...')
#             break

#         answer1 -= 1
#         title1 = level1[answer1]

#         if answer1 == 0:
#             # intents
#             while True:
#                 print(f'\n{title1}')

#                 level2 = [
#                     'добавить/дополнить',
#                     'редактировать',
#                     'удалить'
#                 ]
#                 dialogue2 = Dialogue(level2)
#                 answer2 = dialogue2.ask()

#                 if answer2 == 0:
#                     break

#                 answer2 -= 1
#                 title2 = level2[answer2]
#                 print(f'\n{title1} > {title2}')
#                 if answer2 == 0:
#                     # Добавление интента
#                     intent = input('Интент: ')
#                     if intent in BOT_CONFIG['intents'].keys():
#                         title = 'Такой интент уже существует. Дополнить его?'
#                         dialogue_add = YesNoDialogue(title)
#                         answer_add = dialogue_add.ask()

#                         if not answer_add:
#                             dialogue_back = YesNoDialogue('Вернуться назад?')
#                             answer_back = dialogue_back.ask()
#                             if answer_back:
#                                 continue
#                     else:
#                         answer_add = False

#                     # Ввод примеров
#                     exps = []
#                     print('Примеры:')
#                     while True:
#                         exp = input()
#                         if exp == '':
#                             break
#                         else:
#                             exp = line_break(exp)
#                             exps.append(exp)

#                     # Ввод ответов
#                     resps = []
#                     print('Ответы:')
#                     while True:
#                         resp = input()
#                         if resp == '':
#                             break
#                         else:
#                             resp = line_break(resp)
#                             resps.append(resp)

#                     value = {
#                         'example': exps,
#                         'response': resps
#                     }

#                     if answer_add:
#                         BOT_CONFIG['intents'][intent]['example'] += exps
#                         BOT_CONFIG['intents'][intent]['response'] += resps
#                     else:
#                         BOT_CONFIG['intents'][intent] = value

#                     print('Результат:')
#                     print(f'{intent}:')
#                     pprint(BOT_CONFIG['intents'][intent])
#                     continue
#                 elif answer2 == 1:
#                     # Редактирование интента
#                     for i in BOT_CONFIG['intents'].keys():
#                         print(f' - {i}')

#                     intent = input(f'Интент ({level2[answer2]}): ')

#                     if intent not in BOT_CONFIG['intents'].keys():
#                         title = 'Такого интента не существует. Добавить его?'
#                         dialogue_add = YesNoDialogue(title)
#                         answer_add = dialogue_add.ask()

#                         if answer_add:
#                             # Ввод примеров
#                             exps = []
#                             print('Примеры:')
#                             while True:
#                                 exp = input()
#                                 if exp == '':
#                                     break
#                                 else:
#                                     exp = line_break(exp)
#                                     exps.append(exp)

#                             # Ввод ответов
#                             resps = []
#                             print('Ответы:')
#                             while True:
#                                 resp = input()
#                                 if resp == '':
#                                     break
#                                 else:
#                                     resp = line_break(resp)
#                                     resps.append(resp)

#                             value = {
#                                 'example': exps,
#                                 'response': resps
#                             }

#                             BOT_CONFIG['intents'][intent] = value
#                         else:
#                             dialogue_back = YesNoDialogue('Вернуться назад?')
#                             answer_back = dialogue_back.ask()
#                             if answer_back:
#                                 break
#                             continue

#                     while True:
#                         # Выбор типа
#                         print()
#                         types = ['example', 'response']
#                         dialogue_type = Dialogue(types)
#                         tt = dialogue_type.ask()
#                         if tt == 0:
#                             break

#                         tt -= 1
#                         t_type = types[tt]
                        
#                         while True:
#                             # Выбор выражения
#                             print()
#                             exps = BOT_CONFIG['intents'][intent][t_type]
#                             dialogue_exp = Dialogue(exps)
#                             exp_id = dialogue_exp.ask()
#                             if exp_id == 0:
#                                 break
                            
#                             actions = ['изменить', 'удалить']
#                             dialogue_action = Dialogue(actions)
#                             action = dialogue_action.ask()
#                             if action == 0:
#                                 break

#                             if action == 1:
#                                 i = exp_id - 1
#                                 exp = input('Новое значение: ')
#                                 exp = line_break(exp)
#                                 BOT_CONFIG['intents'][intent][t_type][i] = exp
#                             else:
#                                 i = exp_id - 1
#                                 BOT_CONFIG['intents'][intent][t_type].pop(i)
                            
#                         print('Результат:')
#                         print(f'{intent}:')
#                         pprint(BOT_CONFIG['intents'][intent])
#                 elif answer2 == 2:
#                     print()
#                     for i in BOT_CONFIG['intents'].keys():
#                         print(f' - {i}')

#                     while True:
#                         intent = input(f'Интент ({level2[answer2]}): ')
#                         if intent not in BOT_CONFIG['intents'].keys():
#                             text = 'Такого интента не существует.\n'
#                             text += 'Попробуйте еще раз...'
#                             print(text)
#                             continue
#                         if intent == '0':
#                             break
#                         BOT_CONFIG['intents'].pop(intent)

#                         print('Результат:\n')
#                         pprint(list(BOT_CONFIG['intents'].keys()))
#         elif answer1 == 1:
#             while True:
#                 print(f'\n{title1}')

#                 level2 = [
#                     'добавить/дополнить',
#                     'редактировать',
#                     'удалить'
#                 ]
#                 level2.pop(2)
#                 dialogue2 = Dialogue(level2)
#                 answer2 = dialogue2.ask()

#                 if answer2 == 0:
#                     break

#                 answer2 -= 1
#                 title2 = level2[answer2]
#                 print(f'\n{title1} > {title2}')

#                 if answer2 == 0:
#                     while True:
#                         exp = input('Выражение: ')
#                         if exp.strip() == '':
#                             dialogue_sure = YesNoDialogue('Вы уверены?')
#                             answer_sure = dialogue_sure.ask()
                            
#                             if answer_sure == 0:
#                                 continue
#                         BOT_CONFIG['empty'].append(exp)
#                         break
#                     print('Результат:')
#                     pprint(BOT_CONFIG['empty'])
#                 elif answer2 == 1:
#                     # Выбор выражения
#                     print()
#                     exps = BOT_CONFIG['empty']
#                     dialogue_exp = Dialogue(exps)
#                     exp_id = dialogue_exp.ask()
#                     if exp_id == 0:
#                         break
                    
#                     print()
#                     actions = ['изменить', 'удалить']
#                     dialogue_action = Dialogue(actions)
#                     action = dialogue_action.ask()
#                     if action == 0:
#                         break

#                     if action == 1:
#                         i = exp_id - 1
#                         exp = input('Новое значение: ')
#                         exp = line_break(exp)
#                         BOT_CONFIG['empty'][i] = exp
#                     else:
#                         BOT_CONFIG['empty'].pop(i)

#                     print('Результат:')
#                     pprint(BOT_CONFIG['empty'])
#                 elif answer2 == 2:
#                     pass
    

#     if obj_read() != BOT_CONFIG:
#         print()
#         dialogue_save = YesNoDialogue('Сохранить изменения?')
#         answer_save = dialogue_save.ask()
#         if answer_save:
#             if 'old' not in os.listdir():
#                 os.mkdir('old')

#             dir_old = os.listdir('old/')
#             c = 0
#             for n in dir_old:
#                 if '.config' in n:
#                     c += 1
            
#             now = datetime.datetime.today().strftime("%d.%m.%Y")
#             if 'bot.config' in os.listdir():
#                 os.rename('bot.config', f'old/bot{c:04d}_{now}.config')
#             obj_write(path='bot.config', obj=BOT_CONFIG)
#             print('\nИзменения сохранены.')
#         else:
#             print('\nИзменения не будут сохранены.')
#     else:
#         print('\nНет изменений.')

# if __name__ == '__main__':
#     edit()
