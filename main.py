from logging import warning
import re
from time import timezone
from flask import Flask, redirect,request,render_template,session,flash,redirect,url_for,Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import date, datetime, time ,timedelta, timezone
import passwd
import pytz
import article
import read_maillist
import os
import post

#variable area
last_update = None
latest = None

CST = pytz.timezone('Asia/Taipei')
dt_CST = datetime.now(CST)
today = date(int(dt_CST.strftime("%Y")), int(dt_CST.strftime("%m")), int(dt_CST.strftime("%d")))

f = open('.brd_list', mode = 'r', encoding = 'utf-8')
brd_list = list(f.read().split(',\n'))

class info:
    def __init__(self, title, author, board):
        self.title = title
        self.author = author
        self.board = board
class User(UserMixin):
    pass
announcement = {
    "本網站仍在測試開發階段，可能會有不穩定的狀況發生，請見諒!":"warning"
}
recent_article = {}
hot_article = {}

app = Flask(__name__)
app.secret_key = "ab9e43caebeb0ac3ff17846617b1a205"
app.config["SECRET_KEY"] = "ab9e43caebeb0ac3ff17846617b1a205"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('Username')
    if passwd.chkid(id) == 404:
        return
    user = User()
    user.id = username
    if passwd.chkpwd(username, request.form['Password']) != 403:
        user.is_authenticated = True
    return user

@app.route("/")
def home():
    if len(announcement)!=0:
        for key, value in announcement.items():
            flash(key, value)
    f = open('../article/recent_post', 'r', encoding = 'big5')
    recent_article = dict()
    if(f.read()!=''):
        print(f.read())
        info_list = f.read().split(',')
        for article in info_list:
            print(article)
            #title, board, author, fname = article.split('/')
            #recent_article[fname] = info(title, author, board)
    return render_template('home.html', a_list = recent_article)

@app.route("/bbs")
def boardlist():
    return render_template('board.html', b_list = brd_list)

@app.route("/bbs/<string:boardname>")
def articlelist(boardname):
    dir = f'boards/{boardname[0]}/{boardname}/.DIR'
    print(dir)
    a_list = article.get_article(dir)
    for key, value in a_list.items():
        print(key, value.title, value.author, value.date)
    return render_template('boardlist.html', boardname = boardname, a_list = a_list)

@app.route("/bbs/<boardname>/<filename>", methods = ["POST", "GET"])
def article_read(boardname, filename):
    file_path = f'boards/{boardname[0]}/{boardname}/{filename}'
    f = open(file_path, mode = 'r', encoding = 'big5', errors='ignore')
    cont = f.read()
    f.close()
    if current_user.is_authenticated:
        userid = current_user.id
    else:
        userid = 'guest'
        print('guset')
    if request.method == "POST":
        f = open(file_path, mode = 'a+', encoding = 'big5', errors='ignore')
        print(request.form['options'])
        if request.form['options'] == 'push':
            c_type = "推"
        elif request.form['options'] == 'bad':
            c_type = "噓"
        else:
            c_type = "→"
        f.write("{} {} :{}  {}/{} {}:{}\n".format(c_type, userid, request.form['comment'], dt_CST.strftime("%m"), dt_CST.strftime("%d"), dt_CST.strftime("%H"), dt_CST.strftime("%M")))
        f.close()
        flash("正在發布留言中...", 'warning')
        return render_template('article_read.html', content = cont, id = userid, dir = file_path, r_url = f"/bbs/{boardname}/{filename}",commented = True)
    else:
        return render_template('article_read.html', content = cont, id = userid, dir = file_path, commented = False)

@app.route("/login",methods = ["POST","GET"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)
    username = request.form['Username']
    if passwd.chkid(username) == 404:
        flash('Your username or password is incorrect! ({})'.format(passwd.chkid(id)),'danger')
        return render_template("login.html")
    if passwd.chkpwd(username, request.form['Password']) != 403:
        user = User()
        user.id = username
        login_user(user)
        flash(f'使用者{username}您好!','success')
        return redirect(url_for('home'))
    else:
        flash('Your username or password is incorrect! ({})'.format(passwd.chkpwd(username, request.form['Password'])),'danger')
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout sucessfully!",'success')
    return render_template('login.html')

@app.route("/publish")
@login_required
def publish():
    board = request.args.get('board')
    print(board)
    return render_template('publish.html', id=current_user.id, b_list = brd_list, selected = board)

@app.route("/publish/submit",methods = ["POST","GET"])
@login_required
def submit():
    if request.method == 'POST':
        author = current_user.id
        bname = str(request.form['postboard'])
        title = request.form['title']
        content = request.form['content']
        post.post_article(bname, author, author, title, content)
        flash(f"文章發表中，正在重新導向至{bname}看板，若未看見文章請重新整理", 'warning')
        return render_template('post.html', boardname = bname)
        #the backend post already finished, but the code save on another place:P
        #filepath = 
        #os.system(f'bin/post {bname} {title} {author} {fpath}')

@app.route("/mail")
@login_required
def maillist():
    #a_list = read_maillist(current_user.id)
    a_list = {}
    return render_template('mail.html',a_list = a_list)
  
if __name__ == '__main__':
    app.run(host="0.0.0.0")