## MSP-IMPROV (guia)

Baixar o formulário de release no site e enviar para a equipe do MSP Lab.

- **Site Oficial:** [MSP Lab - MSP-IMPROV](https://lab-msp.com/MSP/MSP-Improv.html)
- **Licença:** Restrita (apenas pesquisa acadêmica/não comercial).

Após preencher o formulário do site oficial, a equipe do MSP enviará as instruções de download.

## Estrutura de Diretórios Esperada
O parâmetro `input_dir` deve apontar para a pasta raiz contendo a seguinte estrutura:

```text
/caminho/para/seu/dataset/MSP-IMPROV/   <-- O input_dir deve apontar aqui
│
├── Evaluation.txt              <-- Arquivo de Labels
│
├── All_human_transcriptions/   <-- Pasta com as transcrições (.txt)
│   ├── session1/
│   ├── session2/
│   └── ... 
│
└── Audio/                      <-- Pasta raiz dos áudios (.wav)
    ├── session1/
    ├── session2/
    └── ...
