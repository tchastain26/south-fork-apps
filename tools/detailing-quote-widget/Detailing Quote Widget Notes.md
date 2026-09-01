# Detailing Quote Widget Notes

Created: 2026.09.01
Status: Done

## Idea Brief

### Category

Work & Design

### One-Sentence Job

Give a mobile detailing customer an immediate price range and a clear booking action without requiring a phone call.

### Inputs

- Vehicle type
- Detailing package
- Vehicle condition
- Optional add-ons
- Optional business name and booking URL supplied through safe query parameters

### Outputs

- Estimated price range
- Itemized estimate
- Copy-ready quote summary
- Booking or contact action

### Core Interaction

Choose a vehicle, package, condition, and add-ons. The estimate updates immediately. Copy the estimate or request a booking.

### South Fork Fit

- Single-file HTML
- Public demo with no account
- Useful in under 30 seconds
- Works on mobile and desktop
- All estimate logic runs locally

### Theme Notes

- South Fork dark palette and green accent
- Compact tool-first layout
- Top navigation links to South Fork Apps
- Version marker v1.0

### Security and Privacy Notes

- No analytics, accounts, cookies, uploads, or third-party APIs
- Query parameters are read as text and never inserted through `innerHTML`
- Booking URLs accept only `http:`, `https:`, `mailto:`, and `tel:` protocols
- Clipboard writes require a button click
- PayPal opens only after a direct user click

### Edge Cases

- Empty selection: defaults produce a valid estimate
- Invalid query parameter: ignored or reduced to safe text
- Very long business name: limited to 60 characters and allowed to wrap
- Mobile layout: columns collapse to one

### Acceptance Check

- Estimate changes for every control
- Copy button reports success or fallback instructions
- Purchase and contact links are visible
- No console errors
- No horizontal overflow on phone-sized screens

## What It Does

This is a live sales demo and reusable white-label quote widget for mobile detailing businesses. It calculates an estimate from a vehicle type, service package, condition, and add-ons. Prospects can preview the tool with their own business name through a query parameter. The commercial offer is a custom branded and configured copy for $49 once, delivered within 24 hours.

## How to Use

Open the page and change the vehicle, package, condition, or add-ons. Use Copy estimate to copy the itemized result. Add `?brand=Business%20Name` to the URL for a personalized preview. Optional `contact` and `contactLabel` query parameters can replace the demo booking link when the contact URL uses an approved protocol.

## Changelog

- 2026.09.01 - Initial build and $49 white-label offer
- 2026.09.01 - Passed desktop, 390 px mobile, calculation, clipboard, console, and query-parameter safety checks
