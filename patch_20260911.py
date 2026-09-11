# -*- coding: utf-8 -*-
"""
ISEC サイト更新パッチ（2026-09-11）
  ① グローバルナビを1段表示に（字間・余白を詰め、折返し禁止。1180px以下はドロワー化）
  ② Track Record：「研修・交流に参加した人」→「海を越えた人」（1名）
  ③ 輸出実績の一覧を追加（data/exports.json を単一情報源に。月別グラフ・累計kgも自動集計）
  ④ あゆみ：8月の到着予定 → 8月到着・9/6現場到着・9/7操縦指導開始（実績）
  ⑤ README を新しいデータ構成に合わせて更新
対象：/home/claude/isec/repo（sasuraimitsu/ISEC のクローン）
"""
import json, os, re, sys

REPO = "/home/claude/isec/repo"

def rd(p):
    with open(os.path.join(REPO, p), encoding="utf-8") as f:
        return f.read()

def wr(p, s):
    with open(os.path.join(REPO, p), "w", encoding="utf-8") as f:
        f.write(s)

def rep(s, old, new, label, count=1):
    n = s.count(old)
    assert n == count, f"[{label}] 置換対象が {n} 箇所（期待 {count}）"
    return s.replace(old, new)

# =========================================================
# ① style.css：ナビ1段表示
# =========================================================
css = rd("style.css")

css = rep(css,
"""  display: flex; align-items: center; gap: 28px;
}
.brand { display: flex; align-items: center; gap: 12px; color: inherit; }""",
"""  display: flex; align-items: center; gap: 20px;
}
.brand { display: flex; align-items: center; gap: 12px; color: inherit; flex: 0 0 auto; }""",
"header-inner gap")

css = rep(css,
""".brand-name { font-family: var(--font-display); font-weight: 600; font-size: 15px; letter-spacing: .06em; }""",
""".brand-name { font-family: var(--font-display); font-weight: 600; font-size: 15px; letter-spacing: .06em; white-space: nowrap; }""",
"brand-name nowrap")

css = rep(css,
""".global-nav { margin-left: auto; }
.global-nav ul { display: flex; gap: 26px; }
.global-nav a { color: inherit; font-size: 13.5px; letter-spacing: .08em; position: relative; padding-block: 6px; }""",
"""/* PCナビ：必ず1段に収める（折返し禁止・字間と余白を詰める）。
   収まらない幅（1180px以下）はドロワー表示に切り替える（下のメディアクエリ） */
.global-nav { margin-left: auto; flex: 0 0 auto; }
.global-nav ul { display: flex; flex-wrap: nowrap; gap: clamp(14px, 1.4vw, 20px); }
.global-nav li { flex: 0 0 auto; }
.global-nav a { color: inherit; font-size: 13px; letter-spacing: .04em; white-space: nowrap; position: relative; padding-block: 6px; }""",
"global-nav base")

css = rep(css,
""".header-cta {
  flex: 0 0 auto;
  padding: 10px 20px; border-radius: 999px;
  background: var(--net-gold); color: #fff !important;
  font-size: 13.5px; letter-spacing: .1em; font-weight: 700;""",
""".header-cta {
  flex: 0 0 auto; white-space: nowrap;
  padding: 10px 18px; border-radius: 999px;
  background: var(--net-gold); color: #fff !important;
  font-size: 13px; letter-spacing: .08em; font-weight: 700;""",
"header-cta")

# 旧：768px以下のみドロワー → 新：1180px以下でドロワー（CTAは768px以下で非表示のまま）
css = rep(css,
"""@media (max-width: 768px) {
  .sp-only { display: inline; }

  /* SPナビ：ドロワー化 */
  .global-nav {
    position: fixed; inset: var(--header-h) 0 auto 0;
    background: rgba(13,29,46,.97);
    padding: 12px 24px 28px;
    transform: translateY(-130%);
    transition: transform .35s ease;
  }
  .site-header.is-solid .global-nav { background: rgba(245,247,244,.98); }
  .global-nav.is-open { transform: translateY(0); }
  .global-nav ul { flex-direction: column; gap: 0; }
  .global-nav a { display: block; padding: 14px 4px; font-size: 15px; border-bottom: 1px solid rgba(143,182,196,.25); }
  .header-cta { display: none; }
  .nav-toggle { display: flex; }
""",
"""/* タブレット〜小型PC：ナビが1段に収まらない幅はドロワー化（CTA・言語切替はヘッダーに残す） */
@media (max-width: 1180px) {
  .global-nav {
    position: fixed; inset: var(--header-h) 0 auto 0;
    background: rgba(13,29,46,.97);
    padding: 12px 24px 28px;
    transform: translateY(-130%);
    transition: transform .35s ease;
  }
  .site-header.is-solid .global-nav { background: rgba(245,247,244,.98); }
  .global-nav.is-open { transform: translateY(0); }
  .global-nav ul { flex-direction: column; gap: 0; }
  .global-nav li { flex: none; }
  .global-nav a { display: block; padding: 14px 4px; font-size: 15px; white-space: normal; border-bottom: 1px solid rgba(143,182,196,.25); }
  .lang-switch { margin-left: auto; margin-right: 4px; }
  .nav-toggle { display: flex; margin-left: 0; }
}

@media (max-width: 768px) {
  .sp-only { display: inline; }
  .header-cta { display: none; }
  /* SPのブランド表示：横幅に合わせて2行まで折返し可（英語表記は省略） */
  .brand { flex: 1 1 auto; min-width: 0; }
  .brand-text { min-width: 0; }
  .brand-name { font-size: 13px; letter-spacing: .03em; line-height: 1.3; white-space: normal; }
  .brand-en { display: none; }
  .lang-switch { padding: 6px 10px; }
""",
"drawer breakpoint")

css = rep(css,
""".lang-switch {
  flex: 0 0 auto;
  display: flex; align-items: center; gap: 6px;
  background: none; border: 1px solid currentColor; border-radius: 999px;
  color: inherit; cursor: pointer;
  padding: 7px 14px;""",
""".lang-switch {
  flex: 0 0 auto; white-space: nowrap;
  display: flex; align-items: center; gap: 6px;
  background: none; border: 1px solid currentColor; border-radius: 999px;
  color: inherit; cursor: pointer;
  padding: 7px 12px;""",
"lang-switch")

css = rep(css,
"""html[lang="en"] .global-nav a { letter-spacing: .06em; }""",
"""html[lang="en"] .global-nav a { letter-spacing: .05em; }""",
"en nav letter-spacing")

# 旧768pxブロック内に残っていた lang-switch / nav-toggle の位置指定は 1180px ブロックへ移したので削除
css = rep(css,
"""/* SPナビ内での言語ボタン位置（ヘッダー右に残す） */
@media (max-width: 768px) {
  .lang-switch { margin-left: auto; margin-right: 4px; }
  .nav-toggle { margin-left: 0; }
}
""",
"",
"old lang-switch sp block")

# ③ 輸出実績テーブルのスタイル（Track Record の直後に追加）
css = rep(css,
""".record-pending .record-num { font-size: 20px; color: var(--ink-weak); }""",
""".record-pending .record-num { font-size: 20px; color: var(--ink-weak); }

/* ---------- 輸出実績（一覧：data/exports.json） ---------- */
.export-block { margin-bottom: 40px; }
.export-title {
  font-family: var(--font-display); font-size: 20px; font-weight: 700;
  color: var(--sea-deep); letter-spacing: .06em; margin: 0 0 14px; line-height: 1.5;
}
.export-table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.export-table { width: 100%; border-collapse: collapse; font-size: 13.5px; line-height: 1.7; color: var(--ink); }
.export-table th, .export-table td {
  padding: 12px 10px; text-align: left; vertical-align: top;
  border-bottom: 1px solid rgba(18,38,58,.14);
}
.export-table th {
  font-size: 12px; font-weight: 700; letter-spacing: .08em; color: var(--ink-weak);
  border-bottom-color: rgba(18,38,58,.3); white-space: nowrap;
}
.export-table td.is-date { white-space: nowrap; color: #a4762a; font-weight: 700; letter-spacing: .04em; font-size: 12.5px; }
.export-table th.is-kg, .export-table td.is-kg { text-align: right; white-space: nowrap; }
.export-table td.is-kg { font-family: var(--font-display); font-weight: 700; font-size: 18px; color: var(--sea-deep); line-height: 1.3; }
.export-table td.is-kg small { font-family: var(--font-body); font-weight: 400; font-size: 12px; color: var(--ink-weak); margin-left: 3px; }
.export-note { display: block; font-size: 12px; color: var(--ink-weak); margin-top: 2px; }
.export-table tfoot td { border-bottom: 0; border-top: 1px solid rgba(18,38,58,.3); font-weight: 700; }
@media (max-width: 640px) {
  .export-table { font-size: 13px; }
  .export-table th, .export-table td { padding: 10px 8px; }
  .export-table .is-port { display: none; }
  .export-table td.is-kg { font-size: 16px; }
}""",
"export table css")

wr("style.css", css)
print("style.css ok")

# =========================================================
# ③ index.html：輸出実績ブロックを追加（4指標の下・月別グラフの上）
# =========================================================
html = rd("index.html")
html = rep(html,
"""    <!-- 4指標（data/record.json）。水産物kgは data/volume.json の累計を自動反映 -->
    <dl class="record-grid reveal" id="recordGrid"></dl>
    <div class="volume-wrap reveal" id="volumeWrap" hidden>""",
"""    <!-- 4指標（data/record.json）。水産物kgは data/exports.json の累計を自動反映 -->
    <dl class="record-grid reveal" id="recordGrid"></dl>
    <!-- 輸出実績（data/exports.json）。1件でも登録があれば表示。月別グラフも同じファイルから自動集計 -->
    <div class="export-block reveal" id="exportBlock" hidden>
      <h3 class="export-title" data-i18n="exports.title">輸出実績</h3>
      <div class="export-table-wrap">
        <table class="export-table" id="exportTable"></table>
      </div>
    </div>
    <div class="volume-wrap reveal" id="volumeWrap" hidden>""",
"export block html")
wr("index.html", html)
print("index.html ok")

# =========================================================
# ③ script.js：exports.json を単一情報源に（一覧・月別集計・累計）
# =========================================================
js = rd("script.js")

js = rep(js,
"""let volumeData = null;    // 月別取扱量（data/volume.json）
let recordData = null;    // 4指標（data/record.json）
let historyData = [];     // あゆみ（data/history.json）   // 取り扱い海産物（data/products.json）""",
"""let exportsData = null;   // 輸出実績（data/exports.json）… 一覧・月別グラフ・累計kgの単一情報源
let recordData = null;    // 4指標（data/record.json）
let historyData = [];     // あゆみ（data/history.json）
// productData … 取り扱い海産物（data/products.json）""",
"js vars")

js = rep(js,
"""  "volume.title": "What Has Crossed the Sea",
  "volume.lead": "A record of the fish, vessels and people that have travelled from Shima's ports across the sea. Figures are provisional.",
""",
"""  "volume.title": "What Has Crossed the Sea",
  "volume.lead": "A record of the fish, vessels and people that have travelled from Shima's ports across the sea. Figures are provisional.",
  "exports.title": "Export record",
""",
"i18n exports")

js = rep(js,
"""   data/record.json の items を描画。key が "seafood_kg" の項目は
   data/volume.json の累計kgで値を上書きする（二重管理を防ぐ）。""",
"""   data/record.json の items を描画。key が "seafood_kg" の項目は
   data/exports.json の累計kgで値を上書きする（二重管理を防ぐ）。""",
"record comment")

old_volume_head = """/* ---------------------------------------------------------
   月別の取扱量：SVG棒グラフ
   ---------------------------------------------------------
   数値の追加・修正は data/volume.json を編集するだけです。
--------------------------------------------------------- */
function renderVolume() {
  const sec = document.getElementById("volume");
  const box = document.getElementById("volumeChart");
  if (!sec || !box) return;
  const months = (volumeData && Array.isArray(volumeData.months)) ? volumeData.months : [];
  const valid = months.filter((m) => Number(m.kg) > 0);
  renderRecord(months);
  // 月別グラフは、実績が2か月分以上そろってから表示（1本だけの棒は見せない）
  const wrap = document.getElementById("volumeWrap");
  if (wrap) wrap.hidden = valid.length < 2;
  if (valid.length < 2) return;

  const unit = currentLang === "en" ? (volumeData.unit_en || "kg") : (volumeData.unit_ja || "kg");"""

new_volume_head = """/* ---------------------------------------------------------
   輸出実績（data/exports.json）
   ---------------------------------------------------------
   1件 = 1回の輸出。追加は data/exports.json の items に1ブロック足すだけ。
     date  … "YYYY-MM-DD"（半角）。この形式でない行は無視される（空行対策）
     kg    … 数値。0 や未記入は「—」表示で、累計には入らない
   一覧テーブル・月別グラフ・「海を越えた水産物」の累計kgは
   すべてこのファイルから自動集計する（volume.json は廃止）。
--------------------------------------------------------- */
const EN_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// 有効な行だけを新しい順で返す
function exportItems() {
  const raw = (exportsData && Array.isArray(exportsData.items)) ? exportsData.items : [];
  return raw
    .filter((it) => it && typeof it.date === "string" && /^\\d{4}-\\d{2}-\\d{2}$/.test(it.date))
    .slice()
    .sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
}

// "2026-07-28" → JA "2026.07.28" / EN "28 Jul 2026"
function fmtExportDate(iso) {
  const [y, m, d] = iso.split("-");
  return currentLang === "en"
    ? Number(d) + " " + EN_MONTHS[Number(m) - 1] + " " + y
    : y + "." + m + "." + d;
}

// exports.json → 月別集計（最初の月〜最後の月を欠けなく並べる。輸出0の月は kg:0）
function monthsFromExports(items) {
  if (!items.length) return [];
  const map = new Map();
  items.forEach((it) => {
    const key = it.date.slice(0, 7);
    map.set(key, (map.get(key) || 0) + (Number(it.kg) || 0));
  });
  const keys = [...map.keys()].sort();
  const [y0, m0] = keys[0].split("-").map(Number);
  const [y1, m1] = keys[keys.length - 1].split("-").map(Number);
  const multiYear = y0 !== y1;
  const out = [];
  for (let y = y0, m = m0; y < y1 || (y === y1 && m <= m1); ) {
    const key = y + "-" + String(m).padStart(2, "0");
    out.push({
      month: key,
      label_ja: (multiYear ? y + "年" : "") + m + "月",
      label_en: EN_MONTHS[m - 1] + (multiYear ? " " + String(y).slice(2) : ""),
      kg: map.get(key) || 0,
    });
    m += 1; if (m > 12) { m = 1; y += 1; }
  }
  return out;
}

// 一覧テーブル
function renderExports(items) {
  const block = document.getElementById("exportBlock");
  const table = document.getElementById("exportTable");
  if (!block || !table) return;
  const list = items || exportItems();
  if (!list.length) { block.hidden = true; table.innerHTML = ""; return; }
  block.hidden = false;
  const en = currentLang === "en";
  const ed = exportsData || {};
  const unit = en ? (ed.unit_en || "kg") : (ed.unit_ja || "kg");
  const H = en
    ? { date: "Date", items: "Products", port: "From", dest: "To", kg: "Volume", total: "Total" }
    : { date: "日付", items: "品目", port: "出荷元", dest: "輸出先", kg: "数量", total: "累計" };
  const rows = list.map((it) => {
    const kg = Number(it.kg) || 0;
    const prod = en ? (it.items_en || it.items_ja) : it.items_ja;
    const port = en ? (it.port_en || it.port_ja) : it.port_ja;
    const dest = en ? (it.dest_en || it.dest_ja) : it.dest_ja;
    const note = en ? (it.note_en || it.note_ja) : it.note_ja;
    return "<tr>" +
      '<td class="is-date">' + esc(fmtExportDate(it.date)) + "</td>" +
      "<td>" + esc(prod || "") + (note ? '<span class="export-note">' + esc(note) + "</span>" : "") + "</td>" +
      '<td class="is-port">' + esc(port || "") + "</td>" +
      "<td>" + esc(dest || "") + "</td>" +
      '<td class="is-kg">' + (kg > 0 ? kg.toLocaleString() + "<small>" + esc(unit) + "</small>" : "—") + "</td>" +
      "</tr>";
  }).join("");
  const total = list.reduce((a, it) => a + (Number(it.kg) || 0), 0);
  table.innerHTML =
    "<thead><tr>" +
    "<th>" + H.date + "</th><th>" + H.items + "</th>" +
    '<th class="is-port">' + H.port + "</th><th>" + H.dest + "</th>" +
    '<th class="is-kg">' + H.kg + "</th>" +
    "</tr></thead><tbody>" + rows + "</tbody>" +
    '<tfoot><tr><td colspan="4">' + H.total + "</td>" +
    '<td class="is-kg">' + total.toLocaleString() + "<small>" + esc(unit) + "</small></td></tr></tfoot>";
}

/* ---------------------------------------------------------
   月別の取扱量：SVG棒グラフ（exports.json から自動集計）
--------------------------------------------------------- */
function renderVolume() {
  const sec = document.getElementById("volume");
  const box = document.getElementById("volumeChart");
  if (!sec || !box) return;
  const items = exportItems();
  const months = monthsFromExports(items);
  renderRecord(months);
  renderExports(items);
  const ed = exportsData || {};
  const nbox = document.getElementById("volumeNote");
  if (nbox) nbox.textContent = items.length ? (currentLang === "en" ? (ed.note_en || "") : (ed.note_ja || "")) : "";
  // 月別グラフは、実績が2か月分以上そろってから表示（1本だけの棒は見せない）
  const valid = months.filter((m) => Number(m.kg) > 0);
  const wrap = document.getElementById("volumeWrap");
  if (wrap) wrap.hidden = valid.length < 2;
  if (valid.length < 2) { box.innerHTML = ""; return; }

  const unit = currentLang === "en" ? (ed.unit_en || "kg") : (ed.unit_ja || "kg");"""
js = rep(js, old_volume_head, new_volume_head, "renderVolume head")

js = rep(js,
"""  const nbox = document.getElementById("volumeNote");
  if (nbox) nbox.textContent = currentLang === "en" ? (volumeData.note_en || "") : (volumeData.note_ja || "");
}""",
"""}""",
"renderVolume tail note")

js = rep(js,
"""  const [news, docs, products, volume, history, record] = await Promise.all([
    loadJson("data/news.json"),
    loadJson("data/documents.json"),
    loadJson("data/products.json"),
    loadJson("data/volume.json"),
    loadJson("data/history.json"),
    loadJson("data/record.json"),
  ]);""",
"""  const [news, docs, products, exportsJson, history, record] = await Promise.all([
    loadJson("data/news.json"),
    loadJson("data/documents.json"),
    loadJson("data/products.json"),
    loadJson("data/exports.json"),
    loadJson("data/history.json"),
    loadJson("data/record.json"),
  ]);""",
"init load")

js = rep(js,
"""  if (volume && Array.isArray(volume.months)) volumeData = volume;""",
"""  if (exportsJson && Array.isArray(exportsJson.items)) exportsData = exportsJson;""",
"init assign")

assert "volumeData" not in js, "volumeData の参照が残っています"
wr("script.js", js)
print("script.js ok")

# =========================================================
# ③ data/exports.json 新規（volume.json は廃止）
# =========================================================
exports = {
  "_readme": "輸出実績。items に1件ずつ追加（新旧の順序は自由・表示は date の新しい順に自動整列）。date は YYYY-MM-DD、kg は数値。月別グラフと「海を越えた水産物」の累計kgはこのファイルから自動集計されます。",
  "unit_ja": "kg",
  "unit_en": "kg",
  "note_ja": "※ 協議会を通じて輸出した水産物の数量です。速報値のため、確定後に修正する場合があります。",
  "note_en": "* Volume of seafood exported through the council. Figures are provisional and may be revised.",
  "items": [
    {
      "date": "2026-07-28",
      "items_ja": "安乗鯖・安乗鯵",
      "items_en": "Anori mackerel and Anori horse mackerel",
      "port_ja": "安乗漁港（志摩市）",
      "port_en": "Anori Port, Shima",
      "dest_ja": "カンボジア",
      "dest_en": "Cambodia",
      "kg": 7,
      "note_ja": "協議会として初めての輸出（設立から4日）",
      "note_en": "The council's first export, four days after founding"
    }
  ]
}
wr("data/exports.json", json.dumps(exports, ensure_ascii=False, indent=2) + "\n")
vol = os.path.join(REPO, "data/volume.json")
if os.path.exists(vol):
    os.remove(vol)
print("data/exports.json ok（volume.json 削除）")

# =========================================================
# ② data/record.json：「海を越えた人」
# =========================================================
record = json.loads(rd("data/record.json"))
record["_readme"] = "4指標。seafood_kg は exports.json の累計で自動計算されるので value は無視されます。value が 0 の項目は「準備中」と表示されます。people（海を越えた人）は現地で指導・研修・交流を行った延べ人数を手で更新してください。"
found = False
for it in record["items"]:
    if it["key"] == "trainees":
        it.update({
            "key": "people",
            "label_ja": "海を越えた人",
            "label_en": "People who crossed the sea",
            "unit_ja": "人",
            "unit_en": "",
            "value": 1,
        })
        found = True
assert found, "record.json に trainees が見つかりません"
wr("data/record.json", json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print("data/record.json ok")

# =========================================================
# ④ data/history.json：到着予定 → 実績3件
# =========================================================
hist = json.loads(rd("data/history.json"))
before = len(hist)
hist = [h for h in hist if not h.get("upcoming")]
assert len(hist) == before - 1, "upcoming の項目が1件ではありません"
hist += [
  {
    "date_ja": "令和8年8月",
    "date_en": "August 2026",
    "title_ja": "第1船がカンボジアの港に到着、通関",
    "title_en": "First vessel reaches Cambodia and clears customs",
    "body_ja": "志摩からフラットラックで海上輸送した第1船がカンボジアの港に到着。通関を経て、受入先のコッコン州へ向かいました。",
    "body_en": "Shipped from Shima on a flat rack, the first vessel arrived at a Cambodian port, cleared customs and set off for Koh Kong Province."
  },
  {
    "date_ja": "令和8年9月6日",
    "date_en": "6 September 2026",
    "title_ja": "第1船がコッコン州の現場に到着、受入先の漁業組合と協議",
    "title_en": "First vessel arrives at the Koh Kong site; talks with the host fishing cooperative",
    "body_ja": "クレーンで着水し、現地の漁業組合と受入体制や現地のニーズについて協議しました。",
    "body_en": "The vessel was lowered into the water by crane, and we met the local fishing cooperative to discuss the handover and their needs."
  },
  {
    "date_ja": "令和8年9月7日",
    "date_en": "7 September 2026",
    "title_ja": "現地で始動 ― 志摩の漁師による操縦・整備の指導が始まる",
    "title_en": "Operations begin — a Shima fisherman starts hands-on training in vessel handling and maintenance",
    "body_ja": "井上副会長（第1和丸船長）が現地に渡り、漁船の操縦・整備・安全操業の手ほどきを開始。船に続いて「人」が海を越え、技の継承がここから始まります。",
    "body_en": "Vice-Chairman Inoue, captain of the Dai-ichi Kazu Maru, travelled to the site to begin hands-on instruction in vessel handling, maintenance and safe operation. After the boat, people are now crossing the sea — and the handover of skills begins here.",
    "milestone": True
  }
]
wr("data/history.json", json.dumps(hist, ensure_ascii=False, indent=2) + "\n")
print("data/history.json ok")

# =========================================================
# ⑤ README.md
# =========================================================
md = rd("README.md")
md = rep(md,
"""├── data/
│   ├── news.json         ★ お知らせのデータ（お知らせ更新はこのファイルだけ）
│   └── documents.json    ★ 事業計画・事業報告の一覧データ""",
"""├── data/
│   ├── news.json         ★ お知らせのデータ（お知らせ更新はこのファイルだけ）
│   ├── documents.json    ★ 事業計画・事業報告の一覧データ
│   ├── exports.json      ★ 輸出実績（一覧・月別グラフ・累計kg はここから自動集計）
│   ├── record.json       ★ 「海を越えたもの」の4指標（漁船・人・国の数）
│   ├── history.json      ★ あゆみ（沿革）
│   └── products.json     取り扱い海産物""",
"readme tree")

md = rep(md,
"""---

## 2. 事業計画・事業報告の追加方法""",
"""---

## 1-2. 輸出実績・指標・あゆみの更新方法

### 輸出実績（`data/exports.json`）
輸出が1回あるごとに `items` に1ブロック追加します（順番は自由。画面では日付の新しい順に並びます）。

```json
{
  "date": "2026-09-30",
  "items_ja": "安乗鯖",
  "items_en": "Anori mackerel",
  "port_ja": "安乗漁港（志摩市）",
  "port_en": "Anori Port, Shima",
  "dest_ja": "カンボジア",
  "dest_en": "Cambodia",
  "kg": 12,
  "note_ja": "",
  "note_en": ""
},
```

- `date` は **半角の YYYY-MM-DD**。この形式でない行は表示されません
- `kg` は数値（`"12"` のような文字列でも可）。0 や未記入は「—」表示になり累計に入りません
- 「海を越えた水産物 ○kg」の数字と月別グラフは、このファイルから自動で計算されます（グラフは実績が2か月分そろうと表示）
- `note_ja` は品目の下に小さく出る補足（空文字なら非表示）

### 4指標（`data/record.json`）
- `vessels`（漁船）・`people`（海を越えた人）・`countries`（国）の `value` を手で更新
- `seafood_kg` の `value` は無視されます（exports.json から自動計算）
- `value` が 0 の項目は「準備中」と表示されます

### あゆみ（`data/history.json`）
- 1件1ブロック。`"milestone": true` で金色の節目表示、`"upcoming": true` で「予定」表示
- 予定が実現したら `upcoming` の行を削除するだけで実績になります

---

## 2. 事業計画・事業報告の追加方法""",
"readme exports section")

md = rep(md,
"""- **問い合わせ先メールアドレス**：`script.js` の冒頭 `CONTACT_EMAIL` に設定。変更する場合はこの1行を書き換える""",
"""- **問い合わせ先メールアドレス**：`script.js` の冒頭 `CONTACT_EMAIL` に設定。変更する場合はこの1行を書き換える
- **PCメニューの表示**：ナビは1段固定。幅 1180px 以下ではハンバーガー（ドロワー）表示に切り替わる。項目を増やして収まらなくなったら `style.css` の `.global-nav ul { gap }` か `@media (max-width: 1180px)` の数値を調整""",
"readme nav note")
wr("README.md", md)
print("README.md ok")
print("ALL OK")
