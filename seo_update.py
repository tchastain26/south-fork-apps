#!/usr/bin/env python3
"""Adds meta descriptions, fixes titles, and generates sitemap.xml for South Fork Apps."""

import os
import re
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COLLECTION_DIR = os.path.join(BASE_DIR, "South Fork Apps Collection")
BASE_URL = "https://southforkapps.com"
TODAY = date.today().isoformat()

APP_META = {
    "add-line-numbers":       ("Add Line Numbers",           "Free online tool to add line numbers to any block of text. Paste your text and instantly number every line."),
    "add-prefix-suffix":      ("Add Prefix / Suffix",        "Add a custom prefix, suffix, or both to every line of text. Fast, free, and works in your browser."),
    "age-calculator":         ("Age Calculator",             "Calculate your exact age in years, months, and days from any birth date. Free online age calculator."),
    "base64-decoder":         ("Base64 Decoder",             "Decode Base64-encoded strings back to plain text instantly. Free online Base64 decoder tool."),
    "base64-encoder":         ("Base64 Encoder",             "Encode any text or data to Base64 format instantly. Free online Base64 encoding tool."),
    "bingo-maker":            ("Bingo Card Maker",           "Create custom bingo cards with your own words or phrases. Free printable bingo card generator."),
    "countdown-timer":        ("Countdown Timer",            "Simple countdown timer you can set to any duration. Free browser-based timer with no install required."),
    "csv-column-extractor":   ("CSV Column Extractor",       "Extract specific columns from CSV data instantly. Paste your CSV and pull out just the columns you need."),
    "date-calculator":        ("Date Calculator",            "Calculate the difference between two dates or add/subtract days from any date. Free online date calculator."),
    "debt-snowball":          ("Debt Snowball Calculator",   "Plan your debt payoff with the debt snowball method. Enter your balances and see your payoff order and timeline."),
    "dedupe-lines":           ("Duplicate Line Remover",     "Remove duplicate lines from any list of text instantly. Free online tool to deduplicate text."),
    "dog-poop-tracker":       ("Dog Poop Tracker",           "Track where your dog goes in the yard using GPS. Mark, map, and clear poop locations with this free PWA."),
    "email-extractor":        ("Email Extractor",            "Extract all email addresses from a block of text instantly. Free online email address extractor tool."),
    "extract-urls":           ("URL Extractor",              "Extract all URLs and links from any block of text. Free online link extractor tool."),
    "gemini-3-1-flash-tts-studio": ("Gemini TTS Studio",    "Convert text to speech using Google Gemini. Free browser-based text-to-speech studio powered by Gemini API."),
    "habit-tracker":          ("Habit Tracker",              "Track your daily habits with a simple, free habit tracker. No account required — works right in your browser."),
    "hex-code-color-generator": ("Hex Color Code Generator","Generate random hex color codes or convert colors instantly. Free online hex color picker and generator."),
    "html-entity-decoder":    ("HTML Entity Decoder",        "Decode HTML entities like &amp; and &lt; back to plain text. Free online HTML entity decoder."),
    "html-entity-encoder":    ("HTML Entity Encoder",        "Encode special characters to HTML entities instantly. Free online HTML entity encoding tool."),
    "join-lines":             ("Join Lines",                 "Join multiple lines of text into a single line with a custom separator. Free online line joiner tool."),
    "json-yaml-converter":    ("JSON to YAML Converter",     "Convert JSON to YAML or YAML to JSON instantly. Free online JSON/YAML conversion tool."),
    "list-randomizer":        ("List Randomizer",            "Randomly shuffle any list of items instantly. Paste your list and randomize the order with one click."),
    "magic-8-ball":           ("Magic 8 Ball",               "Ask the Magic 8 Ball your yes or no questions. Free online Magic 8 Ball with classic answers."),
    "markdown-link-cleaner":  ("Markdown Link Cleaner",      "Clean up and reformat messy Markdown links. Free online tool to fix and standardize Markdown hyperlinks."),
    "markdown-list-cleaner":  ("Markdown List Cleaner",      "Clean and reformat Markdown lists instantly. Fix indentation, bullets, and numbering with one click."),
    "markdown-table-maker":   ("Markdown Table Maker",       "Create properly formatted Markdown tables from plain text or CSV data. Free online Markdown table generator."),
    "millisecond-converter":  ("Millisecond Converter",      "Convert milliseconds to seconds, minutes, hours, and more. Free online time unit converter for developers."),
    "number-extractor":       ("Number Extractor",           "Extract all numbers from a block of text instantly. Free online tool to pull numbers out of any string."),
    "password-generator":     ("Password Generator",         "Generate strong, secure random passwords instantly. Free online password generator with customizable options."),
    "pomodoro-timer":         ("Pomodoro Timer",             "Stay focused with a free Pomodoro timer. 25-minute work sessions with short and long break intervals."),
    "quote-escaper":          ("Quote Escaper",              "Escape or unescape quotes in strings for use in code. Free online quote escaping tool for developers."),
    "rain-simulator":         ("Rain Simulator",             "Watch and listen to a relaxing rain simulation in your browser. Free ambient rain sound and visual tool."),
    "random-picker":          ("Random Picker",              "Pick a random item from any list instantly. Paste your options and let the random picker choose for you."),
    "reading-time-calculator":("Reading Time Calculator",    "Calculate how long it takes to read any text. Paste your content and get an estimated reading time instantly."),
    "recipe-scaler":          ("Recipe Scaler",              "Scale any recipe up or down by changing the number of servings. Free online recipe scaling tool."),
    "remove-empty-lines":     ("Empty Line Remover",         "Remove all blank lines from a block of text instantly. Free online tool to clean up empty lines."),
    "reverse-lines":          ("Reverse Lines",              "Reverse the order of lines in any block of text. Free online line reversal tool."),
    "slugify-text":           ("Slugify Text",               "Convert any text to a URL-friendly slug. Free online slugifier for creating clean URLs and filenames."),
    "smart-quotes-converter": ("Smart Quotes Converter",     "Convert curly smart quotes to straight quotes or vice versa. Free online quote conversion tool."),
    "sort-lines-alpha":       ("Sort Lines Alphabetically",  "Sort any list of lines into alphabetical order instantly. Free online alphabetical text sorter."),
    "sort-lines-length":      ("Sort Lines by Length",       "Sort lines of text by character length, shortest or longest first. Free online line length sorter."),
    "split-text":             ("Text Splitter",              "Split text into chunks by character count, word count, or delimiter. Free online text splitting tool."),
    "strip-line-numbers":     ("Strip Line Numbers",         "Remove line numbers from numbered text instantly. Free online tool to strip line numbers from any content."),
    "symbol-pad":             ("Symbol Pad",                 "Copy and paste special characters, symbols, and Unicode characters instantly. Free online symbol keyboard."),
    "task-timer":             ("Task Timer",                 "Time how long individual tasks take with a simple task timer. Free browser-based productivity timer."),
    "temperature-converter":  ("Temperature Converter",      "Convert between Fahrenheit, Celsius, and Kelvin instantly. Free online temperature conversion tool."),
    "text-case-converter":    ("Text Case Converter",        "Convert text to uppercase, lowercase, title case, or sentence case instantly. Free online case converter."),
    "text-repeater":          ("Text Repeater",              "Repeat any text a set number of times with a custom separator. Free online text repetition tool."),
    "timestamp-converter":    ("Timestamp Converter",        "Convert Unix timestamps to readable dates and vice versa. Free online Unix timestamp converter."),
    "tip-calculator":         ("Tip Calculator",             "Calculate the tip and split the bill for any group size. Free online tip calculator."),
    "transfer-time-estimator":("Transfer Time Estimator",    "Estimate how long a file transfer will take at any connection speed. Free online transfer time calculator."),
    "trim-lines":             ("Trim Lines",                 "Remove leading and trailing whitespace from every line of text. Free online line trimmer tool."),
    "typing-test":            ("Typing Speed Test",          "Test your typing speed and accuracy with a free online typing test. See your WPM and error rate instantly."),
    "unicode-normalizer":     ("Unicode Normalizer",         "Normalize Unicode text to standard forms (NFC, NFD, NFKC, NFKD). Free online Unicode normalization tool."),
    "unit-converter":         ("Unit Converter",             "Convert between hundreds of units across length, weight, volume, and more. Free online unit conversion tool."),
    "url-decoder":            ("URL Decoder",                "Decode URL-encoded strings back to plain text instantly. Free online URL percent-encoding decoder."),
    "url-encoder":            ("URL Encoder",                "Encode text to URL-safe percent-encoded format instantly. Free online URL encoding tool."),
    "url-extractor":          ("URL Extractor",              "Extract all URLs from any block of text or HTML. Free online link and URL extraction tool."),
    "virtual-pop":            ("Virtual Bubble Wrap",        "Pop virtual bubble wrap in your browser. Satisfying, stress-relieving, and endlessly poppable."),
    "whitespace-visualizer":  ("Whitespace Visualizer",      "Make invisible whitespace characters visible in any text. Free online whitespace and tab visualization tool."),
    "word-counter":           ("Word Counter",               "Count words, characters, sentences, and paragraphs in any text. Free online word counter tool."),
    "sql-pretty-printer":     ("SQL Pretty Printer",         "Format and indent messy SQL queries instantly. Free online SQL formatter with syntax highlighting."),
    "reading-level-analyzer": ("Reading Level Analyzer",     "Analyze the reading level of any text. Get Flesch-Kincaid grade level and readability scores instantly. Free online tool."),
    "token-usage-calculator": ("Token Usage Calculator",     "Estimate LLM token counts and API costs for GPT-4o, Claude, and Gemini. Free online token calculator."),
    "encrypt-decrypt":        ("Encrypt / Decrypt Message",  "Encrypt and decrypt messages with a passphrase using AES-256 in your browser. No data leaves your device. Free tool."),
    "lorem-ipsum-generator":  ("Lorem Ipsum Generator",      "Generate Lorem Ipsum placeholder text by paragraphs, sentences, or words instantly. Free online Lorem Ipsum generator."),
    "regex-tester":           ("Regex Tester",               "Test and debug regular expressions in real time with live match highlighting and group captures. Free online regex tester."),
    "color-contrast-checker": ("Color Contrast Checker",     "Check color contrast ratios for WCAG AA and AAA accessibility compliance. Free online color contrast tool."),
    "text-diff":              ("Text Diff",                  "Compare two blocks of text and see differences highlighted line by line. Free online text diff tool."),
    "hash-generator":         ("Hash Generator",             "Generate SHA-256, SHA-512, SHA-1, and SHA-384 hashes from any text instantly in your browser. Free online hash generator."),
    "markdown-to-html":       ("Markdown to HTML Converter", "Convert Markdown to clean HTML instantly with a live preview. Free online Markdown to HTML converter."),
    "aspect-ratio-calculator":("Aspect Ratio Calculator",    "Calculate aspect ratios and scale dimensions for video, photo, and design work. Free online aspect ratio calculator."),
    "word-frequency":         ("Word Frequency Counter",     "Find the most common words in any text ranked by usage. Free online word frequency analyzer with stop word filtering."),
    "json-formatter":         ("JSON Formatter & Validator", "Format, beautify, and validate JSON instantly with syntax highlighting. Free online JSON formatter and minifier."),
    "percentage-calculator":  ("Percentage Calculator",      "Calculate percentages, percentage change, and add or subtract percentages instantly. Free online percentage calculator."),
    "color-converter":        ("Color Format Converter",     "Convert colors between HEX, RGB, HSL, and HSB formats with a live preview. Free online color converter."),
    "binary-hex-converter":   ("Binary, Hex & Decimal Converter", "Convert between binary, hexadecimal, decimal, and octal instantly. Free online number base converter."),
    "bmi-calculator":         ("BMI Calculator",              "Calculate your Body Mass Index in imperial or metric units. Free online BMI calculator with healthy weight range."),
    "loan-calculator":        ("Loan Payment Calculator",     "Calculate monthly loan payments, total interest, and a full amortization schedule. Free online loan calculator."),
    "timezone-converter":     ("Timezone Converter",          "Convert times between any two timezones instantly with a live world clock. Free online timezone converter."),
    "qr-code-generator":      ("QR Code Generator",           "Generate QR codes from any URL, text, WiFi, or contact info. Download as PNG. Free online QR code generator."),
    "decision-spinner":       ("Decision Spinner",            "Can't decide? Add your options and spin the wheel. Free online decision spinner and random picker wheel."),
    "meeting-cost-tracker":   ("Meeting Cost Tracker",        "See how much your meeting costs in real time. Enter attendees and salaries and watch the cost tick up. Free tool."),
    "teleprompter":           ("Teleprompter",                "Free browser-based teleprompter for video creators. Adjust speed, font size, and mirror mode. No signup required."),
    "star-wars-crawl":        ("Star Wars Opening Crawl Generator", "Create your own Star Wars-style opening crawl with custom text. Free online Star Wars crawl generator."),
    "html-preview":           ("HTML Live Preview",           "Write HTML and see it rendered live in a preview pane. Includes templates and download. Free online HTML editor."),
}

def update_app(app_name, title, description):
    path = os.path.join(COLLECTION_DIR, app_name, "index.html")
    if not os.path.exists(path):
        print(f"SKIP (not found): {app_name}")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False

    # Fix title — standardize to "Title | South Fork Apps"
    new_title = f"{title} | South Fork Apps"
    old_title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
    if old_title_match and old_title_match.group(1) != new_title:
        content = re.sub(r"<title>.*?</title>", f"<title>{new_title}</title>", content, flags=re.IGNORECASE)
        changed = True

    # Add or update meta description
    desc_tag = f'<meta name="description" content="{description}">'
    existing = re.search(r'<meta\s+name=["\']description["\'].*?>', content, re.IGNORECASE)
    if existing:
        if existing.group(0) != desc_tag:
            content = re.sub(r'<meta\s+name=["\']description["\'].*?>', desc_tag, content, flags=re.IGNORECASE)
            changed = True
    else:
        # Insert after <title> tag
        content = re.sub(r"(</title>)", r"\1\n  " + desc_tag, content, count=1, flags=re.IGNORECASE)
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"UPDATED: {app_name}")
    else:
        print(f"OK: {app_name}")

def build_sitemap():
    urls = [BASE_URL + "/"]
    for app_name in sorted(os.listdir(COLLECTION_DIR)):
        app_path = os.path.join(COLLECTION_DIR, app_name)
        if os.path.isdir(app_path) and os.path.exists(os.path.join(app_path, "index.html")):
            encoded = app_name.replace(" ", "%20")
            urls.append(f"{BASE_URL}/South%20Fork%20Apps%20Collection/{encoded}/")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n"
    sitemap += "</urlset>\n"

    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"\nSITEMAP: {len(urls)} URLs written to sitemap.xml")

if __name__ == "__main__":
    print("=== Updating app meta tags ===")
    for app_name, (title, description) in APP_META.items():
        update_app(app_name, title, description)

    print("\n=== Building sitemap ===")
    build_sitemap()
    print("\nDone.")
