import os
import sqlite3
import datetime
import bcrypt
# import hashlib
# import base64, os
from flask import Flask , render_template , request , redirect , session
app = Flask(__name__)
app.secret_key = 'minpuro'

@app.route('/home')
def index():
    return render_template('index.html')



# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# フロントページに降順昇順でプロジェクト3つを出す
@app.route('/')
def home_index():
    #データベースとの接続
    conn = sqlite3.connect('minpuro.db')
    c = conn.cursor()
    # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
    # c.execute("select pro_name, pj_txt, category from project order by pj_ID desc limit 0, 3") 
    c.execute("select pj_ID, pro_name, pj_txt, category from project order by pj_ID desc limit 0, 3") 
    comment_list = []
    for row in c.fetchall():
        # comment_list.append({"pro_name": row[0], "pj_txt": row[1], "category": row[2]})
        comment_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3]})
        print(comment_list)
    c.close()
    print(comment_list)
    return render_template('index.html'  , comment_list = comment_list)


# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# カテゴリーページに12こプロジェクトを抽出
@app.route('/category')
def category():
    conn = sqlite3.connect('minpuro.db')
    c = conn.cursor()
    ca = "ca"
    c.execute("select pj_ID, pro_name, pj_txt, category from project where category = ? order by pj_ID desc limit 0, 12",(ca,)) 
    ca_list = []
    for row in c.fetchall():
        ca_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3]})
        print(ca_list)

    cb = "cb"
    c.execute("select pj_ID, pro_name, pj_txt, category from project where category = ? order by pj_ID desc limit 0, 12",(cb,))
    cb_list = []
    for row in c.fetchall():
        cb_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3]})
        print(cb_list)

    cc = "cc"
    c.execute("select pj_ID, pro_name, pj_txt, category from project where category = ? order by pj_ID desc limit 0, 12",(cc,)) 
    cc_list = []
    for row in c.fetchall():
        cc_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3]})
        print(cc_list)

    cd = "cd"
    c.execute("select pj_ID, pro_name, pj_txt, category from project where category = ? order by pj_ID desc limit 0, 12",(cd,)) 
    cd_list = []
    for row in c.fetchall():
        cd_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3]})
        print(cd_list)

    c.close()
    return render_template('category.html'  , ca_list = ca_list , cb_list = cb_list , cc_list = cc_list , cd_list = cd_list)

# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー


@app.route('/login')
def login():
    return render_template('login.html')

# ログイン情報チェックーーーーーーーーーーー
@app.route("/login", methods=["POST"])
def login_get():


    dr_name = request.form.get("dr_name")
    l_password = request.form.get("password")


    # print(s_password)

    # passwordを変換
    # password = password.encode()
    # salt = base64.b64encode(os.urandom(16))
    # salt = os.urandom(16)
    # library_hashed = hashlib.pbkdf2_hmac('sha256', password, salt, 10000)

    # パスワードをs_passwordへ
    # s_password = library_hashed
    # print(s_password)


    conn = sqlite3.connect("minpuro.db")
    c = conn.cursor()
    #nameとpasswordが一致する人のidを取得
    c.execute("select pf_ID,password,salt from profile where dr_name = ?", (dr_name,))
    login_list = []
    for row in c.fetchall():
        login_list.append({"pf_ID": row[0], "password": row[1], "salt": row[2]})
    # n_list = list(login_list(tuple))
    # saltの抽出確認(200814)
    # print(n_list)
    s_salt = str(login_list[0])

    encoded_pw = l_password.encode()

    # パスワードをハッシュ化
    s_password = bcrypt.hashpw(encoded_pw, s_salt)

    conn.close()

    # bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds)).decode()

    #ログインが成功したとき
    # if pf_ID is None:
    if password == s_password:
        session["pf_ID"] = pf_ID[0] #タプル型から値を取り出す
        pf_ID = int(pf_ID[0])  # IDをとってきた

        pf_url = ("/mypage/"+str(pf_ID))

        return redirect(pf_url, login_list = login_list)

        # return redirect("/login")
    #ログインが失敗した時
    else:  
        return redirect("/login")
        # session["pf_ID"] = pf_ID[0] #タプル型から値を取り出す
        # pf_ID = int(pf_ID[0])  # IDをとってきた

        # pf_url = ("/mypage/"+str(pf_ID))

        # return redirect(pf_url)


# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー




@app.route("/regist", methods=["GET"])
def form_get():
    return render_template("form.html")



@app.route('/regist', methods=["POST"])
def do_regist():
    # saltの生成
    salt = bcrypt.gensalt(rounds=10, prefix=b'2a')

    # 登録情報
    name = request.form.get("name")
    dr_name = request.form.get("dr_name")
    p_name = request.form.get("p_name")
    p_address = request.form.get("p_address")
    password = request.form.get("password")
    dig = request.form.get("dig")
    area = request.form.get("area")
    interest = request.form.get("interest")
    f_txt = request.form.get("f_txt")
    conn = sqlite3.connect("minpuro.db")
    
    # パスワードをハッシュ化
    s_password = bcrypt.hashpw(password.encode("UTF-8"), salt)

    # パスワード検証
    # bcrypt.checkpw(password, hashed_password)

    c = conn.cursor()
    c.execute("insert into profile values(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, dr_name, p_name, p_address, s_password, dig, area, interest, f_txt, salt))
    conn.commit()
    conn.close()
    return redirect("/login")



# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# マイページの表示
@app.route("/mypage/<int:pf_ID>", methods=["GET"])
def mypage(pf_ID):
    # ログインしていた場合とそうでない場合で処理を分ける(200814)
    try :
        # session存在の確認
        session["pf_ID"]

        conn = sqlite3.connect('minpuro.db')
        c = conn.cursor()
        c.execute("select dr_name, dig, area, interest, f_txt from profile where pf_ID = ?" ,(pf_ID,))
        page_list = []
        for row in c.fetchall():
            page_list.append({"dr_name": row[0], "dig": row[1], "area": row[2], "interest": row[3], "f_txt": row[4]})
        # c.close()
        # return render_template("mypage.html", page_list = page_list)


    # # マイページのhtml
    # @app.route('/mypage/<int:pf_ID>' , methods=["GET"])
    # def mypage_ditail(pf_ID):
    #     # owner_ID = session["pf_ID"]
    #     conn = sqlite3.connect('minpuro.db')
    #     c = conn.cursor()
    #     c.execute("select dr_name,dig,area,interest,f_txt from profile where pf_ID = ?",(pf_ID,))
    #     mypage_list = []
    #     for row in c.fetchall():
    #         mypage_list.append({"dr_name": row[0], "dig": row[1], "area": row[2], "interest": row[3], "f_txt": row[4]})
    #     print(mypage_list)
        c = conn.cursor()
        c.execute("select pj_ID, pro_name, pj_txt, category, pj_count from project where owner_ID = ?",(pf_ID,))
        myproject_list = []
        for row in c.fetchall():
            myproject_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3]})
        print(myproject_list)


        c.close()
        return render_template('mypage.html' , page_list = page_list, myproject_list = myproject_list)
    

    except KeyError:
        # session["pf_ID"]が存在していなかった時の処理
        return redirect("/login")


# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# プロジェクト参加ページ
@app.route("/project/<int:pj_ID>", methods=["GET"])
def project(pj_ID):
    # ログインしていた場合とそうでない場合で処理を分ける
    try :
        # session存在の確認
        session["pf_ID"]

        # sessionが存在していた場合の処理
        pf_ID = session["pf_ID"]
        conn = sqlite3.connect('minpuro.db')
        c = conn.cursor()
        c.execute("select pj_ID, pro_name, pj_txt, pj_count from project where pj_ID = ?" ,(pj_ID,))
        project_list = []
        for row in c.fetchall():
            project_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3]})

        c = conn.cursor()
        c.execute("select prjuser_ID, prjpj_ID from prj where prjuser_ID = ? and prjpj_ID = ?" ,(pf_ID, pj_ID,))
        prj_check_list = []
        for row in c.fetchall():
            prj_check_list.append({"prjuser_ID": row[0], "prjpj_ID": row[1]})
        print(prj_check_list)
        c.close()

        if prj_check_list == []:
            return render_template("project.html" , project_list = project_list, prj_check_list = prj_check_list)
        else:
            pj_ID = int(pj_ID)
            prj_url = ("/pro_detail/"+str(pj_ID))
            return redirect(prj_url)


    except KeyError:
        # session["pf_ID"]が存在していなかった時の処理
        return redirect("/login")





# 新規プロジェクト立ち上げーーーーーーーーーーーーーーーーーー
@app.route('/build')
def build():
    return render_template('newpro.html')

@app.route("/build", methods=["POST"])
def build_project():
    # ログインしていた場合とそうでない場合で処理を分ける
    try :
        # session存在の確認
        session["pf_ID"]

        owner_ID = session["pf_ID"] 
        # upload = request.form.get['upload']
        # if not upload.pffile.lower().endswith(('.png', '.jpg', '.jpeg')):
        #     return 'png,jpg,jpeg形式のファイルを選択してください'
        
        # save_path = get_save_path()
        # print(save_path)
        # prfile = upload.prfile
        # upload.save(os.path.join(save_path,prfile))
        # print(prfile)
        # conn = sqlite3.connect('project.db')
        # c = conn.cursor()
        # c.execute("update user set t_img = ?, (prfile)) #prfileはプロジェクト画像の保管ファイル
        # conn.commit()  #だめだったら2つに分けて書く！！！！！！！！！！！！！！！！！
        # conn.close()

        pro_name = request.form.get("pro_name")
        pj_txt = request.form.get("pj_txt")
        pj_period = request.form.get("pj_period")
        pj_count = request.form.get("pj_count")
        category = request.form.get("category")
        print(category)

        if category == "1":
            category = "ca"
        elif category == "2":
            category = "cb"
        elif category == "3":
            category = "cc"
        else:
            category = "cd"

        #t_imgは一つ上のc.executeで取り込み済み！！！！
        conn = sqlite3.connect("minpuro.db")
        c = conn.cursor()
        c.execute("insert into project values(null, ?, ?, ?, ?, ?, ?)", (pro_name, pj_txt, owner_ID, pj_period, category, pj_count))
        conn.commit()
        conn.close()
        pf_ID = session["pf_ID"]
        pf_ID = int(pf_ID)
        pf_url = ("/mypage/"+str(pf_ID))

        return redirect(pf_url)
        # return "やったぜ！" # render_template("bbs-master/bbs.html")

    except KeyError:
    # session["pf_ID"]が存在していなかった時の処理
        return redirect("/login")




# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# 研究の個人投稿場 参加するボタンを押したら個々のプロジェクトページに移動（中間テーブルに書き込み）
@app.route("/pro_detail/<int:pj_ID>" ,methods=["POST","GET"])
def project_p(pj_ID):
     # ログインしていた場合とそうでない場合で処理を分ける
    try :
    # session存在の確認
        session["pf_ID"]


        pf_ID = session['pf_ID']
        prjuser_ID = session['pf_ID']
        session["pj_ID"] = pj_ID
        conn = sqlite3.connect('minpuro.db')

        c = conn.cursor()
        c.execute("insert into prj values(null, ?, ?)", (prjuser_ID, pj_ID))
        conn.commit()
        c.execute("select pj_ID, pro_name, pj_txt, category, pj_count from project where pj_ID = ? order by pj_ID desc limit 0, 3",(pj_ID,))
        pro_detail_list = []
        for row in c.fetchall():
            pro_detail_list.append({"pj_ID": row[0], "pro_name": row[1], "pj_txt": row[2], "category": row[3], "pj_count": row[4]})
        
        # 投稿の部分の個人ネーム
        c = conn.cursor()
        c.execute("select pf_ID, dr_name from profile where pf_ID = ?",(pf_ID,))
        profile_bbs_list = []
        for row in c.fetchall():
            profile_bbs_list.append({"pf_ID": row[0], "dr_name": row[1]})
            print(profile_bbs_list)

        c = conn.cursor()
        c.execute("select pro_name, pj_txt, category, pj_count from project join prj on prjpj_ID = pj_ID where pj_ID = ? order by pj_ID desc limit 0, 3", (pj_ID,))
        pro_join_list = []
        for row in c.fetchall():
            pro_join_list.append({"pro_name": row[0], "pj_txt": row[1], "category": row[2], "pj_count": row[3]})
        print(pro_join_list)


        # 投稿の表示
        c = conn.cursor()
        c.execute("select id,user_id,comment,time,bbs_pj_id from bbs where bbs_pj_id = ?",(pj_ID,))
        project_post_list = []
        for row in c.fetchall():
            project_post_list.append({"id": row[0], "user_id": row[1], "comment": row[2], "time": row[3], "bbs_pj_id": row[4]})
            print(profile_bbs_list)


        c.close()
        return render_template("bbs.html", pro_detail_list = pro_detail_list, pro_join_list = pro_join_list, profile_bbs_list = profile_bbs_list, project_post_list = project_post_list)
    

    except KeyError:
        # session["pf_ID"]が存在していなかった時の処理
        return redirect("/login")




# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    # c.execute("select pro_name, pj_txt, category from project where category = ? order by pj_ID desc limit 0, 12",(cd,)) 






# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# bbsページの投稿欄
@app.route("/add", methods=["POST"])
def add():
    user_id = session['pf_ID']
    bbs_pj_id = session['pj_ID']
    # フォームから入力されたアイテム名の取得
    comment = request.form.get("comment")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect('minpuro.db')
    c = conn.cursor()
    # DBにデータを追加する
    c.execute("insert into bbs values(null,?,?,?,?)", (user_id, comment, time, bbs_pj_id))
    conn.commit()


    # # プロジェクト投稿の表示
    # c = conn.cursor()
    # c.execute("select id,user_id,comment,time,bbs_pj_id from bbs where bbs_pj_id = ?",(bbs_pj_id))
    # project_post_list = []
    # for row in c.fetchall():
    #     project_post_list.append({"id": row[0], "user_id": row[1], "comment": row[2], "time": row[3], "bbs_pj_id": row[4]})
    #     print(profile_bbs_list)

    
    conn.close()
    pj_ID = session["pj_ID"]
    pj_url = ("/pro_detail/"+str(pj_ID))

    return redirect(pj_url)
    # return redirect("/pro_detail/<int:pj_ID>")


@app.route("/edit")
def update_item():
     # ブラウザから送られてきたデータを取得
    item_id = request.args.get("item_id") # id
    item_id = int(item_id)# ブラウザから送られてきたのは文字列なので整数に変換する
    comment = request.args.get("comment") # 編集されたテキストを取得する

    # 既にあるデータベースのデータを送られてきたデータに更新
    conn = sqlite3.connect('minpuro.db')
    c = conn.cursor()
    c.execute("update bbs set comment = ? where id = ?",(comment,item_id))
    conn.commit()
    conn.close()

    # アイテム一覧へリダイレクトさせる
    return redirect("/bbs")


@app.route('/del' ,methods=["POST"])
def del_task():
    # クッキーから user_id を取得
    id = request.form.get("comment_id")
    id = int(id)
    conn = sqlite3.connect("minpuro.db")
    c = conn.cursor()
    c.execute("delete from bbs where id = ?", (id,))
    conn.commit()
    c.close()
    return redirect("/bbs")
    

# ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
# ログアウト
@app.route("/logout")
def logout():
    session.pop('pf_ID',None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/login")






if __name__ == "__main__":
    app.run(debug = True)

    # プロジェクトスレッドを作りたいのです