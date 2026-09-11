# -*- coding: utf-8 -*-
"""
ISEC サイト追加パッチ（2026-09-11 その2）
  輸出実績を「1か月＝1行」に変更（入力も表示も月単位）
    data/exports.json … items(date) → months(month "YYYY-MM")
    script.js         … 月単位の集計・表示。同じ月を2回書いても合算して1行にまとめる
    index.html / README.md … 説明を月単位に
前提：patch_20260911.py 適用済みの /home/claude/isec/repo
"""
import json, os

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
# script.js
# =========================================================
js = rd("script.js")

# 冒頭の変数コメント
js = rep(js,
"""let exportsData = null;   // 輸出実績（data/exports.json）… 一覧・月別グラフ・累計kgの単一情報源""",
"""let exportsData = null;   // 輸出実績（data/exports.json、1か月＝1行）… 一覧・月別グラフ・累計kgの単一情報源""",
"js var comment")

# 輸出実績ブロック（前パッチで入れたもの）をまるごと月単位版に差し替え
start = js.index("/* ---------------------------------------------------------\n   輸出実績（data/exports.json）")
end_marker = """/* ---------------------------------------------------------
   月別の取扱量：SVG棒グラフ（exports.json から自動集計）
--------------------------------------------------------- */"""
end = js.index(end_marker)
new_block = '''/* ---------------------------------------------------------
   輸出実績（data/exports.json）… 1か月 ＝ 1行
   ---------------------------------------------------------
   月ごとに months に1ブロック足すだけ。
     month … "YYYY-MM"（半角・月は2桁）。この形式でない行は無視される（空行対策）
     kg    … その月の合計数量（数値）。0 や未記入は「—」表示で累計に入らない
   一覧テーブル・月別グラフ・「海を越えた水産物」の累計kgは
   すべてこのファイルから自動集計する。
   同じ月を2回書いてしまった場合は kg を合算し、品目などは「・」でつないで1行にまとめる。
--------------------------------------------------------- */
const EN_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const EXPORT_TEXT_KEYS = ["items_ja", "items_en", "port_ja", "port_en", "dest_ja", "dest_en", "note_ja", "note_en"];

// 有効な月だけを（同じ月は合算して）新しい順で返す
function exportMonths() {
  const raw = (exportsData && Array.isArray(exportsData.months)) ? exportsData.months : [];
  const map = new Map();
  raw.forEach((it) => {
    if (!it || typeof it.month !== "string" || !/^\\d{4}-(0[1-9]|1[0-2])$/.test(it.month)) return;
    if (!map.has(it.month)) map.set(it.month, { month: it.month, kg: 0, texts: {} });
    const row = map.get(it.month);
    row.kg += Number(it.kg) || 0;
    EXPORT_TEXT_KEYS.forEach((k) => {
      const v = String(it[k] == null ? "" : it[k]).trim();
      if (!v) return;
      const list = row.texts[k] || (row.texts[k] = []);
      if (!list.includes(v)) list.push(v);
    });
  });
  return [...map.values()]
    .map((row) => {
      const out = { month: row.month, kg: row.kg };
      EXPORT_TEXT_KEYS.forEach((k) => { out[k] = (row.texts[k] || []).join(k.endsWith("_en") ? ", " : "・"); });
      return out;
    })
    .sort((a, b) => (a.month < b.month ? 1 : a.month > b.month ? -1 : 0));
}

// "2026-07" → JA "2026年7月" / EN "Jul 2026"
function fmtExportMonth(ym) {
  const y = ym.slice(0, 4), m = Number(ym.slice(5, 7));
  return currentLang === "en" ? EN_MONTHS[m - 1] + " " + y : y + "年" + m + "月";
}

// グラフ用：最初の月〜最後の月を欠けなく並べる（輸出0の月は kg:0）
function chartMonths(rows) {
  if (!rows.length) return [];
  const kgOf = new Map(rows.map((r) => [r.month, r.kg]));
  const keys = rows.map((r) => r.month).sort();
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
      kg: kgOf.get(key) || 0,
    });
    m += 1; if (m > 12) { m = 1; y += 1; }
  }
  return out;
}

// 一覧テーブル（月ごと1行）
function renderExports(rows) {
  const block = document.getElementById("exportBlock");
  const table = document.getElementById("exportTable");
  if (!block || !table) return;
  const list = rows || exportMonths();
  if (!list.length) { block.hidden = true; table.innerHTML = ""; return; }
  block.hidden = false;
  const en = currentLang === "en";
  const ed = exportsData || {};
  const unit = en ? (ed.unit_en || "kg") : (ed.unit_ja || "kg");
  const pick = (r, k) => (en ? (r[k + "_en"] || r[k + "_ja"]) : r[k + "_ja"]) || "";
  const showPort = list.some((r) => pick(r, "port")); // 出荷元がどの月にも無ければ列ごと省略
  const H = en
    ? { month: "Month", items: "Products", port: "From", dest: "To", kg: "Volume", total: "Total" }
    : { month: "年月", items: "品目", port: "出荷元", dest: "輸出先", kg: "数量", total: "累計" };
  const body = list.map((r) => {
    const note = pick(r, "note");
    return "<tr>" +
      '<td class="is-date">' + esc(fmtExportMonth(r.month)) + "</td>" +
      "<td>" + esc(pick(r, "items")) + (note ? '<span class="export-note">' + esc(note) + "</span>" : "") + "</td>" +
      (showPort ? '<td class="is-port">' + esc(pick(r, "port")) + "</td>" : "") +
      "<td>" + esc(pick(r, "dest")) + "</td>" +
      '<td class="is-kg">' + (r.kg > 0 ? r.kg.toLocaleString() + "<small>" + esc(unit) + "</small>" : "—") + "</td>" +
      "</tr>";
  }).join("");
  const total = list.reduce((a, r) => a + r.kg, 0);
  table.innerHTML =
    "<thead><tr>" +
    "<th>" + H.month + "</th><th>" + H.items + "</th>" +
    (showPort ? '<th class="is-port">' + H.port + "</th>" : "") +
    "<th>" + H.dest + "</th>" +
    '<th class="is-kg">' + H.kg + "</th>" +
    "</tr></thead><tbody>" + body + "</tbody>" +
    '<tfoot><tr><td colspan="' + (showPort ? 4 : 3) + '">' + H.total + "</td>" +
    '<td class="is-kg">' + total.toLocaleString() + "<small>" + esc(unit) + "</small></td></tr></tfoot>";
}

'''
js = js[:start] + new_block + js[end:]

js = rep(js,
"""  const items = exportItems();
  const months = monthsFromExports(items);
  renderRecord(months);
  renderExports(items);
  const ed = exportsData || {};
  const nbox = document.getElementById("volumeNote");
  if (nbox) nbox.textContent = items.length ? (currentLang === "en" ? (ed.note_en || "") : (ed.note_ja || "")) : "";""",
"""  const rows = exportMonths();
  const months = chartMonths(rows);
  renderRecord(months);
  renderExports(rows);
  const ed = exportsData || {};
  const nbox = document.getElementById("volumeNote");
  if (nbox) nbox.textContent = rows.length ? (currentLang === "en" ? (ed.note_en || "") : (ed.note_ja || "")) : "";""",
"renderVolume body")

js = rep(js,
"""  if (exportsJson && Array.isArray(exportsJson.items)) exportsData = exportsJson;""",
"""  if (exportsJson && Array.isArray(exportsJson.months)) exportsData = exportsJson;""",
"init assign months")

for leftover in ("exportItems", "monthsFromExports", "fmtExportDate"):
    assert leftover not in js, f"{leftover} が残っています"
wr("script.js", js)
print("script.js ok")

# =========================================================
# data/exports.json（月単位）
# =========================================================
exports = {
  "_readme": "輸出実績（1か月＝1行）。months に月ごとに1ブロック追加。month は YYYY-MM（半角・月は2桁）、kg はその月の合計数量（数値）。一覧・月別グラフ・「海を越えた水産物」の累計kgはこのファイルから自動集計されます。",
  "unit_ja": "kg",
  "unit_en": "kg",
  "note_ja": "※ 協議会を通じて輸出した水産物の月別数量です。速報値のため、確定後に修正する場合があります。",
  "note_en": "* Monthly volume of seafood exported through the council. Figures are provisional and may be revised.",
  "months": [
    {
      "month": "2026-07",
      "items_ja": "安乗鯖・安乗鯵",
      "items_en": "Anori mackerel and Anori horse mackerel",
      "port_ja": "安乗漁港（志摩市）",
      "port_en": "Anori Port, Shima",
      "dest_ja": "カンボジア",
      "dest_en": "Cambodia",
      "kg": 7,
      "note_ja": "7月28日、協議会として初めての輸出",
      "note_en": "First export by the council, 28 July"
    }
  ]
}
wr("data/exports.json", json.dumps(exports, ensure_ascii=False, indent=2) + "\n")
print("data/exports.json ok")

# =========================================================
# index.html コメント
# =========================================================
html = rd("index.html")
html = rep(html,
"""    <!-- 輸出実績（data/exports.json）。1件でも登録があれば表示。月別グラフも同じファイルから自動集計 -->""",
"""    <!-- 輸出実績（data/exports.json、1か月＝1行）。1か月分でも登録があれば表示。月別グラフも同じファイルから自動集計 -->""",
"html comment")
wr("index.html", html)
print("index.html ok")

# =========================================================
# README.md
# =========================================================
md = rd("README.md")
start = md.index("### 輸出実績（`data/exports.json`）")
end = md.index("### 4指標（`data/record.json`）")
md = md[:start] + """### 輸出実績（`data/exports.json`）
**1か月＝1行**です。月末などに、その月の合計を `months` に1ブロック追加します（順番は自由。画面では新しい月が上に並びます）。

```json
{
  "month": "2026-09",
  "items_ja": "安乗鯖・安乗鯵",
  "items_en": "Anori mackerel and Anori horse mackerel",
  "port_ja": "安乗漁港（志摩市）",
  "port_en": "Anori Port, Shima",
  "dest_ja": "カンボジア",
  "dest_en": "Cambodia",
  "kg": 12,
  "note_ja": "",
  "note_en": ""
},
```

- `month` は **半角の YYYY-MM**（9月なら `2026-09`）。この形式でない行は表示されません
- `kg` はその月の合計数量（数値）。0 や未記入は「—」表示になり累計に入りません
- `items_ja` は月内に輸出した品目を「・」でつないで書く。`port_ja`（出荷元）はどの月にも書かなければ列ごと省略されます
- `note_ja` は品目の下に小さく出る補足（空文字なら非表示）。`_en` は省略すると英語画面でも日本語表示
- 同じ月を2回書いてしまっても、kg は合算・品目は「・」でつないで1行にまとまります
- 「海を越えた水産物 ○kg」の数字と月別グラフは、このファイルから自動で計算されます（グラフは2か月分の実績がそろうと表示）

""" + md[end:]
wr("README.md", md)
print("README.md ok")
print("ALL OK")
