# Question packs ("Check for updates")

The app reads `manifest.json` from the public repository
`ronjin-design/ghamgah-hadis-bank` (only when the student taps the update
button on the Profile page). That repository holds exam questions only,
nothing personal. Its `.gitattributes` stores files byte-for-byte so the
SHA-256 checksums stay exact.

## Publishing a pack

1. Add `pack-NNNN.json` with the next version number (format below).
2. `python make_manifest.py <repo folder>` writes `manifest.json` with each
   pack's SHA-256 and format.
3. Commit and push both files. GitHub may take about five minutes to serve
   them.

## Pack format

```json
{
  "version": 2,
  "format": 2,
  "subjects": [
    {"key": "English", "fa": "زبان انگلیسی", "tr": "Zaban-e Engelisi", "sort_order": 4}
  ],
  "questions": [{
    "subject": "Biology",
    "session": "1404-Khordad",
    "number": 12,
    "topic_tag": "dna-replication",
    "total_points": 1.0,
    "source": "official",
    "correction": false,
    "textbook": {"fa": "...", "en": "...", "tr": "...", "pages": "8–14"},
    "text": {
      "fa": {"topic_label": "...", "question": "...", "grading_key": "- [0.5] ...\n- [0.5] ...",
             "final_resolution": "...", "notes": "", "keywords": ["..."]},
      "en": {"...": "same fields"},
      "tr": {"...": "same fields"}
    }
  }]
}
```

- **Format 1** (the default when `format` is missing) has questions for
  existing subjects at real sittings only.
- **Format 2** (app 2.6.0+) adds three things:
  - **Mock exams**: `session` like `1404-Mock2` ("Mock exam 2 · 1404"). They
    show under Exam marathons, after that year's real sittings.
  - **New subjects**: listed in `subjects`. `key` is the English name. An
    existing subject is never renamed.
  - **Corrections**: `"correction": true` rewrites the question with the
    same subject, session and number in place (text, answer, grading key,
    textbook). Her progress, draft, notes and speed runs on it stay attached.
- **Distractors** (optional, app 3.1.0+): each language block may add
  `"distractors": ["…", "…", "…"]`, three or more wrong answers for the
  multiple-choice Crucible. They must be distinct and must not repeat
  `final_resolution`. Without them the app uses three keywords from the same
  subject's Codex. Older apps ignore the field, so the format stays 2.
- A pack with a newer `format` than the app knows stops the update there, and
  the app asks her to update. Packs before it are still applied.

## Rules, checked before anything is written

- `subject` must exist, or be added by the same pack.
- `session` is `<year>-<Khordad|Shahrivar|Dey>` or `<year>-Mock<n>`.
- `number` 0 or 901+ means the paper number is unknown. Subject, session and
  number together must be unique.
- All three languages are required, with the same grading steps, summing to
  `total_points`.
- One bad entry rejects the whole pack, and her bank stays as it was.

Without `correction`, a question already on the phone is skipped, never
overwritten. A pack never changes her profile, notes, progress, streak,
speed runs, exam dates or bookmarks.
