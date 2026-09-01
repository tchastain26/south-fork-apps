// Finds every page that scrolls horizontally at 375px, works out which element
// is responsible, and injects a scoped media query so the wide content scrolls
// inside its own box instead of dragging the whole page sideways.
// Clipping with overflow:hidden is deliberately avoided: on a page like the
// periodic table it would make half the content unreachable.
const fs = require("fs"), path = require("path"), http = require("http");
const { chromium } = require("playwright");
const ROOT = process.cwd(), PORT = Number(process.env.PORT || 8813);
const APPLY = process.env.APPLY === "1";
const MARK_START = "/* SFA_MOBILE_FIX_START */", MARK_END = "/* SFA_MOBILE_FIX_END */";

const types = {".html":"text/html",".js":"text/javascript",".css":"text/css",".jpg":"image/jpeg",".png":"image/png",".svg":"image/svg+xml",".json":"application/json",".xml":"application/xml",".webmanifest":"application/manifest+json",".ico":"image/x-icon"};
const server = http.createServer((req,res)=>{
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, {"Content-Type": types[path.extname(f)] || "application/octet-stream"});
  fs.createReadStream(f).pipe(res);
});

function injectCss(file, css) {
  let s = fs.readFileSync(file, "utf8");
  const re = new RegExp(MARK_START.replace(/[.*+?^${}()|[\]\\]/g,"\\$&") + "[\\s\\S]*?" + MARK_END.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"), "g");
  s = s.replace(re, "");
  const block = `${MARK_START}\n@media (max-width: 640px){\n${css}\n}\n${MARK_END}`;
  const i = s.lastIndexOf("</style>");
  if (i === -1) return false;
  s = s.slice(0, i) + block + "\n" + s.slice(i);
  fs.writeFileSync(file, s);
  return true;
}

(async () => {
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
  await ctx.route("**/*", r => /googlesyndication|doubleclick|googleads|adtrafficquality|fonts\.googleapis|fonts\.gstatic|cdnjs|jsdelivr/.test(r.request().url()) ? r.abort() : r.continue());

  const slugs = fs.readdirSync(path.join(ROOT,"tools")).filter(d => fs.existsSync(path.join(ROOT,"tools",d,"index.html")));
  const results = [];
  for (const slug of slugs) {
    const page = await ctx.newPage();
    try {
      await page.goto(`http://127.0.0.1:${PORT}/tools/${slug}/`, { waitUntil: "domcontentloaded", timeout: 30000 });
      await page.waitForTimeout(200);
      const r = await page.evaluate(() => {
        const vw = document.documentElement.clientWidth;
        if (document.documentElement.scrollWidth <= vw + 2) return null;
        const offenders = [...document.querySelectorAll("body *")]
          .map(e => ({ e, r: e.getBoundingClientRect() }))
          .filter(x => x.r.width > 0 && x.r.right > vw + 2);
        if (!offenders.length) return { sw: document.documentElement.scrollWidth, sels: [] };
        const selOf = (el) => {
          if (!el || el === document.body || el === document.documentElement) return null;
          if (el.id) return "#" + CSS.escape(el.id);
          const cls = (el.className || "").toString().trim().split(/\s+/).filter(Boolean);
          if (cls.length) return "." + cls.map(c => CSS.escape(c)).join(".");
          return null;
        };
        // The element that sticks out cannot scroll itself: its own width is the
        // problem. Walk up to the nearest ancestor that DOES fit the viewport and
        // make that the scroll container, which is what actually contains the overflow.
        const sels = [];
        for (const { e } of offenders) {
          let node = e, container = null;
          for (let i = 0; i < 8 && node && node !== document.body; i++) {
            const p = node.parentElement;
            if (!p || p === document.body) break;
            if (p.getBoundingClientRect().width <= vw + 2) { container = p; break; }
            node = p;
          }
          for (const cand of [container, e]) {
            const sel = selOf(cand);
            if (sel && !sels.includes(sel)) { sels.push(sel); break; }
          }
          if (sels.length >= 3) break;
        }
        return { sw: document.documentElement.scrollWidth, sels };
      });
      if (r) results.push({ slug, ...r });
    } catch (e) { /* skip */ }
    await page.close();
  }

  console.log(`pages overflowing at 375px: ${results.length}`);
  let fixed = 0;
  for (const r of results) {
    if (!r.sels.length) { console.log(`  ${r.slug}: no selector, needs manual work`); continue; }
    const css = r.sels.map(s => `  ${s}{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;}`).join("\n");
    if (APPLY) {
      if (injectCss(path.join(ROOT,"tools",r.slug,"index.html"), css)) fixed++;
    }
    console.log(`  ${r.slug} (sw=${r.sw}) -> ${r.sels.join(", ")}`);
  }
  if (APPLY) console.log(`\ninjected scoped fixes into ${fixed} pages`);
  await browser.close(); server.close();
})();
