[🇺🇸 English](../en/emodb.md) | [🇧🇷 Português](../pt-br/emodb.md) | 🇩🇪 Deutsch

## EmoDB (Anleitung)

EmoDB (Berliner Datenbank der emotionalen Sprache) ist ein offener Datensatz emotionaler Sprache auf **Deutsch**, der frei zum Download verfügbar ist.

- **Offizielle Website:** [EmoDB - TU Berlin](http://emodb.bilderbar.info/)
- **Lizenz:** Frei für akademische/nicht-kommerzielle Forschungszwecke (mit Namensnennung).

Laden Sie einfach die `.wav`-Dateien herunter und entpacken Sie sie. Die Suche des Loaders ist **rekursiv**, sodass die offiziellen Ordner (`wav/` oder `EmoDB_1/`/`EmoDB_2/`) problemlos direkt im Stammverzeichnis entpackt werden können.

## Erwartete Verzeichnisstruktur
Der Parameter `input_dir` muss auf das Stammverzeichnis mit den `.wav`-Dateien zeigen (direkt oder in Unterordnern):

```text
/pfad/zu/ihrem/datensatz/EmoDB/    <-- input_dir muss hierhin zeigen
│
├── wav/                           <-- Audio (.wav) — auch im Stammverzeichnis oder in Unterordnern akzeptiert
│   ├── 03a01Fa.wav
│   ├── 03a01Nc.wav
│   └── ...
│
└── ... (andere Ordner wie lablaut/, silb/ werden ignoriert)
```

## Hinweise

- Jeder Dateiname folgt einer festen Konvention aus **7 Zeichen** (`SSTTTEV`):
  - `SS` → Sprechernummer (2 Ziffern);
  - `TTT` → Code des gesprochenen Textes (z. B. `a01`, `b03`);
  - `E` → Anfangsbuchstabe der Emotion (auf Deutsch);
  - `V` → Aufnahmeversion (`a`, `b`, ...), im Schema ignoriert.
- Dateien, deren Namen diesem Muster nicht entsprechen, werden ignoriert.
- Das Geschlecht jedes der 10 Sprecher wird aus der offiziellen Korpusdokumentation ermittelt.
- Die deutschen Sätze zu jedem Textcode werden in `sentence_text` wiederhergestellt.

### Emotionszuordnung (deutscher Anfangsbuchstabe → Standard)

| Code | Deutsch     | Emotion |
|------|-------------|---------|
| W    | Wut         | Anger   |
| L    | Langeweile  | Boredom |
| E    | Ekel        | Disgust |
| A    | Angst       | Fear    |
| F    | Freude      | Happy   |
| T    | Trauer      | Sad     |
| N    | Neutral     | Neutral |
