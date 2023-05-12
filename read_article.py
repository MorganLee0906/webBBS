import re
def read_article(dir):
    f = open(dir, mode = 'r', encoding = 'big5', errors='ignore')
    cont = f.read().split('看板:')
    print(cont)