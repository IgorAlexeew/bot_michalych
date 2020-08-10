import random
import string
import re
import sys

# sep = '\\' if '\\' in __file__ else '/'
# sep = '\\' if '\\' in __file__ else '/'
# path = __file__.split(sep)
# path = sep.join(path[:-1] + [''])
# print(path)
# sys.path += [f'{path}{sep}config']
# print(sys.path)

from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.linear_model import LogisticRegression
import joblib
# from config.config import BOT_CONFIG
from extra import get_path

path_set = get_path()


class Bot():
    def __init__(self, *args, **kwargs):
        sep = path_set[2]
        self.config_path = sep.join(path_set[1] + ['config', ''])
        if 'config' in kwargs:
            self.config_ = kwargs['config']
        elif 'path_config' in kwargs:
            self.config_ = self.open_config(kwargs['path_config'])
        else:
            self.config_ = self.open_config(f'{self.config_path}bot.config')

        self.threshold = 0.44

        X_text = []
        y = []
        for intent, value in self.config_['intents'].items():
            X_text += value['example']
            y += [intent] * len(value['example'])

        self.vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        X_text = self.clean_str(X_text)
        X = self.vectorizer.fit_transform(X_text)

        self.model = LogisticRegression(solver='lbfgs', multi_class='auto')
        self.model.fit(X, y)

    def get_answer(self, text):
        intent = self.get_intent(text)

        if intent:
            return self.response_by_intent(intent)

        # generative model
        # TO DO

        return self.get_failure_phrase()

    def get_intent(self, text):
        text_vector = self.vectorizer.transform([self.clean_str(text)]).toarray()[0]
        probas_list = self.model.predict_proba([text_vector])[0]
        # np_array = probas_list
        probas_list = list(probas_list)
        max_proba = max(probas_list)
        index = probas_list.index(max_proba)
        # print(f'(proba:   {max_proba:>10.3f})')
        # avg = np_array.mean()
        # std = np_array.std()
        # print(f'(average: {avg:>10.3f})')
        # print(f'(std:     {std:>10.3f})')
        # print(f'(intent: {self.model.classes_[index]})')

        if max_proba > self.threshold:
            index = probas_list.index(max_proba)
            return self.model.classes_[index]

    def response_by_intent(self, intent):
        responses = self.config_['intents'][intent]['response']
        return random.choice(responses)
    
    def get_failure_phrase(self):
        failure_phrases = self.config_['empty']
        return random.choice(failure_phrases)

    def clean_str(self, text):
        if isinstance(text, str):
            res = text
            translate_table = dict((ord(char), ' ') for char in string.punctuation)   
            res = res.translate(translate_table)
            res = res.strip()
            res = re.sub(r'\s+', ' ', res)
            return res
        elif isinstance(text, list):
            res = []
            for t in text:
                res.append(self.clean_str(t))
            return res
        else:
            pass
    
    def save_model(self):
        joblib.dump(self.model, 'config/bot.model')
    
    def open_model(self):
        m = joblib.load('config/bot.model')
        return m
    
    def open_config(self, path='config/bot.config'):
        CONFIG = {}

        with open(f'{path}', 'r', encoding='utf-8') as f:
            file = f.read()
            file = re.sub(r'(\t){1}', ' ', file)
            file = file.split('\n')

        klevel = []

        for line in file:
            print(line)
            if line.strip() == '' and len(klevel) > 0:
                klevel.pop(-1)

            if re.match(r'\b[a-z]*:', line):
                CONFIG[line[:-1]] = {}
                klevel = []
                klevel.append(line[:-1])
                continue

            if re.match(r'\b.*', line) and len(klevel) == 3:
                CONFIG[klevel[0]][klevel[1]][klevel[2]] += f'\n{line}'
                continue

            if re.match(r'\s{4}\b[a-z]*:', line):
                # if 'intents' not in CONFIG:
                #     CONFIG['intents'] = None
                if len(klevel) > 1:
                    klevel.pop(-1)

                CONFIG[klevel[0]][line.strip(' :')] = {}
                klevel.append(line.strip(' :'))
                continue

            if re.match(r'\s{8}\b[a-z]*:', line):
                # if 'intents' not in CONFIG:
                #     CONFIG['intents'] = None
                CONFIG[klevel[0]][klevel[1]][line.strip(' :')] = []
                klevel.append(line.strip(' :'))
                continue

            if re.match(r'\s{12}\b.*', line) and len(klevel) == 3:
                CONFIG[klevel[0]][klevel[1]][klevel[2]].append(line.strip())
                continue

            if re.match(r'\s{12}\b.*', line) and len(klevel) == 1:
                if CONFIG[klevel[0]] == {}:
                    CONFIG[klevel[0]] = []
                CONFIG[klevel[0]].append(line.strip())
                continue
        # from pprint import pprint
        # pprint(CONFIG)
        return CONFIG



if __name__ == '__main__':
    bot = Bot()
    bot.save_model()
    # print(BOT_CONFIG)
    while True:
        text = input('Я:       ')
        
        # print(f'(tech: {bot.get_intent(text)})')
        print('Михалыч:', bot.get_answer(text))
        if bot.get_intent(text) == 'goodbye':
            break
