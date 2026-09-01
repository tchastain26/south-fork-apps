// Renders every page at 375px and reports any that scroll horizontally.
// "Content wider than screen" is a Google mobile-usability failure, and mobile
// converts far better than desktop here (1.38% CTR against 0.17%).

const fs = require("fs"), path = require("path"), http = require("http");
const { chromium } = require("playwright");
const ROOT = process.cwd(), PORT = Number(process.env.PORT || 8811);

const types = {".html":"text/html",".js":"text/javascript",".css":"text/css",".jpg":"image/jpeg",".png":"image/png",".svg":"image/svg+xml",".json":"application/json",".xml":"application/xml",".webmanifest":"application/manifest+json",".ico":"image/x-icon"};
const server = http.createServer((req,res)=>{
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, {"Content-Type": types[path.extname(f)] || "application/octet-stream"});
  fs.createReadStream(f).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2 });
  await ctx.route("**/*", r => /googlesyndication|doubleclick|googleads|adtrafficquality|fonts\.googleapis|fonts\.gstatic|cdnjs|jsdelivr/.test(r.request().url()) ? r.abort() : r.continue());

  const slugs = fs.readdirSync(path.join(ROOT,"tools")).filter(d => fs.existsSync(path.join(ROOT,"tools",d,"index.html")));
  const targets = ["/", "/about/", "/contact/", "/privacy/", "/categories/", ...slugs.map(s=>`/tools/${s}/`)];
  const bad = [];
  for (const t of targets) {
    const page = await ctx.newPage();
    try {
      await page.goto(`http://127.0.0.1:${PORT}${t}`, { waitUntil: "domcontentloaded", timeout: 30000 });
      await page.waitForTimeout(250);
      const r = await page.evaluate(() => {
        const vw = document.documentElement.clientWidth;
        const sw = document.documentElement.scrollWidth;
        let worst = null;
        if (sw > vw + 2) {
          // An element inside a scroll container sticks out in its own box but
          // does not widen the document, so blaming it sends you chasing the
          // wrong element. Only count offenders with no scrolling ancestor.
          const inScroller = (el) => {
            let n = el.parentElement;
            while (n && n !== document.body) {
              const ox = getComputedStyle(n).overflowX;
              if (ox === "auto" || ox === "scroll" || ox === "hidden") return true;
              n = n.parentElement;
            }
            return false;
          };
          const els = [...document.querySelectorAll("body *")].map(e => ({ e, r: e.getBoundingClientRect() }))
            .filter(x => x.r.width > 0 && x.r.right > vw + 2)
            .filter(x => !inScroller(x.e))
            .sort((a,b) => b.r.right - a.r.right);
          if (els.length) worst = { tag: els[0].e.tagName, id: els[0].e.id || "", cls: (els[0].e.className||"").toString().slice(0,60), right: Math.round(els[0].r.right) };
        }
        return { vw, sw, worst };
      });
      if (r.sw > r.vw + 2) bad.push({ t, sw: r.sw, worst: r.worst });
    } catch (e) { bad.push({ t, error: String(e).slice(0,60) }); }
    await page.close();
  }
  console.log(`checked ${targets.length} pages at 375px`);
  console.log(`horizontal overflow: ${bad.length}`);
  for (const b of bad) console.log("  ", b.t, "scrollWidth=" + b.sw, b.worst ? `<${b.worst.tag} ${b.worst.id||b.worst.cls}> right=${b.worst.right}` : (b.error||""));
  await browser.close(); server.close();
})();
