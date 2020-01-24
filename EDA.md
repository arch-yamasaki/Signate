# 概要

様々な解析やテクニックをまとめる。

## ラベルについて
1_overall	資料範囲全体
2_handwritten	くずし字の文字ライン
3_typography	くずし字以外の文字ライン
4_illustration	イラスト（写真含む）
5_stamp	印影（蔵書印等）
6_headline	見出し
7_caption	図表見出し
8_textline	6_headline, 7_caption 以外の文字ライン
9_table	表


## EDA

### 全体

- 仮説
  - 古典籍の下にある横の現代文字がFalseなため、近代の横文字の認識率めちゃくちゃ悪い。
  - 古典籍には評もあるがそれもFalse扱いなので、それも非常に良くない。
- 結論
  - 古典籍と近代モデルは別で学習させる。
- 考慮すべきこと
  - イラスト(4),印影(5)の学習数が減る。 
    - 一旦は無視で良さそう。
    - => 何かイラストのデータセットを追加したい。



### 各種

- 2,3 は明治以降のものにはない。
- 縦の数字が全然取れてない、なんでだ？
  - ![](images/2020-01-22-02-34-26.png)
  - 近代のやつが、古代として認識されてそう。(3_typoになってるので)

- 4ilust
  - 近代史では理科のイラスト多い
    - 電気回路  (検索：「電気回路　問題」)
    - グラフ
    - 白黒風景写真系も多め。
    - 数学のグラフとかも(test)
    - 気持ち悪い細胞とかアメーバとかも(test)

- 6_headline見出し
  - めちゃくちゃむずい。8との見分けつかなさすぎる。
  - 可能なのは、前半に数字出てくるものは多い。
  - 実際そこそこ取れてるから一旦ガン無視で
- 7_caption	図表見出し
  - 表の近くは図表
  - 表・図と下の文字があっても図表
  - 8_textlineの縦がたくさんあって、横長なのはcaptionとかにしていい。
- 8_textline
  - 全体的によく取れてる。

## 技術テクニック

### Driveにデータをダウンロードする。

- WHAT: Google Driveのデータをmountするのでなく、contentにダウンロードする。
- WHY:
  - Google DriveのマウントはIOに二条に時間がかかりストレス。
  - その他ファイルストレージは料金結構かかったり、ファイルをDrive内で一元管理できずめんどくさい。
  - zipをcontentにダウンロードして、unzipするのが最速。
- HOW:
  - 1. datasetをzip化してGoogle Driveに。
  - 2. 対象データを共有設定で公開かつIDを取得する。
  - 3. 以下のコマンドでwgetする。 [参考URL](https://medium.com/@acpanjan/download-google-drive-files-using-wget-3c2c025a8b99)
  - 4. 
```sh
# /content/devide_dataset.zip にデータをダウンロードする。
# <FILEID> : 1CgrE1TL_-9G6qoKjk9HU0gC-fd-y9ihl など
# <FILENAME> : /content/devide_dataset.zip
!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=<FILEID>' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=<FILEID>" -O <FILENAME> && rm -rf /tmp/cookies.txt

# データをunzipする。-dは展開dirを指定。 '/content/devide_dataset'ができる。
!unzip -q <FILENAME> -d /content

```