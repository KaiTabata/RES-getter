from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, session
import requests
from datetime import timedelta #settion管理で時間情報を用いるため

'''meta tag追跡用'''
from bs4 import BeautifulSoup
from urllib.parse import urljoin



app = Flask(__name__)
app.secret_key = "user"
app.permanent_session_lifetime = timedelta(minutes=5) # -> 5分 #(days=5) -> 5日保存


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        # フォームからデータを取得する
        DocNo = request.form.get('doc')
        DocNo = str(DocNo)
        print(DocNo)
        # DocNoが指定されているかどうかを確認する
        if DocNo == "":
            # DocNoが指定されていない場合は、エラーメッセージを表示する
            flash("DocNoが指定されていません")
            return render_template("index.html")
        
        # DocNoが指定されている場合は、DocNoを使用してURLを作成する
        redirect_url = "https://daccess-ods.un.org/access.nsf/Get?OpenAgent&DS="+DocNo+"&Lang=E"
        print(redirect_url)
        # URLが無効な場合は、処理を中断する
        if redirect_url is None or redirect_url == "":
            flash("無効なURLです")
            return render_template("index.html")
        
        # リダイレクト先のURLが変更される限り、繰り返し処理を行う
        while True:
            # HTTP HEADリクエストを送信する
            try:
                # HTTP HEADリクエストを送信する
                response = requests.get(redirect_url, timeout=10)
            except Exception as e:
                # 例外が発生した場合は、エラーメッセージを表示する
                flash(str(e))
                return render_template("index.html")

            # HTMLページからMETAタグを抽出する
            soup = BeautifulSoup(response.text, "html.parser")
            meta_tag = soup.find("meta", attrs={"http-equiv": "refresh"})

            # METAタグからリダイレクト先のURLを取得する
            try:
                new_redirect_url = meta_tag["content"].split(";")[1].split("=")[1]
            except:
                break
            
            # リダイレクト先のURLが相対パスの場合、絶対パスに変換する
            new_redirect_url = urljoin(redirect_url, new_redirect_url)

            # リダイレクト先のURLが変更されなかった場合、繰り返し処理を終了する
            if redirect_url == new_redirect_url:
                break

            # リダイレクト先のURLを更新する
            redirect_url = new_redirect_url

        # 最終的なリダイレクト先のURLを取得する
        DocURL = redirect_url
        print(DocURL)
        string = DocURL
        string = string.replace("PDF", "doc")
        string = string.replace(".pdf", ".docx")
        DocURL = string
    button = "on"
    print(DocURL)
    return render_template('index.html', DocNo=DocNo, DocURL=DocURL, button=button)

@app.route('/download/<DocNo>/<DocURL>')
def download(DocNo, DocURL):
    return render_template("download.html", DocURL=DocURL,)


if __name__ == "__main__":
    app.run(port=8000, debug=True)