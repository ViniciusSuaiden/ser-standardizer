## IEMOCAP (guia)

Este BD requer uma solicitação formal de acesso para fins de pesquisa.

- **Site Oficial:** [SAIL - USC IEMOCAP](https://sail.usc.edu/iemocap/)
- **Solicitação de Acesso:** [Formulário de Release](https://sail.usc.edu/iemocap/iemocap_release.htm)
- **Licença:** Restrita (apenas pesquisa acadêmica/não comercial).

Após preencher o formulário no link acima, a equipe da USC enviará as instruções de download

## Estrutura de Diretórios Esperada
O parâmetro `input_dir` deve apontar para a pasta raiz contendo a seguinte estrutura:

```text
/caminho/para/seu/dataset/IEMOCAP/  <-- O input_dir deve apontar aqui
│
├── Session1/
│   ├── dialog/
│   │   ├── EmoEvaluation/      <-- Labels (.txt)
│   │   ├── transcriptions/     <-- Texto falado (.txt)
│   │   └── wav/                <-- Áudios (.wav organizados por cena)
│
├── Session2/
├── Session3/
├── Session4/
└── Session5/
