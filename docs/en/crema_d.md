🇺🇸 English | [🇧🇷 Português](../pt-br/crema_d.md)

## CREMA-D (guide)

The data is hosted on GitHub, but the audio files use **Git LFS (Large File Storage)**.

- **Official GitHub:** [CheyneyComputerScience/CREMA-D](https://github.com/CheyneyComputerScience/CREMA-D)
- **License:** Open Database License (ODbL)

### ⚠️ Important: do not download the ZIP!
If you use the **"Download ZIP"** button from the GitHub web interface, the `.wav` files **will not be downloaded correctly**. You will only get "pointers" (small text files) referencing Git LFS, which makes the loader fail.

**Correct download method:**
Make sure you have `git-lfs` installed and clone the repository from the terminal:

```bash
# 1. Install LFS support (if you don't have it)
git lfs install

# 2. Clone the repository
git clone https://github.com/CheyneyComputerScience/CREMA-D.git
```

## Expected Directory Structure
For the loader to work correctly, **do not rename** the key internal files (`VideoDemographics.csv` and `finishedResponses.csv`) nor the audio folder (`AudioWAV`).

The `input_dir` parameter must point to the root folder with the following structure:

```text
/path/to/your/dataset/CREMA-D/  <-- input_dir must point here
│
├── AudioWAV/                   <-- Required folder with the .wav files
│   ├── 1001_DFA_ANG_XX.wav
│   ├── 1001_DFA_DIS_XX.wav
│   └── ...
│
├── VideoDemographics.csv       <-- Required (actor metadata)
├── finishedResponses.csv       <-- Required (ratings/labels)
│
└── ... (other files are ignored)
```
