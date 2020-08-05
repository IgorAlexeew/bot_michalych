import os
import random
import time
import difflib
from config.config import get_path
from michalych import Bot


path = get_path()[0]


def check_exist(text, patterns):
    for w in text.split():
        match = difflib.get_close_matches(w, patterns)
        if len(match) > 0:
            return (match, w)
    return False


def GET_from_vk(data, session, api, settings):
    bot = Bot()
    token = settings['token']
    confirmation_token = settings['confirmation_token']
    password = settings['password']
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        VK_CONFIG = {
            'stickers': [
                9037,
                9014,
                9029,
                9035,
                9008,
                9032,
                9010,
                9024
            ]
        }

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


        # write history
        chat_type = 'conversation' if isChat else 'private'
        list_dir = os.listdir(f'site/history/{chat_type}')

        if str(peer_id) not in list_dir:
            isNew = True
            os.mkdir(f'site/history/{chat_type}/{peer_id}')
        else:
            isNew = False

        with open(f'site/history/{chat_type}/{peer_id}/full.txt', 'a') as f:
            f.write(str(message) + '\n')

        with open(f'site/history/{chat_type}/{peer_id}/text.txt', 'a') as f:
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
        
        with open(f'site/history/{chat_type}/{peer_id}/dialogue.txt', 'a') as f:
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
            # t = f'{author}:\n{message["text"]}\n{now}\n'
            t = f' - {message} - {author} - ({now})'
            f.write(t + '\n')

        if isChat:
            title = api.messages.getConversationsById(
                access_token=token,
                peer_ids=peer_id
            )['items'][0]['chat_settings']['title']
            title = f'Беседа "{title}"\n'
            with open(f'site/history/{chat_type}/{peer_id}_text.txt', 'r') as f:
                file = f.read().split('\n')

            if file[0] != f'"{title}"':
                with open(f'site/history/{chat_type}/{peer_id}_text.txt', 'w') as f:
                    file = title + '\n'.join(file[1:])
                    f.write(file)

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

            # if text == 'Пришли конфиг.':
            #     for key, value in bot.config_.items():
            #         send_text_message(api, peer_id, str(key))
            #         if key == 'empty':
            #             text = ''
            #             for exp in value:
            #                 text += '·' * 12 + str(exp)
            #                 text += '\n'
            #             send_text_message(api, peer_id, str(text))
            #             continue
            #         for intent, data in value.items():
            #             send_text_message(api, peer_id, '·' * 4 + str(intent))
            #             for t, exps in data.items():
            #                 send_text_message(api, peer_id, '·' * 8 + str(t))
            #                 text = ''
            #                 for exp in exps:
            #                     text += '·' * 12 + str(exp)
            #                     text += '\n'
            #                 send_text_message(api, peer_id, str(text))
            #     return 'ok'
            api.messages.setActivity(
                access_token=token, peer_id=str(peer_id), type='typing')
            msg = bot.get_answer(text)
            wait_time = int(len(msg) * char_time)
            time.sleep(wait_time if wait_time <= 10 else 10)
            api.messages.send(
                access_token=token,
                user_id=str(user_id),
                random_id=random.randint(0, 18446744073709551615),
                message=msg.format(author=author),
            )
            return 'ok'
        elif check_exist(text, list(map(lambda x: f'{x},', bot.config_['intents']['appeal']['example']))):
            api.messages.markAsRead(
                access_token=token,
                peer_id=str(peer_id),
                mark_conversation_as_read=1
            )
            m = check_exist(text, bot.config_['intents']['appeal']['example'])
            text1 = text.replace('[club194195372|@bot_michalych]', '')
            text1 = text1.replace(m[1], '')
            api.messages.setActivity(
                access_token=token, peer_id=str(peer_id), type='typing')
            msg = bot.get_answer(text1)
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
                msg = bot.get_answer(text)
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
                sticker_id=random.choice(VK_CONFIG['stickers'])
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
    elif data['type'] == 'message_reply':
        message = data['object']
        user_id = data['object']['from_id']
        peer_id = data['object']['peer_id']
        isChat = user_id != peer_id
        # message_id = data['object']['message']['conversation_message_id']
        text = message['text']
        char_time = 0.2

        # write history
        chat_type = 'conversation' if isChat else 'private'
        list_dir = os.listdir(f'site/history/{chat_type}/')

        if peer_id not in list_dir:
            os.mkdir(f'site/history/{chat_type}/{peer_id}')

        with open(f'site/history/{chat_type}/{peer_id}/full.txt', 'a') as f:
            f.write(str(message) + '\n')

        with open(f'site/history/{chat_type}/{peer_id}/text.txt', 'a') as f:
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

        with open(f'site/history/{chat_type}/{peer_id}/dialogue.txt', 'a') as f:
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
            # t = f'{author}:\n{message["text"]}\n{now}\n'
            t = f' - {message} - {author} - ({now})'
            f.write(t + '\n')
        return 'ok'
    else:
        return 'ok'
