# print('Hello, World!')
# print('It is test file.')
# print('I hope it is working...')
# print('Мда...')

import time

def logsmth(text):
    # text_array = []
    # text_array = ' '.join(args)
    with open('mysite/log_by_hook.txt', 'a') as f:
        f.write(time.strftime("%H:%M:%S %d.%m.%Y", time.localtime()) + f' -> {text}' + '\n')
    print('Мда...')
