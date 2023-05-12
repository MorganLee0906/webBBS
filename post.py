from datetime import datetime
import os
import random
weekd = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
info = '作者: {} ({}) 看板: {} \n標題: {} \n時間: {} \n'
def post_article(board, user, nickname, title, content):
    fname = "M."+str(int(datetime.now().timestamp()))+".A."+str(random.randint(100,999))
    w = open("../article/{}".format(fname), 'w', encoding='big5')
    w.write(info.format(user, nickname, board, title, datetime.now().ctime()))
    w.write(content)
    w.write('\n--\n')
    w.write('※  發信站: webBBS(pttest.cc), 來自:網頁版服務\n')
    w.close()
    f = open("../article/recent_post", 'a', encoding = 'big5')
    f.write(f'{title}/{board}/{user}/{fname},\n')
    f.close()
    #os.system('./bin/post {} {} {} {}'.format(board, title, user, "~/article/{}".format(fname)))

if __name__ == '__main__':
    cont = "Test\ntteesstt\n"
    post('Gossiping', 'Tester.', 'Test', 'Test', cont)