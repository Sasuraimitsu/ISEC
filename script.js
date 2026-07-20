/* =========================================================
   伊勢志摩水産物輸出促進協議会 LP script.js（日英切替対応版）
   ---------------------------------------------------------
   ★ 最初にここだけ設定 ★ Gmail作成後にアドレスを書き換え
   ========================================================= */
const CONTACT_EMAIL = "iseshima.suisan.export@gmail.com"; // ← 変更してください

/* =========================================================
   多言語辞書
   ・HTML側の data-i18n（テキスト）/ data-i18n-html（<br>等を含む）
     / data-i18n-ph（placeholder）/ data-i18n-content（meta）に対応。
   ・日本語はHTMLに直書きされているため、辞書はENのみ持ち、
     JA復帰時はページ読込時に退避した原文へ戻します。
   ========================================================= */
const I18N_EN = {
  "meta.title": "Iseshima Seafood Export Council | From Japan's sacred larder to the world.",
  "meta.desc": "Fishermen, wholesalers, processors and exporters of Ise-Shima, Japan, working as one council to deliver Shima's seafood to Hanoi, Vietnam.",

  "brand.name": "Iseshima Seafood Export Council",
  "brand.sub": "伊勢志摩水産物輸出促進協議会",

  "nav.about": "About",
  "nav.products": "Our Seafood",
  "nav.route": "Shima to Hanoi",
  "nav.members": "Members",
  "nav.news": "News",
  "nav.contact": "Contact",

  "hero.eyebrow": "Shima, Mie Prefecture — from the ports of Shijima, Anori and Ugata",
  "hero.title": "Iseshima Seafood<br>Export Council",
  "hero.lead": "Fishermen, wholesalers, freezing &amp; processing, seaweed, and export trade.<br>Five partners of the Ise-Shima sea working as one,<br>bringing the pride of the day's catch to tables across the sea.",
  "hero.cta1": "See the route from Shima to Hanoi",
  "hero.cta2": "Talk to us about trade",
  "hero.cert.sqf": "SQF (GFSI-recognized)",
  "hero.tategaki": "From Japan's sacred larder, to the world.",

  "ports.caption": "Our home waters",
  "ports.p1": "Shijima",
  "ports.p1n": "Home port of fishing vessel Dai-ichi Kazumaru",
  "ports.p2": "Anori",
  "ports.p2n": "Wholesale and processing under one roof",
  "ports.p3": "Ugata",
  "ports.p3n": "Two certified plants: freezing and seaweed",

  "about.title": "Five partners, no rivalry —<br class=\"sp-only\">bound by one sea.",
  "about.lead": "The Iseshima Seafood Export Council was founded by five partners of Shima: <strong>fishermen, a wholesaler, a freezing &amp; processing plant, a seaweed house, and an export trading company</strong>. Because none of us competes on the same product, we cover the entire chain — catching, selecting, processing and delivering — as one. Two internationally certified plants (HACCP, SQF, JFS-B) and our own retail channels in Southeast Asia: we export the blessings of the Ise-Shima sea together with their freshness and trust.",
  "about.f1t": "Founded",
  "about.f1d": "July 2026",
  "about.f2t": "Head office",
  "about.f2d": "Anori, Ago-cho, Shima City, Mie, Japan",
  "about.f3t": "Members",
  "about.f3d": "4 companies + fishermen (Shima / Osaka)",
  "about.f4t": "First target market",
  "about.f4d": "Hanoi, Vietnam",

  "products.title": "Four blessings raised by the Shima sea.",
  "products.lead": "From filleting to prepared foods — small lots, wide variety, tailored to each restaurant's plate.",
  "products.c1t": "Fresh Fish",
  "products.c1d": "Seasonal fish caught by Shima's pole-and-line and longline fishermen. Selected on the day, by the eyes that know this sea best.",
  "products.c1tag": "F/V Dai-ichi Kazumaru and partner fishermen",
  "products.c2t": "Frozen & Processed",
  "products.c2d": "From fillets to prepared foods at a HACCP / SQF certified plant. Freshness sealed in, in formats ready for your kitchen.",
  "products.c2tag": "Iseshima Reito (Anori — on-site integrated processing)",
  "products.c3t": "Seaweed (Hijiki & Wakame)",
  "products.c3d": "Selection and sterilization refined over 150 years. From a JFS-B certified plant, the aroma of Ise-Shima's shores to the world.",
  "products.c3tag": "Kaneu Foods (Shijima / Ugata plant)",
  "products.c4t": "Oysters",
  "products.c4d": "Raised in the calm inlets of Ise-Shima, exemplified by Matoya Bay. Delivering the wisdom of aquaculture to the next market.",
  "products.c4tag": "In partnership with Shima's oyster farmers (expanding)",

  "route.title": "Morning at a Shima port. Tomorrow, a table in Hanoi.",
  "route.lead": "Collection, processing and freezing are completed on a single site; from our base minutes from Haneda Airport, Hanoi is about six hours by direct flight. A relay of freshness is the blueprint of this route.",
  "route.s1t": "Landing",
  "route.s1d": "The day's catch from the ports of Shijima and Anori.",
  "route.s2t": "Processing & Freezing",
  "route.s2d": "Same-day processing at a HACCP / SQF certified plant, right by the port.",
  "route.s3t": "Airfreight from Haneda",
  "route.s3d": "From our export base near the airport — about 6 hours by direct flight.",
  "route.s4t": "To tables in Hanoi",
  "route.s4d": "Our own local sales channels carry it to the very last plate.",

  "why.title": "Trust is built on paper and on the ground.",
  "why.s1t": "Two internationally certified plants",
  "why.s1d": "HACCP, SQF (GFSI-recognized) and JFS-B. We meet destination standards facility-first.",
  "why.s2t": "A supply chain on one site",
  "why.s2d": "The processing plant sits inside the wholesaler's premises. From collection to frozen storage with zero transfer — freshness protected.",
  "why.s3t": "Our own channels in Southeast Asia",
  "why.s3d": "Export experience to Vietnam and Cambodia, with our own local retail. We trade within earshot of the market.",
  "why.s4t": "Small lots, wide variety",
  "why.s4d": "Fillets or prepared foods — flexible supply matched to your menu.",

  "members.title": "The five partners",
  "members.m1r": "Chair / Wholesale",
  "members.m1n": "Shinsei Suisan Co., Ltd.",
  "members.m1d": "The discerning eye and trade network of Ise-Shima (Anori, Shima)",
  "members.m2r": "Vice-chair / Freezing & Processing",
  "members.m2n": "Iseshima Reito Co., Ltd.",
  "members.m2d": "HACCP / SQF certified plant; exports to Hong Kong and Taiwan",
  "members.m3r": "Vice-chair / Fisherman",
  "members.m3n": "Kazu Inoue (F/V Dai-ichi Kazumaru)",
  "members.m3d": "The Shijima sea and its network of fishermen",
  "members.m4r": "Vice-chair / Seaweed",
  "members.m4n": "Kaneu Foods Co., Ltd.",
  "members.m4d": "Founded 150 years ago; JFS-B certified plant (Shijima / Ugata)",
  "members.m5r": "Secretariat / Export",
  "members.m5n": "METIS Co., Ltd.",
  "members.m5d": "Exports to Vietnam & Cambodia; export base minutes from Haneda",
  "members.adv": "Adviser: Ayumu Katano (FISK JAPAN) / In cooperation with Mie Prefecture, Shima City and JETRO Mie",

  "news.title": "News",
  "news.tag1": "Notice",
  "news.tag2": "Business",
  "news.tag3": "Upcoming",
  "news.n1": "The Iseshima Seafood Export Council has been established.",
  "news.n2": "First shipment of Shima's used fishing vessels has departed (giving retired fishermen's boats a second life).",
  "news.n3": "Facility registration for Vietnam and international certification work begins.",

  "contact.title": "Trade, visits and media inquiries",
  "contact.lead": "Overseas buyers, restaurants and retailers, press and government — we would love to hear from you.",
  "form.name": "Your name",
  "form.req": "Required",
  "form.req2": "Required",
  "form.req3": "Required",
  "form.name.ph": "e.g. John Smith",
  "form.org": "Company / Organization",
  "form.org.ph": "e.g. Hanoi Fine Foods Co., Ltd.",
  "form.mail": "Your email",
  "form.mail.ph": "e.g. you@example.com",
  "form.body": "Your inquiry",
  "form.body.ph": "e.g. We are looking to source fresh fish and frozen fillets for Japanese restaurants in Hanoi.",
  "form.note": "Pressing the button opens your email app with the message pre-filled.",
  "form.submit": "Send us an email",
  "form.alt": "If your email app does not open, please write to us directly:",

  "footer.name": "Iseshima Seafood Export Council",
  "footer.sub": "伊勢志摩水産物輸出促進協議会",
  "footer.addr": "Anori, Ago-cho, Shima City, Mie, Japan (c/o Shinsei Suisan Co., Ltd.)",
};

/* ---------------------------------------------------------
   言語切替の実装
   ・読込時に日本語原文（HTML直書き）を退避 → JA復帰に使用
   ・選択言語は localStorage に保存（使えない環境でも動作）
--------------------------------------------------------- */
const LANG_KEY = "iseshima_lp_lang";
const jaStore = { text: new Map(), html: new Map(), ph: new Map(), content: new Map() };

// 原文退避
document.querySelectorAll("[data-i18n]").forEach((el) => jaStore.text.set(el, el.textContent));
document.querySelectorAll("[data-i18n-html]").forEach((el) => jaStore.html.set(el, el.innerHTML));
document.querySelectorAll("[data-i18n-ph]").forEach((el) => jaStore.ph.set(el, el.getAttribute("placeholder") || ""));
document.querySelectorAll("[data-i18n-content]").forEach((el) => jaStore.content.set(el, el.getAttribute("content") || ""));

let currentLang = "ja";

function applyLang(lang) {
  currentLang = lang === "en" ? "en" : "ja";
  document.documentElement.lang = currentLang;

  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    el.textContent = currentLang === "en" ? (I18N_EN[key] ?? jaStore.text.get(el)) : jaStore.text.get(el);
  });
  document.querySelectorAll("[data-i18n-html]").forEach((el) => {
    const key = el.getAttribute("data-i18n-html");
    el.innerHTML = currentLang === "en" ? (I18N_EN[key] ?? jaStore.html.get(el)) : jaStore.html.get(el);
  });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
    const key = el.getAttribute("data-i18n-ph");
    el.setAttribute("placeholder", currentLang === "en" ? (I18N_EN[key] ?? jaStore.ph.get(el)) : jaStore.ph.get(el));
  });
  document.querySelectorAll("[data-i18n-content]").forEach((el) => {
    const key = el.getAttribute("data-i18n-content");
    el.setAttribute("content", currentLang === "en" ? (I18N_EN[key] ?? jaStore.content.get(el)) : jaStore.content.get(el));
  });

  // <title>（data-i18nを付けてあるが、明示的にも更新）
  document.title = currentLang === "en" ? I18N_EN["meta.title"] : jaStore.text.get(document.querySelector("title"));

  // 切替ボタンの表示状態
  document.querySelectorAll(".lang-opt").forEach((opt) => {
    opt.classList.toggle("is-current", opt.getAttribute("data-lang-opt") === currentLang);
  });

  // 選択を記憶（プライベートモード等で失敗しても無視）
  try { localStorage.setItem(LANG_KEY, currentLang); } catch (_) {}
}

// 初期言語：保存値 → ブラウザ言語 → 日本語
(function initLang() {
  let saved = null;
  try { saved = localStorage.getItem(LANG_KEY); } catch (_) {}
  const preferEn = (navigator.language || "").toLowerCase().startsWith("en");
  applyLang(saved || (preferEn ? "en" : "ja"));
})();

const langSwitch = document.getElementById("langSwitch");
if (langSwitch) {
  langSwitch.addEventListener("click", () => applyLang(currentLang === "ja" ? "en" : "ja"));
}

/* ---------------------------------------------------------
   ヘッダー：スクロールで背景切替
--------------------------------------------------------- */
const siteHeader = document.getElementById("siteHeader");
function updateHeader() {
  if (!siteHeader) return;
  siteHeader.classList.toggle("is-solid", window.scrollY > 40);
}
window.addEventListener("scroll", updateHeader, { passive: true });
updateHeader();

/* ---------------------------------------------------------
   モバイルナビ
--------------------------------------------------------- */
const navToggle = document.getElementById("navToggle");
const globalNav = document.getElementById("globalNav");
if (navToggle && globalNav) {
  navToggle.addEventListener("click", () => {
    const open = globalNav.classList.toggle("is-open");
    navToggle.classList.toggle("is-open", open);
    navToggle.setAttribute("aria-expanded", String(open));
  });
  globalNav.querySelectorAll("a").forEach((a) => {
    a.addEventListener("click", () => {
      globalNav.classList.remove("is-open");
      navToggle.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

/* ---------------------------------------------------------
   スクロール出現
--------------------------------------------------------- */
const revealTargets = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window && revealTargets.length > 0) {
  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -10% 0px", threshold: 0.1 }
  );
  revealTargets.forEach((el) => revealObserver.observe(el));
} else {
  revealTargets.forEach((el) => el.classList.add("is-visible"));
}

/* ---------------------------------------------------------
   航路ステップの点灯
--------------------------------------------------------- */
const routeSteps = document.querySelectorAll(".route-step");
if ("IntersectionObserver" in window && routeSteps.length > 0) {
  const stepObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        entry.target.classList.toggle("is-active", entry.isIntersecting);
      });
    },
    { rootMargin: "-30% 0px -30% 0px", threshold: 0 }
  );
  routeSteps.forEach((el) => stepObserver.observe(el));
}

/* ---------------------------------------------------------
   お問い合わせ（mailto方式）
   件名・本文は表示中の言語で組み立てます。
--------------------------------------------------------- */
const contactForm = document.getElementById("contactForm");

function buildMailto(name, org, email, body) {
  const en = currentLang === "en";
  const subject = en
    ? `[Inquiry] ${name} (${org || "Individual"})`
    : `【お問い合わせ】${name}様（${org || "個人"}）`;
  const lines = en
    ? [
        "To: Iseshima Seafood Export Council",
        "",
        `Name: ${name}`,
        `Company / Organization: ${org || "(not provided)"}`,
        `Email: ${email}`,
        "",
        "--- Inquiry ---",
        body,
        "",
        "* Composed from the website contact form.",
      ]
    : [
        "伊勢志摩水産物輸出促進協議会 御中",
        "",
        `お名前：${name}`,
        `会社名・団体名：${org || "（未記入）"}`,
        `ご連絡先メール：${email}`,
        "",
        "── ご相談内容 ──",
        body,
        "",
        "※本メールはWebサイトのお問い合わせフォームから作成されました。",
      ];
  return (
    "mailto:" + encodeURIComponent(CONTACT_EMAIL) +
    "?subject=" + encodeURIComponent(subject) +
    "&body=" + encodeURIComponent(lines.join("\n"))
  );
}

if (contactForm) {
  contactForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const nameInput = document.getElementById("cfName");
    const orgInput  = document.getElementById("cfOrg");
    const mailInput = document.getElementById("cfMail");
    const bodyInput = document.getElementById("cfBody");
    const note      = document.getElementById("formNote");

    let hasError = false;
    [nameInput, mailInput, bodyInput].forEach((input) => {
      const empty = input.value.trim() === "";
      input.classList.toggle("is-error", empty);
      if (empty) hasError = true;
    });
    const mailValue = mailInput.value.trim();
    if (mailValue !== "" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mailValue)) {
      mailInput.classList.add("is-error");
      hasError = true;
    }

    if (hasError) {
      if (note) note.textContent = currentLang === "en"
        ? "Please check the highlighted fields (required / email format)."
        : "赤枠の項目をご確認ください（必須項目・メール形式）。";
      return;
    }
    if (note) note.textContent = currentLang === "en"
      ? "Opening your email app… (if nothing opens, use the address below)"
      : "メール作成画面を開いています…（開かない場合は下のアドレスへ直接ご連絡ください）";

    window.location.href = buildMailto(
      nameInput.value.trim(), orgInput.value.trim(), mailValue, bodyInput.value.trim()
    );
  });

  contactForm.querySelectorAll("input, textarea").forEach((input) => {
    input.addEventListener("input", () => input.classList.remove("is-error"));
  });
}

/* ---------------------------------------------------------
   フォールバックリンク＆年
--------------------------------------------------------- */
const mailFallback = document.getElementById("mailFallback");
if (mailFallback) {
  mailFallback.href = "mailto:" + CONTACT_EMAIL;
  mailFallback.textContent = CONTACT_EMAIL;
}
const yearEl = document.getElementById("year");
if (yearEl) yearEl.textContent = String(new Date().getFullYear());
