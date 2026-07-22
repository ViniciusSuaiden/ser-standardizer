[🇺🇸 English](../en/emodb.md) | 🇧🇷 Português | [🇩🇪 Deutsch](../de/emodb.md)

## EmoDB (guia)

O EmoDB (Berlin Database of Emotional Speech) é um dataset aberto de fala emocional em **alemão**, de download livre.

- **Site Oficial:** [EmoDB - TU Berlin](http://emodb.bilderbar.info/)
- **Licença:** Uso livre para fins de pesquisa acadêmica/não comercial (com atribuição).

Basta baixar e descompactar os arquivos `.wav`. A busca do loader é **recursiva**, então as pastas oficiais (`wav/`, ou `EmoDB_1/`/`EmoDB_2/`) podem ser extraídas dentro da raiz sem problema.

## Estrutura de Diretórios Esperada
O parâmetro `input_dir` deve apontar para a pasta raiz que contém os arquivos `.wav` (diretamente ou em subpastas):

```text
/caminho/para/seu/dataset/EmoDB/    <-- O input_dir deve apontar aqui
│
├── wav/                            <-- Áudios (.wav) — também aceito na raiz ou em subpastas
│   ├── 03a01Fa.wav
│   ├── 03a01Nc.wav
│   └── ...
│
└── ... (outras pastas como lablaut/, silb/ são ignoradas)
```

## Observações

- O nome de cada arquivo segue um padrão fixo de **7 caracteres** (`SSTTTEV`):
  - `SS` → número do locutor (2 dígitos);
  - `TTT` → código do texto falado (ex.: `a01`, `b03`);
  - `E` → inicial da emoção (em alemão);
  - `V` → versão da gravação (`a`, `b`, ...), ignorada no schema.
- Arquivos com nome fora desse padrão são ignorados.
- O gênero de cada um dos 10 locutores é resolvido pela documentação oficial do corpus.
- As frases em alemão associadas a cada código de texto são restauradas em `sentence_text`.

### Mapeamento de emoções (inicial alemã → padrão)

| Código | Alemão      | Emoção  |
|--------|-------------|---------|
| W      | Wut         | Anger   |
| L      | Langeweile  | Boredom |
| E      | Ekel        | Disgust |
| A      | Angst       | Fear    |
| F      | Freude      | Happy   |
| T      | Trauer      | Sad     |
| N      | Neutral     | Neutral |
