## CREMA-D (guia)

Os dados estão hospedados no GitHub, mas utilizam **Git LFS (Large File Storage)** para os arquivos de áudio.

- **GitHub Oficial:** [CheyneyComputerScience/CREMA-D](https://github.com/CheyneyComputerScience/CREMA-D)
- **Licença:** Open Database License (ODbL)

### ⚠️ Importante: Não baixe o ZIP!
Se você utilizar o botão **"Download ZIP"** da interface web do GitHub, os arquivos `.wav` **não serão baixados corretamente**. Você receberá apenas "ponteiros" (arquivos de texto pequenos) referenciando o Git LFS, o que fará o loader falhar.

**Método correto de download:**
Certifique-se de ter o `git-lfs` instalado e clone o repositório via terminal:

```bash
# 1. Instale o suporte a LFS (caso não tenha)
git lfs install

# 2. Clone o repositório
git clone https://github.com/CheyneyComputerScience/CREMA-D.git
```

## Estrutura de Diretórios Esperada
Para que o loader funcione corretamente, **não renomeie** os arquivos internos chave (`VideoDemographics.csv` e `finishedResponses.csv`) nem a pasta de áudio (`AudioWAV`).

O parâmetro `input_dir` deve apontar para a pasta raiz contendo a seguinte estrutura:

```text
/caminho/para/seu/dataset/CREMA-D/  <-- O input_dir deve apontar aqui
│
├── AudioWAV/                   <-- Pasta obrigatória com os arquivos .wav
│   ├── 1001_DFA_ANG_XX.wav
│   ├── 1001_DFA_DIS_XX.wav
│   └── ...
│
├── VideoDemographics.csv       <-- Obrigatório (metadados dos atores)
├── finishedResponses.csv       <-- Obrigatório (avaliações/labels)
│
└── ... (outros arquivos são ignorados)
