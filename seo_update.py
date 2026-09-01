#!/usr/bin/env python3
"""Adds meta descriptions, fixes titles, and generates sitemap.xml for South Fork Apps."""

import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COLLECTION_DIR = os.path.join(BASE_DIR, "South Fork Apps Collection")
BASE_URL = "https://southforkapps.com"
TODAY = date.today().isoformat()

APP_META = {
    "detailing-quote-widget": ("Detailing Quote Widget",    "Give detailing customers an instant estimate with a custom-branded quote widget. Live demo and one-time setup with no subscription."),
    "currency-converter":     ("Currency Converter",         "Convert between 30+ world currencies instantly using a built-in rate table. Free online currency converter."),
    "heart-rate-zones":       ("Heart Rate Zones",           "Calculate your 5 aerobic training zones by age or custom max heart rate. Supports Karvonen method. Free online tool."),
    "net-worth-tracker":      ("Net Worth Tracker",          "Add assets and liabilities to calculate your net worth instantly. Free browser-based net worth calculator with visual breakdown."),
    "file-size-converter":    ("File Size Converter",        "Convert between bytes, KB, MB, GB, TB, and PB instantly. Free online file size converter with bit equivalents."),
    "metronome":              ("Metronome",                  "Free online metronome with BPM slider, tap tempo, visual beat, and audio click. Works in your browser with no install."),
    "tag-stripper":           ("Tag Stripper",               "Remove HTML tags, XML tags, or Markdown formatting from any text instantly. Free online tag and markup stripper."),
    "word-wrap":              ("Word Wrap",                  "Wrap text at any column width with hard or soft wrapping. Free online word wrap formatter for text, code, and emails."),
    "cron-builder":           ("CRON Expression Builder",    "Build and explain CRON expressions visually with plain-English descriptions and common presets. Free online CRON builder."),
    "pace-calculator":        ("Pace Calculator",            "Calculate running or walking pace, distance, or time. Enter any two values and get the third. Free online pace calculator."),
    "tab-space-converter":      ("Tab ↔ Space Converter",    "Convert tabs to spaces or spaces to tabs with custom tab width. Free online code indentation converter."),
    "caesar-cipher":            ("Caesar Cipher",             "Encode and decode text with a Caesar or ROT cipher. Includes ROT13 preset. Free online Caesar cipher tool."),
    "vigenere-cipher":          ("Vigenère Cipher",           "Encode and decode text with the Vigenère cipher using a custom keyword. Free online Vigenère cipher tool."),
    "prime-factorization":      ("Prime Factorization",       "Find the prime factors of any number instantly. Shows exponents, factor count, and sum. Free online prime factorization tool."),
    "gcd-lcm-calculator":       ("GCD & LCM Calculator",      "Calculate the greatest common divisor and least common multiple of up to 6 numbers. Free online GCD LCM calculator."),
    "screen-size-checker":      ("Screen Size Checker",       "See your browser viewport, screen resolution, device pixel ratio, and orientation in real time. Free online tool."),
    "html-minifier":            ("HTML Minifier",              "Minify HTML by stripping whitespace and comments. See byte savings instantly. Free online HTML minifier tool."),
    "credit-card-validator":    ("Credit Card Validator",     "Validate card numbers using the Luhn algorithm and detect card type. Visa, Mastercard, Amex, and more. Free tool."),
    "markdown-frontmatter":     ("Markdown Frontmatter Generator", "Generate YAML or TOML frontmatter for blog posts and static sites. Free online frontmatter builder."),
    "haiku-checker":            ("Haiku Checker",              "Count syllables per line and check for the 5-7-5 haiku pattern. Free online syllable counter and haiku validator."),
    "text-alignment":           ("Text Alignment Formatter",  "Left, right, center, or justify text to a fixed column width. Free online text alignment and padding tool."),
    "color-blindness-simulator":("Color Blindness Simulator", "See how a color appears under protanopia, deuteranopia, tritanopia, and achromatopsia. Free online color blindness tool."),
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
    "decision-matrix":        ("Decision Matrix",            "Score options against weighted criteria to rank competing choices with live totals, percentages, and sortable results. Free online tool."),
    "dedupe-lines":           ("Duplicate Line Remover",     "Remove duplicate lines from any list of text instantly. Free online tool to deduplicate text."),
    "dog-poop-tracker":       ("Dog Poop Tracker",           "Track where your dog goes in the yard using GPS. Mark, map, and clear poop locations with this free PWA."),
    "email-extractor":        ("Email Extractor",            "Extract all email addresses from a block of text instantly. Free online email address extractor tool."),
    "gemini-3-1-flash-tts-studio": ("Gemini TTS Studio",    "Convert text to speech using Google Gemini. Free browser-based text-to-speech studio powered by Gemini API."),
    "hangman":                ("Hangman",                    "Play classic hangman with category hints, difficulty modes, keyboard input, and persistent stats. Free online tool."),
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
    "rock-paper-scissors":    ("Rock Paper Scissors",        "Play rock paper scissors against the computer with saved scores, streak tracking, and recent round history. Free online tool."),
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
    "tic-tac-toe":            ("Tic Tac Toe",                "Play tic tac toe against an unbeatable computer or a second player with saved local scoreboards. Free online tool."),
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
    "periodic-table":         ("Periodic Table",             "Explore all 118 elements in a clickable periodic table with mass, group, period, phase, and electron configuration. Free online tool."),
    "quadratic-solver":       ("Quadratic Solver",           "Solve ax² + bx + c = 0 with real or complex roots, step-by-step work, discriminant details, and a live parabola graph. Free online tool."),
    "color-converter":        ("Color Format Converter",     "Convert colors between HEX, RGB, HSL, and HSB formats with a live preview. Free online color converter."),
    "binary-hex-converter":   ("Binary, Hex & Decimal Converter", "Convert between binary, hexadecimal, decimal, and octal instantly. Free online number base converter."),
    "bmi-calculator":         ("BMI Calculator",              "Calculate your Body Mass Index in imperial or metric units. Free online BMI calculator with healthy weight range."),
    "loan-calculator":        ("Loan Payment Calculator",     "Calculate monthly loan payments, total interest, and a full amortization schedule. Free online loan calculator."),
    "timezone-converter":     ("Timezone Converter",          "Convert times between any two timezones instantly with a live world clock. Free online timezone converter."),
    "unit-circle":            ("Unit Circle Reference",       "Interactive unit circle with standard angles, radians, exact sin cos tan values, coordinates, and quadrant patterns. Free online tool."),
    "qr-code-generator":      ("QR Code Generator",           "Generate QR codes from any URL, text, WiFi, or contact info. Download as PNG. Free online QR code generator."),
    "decision-spinner":       ("Decision Spinner",            "Can't decide? Add your options and spin the wheel. Free online decision spinner and random picker wheel."),
    "meeting-cost-tracker":   ("Meeting Cost Tracker",        "See how much your meeting costs in real time. Enter attendees and salaries and watch the cost tick up. Free tool."),
    "teleprompter":           ("Teleprompter",                "Free browser-based teleprompter for video creators. Adjust speed, font size, and mirror mode. No signup required."),
    "star-wars-crawl":        ("Star Wars Opening Crawl Generator", "Create your own Star Wars-style opening crawl with custom text. Free online Star Wars crawl generator."),
    "html-preview":           ("HTML Live Preview",           "Write HTML and see it rendered live in a preview pane. Includes templates and download. Free online HTML editor."),
    "nato-alphabet":          ("NATO Phonetic Alphabet Converter", "Convert any text to the NATO phonetic alphabet. Alpha, Bravo, Charlie. Free online NATO alphabet converter."),
    "morse-code":             ("Morse Code Translator",       "Translate text to Morse code and back with audio playback. Free online Morse code translator and decoder."),
    "compound-interest":      ("Compound Interest Calculator", "Calculate compound interest with monthly contributions. Includes growth chart and year-by-year table. Free online calculator."),
    "rule-of-72":             ("Rule of 72",                  "Enter an interest rate to instantly see how many years it takes to double your money. Free online tool."),
    "resistor-color-code":    ("Resistor Color Code",         "Decode or build 4-band and 5-band resistor color codes with real-time ohm display. Free online tool."),
    "roman-numerals":         ("Roman Numeral Converter",      "Convert numbers to Roman numerals and Roman numerals to numbers. Free online Roman numeral converter with breakdown."),
    "zalgo-text":             ("Zalgo Text Generator",         "Generate creepy glitchy Zalgo text with adjustable chaos level. Free online Zalgo text generator and corrupted text maker."),
    "kanban-board":           ("Kanban Board",                 "Simple drag-and-drop Kanban board saved in your browser. Add columns, cards, and tags. Free online Kanban tool."),
    "life-stats":             ("Life Stats Calculator",        "See how many heartbeats, breaths, and full moons you've lived through. Enter your birthday for live stats. Free tool."),
    "meeting-agenda-builder": ("Meeting Agenda Builder",      "Build a timed meeting agenda and copy it as formatted plain text or Markdown with totals, owners, and notes. Free online tool."),
    "word-clock":             ("Word Clock",                   "A live clock that spells out the current time in words on a glowing letter grid. Free online word clock with fullscreen mode."),
    "css-gradient-generator": ("CSS Gradient Generator",       "Generate linear, radial, and conic CSS gradients visually with live preview. Copy ready CSS code. Free online tool."),
    "password-strength":      ("Password Strength Checker",    "Check password strength with entropy score and time-to-crack estimate. All checks run locally. Free online password checker."),
    "color-palette":          ("Color Palette Generator",      "Generate complementary, analogous, triadic, and square color palettes from any base color. Free online color palette tool."),
    "stopwatch":              ("Stopwatch with Laps",          "A precise stopwatch with lap tracking, fastest and slowest lap highlights, and CSV export. Free online stopwatch."),
    "box-shadow-generator":   ("CSS Box Shadow Generator",     "Generate CSS box shadows visually. Stack multiple layers, adjust blur, spread, and offset. Free online box shadow tool."),
    "flip-clock":             ("Flip Clock",                   "A beautiful animated flip clock with smooth card-flip transitions and date display. Free online flip clock with fullscreen mode."),
    "random-quote":           ("Random Quote Generator",       "Get inspired with random quotes filtered by category. Wisdom, tech, creativity, motivation, and life. Free online quote generator."),
    "number-to-words":        ("Number to Words Converter",    "Convert numbers to words in standard, currency, and ordinal formats. Great for checks and documents. Free online converter."),
    "text-to-speech":         ("Text to Speech",               "Convert text to speech using your browser's built-in voices. Adjust rate, pitch, and volume. Free online text-to-speech tool."),
    "css-unit-converter":     ("CSS Unit Converter",           "Convert between px, rem, em, vw, vh, pt, and cm. Set viewport and root font size. Free online CSS unit converter for developers."),
    "csv-json-converter":     ("CSV to JSON Converter",        "Convert CSV to JSON and JSON to CSV instantly. Supports custom delimiters and headers. Free online CSV JSON converter."),
    "dice-roller":            ("Dice Roller",                  "Roll d4, d6, d8, d10, d12, d20, and d100 with modifiers and roll history. Free online dice roller for tabletop games."),
    "jwt-decoder":            ("JWT Decoder",                  "Decode JSON Web Tokens instantly. See header, payload, expiration, and claims. Everything runs in your browser. Free online JWT decoder."),
    "bill-splitter":          ("Bill Splitter",                "Split a restaurant bill unevenly between any number of people. Assign individual subtotals and split tax and tip proportionally. Free online bill splitter."),
    "break-even-calculator":  ("Break-Even Calculator",        "Enter fixed costs, variable cost per unit, and selling price to find break-even volume. Free online tool."),
    "sleep-cycle-calculator": ("Sleep Cycle Calculator",       "Find the best times to wake up or go to sleep based on 90-minute sleep cycles. Wake up refreshed instead of groggy. Free online sleep calculator."),
    "breath-timer":           ("Breath Timer",                 "Guided breathing timer with animated visual cues for box breathing, 4-7-8, and calm patterns. Free online breath timer."),
    "pay-converter":          ("Pay Converter",                "Convert any salary between hourly, daily, weekly, biweekly, monthly, and annual pay rates instantly. Free online pay rate converter."),
    "savings-goal-planner":   ("Savings Goal Planner",         "Calculate how long it takes to reach a savings goal or how much to save per month. Includes interest. Free online savings calculator."),
    "noise-generator":        ("Noise Generator",              "Play white, brown, or pink ambient noise in your browser. No download required. Free online noise generator for focus and sleep."),
    "ascii-art-generator":    ("ASCII Art Generator",          "Convert text to ASCII block letter art with multiple style options. Free online ASCII art text generator."),
    "color-mixer":            ("Color Mixer",                  "Blend two colors with a ratio slider and see the result as HEX, RGB, and HSL. Free online color mixing tool."),
    "css-filter-generator":   ("CSS Filter Generator",         "Generate CSS filter strings with sliders for blur, brightness, contrast, grayscale, hue-rotate, and more. Free online tool."),
    "number-formatter":       ("Number Formatter",             "Format numbers with custom decimal places, currency symbols, thousand separators, and get formatted, scientific, ordinal, and word output."),
    "chmod-calculator":       ("chmod Calculator",             "Calculate Unix file permissions with a checkbox grid or octal input. Shows symbolic, binary, and chmod command output. Free online tool."),
    "coin-flipper":           ("Coin Flipper",                 "Flip a virtual coin with a satisfying animation. Tracks heads and tails counts and current streak. Free online coin flip tool."),
    "isbn-validator":         ("ISBN Validator",               "Validate ISBN-10 or ISBN-13 numbers, format with hyphens, and convert between ISBN-10 and ISBN-13. Free online tool."),
    "color-name-finder":      ("Color Name Finder",            "Find the closest CSS named color to any hex value. Shows the 5 nearest named colors with swatches. Free online color name tool."),
    "fibonacci-sequence":     ("Fibonacci Sequence",           "Generate Fibonacci sequences, find the Nth term, or check if a number is a Fibonacci number. Free online Fibonacci tool."),
    "body-fat-calculator":    ("Body Fat Calculator",          "Estimate body fat percentage using the US Navy method. Supports imperial and metric. Shows category and visual bar."),
    "passphrase-generator":   ("Passphrase Generator",         "Generate strong memorable passphrases from a 200+ word list. Customize word count, separator, capitalization, and numbers."),
    "base-converter":         ("Base Converter",               "Convert numbers between any base from 2-36 including binary, octal, decimal, hex, and base-32. Click any row to copy."),
    "uuid-generator":         ("UUID Generator",               "Generate UUID v4 or v7 values in batches. Copy uppercase, lowercase, braced, or hyphenless IDs instantly. Free online UUID generator."),
    "robots-txt-builder":     ("Robots.txt Builder",           "Build a clean robots.txt file with disallow rules, sitemap lines, crawl delay, and optional AI crawler blocking. Free online robots.txt generator."),
    "css-clamp-generator":    ("CSS Clamp Generator",          "Generate fluid CSS clamp() values from min and max sizes and viewport widths. Includes live preview and ready-to-copy CSS. Free online clamp calculator."),
    "svg-to-data-url":        ("SVG to Data URL Converter",    "Paste raw SVG markup and get a URL-encoded data URL plus ready-to-copy CSS background-image syntax. Free online SVG data URL converter."),
    "no-list":                ("No List",                       "Build your personal No List (a running record of commitments you've chosen to decline). Say no with intention and stick to it. Free online tool."),
    "hype-machine":           ("The Hype Machine",              "Type anything mundane and watch it become legendary. Free online hype generator that transforms boring text into epic marketing copy."),
    "meeting-email":          ("Could've Been an Email",        "Answer 7 quick questions and get a blunt verdict on whether your meeting should have been an email. Free online meeting analyzer."),
    "nap-calculator":         ("Nap Calculator",                "Wake up refreshed every time. Calculate the perfect nap length or bedtime based on 90-minute sleep cycles. Free online sleep calculator."),
    "image-to-data-url":      ("Image to Data URL",             "Convert any image (PNG, JPEG, GIF, WebP, SVG) to a Base64 data URL instantly in your browser. Output as CSS, HTML, or raw Base64. Free online image encoder."),
    "http-status-codes":      ("HTTP Status Codes",             "Complete HTTP status code reference with descriptions, common causes, and fix notes for all 1xx–5xx codes. Search by number, name, or keyword. Free online HTTP reference."),
    "css-specificity":        ("CSS Specificity Calculator",    "Calculate the (A, B, C) specificity score of any CSS selector. Compare multiple selectors side by side with visual ranking. Free online CSS specificity tool."),
    # Music Tools suite (added 2026.05.09)
    "bass-fretboard":         ("Bass Fretboard",               "Interactive bass guitar fretboard showing note names across 4 strings and 24 frets. Highlight scales, modes, and root positions in standard EADG tuning."),
    "bpm-counter":            ("BPM Counter",                  "Tap tempo BPM counter. Tap any key or the button to calculate your beats per minute in real time. Resets automatically after 3 seconds of silence."),
    "chord-finder":           ("Chord Finder",                 "Click notes on a piano keyboard to identify the chord. Shows all matching chord names, root, type, and inversion instantly. Free online chord identifier."),
    "chord-formulas":         ("Chord Formulas",               "Reference chart for chord formulas and interval structures. Covers triads, seventh chords, extended chords, suspended, and altered chords. Free music theory reference."),
    "chord-transposer":       ("Chord Transposer",             "Transpose guitar or piano chords to any key. Paste chord sheets, select original and target key, get transposed output instantly. Free online chord transposer."),
    "chords-in-keys":         ("Chords in Keys",               "See all diatonic chords for any major or minor key. Select a root and mode to get all 7 chords with Roman numeral analysis. Free music theory tool."),
    "chromatic-scale":        ("Chromatic Scale",              "Interactive chromatic scale tool. Click any of the 12 notes to hear it and see enharmonic equivalents. Free online music theory reference."),
    "circle-of-fifths":       ("Circle of Fifths",             "Interactive Circle of Fifths showing all 12 major and relative minor keys. Click any key to see its signature, chords, and relatives. Free music theory tool."),
    "circle-of-thirds":       ("Circle of Thirds",             "The Circle of Thirds shows harmonic relationships between chords a major or minor third apart. Explore chromatic mediant relationships. Free music theory tool."),
    "clef-reference":         ("Clef Reference",               "Treble and bass clef note position reference. Shows every note on both staves including ledger lines. Free online music staff reference."),
    "common-chord-progressions": ("Common Chord Progressions", "Reference library of common chord progressions by genre. Shows Roman numerals and chord names in any key with audio playback. Free music theory tool."),
    "diatonic-scale":         ("Diatonic Scale",               "Comprehensive diatonic scale reference. Select any major key to see all 7 scale notes, triads, seventh chords, and all 7 modal rotations. Free online tool."),
    "drum-patterns":          ("Drum Patterns",                "Visual drum pattern reference and sequencer. Browse common patterns for rock, funk, jazz, and reggae with Web Audio playback. Free online drum tool."),
    "guitar-chords":          ("Guitar Chords",                "Guitar chord diagram browser. View fingering diagrams for open and barre chords across all roots and types. Free online guitar chord reference."),
    "guitar-fretboard":       ("Guitar Fretboard",             "Interactive guitar fretboard showing note names across all 6 strings and 12 frets. Highlight scales and modes in standard or alternate tunings."),
    "guitar-tuning-chart":    ("Guitar Tuning Chart",          "Reference chart for standard and alternate guitar tunings. Shows string-by-string notes for open, drop, and modal tunings. Free online guitar reference."),
    "key-signatures":         ("Key Signatures",               "Complete reference for all 30 major and minor key signatures. Shows sharps, flats, and relative key relationships. Free online music theory tool."),
    "lil-beat-maker":         ("Lil Beat Maker",               "Browser-based step sequencer. Build drum patterns with 8 tracks and up to 32 steps, adjust BPM, and play back with Web Audio. Free online beat maker."),
    "music-intervals":        ("Music Intervals",              "Reference chart for all musical intervals with names, abbreviations, half steps, and examples. Includes unison through two octaves. Free music theory tool."),
    "music-theory-cheat-sheet": ("Music Theory Cheat Sheet",  "Comprehensive music theory cheat sheet. Quick reference for intervals, scales, chords, circle of fifths, and Roman numeral analysis. Free online reference."),
    "note-identification":    ("Note Identification",          "Music note identification trainer. See a note on a treble or bass clef staff and identify it by name. Tracks score, streak, and accuracy. Free ear trainer."),
    "overtone-series":        ("Overtone Series",              "Visual overtone series explorer. Select a fundamental note and see the first 16 harmonics with frequencies and note names. Free online acoustics tool."),
    "paradiddle":             ("Paradiddle",                   "Drum rudiment trainer for paradiddle patterns. See R/L sticking notation, hear the pattern at any BPM, practice all four paradiddle variations. Free drum tool."),
    "pentatonic-scale":       ("Pentatonic Scale",             "Pentatonic scale explorer. Select any root and see major or minor pentatonic notes on a piano keyboard with guitar box patterns. Free music theory tool."),
    "piano-chords":           ("Piano Chords",                 "Visual piano chord reference. Select any root note and chord type to see and hear the voicing on an interactive piano keyboard. Free online piano chord tool."),
    "piano-notes-on-staff":   ("Piano Notes on Staff",         "Click any piano key to see the note appear on the treble and bass clef staff. Shows note name, octave, frequency, and staff position. Free online tool."),
    "relative-pitch":         ("Relative Pitch Trainer",       "Interval ear training. Hear two notes and identify the musical interval between them. Tracks score, streak, and accuracy across all 12 intervals. Free ear trainer."),
    "rhythm-challenge":       ("Rhythm Challenge",             "Rhythm tapping challenge. See a rhythm pattern, hear it played, then tap it back. Scores your timing accuracy in milliseconds. Free online rhythm trainer."),
    "scale-finder":           ("Scale Finder",                 "Find any musical scale by root note and type. Shows all scale notes, intervals, and degrees on a mini piano keyboard. Free online scale reference."),
    "scale-formulas":         ("Scale Formulas",               "Reference chart for musical scale formulas. Shows whole/half step patterns for major, minor, modes, pentatonic, and blues scales. Free music theory tool."),
    "solfege":                ("Solfege",                      "Interactive solfege reference. Click Do Re Mi Fa Sol La Ti to hear each syllable and see its scale degree, interval, and note name. Free online solfege tool."),
    "time-signatures":        ("Time Signatures",              "Time signature reference with beat groupings, feel descriptions, and count-in playback. Free online music theory reference."),
    "ukulele-chords":         ("Ukulele Chords",               "Ukulele chord diagram browser. View fingering diagrams for common chords in standard GCEA tuning across all roots and types. Free online ukulele chord tool."),
    "ukulele-fretboard":      ("Ukulele Fretboard",            "Interactive ukulele fretboard showing all note names across 4 strings and 12 frets. Highlight scales and modes in standard GCEA tuning."),
    "virtual-piano":          ("Virtual Piano",                "Playable virtual piano in your browser. Click keys or use your keyboard to play notes across two octaves with sustain control. Free online piano."),
    "xylophone":              ("Xylophone",                    "Playable virtual xylophone in your browser. Click colorful bars to play notes across two octaves. Use your keyboard for fast playing. Free online xylophone."),
    "triangle-solver":        ("Triangle Solver",              "Solve any triangle from three known values, including ambiguous SSA cases. Free online tool."),
    "statistics-calculator":  ("Statistics Calculator",        "Compute mean, median, mode, range, variance, and standard deviation for any dataset. Free online tool."),
    "code-viewer":            ("Code Viewer",                  "Paste code and get instant syntax highlighting for 30+ programming languages. Free online code viewer with auto-detect and line numbers."),
}

# Newest 4 apps shown in the "New" section on the homepage.
# Update this list whenever new apps are pushed. Format:
# (folder_name, display_title, category, material_icon, short_description)
LATEST_APPS = [
    ("detailing-quote-widget", "Detailing Quote Widget",     "Work & Design", "request_quote", "Give detailing customers an instant estimate, then buy a custom-branded version with your prices and booking link."),
    ("meeting-agenda-builder", "Meeting Agenda Builder",      "Productivity & Planning", "event_note",   "Build timed agendas with owners, notes, total meeting length, and copy-ready plain-text or Markdown output."),
    ("decision-matrix", "Decision Matrix",                "Productivity & Planning", "balance",       "Score options against weighted criteria, then rank the results with live totals, percentages, and winning picks."),
    ("unit-circle", "Unit Circle Reference",            "Everyday Tools", "trip_origin",   "Click standard angles to see exact coordinates plus sine, cosine, and tangent values with degree and radian labels."),
    ("quadratic-solver", "Quadratic Solver",              "Everyday Tools", "functions",     "Solve ax² + bx + c = 0 with real or complex roots, full working, discriminant details, and a live parabola graph."),
    ("periodic-table", "Periodic Table",                "Everyday Tools", "science",        "Explore all 118 elements with a clickable layout, category filters, phase markers, and fast detail lookup."),
]

def update_latest_drop():
    index_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(index_path):
        print("SKIP (not found): index.html (latest drop)")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    card_class = (
        'class="group rounded-2xl border border-primary/20 bg-surface-container-low/80 p-6 '
        'backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 hover:border-primary/40 hover:bg-surface-container"'
    )
    cards = ""
    for folder, title, category, icon, desc in LATEST_APPS:
        cat_html = category.replace("&", "&amp;")
        cards += (
            f'      <a href="/South%20Fork%20Apps%20Collection/{folder}/" target="_blank" rel="noopener" {card_class}>\n'
            f'        <div class="mb-5 flex items-start justify-between gap-3">\n'
            f'          <span class="inline-flex rounded-full border border-primary/30 bg-primary/10 px-3 py-1 font-label text-[11px] font-black uppercase tracking-[0.18em] text-primary">New</span>\n'
            f'          <span class="material-symbols-outlined text-3xl text-primary/90">{icon}</span>\n'
            f'        </div>\n'
            f'        <div class="mb-3 text-xs font-black uppercase tracking-[0.18em] text-on-surface-variant">{cat_html}</div>\n'
            f'        <h3 class="mb-3 font-headline text-2xl font-bold text-on-surface">{title}</h3>\n'
            f'        <p class="mb-5 text-sm leading-6 text-on-surface-variant">{desc}</p>\n'
            f'        <span class="font-label text-xs font-black uppercase tracking-[0.18em] text-primary">Launch app</span>\n'
            f'      </a>\n'
        )

    new_content = re.sub(
        r'<!-- LATEST_DROP_START -->.*?<!-- LATEST_DROP_END -->',
        f'<!-- LATEST_DROP_START -->\n{cards}<!-- LATEST_DROP_END -->',
        content,
        flags=re.DOTALL,
    )

    if new_content != content:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("UPDATED: index.html (latest drop)")
    else:
        print("OK: index.html (latest drop)")

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
    base_path = Path(BASE_DIR)
    urls = []

    for index_path in sorted(base_path.rglob("index.html")):
        rel_parts = index_path.relative_to(base_path).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        if rel_parts[0] == "2025":
            continue

        rel = index_path.relative_to(base_path)
        if rel == Path("index.html"):
            urls.append(BASE_URL + "/")
            continue

        parts = [quote(part) for part in rel.parts[:-1]]
        urls.append(f"{BASE_URL}/{'/'.join(parts)}/")

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

    print("\n=== Updating latest drop ===")
    update_latest_drop()

    print("\n=== Building sitemap ===")
    build_sitemap()
    print("\nDone.")
