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
| `original-preservado.txt` | SHA-256 idêntico antes/depois da movimentação do original. A auditoria também compara o blob com a base Git. |

O PDF apresenta o texto autêntico de `02-eslint-inicial.txt`, identificado como transcrição. A captura de imagem do terminal não estava disponível no ambiente de comandos. Uma transcrição não é apresentada como screenshot.
