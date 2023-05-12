import re
class info:
    def __init__(self, title, author, date):
        self.title = title
        self.author = author
        self.date = date
def get_article(dir):
    f = open(dir, mode = 'r', encoding = 'big5', errors='ignore')
    lis = re.split('[\0]{15,}', f.read())
    #pat = 'M.(\d+).A.([0-9]|[A-F]{3})'
    #re_find = re.findall(pat,f.read())
    #print(re_find)
    a_lis = dict()
    #print(lis)
    for i in lis:
        try:
            fname, oinfo = re.split('\0{10}[^\0]*\0{2}',i)
            author, oinfo2 = re.split('\0{5}', oinfo)
            date , title = re.split('\0', oinfo2)
            a_lis[fname] = info(title, author, date)
            print(a_lis[fname].title)
        except:
            continue
    f.close()
    return a_lis