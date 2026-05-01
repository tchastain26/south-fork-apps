# Personal Newspaper — App Idea

**Source:** Inbox (Personal newspaper.md, captured from podcast transcript)

## The Idea
A personalized daily front page delivered every morning at 5am. Looks like a newspaper. Built from RSS feeds (not Matter/Notion). AI summarizes articles. Weather in the corner. Local news included.

Tucker doesn't like the name "Daily Star" — should be something personal. Candidates: The Bluff City Bulletin, The Magpie Morning, The Chastain Chronicle, The Morning Fork.

## Feature Set (from transcript)
- Morning edition: 10 articles at 5am
- Evening edition: 5 articles + one long read
- Magazine-style layout with images pulled from articles
- Small weather widget in corner
- AI summaries for each article (so you can skim without jumping to another app)
- If an article is a product link: auto-fetch the product page and summarize what it is
- Priority/ranking logic decides which articles to show and in what order
- Single-page format — everything in one place

## Sources
- RSS feeds (Tucker's existing curated list from podcast pipeline or Reeder/NetNewsWire)
- No Matter or Notion dependency

## Build Approach
- Python script runs at 5am via launchd, generates a static HTML file
- Script reads RSS feeds, fetches article text (Diffbot / defunnel API / trafilatura), sends to Ollama (local) or Claude API for summaries
- Writes output to a local HTML file that auto-opens in browser, OR serves it via a persistent local web server
- Weather from Open-Meteo (free, no API key)

## Priority
High interest, medium complexity. Would replace morning browsing across apps.
