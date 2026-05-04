#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const http = require("http");
const sharp = require("sharp");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname);
const COLLECTION_DIR = path.join(ROOT, "South Fork Apps Collection");
const INDEX_PATH = path.join(ROOT, "index.html");
const PORT = 8766;

function escapeHtml(value) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function wrapText(text, limit) {
  const words = text.split(/\s+/);
  const lines = [];
  let line = "";
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > limit && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) lines.push(line);
  return lines;
}

function parseApps() {
  const text = fs.readFileSync(INDEX_PATH, "utf8");
  const start = text.indexOf('<div id="appGrid"');
  const end = text.indexOf('<div id="noResults"');
  const grid = text.slice(start, end);
  const pattern = /<div data-app-card data-title="([^"]+)" data-description="([^"]+)" data-category="([^"]+)".*?<a href="\.\/South Fork Apps Collection\/([^/]+)\//gs;
  const apps = [];
  for (const match of grid.matchAll(pattern)) {
    apps.push({
      title: match[1]
        .replace(/&amp;/g, "&")
        .replace(/&#x27;/g, "'")
        .replace(/&quot;/g, '"'),
      description: match[2]
        .replace(/&amp;/g, "&")
        .replace(/&#x27;/g, "'")
        .replace(/&quot;/g, '"'),
      category: match[3].replace(/&amp;/g, "&"),
      slug: match[4],
    });
  }
  return apps;
}

function contentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return (
    {
      ".html": "text/html; charset=utf-8",
      ".css": "text/css; charset=utf-8",
      ".js": "application/javascript; charset=utf-8",
      ".json": "application/json; charset=utf-8",
      ".svg": "image/svg+xml",
      ".png": "image/png",
      ".jpg": "image/jpeg",
      ".jpeg": "image/jpeg",
      ".webp": "image/webp",
      ".xml": "application/xml; charset=utf-8",
      ".txt": "text/plain; charset=utf-8",
    }[ext] || "application/octet-stream"
  );
}

function createServer() {
  return http.createServer((req, res) => {
    const requestPath = decodeURIComponent((req.url || "/").split("?")[0]);
    let filePath = path.join(ROOT, requestPath === "/" ? "index.html" : requestPath);
    if (!filePath.startsWith(ROOT)) {
      res.writeHead(403);
      res.end("Forbidden");
      return;
    }

    try {
      const stat = fs.existsSync(filePath) && fs.statSync(filePath);
      if (stat && stat.isDirectory()) {
        filePath = path.join(filePath, "index.html");
      }
      if (!fs.existsSync(filePath)) {
        res.writeHead(404);
        res.end("Not found");
        return;
      }
      res.writeHead(200, { "Content-Type": contentType(filePath) });
      fs.createReadStream(filePath).pipe(res);
    } catch (error) {
      res.writeHead(500);
      res.end(String(error));
    }
  });
}

async function renderShareImage(app, screenshotPath, sharePath) {
  const screenshot = await sharp(screenshotPath)
    .resize(470, 470, { fit: "cover", position: "top" })
    .jpeg({ quality: 82 })
    .toBuffer();

  const titleLines = wrapText(app.title, 22).slice(0, 3);
  const descLines = wrapText(app.description, 46).slice(0, 3);
  const titleTspans = titleLines
    .map((line, index) => `<tspan x="80" dy="${index === 0 ? 0 : 56}">${escapeHtml(line)}</tspan>`)
    .join("");
  const descTspans = descLines
    .map((line, index) => `<tspan x="80" dy="${index === 0 ? 0 : 28}">${escapeHtml(line)}</tspan>`)
    .join("");

  const overlaySvg = `
  <svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#111412"/>
        <stop offset="100%" stop-color="#1d2c21"/>
      </linearGradient>
      <linearGradient id="glow" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="rgba(125,219,132,0.15)"/>
        <stop offset="100%" stop-color="rgba(170,204,218,0.08)"/>
      </linearGradient>
    </defs>
    <rect width="1200" height="630" fill="url(#bg)"/>
    <rect width="1200" height="630" fill="url(#glow)"/>
    <rect x="730" y="80" width="390" height="470" rx="22" fill="#0d100e" stroke="rgba(125,219,132,0.28)"/>
    <rect x="80" y="82" width="120" height="34" rx="17" fill="rgba(125,219,132,0.12)" stroke="rgba(125,219,132,0.35)"/>
    <text x="140" y="104" text-anchor="middle" fill="#7ddb84" font-family="Plus Jakarta Sans, Arial, sans-serif" font-size="14" font-weight="800" letter-spacing="2.4">${escapeHtml(app.category.toUpperCase())}</text>
    <text x="80" y="175" fill="#e8e8e8" font-family="Plus Jakarta Sans, Arial, sans-serif" font-size="58" font-weight="800">${titleTspans}</text>
    <text x="80" y="350" fill="#aab5ac" font-family="Plus Jakarta Sans, Arial, sans-serif" font-size="24" font-weight="500">${descTspans}</text>
    <text x="80" y="528" fill="#7ddb84" font-family="Plus Jakarta Sans, Arial, sans-serif" font-size="18" font-weight="800" letter-spacing="2.8">SOUTH FORK APPS</text>
  </svg>`;

  const canvas = sharp({
    create: {
      width: 1200,
      height: 630,
      channels: 4,
      background: "#111412",
    },
  });

  await canvas
    .composite([
      { input: Buffer.from(overlaySvg) },
      { input: screenshot, top: 80, left: 730 },
    ])
    .jpeg({ quality: 85, mozjpeg: true })
    .toFile(sharePath);
}

async function main() {
  const apps = parseApps();
  const server = createServer();
  await new Promise((resolve) => server.listen(PORT, "127.0.0.1", resolve));

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1024 },
    deviceScaleFactor: 1,
    colorScheme: "dark",
    geolocation: { latitude: 36.469, longitude: -82.263 },
    permissions: ["geolocation", "clipboard-read", "clipboard-write"],
  });

  for (const [index, app] of apps.entries()) {
    const page = await context.newPage();
    const url = `http://127.0.0.1:${PORT}/South%20Fork%20Apps%20Collection/${app.slug}/`;
    const appDir = path.join(COLLECTION_DIR, app.slug);
    const screenshotPath = path.join(appDir, "screenshot.jpg");
    const sharePath = path.join(appDir, "share.jpg");

    await page.goto(url, { waitUntil: "networkidle", timeout: 120000 });
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(600);
    await page.screenshot({
      path: screenshotPath,
      type: "jpeg",
      quality: 78,
      clip: { x: 0, y: 0, width: 1280, height: 920 },
    });
    await renderShareImage(app, screenshotPath, sharePath);
    await page.close();
    console.log(`[${index + 1}/${apps.length}] ${app.slug}`);
  }

  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
