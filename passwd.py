from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
loaded = dict()
def upd():
    loaded.clear()
    start()
    f = open('../.useraccount', mode = 'r', encoding='utf-8')
    
    apwd = f.read().split(',\n')
    f.close()

    #Clear the file with unencrypt passwd.
    f = open('../.useraccount', mode = 'w', encoding='utf-8')
    f.close()
    #Clear the file with old passwd.
    f = open('.webpasswd', mode = 'w', encoding = 'utf-8')
    f.close()

    w = open('.webpasswd', mode = 'a', encoding = 'utf-8')

    for user in range(0,len(apwd)-1):
        id, passwd = apwd[user].split(':')
        print(passwd, '\t', type(passwd))
        cryptpwd = bcrypt.generate_password_hash(password=passwd).decode('utf-8')
        loaded[id] = cryptpwd
    for id in loaded:
        w.write("{}:{},\n".format(id, loaded[id]))
    w.close()
def start():
    f = open('.webpasswd', mode = 'r', encoding = 'utf-8')
    apwd = f.read().split(',\n')
    f.close()
    for user in range(0,len(apwd)-1):
        id, passwd = apwd[user].split(':')
        loaded[id] = passwd
def chkid(id):
    if id not in loaded:
        upd()
        # If id not in list, check new uer again.
        if id not in loaded:
            return 404
def chkpwd(id, input):
    print(loaded[id])
    if bcrypt.check_password_hash(loaded[id], input):
        return id
    else:
        return 403
def loaduser():
    upd()
    rt = list()
    for id in loaded:
        rt.append(id)
    return rt