[🇧🇷 Português](../../datasets/ravdess.md) | 🇺🇸 English

## RAVDESS (guide)

This dataset is open-source and does not require formal approval, it only requires proper attribution (citation).

- **Official Site:** [Zenodo - RAVDESS](https://zenodo.org/records/1188976)
- **Content:** The dataset contains Speech and Song, but this library filters it to keep only the Speech subset.
- **License:** Creative Commons BY-NC-SA 4.0.

For the script to work, we recommend downloading `Audio_Speech_Actors_01-24.zip` (audio and speech only), unzipping it, and making sure the actor folders are at the root.

## Expected Directory Structure
The `input_dir` parameter must point to the root folder containing the actor subfolders (`Actor_XX`), as shown below:

```text
/path/to/your/dataset/RAVDESS/  <-- input_dir must point here
│
├── Actor_01/                   <-- Required folders
│   ├── 03-01-01-01-01-01-01.wav    <-- .wav files
│   ├── 03-01-05-01-02-01-01.wav
│   └── ...
│
├── Actor_02/
├── ...
└── Actor_24/
```
