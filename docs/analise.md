# Análise e auditoria da atividade

**Disciplina:** Teste de Software (README do projeto original).

**Aluno:** Luidi Cadete Silva · **Matrícula:** 1447551.

**Data:** 18/10/2026 · **Fork:** https://github.com/LuidiC/test-smelly · **Branch:** main.

**Base:** `fc5cc1206e9bcd40d5b6c705d48a67659672c6c5`.

O PDF oficial foi lido integralmente, nas quatro páginas. A análise considera o código real, não apenas os exemplos de smells citados no enunciado.

## Diagnóstico manual

As linhas referem-se ao arquivo `__tests__/userService.smelly.test.js`, preservado integralmente ao movê-lo de `test/` para o caminho exigido.

| Tipo e localização | Problema e impacto | Decisão na suíte limpa |
| --- | --- | --- |
| Eager Test, linhas 18-31 | Cria e consulta no mesmo caso; intercala ações e asserções. Uma falha na criação impede o diagnóstico da consulta, amplia o escopo e dificulta manutenção. | Separar criação e consulta; cadastrar o usuário na preparação do cenário de busca. |
| Conditional Test Logic, linhas 33-52, especialmente 40-49 | `for` e `if/else` controlam as asserções executadas. Cenários de permissões ficam misturados e as verificações dependem do fluxo. | Casos separados para usuário comum e administrador; verificar retorno e estado persistido. |
| Teste frágil por formatação, linhas 54-63 | Exige linha com pontuação e quebra de linha, além de cabeçalho exato. Alterações cosméticas geram falsos alarmes; Bob é criado, mas sua presença não é verificada. | Conferir IDs e nomes de ambos e estados em cenários próprios, sem fixar o leiaute. |
| Asserção condicional e falso positivo, linhas 66-75 | O único `expect` está no `catch`. Se a operação deixar de lançar, o teste passa sem asserções. O comentário da linha 68 é impreciso: o `catch` não é necessário para passar. | Usar `toThrow`, exigindo a exceção. Testar também o limite válido de 18 anos. |
| Teste ignorado e vazio, linhas 77-79 | `test.skip` e ausência de asserções excluem o cenário sem usuários. O nome fala em lista, mas a API gera relatório textual. | Implementar a mensagem de ausência de usuários no arquivo novo e preservar o skip no original. |

Não foi atribuído “Convidado Misterioso” a fixtures locais. Vários `expect` podem verificar um único resultado: desativar deve retornar sucesso e manter o cadastro com status inativo.

## Configuração e comparação automática

- Node 24.14.1, npm 11.11.0, Jest 29.7.0.
- Instalação: `npm install --save-dev --save-exact eslint@8.57.1 eslint-plugin-jest@28.14.0`.
- ESLint 8 aceita `.eslintrc.json` diretamente; plugin compatível com ESLint 8 e Node >=20. A versão fora de suporte foi escolhida para reproduzir o formato acadêmico exigido.
- Presets `eslint:recommended` e `plugin:jest/recommended`; regras `jest/no-disabled-tests: warn`, `jest/no-conditional-expect: error`, `jest/no-identical-title: error`.
- Primeira execução, antes da suíte limpa: `npx eslint .`, saída 1; quatro erros nas linhas 44, 46, 49 e 73; dois avisos na linha 77.
- O linter encontrou asserções condicionais, teste ignorado e teste sem asserções. Não identificou Eager Test nem fragilidade de formatação. A análise manual é complementar. Não houve título idêntico detectado, embora a regra esteja ativa.
- Após refatorar, o diagnóstico global permanece exclusivamente no original. O arquivo limpo tem zero erros e avisos com `--max-warnings=0`.

## Decisões e resultados

A suíte limpa agrupa casos por operação e aplica AAA. O `beforeEach` limpa o banco compartilhado; nenhum caso depende da ordem ou do resultado de outro. `test.each` declara três entradas de campos ausentes sem laços ou condicionais nos corpos dos testes.

O gerador do PDF extrai diretamente o teste original de exceção (linhas 66-75) e a versão limpa (61-70). `criarMenor` adia a chamada para que `toThrow` observe a exceção; a execução ocorre dentro do matcher, conforme o padrão necessário para esse tipo de asserção.

| Validação real | Resultado | Evidência em `docs/evidencias/` |
| --- | --- | --- |
| Jest inicial | 4 aprovados e 1 ignorado | `01-jest-original.txt` |
| ESLint inicial | 4 erros, 2 avisos; saída 1 | `02-eslint-inicial.txt` |
| ESLint limpo | 0 erros, 0 avisos; saída 0 | `03-eslint-clean.txt` |
| `npm test` completo | 22 aprovados, 1 ignorado original; 2 suítes aprovadas | `04-jest-final.txt` |
| ESLint global final | mesmos diagnósticos, só no original | `05-eslint-final.txt` |
| Cobertura limpa isolada | 18 casos; 100% nas quatro métricas | `06-cobertura-clean.txt` |
| Seis mutações dirigidas | limpa detectou 6/6; original 2/6 | `07-mutacoes-dirigidas.txt` |
| Instalação pelo lockfile e nova validação | `npm ci`, `npm test` e `npm run lint:clean` aprovados | `08-reproducibilidade.txt` |
| Reprodução dos diagnósticos iniciais | 4 erros e 2 avisos no original; saída 1 | `09-eslint-reproducao.txt` e `eslint-inicial.png` |
| Validação após a inclusão da captura | 22 aprovados e 1 ignorado original; lint limpo com saída 0 | `10-validacao-documental.txt` |

As mutações removeram a idade mínima, rejeitaram indevidamente 18 anos, permitiram desativar administrador, impediram a mudança de status, omitiram Bob do relatório e removeram a validação de campos. Cada suíte passou no controle sem mutações. Todos os defeitos foram detectados pela limpa; quatro escaparam do original. As alterações foram realizadas em cópias temporárias, sem modificar o serviço do repositório. O experimento não equivale a uma campanha completa de mutação.

## Limitações registradas

1. O original contém um `test.skip` preservado por exigência do professor. Não há skips novos. Foram 22 testes aprovados e 1 ignorado, não 23 executados.
2. A captura real do terminal foi fornecida manualmente pelo aluno em `docs/evidencias/eslint-inicial.png` e incluída na seção do ESLint do PDF. É identificada como reprodução dos diagnósticos iniciais, realizada após a refatoração. A imagem foi preservada sem alterações, com 4 erros, 2 avisos e código de saída 1 visíveis; todos os diagnósticos pertencem ao original. A saída textual da primeira execução também foi mantida.
3. Uma tentativa no sandbox falhou por `EPERM` ao renomear o cache, antes de executar testes (`04a-jest-restricao-do-ambiente.txt`). A execução com acesso normal ao cache passou, sem alteração no código.
4. Cobertura de 100% e seis mutações detectadas não provam ausência de defeitos.

## Auditoria pelos critérios do professor

- **Identificação (20%):** cinco problemas reais com localização, riscos e correção; ao menos três tipos distintos.
- **Ferramenta (15%):** versões compatíveis, `.eslintrc.json`, três regras obrigatórias e saídas inicial/final.
- **Refatoração (40%):** 18 casos limpos, AAA, cenários focados, sem condicionais problemáticas, verificações comportamentais e isolamento; serviço intacto.
- **Relatório (25%):** quatro páginas com capa, análise, antes/depois reais, captura autêntica do terminal identificada como reprodução dos diagnósticos iniciais e conclusão; renderização, legibilidade e paginação verificadas.
- **Repositório:** fork LuidiC, `origin` e `upstream`, conteúdo original preservado, README e lockfile; sem dependências instaladas, cache ou credenciais preparados para commit.
- **Publicação:** um commit de implementação e um novo commit exclusivamente documental na branch `main`, sem reescrever o histórico, com push e verificação remota. O hash final é informado na resposta de entrega e no histórico Git, evitando autorreferência no próprio commit.

## Referências

- PDF oficial, páginas 1-4: requisitos e critérios.
- [Base e créditos: CleitonSilvaT/test-smelly](https://github.com/CleitonSilvaT/test-smelly).
- [ESLint: migração de configuração](https://eslint.org/docs/latest/use/configure/migration-guide).
- [Plugin oficial Jest](https://github.com/jest-community/eslint-plugin-jest).
