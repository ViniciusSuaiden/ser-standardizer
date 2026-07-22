🇺🇸 English | [🇧🇷 Português](../pt-br/msp_improv.md)

## MSP-IMPROV (guide)

Download the release form on the site and send it to the MSP Lab team.

- **Official Site:** [MSP Lab - MSP-IMPROV](https://lab-msp.com/MSP/MSP-Improv.html)
- **License:** Restricted (academic/non-commercial research only).

After filling out the form on the official site, the MSP team will send the download instructions.

## Expected Directory Structure
The `input_dir` parameter must point to the root folder with the following structure:

```text
/path/to/your/dataset/MSP-IMPROV/   <-- input_dir must point here
│
├── Evaluation.txt              <-- Labels file
│
├── All_human_transcriptions/   <-- Folder with the transcriptions (.txt)
│   ├── session1/
│   ├── session2/
│   └── ...
│
└── Audio/                      <-- Root audio folder (.wav)
    ├── session1/
    ├── session2/
    └── ...
```
