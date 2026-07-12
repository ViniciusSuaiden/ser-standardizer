[🇧🇷 Português](../../datasets/iemocap.md) | 🇺🇸 English

## IEMOCAP (guide)

This database requires a formal access request for research purposes.

- **Official Site:** [SAIL - USC IEMOCAP](https://sail.usc.edu/iemocap/)
- **Access Request:** [Release Form](https://sail.usc.edu/iemocap/iemocap_release.htm)
- **License:** Restricted (academic/non-commercial research only).

After filling out the form at the link above, the USC team will send you the download instructions.

## Expected Directory Structure
The `input_dir` parameter must point to the root folder with the following structure:

```text
/path/to/your/dataset/IEMOCAP/  <-- input_dir must point here
│
├── Session1/
│   ├── dialog/
│   │   ├── EmoEvaluation/      <-- Labels (.txt)
│   │   ├── transcriptions/     <-- Spoken text (.txt)
│   │   └── wav/                <-- Audio (.wav organized by scene)
│
├── Session2/
├── Session3/
├── Session4/
└── Session5/
```
