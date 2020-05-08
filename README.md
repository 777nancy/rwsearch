# rwsearch
<font color="Red">某検索サイト</font>の検索口数をGET！
## 特徴
seleniumを利用して、アカウントの`ログイン`と`検索`を行います

## install方法
```
pip install -e git+https://github.com/777nancy/rwsearch.git#egg=rwsearch
```

## 利用方法
```
rwsearch -u user_id -p password [-n NUM] [--chrome-driver CHROME_DRIVER] [--add-on ADD_ON] [--debug]
```
## 備考
```
-n, --num      : 検索回数(デフォルト: 30)
--chrome-driver: Chromeドライバー(デフォルト: Chrome81)
--add-on       : Chromeの.crx形式のアドオン用ファイル(デフォルト: 2020/05/08時点のファイル)
--debug        : デバッグモードの有無(デフォルト: False)
```