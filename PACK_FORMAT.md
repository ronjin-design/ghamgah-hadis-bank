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
- **Format 3** (app 3.6.0+) adds the chapter reader's content. A format 3
  pack may hold only these, with no questions:
  - **`reader_cards`**: short concept cards for a chapter, in our own words
    (never copied textbook text):
    `{"subject": "Biology", "chapter": 2, "position": 1, "key": "bio-2-membrane",
    "title": {"fa": "…", "en": "…", "tr": "…"}, "body": {"fa": "…", "en": "…", "tr": "…"}}`.
    Codex terms in the body become tap-links on their own.
  - **`barom`**: Ministry Barom-Bandi notes for a chapter, only from
    official keys:
    `{"subject": "Biology", "chapter": 2, "key": "bio-2-transport", "points": 1.25,
    "source": "1403-Khordad Q7", "topic": {"fa": "…", "en": "…", "tr": "…"},
    "note": {"fa": "…", "en": "…", "tr": "…"}}` (`note` is optional).
  - `chapter` is 1 or more. `key` is unique within the pack. A later pack
    with the same subject and `key` replaces the card or note.
  - `points` must be a positive multiple of 0.25, and `source` is required.
  - The reader also builds its Official Examiners' View from the official
    grading keys already in the bank, so it is never empty for a chapter
    with real questions.
- **Format 4** (app 3.11.0+) adds structured **`lessons`**: a chapter taught
  in ordered units, each with explanations, formulas, worked examples, exam
  traps and the bank questions that practise it. A format 4 pack may hold
  only lessons. Publish one only after the phone has the app that reads it:
  an older app stops at it, and every pack after it waits too.

  ```json
  "lessons": [{
    "subject": "Mathematics", "chapter": 1, "unit": 1, "key": "math-1-domain-range",
    "title":   {"fa": "…", "en": "…", "tr": "…"},
    "summary": {"fa": "…", "en": "…", "tr": "…"},
    "blocks": [
      {"type": "explain", "title": {…}, "body": {…}},
      {"type": "formula", "math": "√g(x)  ⟹  g(x) ≥ 0", "caption": {…}},
      {"type": "example", "title": {…},
       "steps": [{"text": {…}, "math": "x(x − 2) ≥ 0"}, {"text": {…}}],
       "answer": {…}},
      {"type": "trap", "body": {…}}
    ],
    "questions": [{"session": "1401-Dey", "number": 977}]
  }]
  ```

  - `chapter` and `unit` are 1 or more; units show in `unit` order. `key` is
    unique in the pack, and a later pack with the same subject and `key`
    replaces the whole unit.
  - Every `{…}` is fa, en and tr, all non-empty. `summary`, a block's
    `title`, a formula's `caption`, a step's `math` and an example's `answer`
    are optional; everything else is required.
  - Block types are `explain`, `formula`, `example` (at least one step) and
    `trap`, at least one block per unit. Any other type rejects the pack.
  - Math is plain Unicode in one shared string (`math`), shown left to right
    in all three languages: `√`, `²`, `³`, `∘`, `≥`, `≠`, `ℝ`, `∈`, `⟹`.
    Write inverses as `f^(−1)`: no superscript letters or signs. Inside
    text, put math between backticks (`` `f(x) = 2x + 4` ``) so it reads left
    to right inside a Persian sentence; backticks must pair up.
  - `questions` names bank questions of the same subject by session and
    number, in practice order (an empty list is allowed). The app skips one
    it does not have yet. Explanations and examples are in our own words,
    never copied textbook text, and examples never add new exam questions.
- **Format 5** (app 3.12.0+) adds one lesson block, **`diagram`**: a text
  picture (mapping arrows, a horizontal line test, a sign chart, the unit
  circle) shared by all three languages:
  `{"type": "diagram", "art": "  x --> f(x)\n  1 -->  3", "caption": {…}}`.
  - `art` is plain ASCII only (no Persian, no Greek letters: write `pi`), at
    most 36 characters per line and 22 lines. The app shows it in a
    fixed-width font, left to right, never wrapped, and shrinks it to fit the
    screen instead of overflowing. `caption` is optional.
  - Everything else is as in format 4. A pack with a diagram must say
    `"format": 5`; as before, publish it only after the phone has the app
    that reads it.
- **Format 6** (app 3.14.0+) adds **`glossary`**: Pocket Tutor entries that
  turn a Codex term into a micro-lesson.

  ```json
  {"version": 119, "format": 6, "glossary": [
    {"subject": "Biology", "key": "bio-allele",
     "term": {"fa": "دگره", "en": "allele", "tr": "degare"},
     "matches": {"fa": ["الل"], "en": ["alleles"], "tr": ["allel"]},
     "explain": {…}, "analogy": {…}, "contrast": {…},
     "unit": "bio-3-mendel"}
  ]}
  ```

  - The app still builds the Codex from question keywords; an entry attaches
    to a Codex term when the term itself matches the entry's `term` or one of
    its `matches` in any language (ignoring case, half-spaces and
    diacritics). It never matches through the Codex's translations (they
    pair keywords by position, and some lists do not line up in meaning), so
    list every keyword spelling the bank uses in `matches`. Terms with no
    entry look as before.
  - `term` is fa, en and tr, plain words (no backticks). `matches` is
    optional: extra spellings per language, each a non-empty word.
  - `explain` is required; `analogy` ("Picture it") and `contrast` ("Don't
    confuse it with…") are optional. They follow the lesson text rules:
    fa, en and tr, inline math between paired backticks.
  - `unit` is optional: a lesson unit key of the same subject. The entry
    shows a button into that unit once the phone has it.
  - `key` is unique in the pack; a later pack with the same subject and
    `key` replaces the entry. A pack with glossary entries must say
    `"format": 6`.
- **Format 7** (app 3.16.1+) adds an optional **`anim`** id to a `diagram`
  block: `{"type": "diagram", "art": "...", "caption": {...}, "anim": "phys.bohr"}`.
  The app then shows a built-in animation in place of the text picture, with
  pause and "text version" buttons; the text art stays required and is shown
  with reduce-motion on or for an id the app does not know yet.
  - `anim` is lower-case letters, digits, `.` and `-`, at most 48
    characters. Built-in ids (3.16.1): `phys.motion-graphs`, `phys.spring-shm`,
    `phys.wave-types`, `phys.refraction`, `phys.bohr`, `chem.galvanic`,
    `chem.equilibrium`, `chem.collisions`, `chem.micelle`,
    `bio.replication-fork`, `bio.ribosome`, `bio.atp-synthase`.
  - A pack using `anim` must say `"format": 7`, so older apps stop and ask
    for the update instead of storing the unit without its animation (a
    stored unit is not fetched again). Re-issue a unit by its `key`, copied
    unchanged from its latest pack plus the `anim` field (pack 144 does this).
- **Persian 3** ships with app 3.6.0 under the key `Persian` (packs do not
  need to add it). It has three final-exam components, as `topic_tag`:
  `vocabulary` (shown as flashcards: `question` on the front,
  `final_resolution` on the back), `literary-devices` and `thematic-pairs`.
  Lessons go in `textbook` as «درس N» / "Lesson N".
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

## Exam schedule (`exams.json`, app 3.8.0+)

The examiner's desk in the app writes this file and it is published here.
The student's app reads it when it opens and when she checks for updates,
then counts down to each exam in her phone's own time zone.

```json
{"format": 1, "exams": [
  {"id": "BIO-20261110-0900", "subject": "Biology", "session": "1403-Khordad",
   "minutes": 90, "track": "concierge", "unlock_at": "2026-11-10T05:30:00Z"}
]}
```

- `unlock_at` is UTC and must end in `Z`.
- `track` is `concierge` (photos sent for marking) or `sandbox` (she marks
  herself with the Barom-Bandi).
- Only ids, papers and times go here, nothing about the student.
- An exam removed from the file disappears from her phone unless she has
  already sat it. Each exam can be sat once.
- Publish with `python tool/release/publish_exams.py exams.json` from the
  app repository.

## Subjects (app 3.9.0+)

The app ships ten subjects. A pack must use these exact `subject` keys:

| Key | Subject | Board time |
|---|---|---|
| `Biology` | زیست‌شناسی ۳ | 90 min |
| `Chemistry` | شیمی ۳ | 100 min |
| `Physics` | فیزیک ۳ | 100 or 120 min |
| `English` | زبان انگلیسی ۳ | 90 or 120 min |
| `Persian` | ادبیات فارسی ۳ | 90 or 120 min |
| `Mathematics` | ریاضیات ۳ | 120 min |
| `Religion and Life` | دین و زندگی ۳ | 90 min |
| `Arabic` | عربی ۳ | 75 min |
| `Health and Hygiene` | سلامت و بهداشت | 90 min |
| `Social Identity` | هویت اجتماعی | 75 min |

Every board paper is out of 20 with no negative marking. English, Persian,
Religion and Life, Arabic, Health and Hygiene, and Social Identity count in
lessons («درس N» / "Lesson N"); the others count in chapters («فصل N» /
"Chapter N").

A pack for the five newest subjects should also list the subject in
`subjects` (as pack 56 does for Persian). Apps older than 3.9 can then add
the subject instead of stopping on an unknown key.

