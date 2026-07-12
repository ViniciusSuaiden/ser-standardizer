[🇧🇷 Português](../../datasets/msp_podcast.md) | 🇺🇸 English

## MSP-PODCAST (guide)

Download the release form on the site and send it to the MSP Lab team.

- **Official Site:** [MSP Lab - MSP-Podcast](https://lab-msp.com/MSP/MSP-Podcast.html)
- **License:** Restricted (academic/non-commercial research only).

After filling out the form on the official site, the MSP team will send the download instructions.

## Expected Directory Structure
The `input_dir` parameter must point to the root folder with the following structure:

```text
/path/to/your/dataset/MSP-PODCAST/   <-- input_dir must point here
│
├── Labels/
│   └── labels_consensus.csv     <-- Aggregated labels file (required)
│
├── Audios/                      <-- Folder with the audio (.wav, flattened names)
│   ├── MSP-PODCAST_0001_0008.wav
│   └── ...
│
└── Transcripts/                 <-- Folder with the transcriptions (.txt) — optional
    ├── MSP-PODCAST_0001_0008.txt
    └── ...
```

## Notes

- The loader only reads `Labels/labels_consensus.csv`, which already provides, per speaking
  turn, the consensus primary emotion (`EmoClass`), gender, `SpkrID` and the suggested
  partition. The `Audios.tar.gz` archive **does not need to be extracted**: each sample's
  `file_path` is built from the file name (`Audios/<name>.wav`), so the metadata can be
  standardized even without the audio on disk.
- The **Test3** partition is not distributed with labels and therefore does not appear in the output.
- Speakers without an annotated identity are kept with `speaker_id = "Unknown"`
  (the same applies to `gender = "Unknown"`).
- Transcriptions are loaded only if the `Transcripts/` folder exists; otherwise
  `sentence_text` is left empty.

### Emotion mapping (`EmoClass` → standard)

| Code | Emotion  | Code | Emotion     |
|------|----------|------|-------------|
| N    | Neutral  | F    | Fear        |
| H    | Happy    | D    | Disgust     |
| S    | Sad      | C    | Contempt    |
| A    | Anger    | O    | Other       |
| U    | Surprise | X    | Unknown (No agreement) |
