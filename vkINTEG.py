import os
import random
import time
import difflib
import vk
from config.config import get_path
from michalych import Bot


class vkAPI(vk.API):
    def __init__(self, session, token, *args, **kwargs):
        super().__init__(session, *args, **kwargs)
        self.token = token

    def send(self, peer_id, *args, **kwargs):
        ans = self.messages.send(
            access_token=self.token,
            peer_id=str(peer_id),
            random_id=random.randint(0, 18446744073709551615),
            *args,
            **kwargs
        )
        return ans

    def sendMessage(self, peer_id, message):
        ans = self.send(peer_id=peer_id, message=str(message))
        return ans

    def sendSticker(self, peer_id, sticker_id):
        ans = self.send(peer_id=peer_id, sticker_id=sticker_id)
        return ans

    def getSelfInfo(self):
        ans = self.groups.getById(
            access_token=self.token
        )
        return ans

    def markAsRead(self, peer_id):
        ans = self.messages.markAsRead(
            access_token=self.token,
            peer_id=str(peer_id),
            mark_conversation_as_read=1
        )
        return ans

    def setActivity(self, peer_id):
        ans = self.messages.setActivity(
            access_token=self.token,
            peer_id=str(peer_id),
            type='typing'
        )
        return ans

    def getConversationsById(self, peer_id):
        conv = self.messages.getConversationsById(
            access_token=self.token,
            peer_ids=peer_id
        )
        return conv


path = get_path()[0]


def check_exist(text, patterns):
    for w in text.split():
        match = difflib.get_close_matches(w, patterns)
        if len(match) > 0:
            return (match, w)
    return False


def GET_from_vk(data, session, api, settings):
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

        bot = Bot()
        token = settings['token']
        confirmation_token = settings['confirmation_token']
        password = settings['password']

        api = vkAPI(session, token, v='5.122')

        message = data['object']['message']
        user_id = data['object']['message']['from_id']
        peer_id = data['object']['message']['peer_id']
        text = message['text']
        author = api.users.get(access_token=token, user_ids=user_id)[0]
        author = author['last_name'] + ' ' + author['first_name']
        conv = api.getConversationsById(peer_id)
        char_time = 0.2
        isChat = user_id != peer_id
        now = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime())


        # def send(*args, **kwargs):
        #     ans = api.messages.send(
        #         access_token=token,
        #         peer_id=peer_id,
        #         random_id=random.randint(0, 18446744073709551615),
        #         *args,
        #         **kwargs
        #     )
        #     return ans
        

        # def getSelfInfo():
        #     ans = api.groups.getById(
        #         access_token=token
        #     )
        #     return ans
        

        # def markAsRead(peer_id=peer_id):
        #     ans = api.messages.markAsRead(
        #         access_token=token,
        #         peer_id=str(peer_id),
        #         mark_conversation_as_read=1
        #     )
        #     return ans
        
        # def setActivity(peer_id=peer_id):
        #     api.messages.setActivity(
        #         access_token=token,
        #         peer_id=str(peer_id),
        #         type='typing'
        #     )
        

        # def getConversationsById(peer_id=peer_id):
        #     api.messages.getConversationsById(
        #         access_token=token,
        #         peer_ids=peer_id
        #     )


        # write history
        chat_type = 'conversation' if isChat else 'private'
        list_dir = os.listdir(f'site/history/{chat_type}')

        history_path = f"site/history/{chat_type}/{peer_id}"
        if str(peer_id) not in list_dir:
            isNew = True
            os.mkdir(history_path)
        else:
            isNew = False

        with open(f'{history_path}/full.txt', 'a') as f:
            f.write(str(message) + '\n')

        # chat title
        if isChat:
            title = conv['items'][0]['chat_settings']['title']
            title = f'Беседа "{title}" ({peer_id})\n'
        else:
            title = f'Личные сообщения ({peer_id})\n'
            

        with open(f'{history_path}/text.txt', 'a') as f:
            if isNew:
                f.write(title + '\n')
            t = f'{author}:\n{message["text"]}\n{now}\n'
            f.write(t + '\n')
        
        with open(f'{history_path}/dialogue.txt', 'a') as f:
            if isNew:
                f.write(title + '\n')
            # t = f'{author}:\n{message["text"]}\n{now}\n'
            t = f' - {message["text"]} - {author} - ({now})'
            f.write(t + '\n')

        # check chat name changing
        if isChat:
            with open(f'{history_path}/text.txt', 'r') as f:
                file = f.read().split('\n')

            if file[0] != f'{title}':
                with open(f'{history_path}/text.txt', 'w') as f:
                    file = title + '\n'.join(file[1:])
                    f.write(file)
            
            if file[0] != f'{title}':
                with open(f'{history_path}/dialogue.txt', 'w') as f:
                    file = title + '\n'.join(file[1:])
                    f.write(file)

        # send answer
        if not isChat:
            api.markAsRead(peer_id)
            if check_exist(text, ['Скажи им', 'Напиши в визуат гэрлс']) and password in text.split():
                api.sendMessage(peer_id, 'Ок.')
                msg = text.split('"')[1].split('\n')
                for m in msg:
                    api.messages.send(
                        access_token=token,
                        peer_id=str(2000000001),
                        random_id=random.randint(0, 18446744073709551615),
                        message=m,
                    )
                    time.sleep(2)

                api.sendMessage(peer_id, 'Сказал.')
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
            api.setActivity(peer_id)
            msg = bot.get_answer(text)
            wait_time = int(len(msg) * char_time)
            time.sleep(wait_time if wait_time <= 10 else 10)
            author_name = author.split()[1]
            api.sendMessage(peer_id, msg.format(author_name=author_name))
            return 'ok'

        elif check_exist(text, list(map(lambda x: f'{x},', bot.config_['intents']['appeal']['example']))):
            api.markAsRead(peer_id)
            m = check_exist(text, bot.config_['intents']['appeal']['example'])
            vk_appeal = '[club194195372|@bot_michalych]'
            text = text.replace(vk_appeal, '').replace(m[1], '')
            api.setActivity(peer_id)
            msg = bot.get_answer(text)
            # time.sleep(int(len(msg) * char_time))
            author_name = author.split()[1]
            api.sendMessage(peer_id, msg.format(author_name=author_name))
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
                author_name = author.split()[1]
                api.sendMessage(peer_id, msg.format(author_name=author_name))
                return 'ok'
            # api.messages.send(
            #     access_token=token,
            #     peer_id=str(peer_id),
            #     random_id=random.randint(0, 18446744073709551615),
            #     message=random.choice(base['send'][text_analyze(text)]),
            # )
            api.markAsRead(peer_id)
            api.sendSticker(peer_id, random.choice(VK_CONFIG['stickers']))
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
        author = "Михалыч"
        # message_id = data['object']['message']['conversation_message_id']
        text = message['text']
        char_time = 0.2

        # write history
        chat_type = 'conversation' if isChat else 'private'
        list_dir = os.listdir(f'site/history/{chat_type}/')

        if str(peer_id) not in list_dir:
            os.mkdir(f'site/history/{chat_type}/{peer_id}')

        with open(f'site/history/{chat_type}/{peer_id}/full.txt', 'a') as f:
            f.write(str(message) + '\n')

        with open(f'site/history/{chat_type}/{peer_id}/text.txt', 'a') as f:
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
            t = f' - {message["text"]} - {author} - ({now})'
            f.write(t + '\n')
        return 'ok'
    else:
        return 'ok'
