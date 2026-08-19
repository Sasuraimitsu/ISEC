【取り扱い海産物の追加・変更方法】

商品は data/products.json を編集するだけで追加・変更できます。
（index.html や script.js を触る必要はありません）

■ カテゴリ（categories）
  sengyo  … 生鮮
  ichiji  … 一次加工
  chori   … 調理加工品
  yoshoku … 養殖
  ※アイコンは icon で指定：fish（魚）／snow（冷凍）／pot（調理）／wave（海藻・養殖）

■ 商品（items）に1件追加する例
  {
    "category": "chori",
    "name_ja": "煮付け（レトルト）",
    "name_en": "Simmered Fish (Retort)",
    "desc_ja": "◯◯を使った調理済み商品。",
    "desc_en": "Ready-to-eat product made with ...",
    "member_ja": "◯◯株式会社",
    "member_en": "XX Co., Ltd.",
    "photo": "images/products/nitsuke.jpg"
  }

・photo は省略可（省略すると写真なしのカードになります）
・_en を省略すると英語表示でも日本語が使われます
・member_ja に担当会員を書いておくと、新会員の受け入れ時に
  取り扱い品目の重複を確認しやすくなります
・カンマの付け忘れに注意（最後の項目の後ろにはカンマを付けない）
