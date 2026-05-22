# Code Viewer Notes

Created: 2026.05.22
Status: Done

## What It Does

Paste or open any code file and get instant syntax highlighting with line numbers. Split-pane layout: raw input on the left, highlighted output on the right. Language auto-detects or can be set manually from a dropdown covering 20+ languages.

## How to Use

1. Paste code into the left pane or drag a file onto the window
2. Language is auto-detected or select manually from the dropdown
3. Highlighted output appears on the right with line numbers
4. Use "Open File" to load a local file — language is set from the extension automatically
5. "Copy" copies the raw input text

## Notes

- Uses highlight.js 11.9.0 from cdnjs CDN for syntax highlighting (required — no viable inline alternative)
- Theme: Atom One Dark
- Tab key inserts 2 spaces instead of changing focus

## Changelog

- 2026.05.22 — Initial build. Replaces CodeRunner (Setapp).
