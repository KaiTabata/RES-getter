from flask import request
from flask import Flask,render_template
import requests
'''meta tag追跡用'''




app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    if request.method == 'POST':
        DocNo = request.form.get('doc')
        DocNo = str(DocNo)
        DocURL = requests.get("https://daccess-ods.un.org/access.nsf/Get?OpenAgent&DS="+DocNo+"&Lang=E").url
        

        # ここから先のボツ群はDocURLのリダイレクト先を追跡してそのURLからJobNumberを取得しようと邁進していたときのやつ
        ''' soupparser使ってメタタグ追跡しようとしたボツ
from lxml.html import soupparser
        def meta_redirect(content):
            root = soupparser.fromstring(content)
            result_url = root.xpath('//meta[@http-equiv="refresh"]/@content')
            if result_url:
                result_url = str(result_url[0])
                urls = result_url.split('URL=') if len(result_url.split('url=')) < 2    else result_url.split('url=')
                url = urls[1] if len(urls) >= 2 else None
            else:
                return None
            return url
        response = request.get_data(DocURL)
        redirected_url = meta_redirect(response)
        print(DocURL)
        print(redirected_url)
        '''
        '''
        magic使おうとしたボツ
        import magic
import mimetypes
import requests
from lxml import html 
from urllib.parse import urljoin

        def test_for_meta_redirections(r):
            mime = magic.from_buffer(r.content, mime=True)
            extension = mimetypes.guess_extension(mime)
            if extension == '.html':
                html_tree = html.fromstring(r.text)
                attr = html_tree.xpath("//meta[translate(@http-equiv, 'REFSH', 'refsh') = 'refresh']/@content")[0]
                wait, text = attr.split(";")
                if text.lower().startswith("url="):
                    url = text[4:]
                    if not url.startswith('http'):
                        # Relative URL, adapt
                        url = urljoin(r.url, url)
                    return True, url
            return False, None
        def follow_redirections(r, s):
            """
            メタリフレッシュのリダイレクトが存在する場合にたどる再帰関数
            """
            redirected, url = test_for_meta_redirections(r)
            if redirected:
                r = follow_redirections(s.get(url), s)
            return r
        s = requests.session()
        r = s.get(DocURL)
        # test for and follow meta redirects
        r = follow_redirections(r, s)
        '''
        '''
        bs4でメタタグ追跡ボツ
from bs4 import BeautifulSoup
        def meta_redirect(DocURL):
            response = request.get_data(DocURL)
            soup  = BeautifulSoup(response)

            result=soup.find("meta",attrs={"http-equiv":"Refresh"})
            if result:
                wait,text=result["content"].split(";")
                if text.strip().lower().startswith("url="):
                    url=text.strip()[4:]
                    return url
            return result
        print(DocURL)
        redirected_url = meta_redirect(DocURL)
        print(redirected_url)        
        '''

        '''
        HTMLヘッダを利用したリダイレクトと思って作ったボツ
        import sys
        import urllib.request
        def get_redirect_url(DocURL):
            with urllib.request.urlopen(DocURL) as res:
                url = res.geturl() # 最終的な URL を取得
                if DocURL == url:
                    return None # 指定された URL と同じなのでリダイレクトしていない
                else:
                    return url # 指定された URL と異なるのでリダイレクトしている
        redirect_url = get_redirect_url(DocURL)
        print(DocURL)
        print(redirect_url)
        '''
    else:
        DocNo = "none"
    button = "on"
    print(DocURL)
    return render_template('index.html', DocNo=DocNo, DocURL=DocURL, button=button) 


if __name__ == "__main__":
    app.run(port=8000, debug=True)