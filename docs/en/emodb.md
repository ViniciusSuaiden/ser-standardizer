🇺🇸 English | [🇧🇷 Português](../pt-br/emodb.md) | [🇩🇪 Deutsch](../de/emodb.md)

## EmoDB (guide)

EmoDB (Berlin Database of Emotional Speech) is an open emotional speech dataset in **German**, freely available for download.

- **Official Site:** [EmoDB - TU Berlin](http://emodb.bilderbar.info/)
- **License:** Free for academic/non-commercial research use (with attribution).

Just download and unzip the `.wav` files. The loader search is **recursive**, so the official folders (`wav/`, or `EmoDB_1/`/`EmoDB_2/`) can be extracted inside the root without any problem.

## Expected Directory Structure
The `input_dir` parameter must point to the root folder containing the `.wav` files (directly or in subfolders):

```text
/path/to/your/dataset/EmoDB/    <-- input_dir must point here
│
├── wav/                        <-- Audio (.wav) — also accepted at the root or in subfolders
│   ├── 03a01Fa.wav
│   ├── 03a01Nc.wav
│   └── ...
│
└── ... (other folders such as lablaut/, silb/ are ignored)
```

## Notes

- Each file name follows a fixed **7-character** convention (`SSTTTEV`):
  - `SS` → speaker number (2 digits);
  - `TTT` → spoken-text code (e.g., `a01`, `b03`);
  - `E` → emotion initial (in German);
  - `V` → recording take (`a`, `b`, ...), ignored in the schema.
- Files whose names do not match this pattern are ignored.
- The gender of each of the 10 speakers is resolved from the official corpus documentation.
- The German sentences associated with each text code are restored into `sentence_text`.

### Emotion mapping (German initial → standard)

| Code | German      | Emotion |
|------|-------------|---------|
| W    | Wut         | Anger   |
| L    | Langeweile  | Boredom |
| E    | Ekel        | Disgust |
| A    | Angst       | Fear    |
| F    | Freude      | Happy   |
| T    | Trauer      | Sad     |
| N    | Neutral     | Neutral |
