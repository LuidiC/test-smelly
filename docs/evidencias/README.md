# Evidências de execução

Saídas capturadas de comandos reais, sem fabricação de prints. Os caminhos locais refletem o ambiente.

| Arquivo | Comando e interpretação |
| --- | --- |
| `01-jest-original.txt` | `npm test -- --runInBand` antes de refatorar/mover: 4 aprovados, 1 ignorado. |
| `02-eslint-inicial.txt` | Primeira execução de `npx eslint .`, antes da suíte limpa: 4 erros, 2 avisos; saída 1. |
| `03-eslint-clean.txt` | `npx eslint __tests__/userService.clean.test.js --max-warnings=0`: sem diagnósticos, saída 0. |
| `04-jest-final.txt` | `npm test`: 22 aprovados, 1 ignorado no original, 2 suítes aprovadas; saída 0. |
| `04a-jest-restricao-do-ambiente.txt` | Tentativa no sandbox falhou por `EPERM` no cache, sem executar testes. |
| `05-eslint-final.txt` | `npx eslint .`: mesmos diagnósticos, só no original; saída 1 esperada. |
| `06-cobertura-clean.txt` | `npm run coverage -- --runInBand --collectCoverageFrom=src/userService.js --testPathPattern=userService.clean.test.js`: 18 aprovados; quatro métricas em 100%. |
| `07-mutacoes-dirigidas.txt` | Controle e seis defeitos deliberados em cópias temporárias; todos detectados pela limpa. Inclui a saída real das falhas esperadas. |
| `08-reproducibilidade.txt` | `npm ci --offline --cache ../.tools/npm-cache --no-audit --no-fund`, seguido de `npm test` e `npm run lint:clean`: instalação pelo lockfile, testes e lint limpo com código 0. O cache local foi usado apenas para evitar novo download. |
| `09-eslint-reproducao.txt` | Nova execução real de `npx eslint .`, após a refatoração: 4 erros e 2 avisos exclusivamente no original; saída 1. Reproduz os diagnósticos registrados na execução inicial. |
| `eslint-inicial.png` | Captura real do terminal fornecida manualmente pelo aluno, com comando, diagnósticos e código de saída visíveis. Reprodução posterior à criação da suíte limpa; imagem original incluída no PDF sem edição e com proporção preservada. |
| `10-validacao-documental.txt` | `npm test` e `npm run lint:clean`, executados novamente após a inclusão da captura no relatório: 22 aprovados, 1 ignorado original; testes e lint limpo com saída 0. |
| `original-preservado.txt` | SHA-256 idêntico antes/depois da movimentação do original. A auditoria também compara o blob com a base Git. |

O PDF inclui `eslint-inicial.png` na seção do ESLint, com legenda que a identifica como reprodução dos diagnósticos iniciais, capturada manualmente após a refatoração. A imagem substitui a antiga transcrição nessa seção. O arquivo `02-eslint-inicial.txt` preserva a primeira saída textual autêntica. O pequeno artefato de codificação antes do resumo numérico na captura foi mantido como registrado pelo terminal; os totais e todos os diagnósticos estão legíveis.
