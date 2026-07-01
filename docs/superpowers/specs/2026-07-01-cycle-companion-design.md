# Cycle Companion — Design Spec

**Date:** 2026-07-01  
**Status:** Approved  
**Approach:** Option A — Vanilla PWA (no build step)

## Purpose

A private, mobile-first cycle tracking micro app for a partner to log period start dates and see the current cycle phase with actionable support tips — so they know when and how to be more supportive.

## Users

- **v1:** Partner logs period starts (wife tells them verbally).
- **v2 (future):** Wife logs her own details; partner sees a dedicated support-focused view. Data model and storage layer designed to support this without a rewrite.

## Platform

- Phone browser, installable as PWA (Add to Home Screen).
- Offline-capable via service worker.
- Static hosting (GitHub Pages, Netlify, or local file open).

## v1 Features

### Home screen
- Current cycle day and phase name (Period / Follicular / Ovulation / Luteal / PMS).
- Visual progress bar through the current cycle.
- Days until predicted next period.
- 2–3 phase-specific support tips (warm, practical, non-clinical).
- One prominent **"Period started today"** log button.

### Phase logic
- Default 28-day cycle, 5-day period until enough data is logged.
- After 2+ logged period starts, average cycle length is calculated from intervals.
- Phases derived from cycle day and learned lengths.

| Phase     | Timing                                      |
|-----------|---------------------------------------------|
| Period    | Days 1 through period length (default 5)    |
| Follicular| After period until ovulation window           |
| Ovulation | ~3 days around mid-cycle                    |
| Luteal    | After ovulation until PMS window            |
| PMS       | Last 5 days before predicted next period    |

### Onboarding
- If no cycles logged, prompt to log the most recent period start date.

## Out of scope (v1)

- Dual-user / wife login
- Push notifications
- Calendar history view
- Cloud sync / accounts
- Symptom or mood tracking

## Architecture

```
cycle-companion/
├── index.html      # UI layout
├── styles.css      # Mobile-first styling
├── app.js          # UI logic and rendering
├── cycle.js        # Phase math and predictions
├── storage.js      # localStorage adapter (cloud-ready)
├── tips.js         # Phase-specific support copy
├── sw.js           # Service worker
├── manifest.json   # PWA metadata
└── icons/          # App icons
```

### Storage adapter (`storage.js`)

All UI code reads/writes through a `Storage` object. v2 can swap the implementation for a cloud API without touching UI or cycle logic.

```javascript
Storage.getCycles()
Storage.saveCycle(cycle)
Storage.getSettings()
Storage.saveSettings(settings)
```

### Data model

```json
{
  "cycles": [
    { "startDate": "2026-06-01" }
  ],
  "settings": {
    "defaultCycleLength": 28,
    "defaultPeriodLength": 5
  }
}
```

## UI

- Mobile-first, large tap targets.
- Warm palette: rose and sage tones on a soft background.
- Readable typography, minimal chrome.
- Tips rotate within each phase on each app open.

## Deployment

Serve the `cycle-companion/` folder as static files. No build step required.

## Future (v2 hooks)

- `Storage` adapter interface for cloud sync
- `users` array and `syncEnabled` flag in data model (unused in v1)
- Optional calendar/history view
- Wife-facing logging UI
