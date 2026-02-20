## RAVDESS (guia)

Este dataset é open-source e não requer aprovação formal, apenas exige atribuição correta (citação).

- **Site Oficial:** [Zenodo - RAVDESS](https://zenodo.org/records/1188976)
- **Conteúdo:** O dataset contém Fala (Speech) e Canto (Song), mas esta biblioteca o filtra para conter apenas a Fala (Speech).
- **Licença:** Creative Commons BY-NC-SA 4.0.

Para que o script funcione, recomenda-se baixar o arquivo Audio_Speech_Actors_01-24.zip (apenas áudio e fala), descompactá-lo e garantir que as pastas dos atores estejam na raiz.

## Estrutura de Diretórios Esperada
O parâmetro input_dir deve apontar para a pasta raiz contendo as subpastas dos atores (Actor_XX), conforme a estrutura abaixo:

```text
/caminho/para/seu/dataset/RAVDESS/  <-- O input_dir deve apontar aqui
│
├── Actor_01/                       <-- Pastas obrigatórias
│   ├── 03-01-01-01-01-01-01.wav    <-- Arquivos .wav
│   ├── 03-01-05-01-02-01-01.wav
│   └── ...
│
├── Actor_02/
├── ...
└── Actor_24/
