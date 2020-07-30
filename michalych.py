import random
import string
import re
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
from config import BOT_CONFIG

class Bot():
    def __init__(self, config):
        self.config_ = config
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

if __name__ == '__main__':
    bot = Bot(BOT_CONFIG)
    print(BOT_CONFIG)
    while True:
        text = input('Я:       ')
        if text.lower() in ['выход', 'exit', 'пока']:
            print('Михалыч: Пока!')
            break
        # print(f'(tech: {bot.get_intent(text)})')
        print('Михалыч:', bot.get_answer(text))
