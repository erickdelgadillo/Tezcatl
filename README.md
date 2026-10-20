# TEZCATL 🪞

**Reflecting and preserving digital memories.**

A Python toolkit for photo deduplication, EXIF metadata extraction, chronological organization, and digital archive management.

*Tezcatl* means **mirror** in Classical Nahuatl.

> [!WARNING]
> **Legacy code — not safe for use on an irreplaceable photo collection.** Some scripts permanently delete or move files without a dry run, backup, or rollback. Work only on disposable copies. These files are preserved for educational and historical purposes.

## Origins

The five scripts in `legacy/` were developed in **October 2024** as an early Python learning exercise, with guidance from ChatGPT. They are preserved here **without modification** to document the project's beginnings and provide a starting point for a safer implementation.

## Original workflow

| Step | Script | Function |
| --- | --- | --- |
| 1 | [Delete duplicates](legacy/Step1_delete_duplicates.py) | Compute MD5 hashes and remove subsequent matching files. |
| 2 | [Remove JPG with NEF](legacy/Step2_delete_JPG_whit_NEF.py) | Delete JPG files when a NEF with the same base name exists in the same directory. |
| 3 | [Folder organization](legacy/Step3_folder_organization.py) | Read EXIF timestamps and organize images in year/month folders. |
| 4 | [Rename images](legacy/Step4_rename.py) | Rename images using camera model, date, and chronological sequence number. |
| 5 | [Check results](legacy/Step5_Check_results.py) | Compare two archives by EXIF timestamps and copy images that have timestamps unique to one archive. |

These are manually run historical scripts, **not** a validated end-to-end pipeline.

## Structure

```text
Tezcatl/
├── legacy/            # Original 2024 scripts
├── src/               # Future implementation
├── tests/             # Future automated tests
├── docs/              # Documentation and design notes
├── .gitignore
└── README.md
```

## Legacy requirements

- Python 3.8+ (uses the assignment expression `:=`).
- `exifread` package for steps 3–5: `pip install exifread`.
- Original hard-coded Windows paths must be adapted for any local testing.
- Steps 3–4 set `es_ES.utf8` locale; this may not be available on all systems.

## Known issues

- **Step 1:** irreversible deletion, no dry run or manifest; retains the first duplicate encountered.
- **Step 2:** assumes `.JPG` uppercase when constructing paths, and deletes JPEG versions that may have distinct edits.
- **Step 3:** may revisit moved images while traversing directories; destination collisions are not explicitly handled.
- **Step 4:** numbering depends on available files and may change between runs.
- **Step 5:** EXIF capture timestamps are **not** unique file identifiers; unrelated images can share timestamps and missing EXIF timestamps are mishandled. Output filename collisions are possible.
- No automated tests, cross-platform configuration, or robust recovery strategy.

## Development roadmap

- [ ] Add a read-only photo inventory and default `--dry-run`.
- [ ] Replace timestamp-based duplicate comparisons with verified file-content hashes.
- [ ] Preserve RAW/JPEG pairs by default.
- [ ] Add stable collision-resistant naming, audit logs, and a recoverable change manifest.
- [ ] Introduce a cross-platform CLI and configuration.
- [ ] Add tests and fixture images.
- [ ] Support CSV/JSON metadata export for scientific and personal archiving.

## Current status

**Historical archive; redesign planned.** No stable release or production-safe tool is available.
