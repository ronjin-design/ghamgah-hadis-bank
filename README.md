# Ghamgah-E-Hadis question packs

Question packs for the Ghamgah-E-Hadis exam-prep app. The app downloads
`manifest.json` when the student taps «به‌روزرسانی بانک سوالات» (Check for
updates), then fetches any new `pack-NNNN.json`. Every pack is verified
against its SHA-256 in the manifest. Questions are only ever added; nothing
on the phone is overwritten.

This repository holds exam questions only. No personal data is stored here.

## Publishing a pack

1. Add `pack-NNNN.json` with the next version number. The format is described
   in `tool/bank/README.md` in the app repository.
2. Run `python make_manifest.py .`.
3. Commit and push `pack-NNNN.json` and `manifest.json` together.
