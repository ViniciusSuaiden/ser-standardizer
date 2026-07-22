[🇺🇸 English](../en/msp_podcast.md) | 🇧🇷 Português

## MSP-PODCAST (guia)

Baixar o formulário de release no site e enviar para a equipe do MSP Lab.

- **Site Oficial:** [MSP Lab - MSP-Podcast](https://lab-msp.com/MSP/MSP-Podcast.html)
- **Licença:** Restrita (apenas pesquisa acadêmica/não comercial).

Após preencher o formulário do site oficial, a equipe do MSP enviará as instruções de download.

## Estrutura de Diretórios Esperada
O parâmetro `input_dir` deve apontar para a pasta raiz contendo a seguinte estrutura:

```text
/caminho/para/seu/dataset/MSP-PODCAST/   <-- O input_dir deve apontar aqui
│
├── Labels/
│   └── labels_consensus.csv     <-- Arquivo de labels agregados (obrigatório)
│
├── Audios/                      <-- Pasta com os áudios (.wav, nomes achatados)
│   ├── MSP-PODCAST_0001_0008.wav
│   └── ...
│
└── Transcripts/                 <-- Pasta com as transcrições (.txt) — opcional
    ├── MSP-PODCAST_0001_0008.txt
    └── ...
```

## Observações

- O loader lê apenas o `Labels/labels_consensus.csv`, que já traz por turno de fala a
  emoção primária de consenso (`EmoClass`), o gênero, o `SpkrID` e a partição sugerida.
  Os arquivos `Audios.tar.gz` **não precisam estar extraídos**: o `file_path` de cada
  amostra é montado a partir do nome do arquivo (`Audios/<nome>.wav`), permitindo
  padronizar os metadados mesmo sem o áudio em disco.
- A partição **Test3** não é distribuída com labels e, portanto, não aparece na saída.
- Falantes sem identificação anotada são mantidos com `speaker_id = "Unknown"`
  (o mesmo vale para `gender = "Unknown"`).
- As transcrições são carregadas apenas se a pasta `Transcripts/` existir; caso contrário,
  `sentence_text` fica vazio.

### Mapeamento de emoções (`EmoClass` → padrão)

| Código | Emoção   | Código | Emoção      |
|--------|----------|--------|-------------|
| N      | Neutral  | F      | Fear        |
| H      | Happy    | D      | Disgust     |
| S      | Sad      | C      | Contempt    |
| A      | Anger    | O      | Other       |
| U      | Surprise | X      | Unknown (No agreement) |
