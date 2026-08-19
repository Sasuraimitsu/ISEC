【お知らせ（活動報告）の追加方法】

data/news.json を編集するだけで追加できます。新しい記事は「一番上」に足してください。

■ 1件の書き方（すべての項目）
  {
    "date": "2026.08.19",              ← 画面に出る日付
    "datetime": "2026-08-19",          ← 内部用（ハイフン区切り）
    "tag_ja": "活動報告",               ← 左のラベル
    "tag_en": "Report",
    "title_ja": "見出しを書きます",      ← 省略可
    "title_en": "Headline in English",
    "body_ja": "本文を書きます。",
    "body_en": "Body text in English.",
    "photo": "images/news/2026-08_xxxx.jpg"   ← 省略可（サムネイル写真）
  }

■ 写真の入れ方
  1. 写真を横長（3:2程度）にして、ファイル名を半角英数にする
     例：2026-07_anori-saba.jpg
  2. GitHubの images/news フォルダにアップロード
     （フォルダが無い場合は「Add file → Create new file」で
      ファイル名欄に「images/news/.gitkeep」と入力して作成）
  3. news.json の "photo" にパスを書く
     例："photo": "images/news/2026-07_anori-saba.jpg"

  ※写真ファイルが無い場合、サムネイルは自動的に消えて
    文字だけの表示になります（レイアウトは崩れません）
  ※推奨：幅1200px程度・500KB以下

■ 注意
  ・_en を省略すると英語表示でも日本語が使われます
  ・カンマの付け忘れに注意（最後の項目の後ろにはカンマを付けない）
