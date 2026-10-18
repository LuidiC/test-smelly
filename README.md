# Laboratório de Test Smells - Gerenciador de Usuários

Atividade da disciplina **Teste de Software**: identificação de Test Smells, configuração do ESLint e refatoração de testes Jest com o padrão **Arrange, Act, Assert (AAA)**.

**Aluno:** Luidi Cadete Silva · **Matrícula:** 1447551

O serviço simula criação, consulta, desativação e relatório de usuários em memória. Test Smells são sinais de problemas nos testes que dificultam sua compreensão, manutenção ou capacidade de revelar defeitos.

## Origem e preservação

Fork de [CleitonSilvaT/test-smelly](https://github.com/CleitonSilvaT/test-smelly), com os créditos e o histórico do professor preservados. Base: `fc5cc1206e9bcd40d5b6c705d48a67659672c6c5`.

O original armazenava a suíte em `test/`, embora o enunciado e o README indicassem `__tests__/`. Ela foi movida para o caminho exigido **sem alteração de conteúdo**; o SHA-256 está em [original-preservado.txt](docs/evidencias/original-preservado.txt). A lógica de `src/userService.js` permanece intacta.

## Tecnologias e instalação

JavaScript, Node.js, npm, Jest, Babel, ESLint e eslint-plugin-jest. Ambiente validado: Node **24.14.1**, npm **11.11.0**, Jest **29.7.0**, ESLint **8.57.1** e eslint-plugin-jest **28.14.0**.

```bash
git clone https://github.com/LuidiC/test-smelly.git
cd test-smelly
npm ci
```

O lockfile foi incluído para fixar as dependências. A instalação inicial foi feita com `npm install`.

O ESLint 8.57.1 aceita `.eslintrc.json` diretamente. Essa versão está fora de suporte; o uso atende ao formato legado da atividade. O plugin 28.14.0 é compatível com essa versão e com o Node utilizado. A configuração mantém as três regras obrigatórias e os presets recomendados de ESLint/Jest. [Documentação oficial sobre migração](https://eslint.org/docs/latest/use/configure/migration-guide).

## Executar e validar

```bash
npm test
npx eslint .
npm run lint:clean
npm run coverage -- --runInBand --collectCoverageFrom=src/userService.js --testPathPattern=userService.clean.test.js
```

`npm test`: **22 testes passaram** (4 originais + 18 limpos), **1 original ignorado**, 0 falhas, 2 suítes aprovadas. A suíte limpa não tem testes ignorados. O `test.skip` original foi preservado; seu cenário foi implementado como relatório sem usuários na suíte nova, pois a API retorna texto, não uma lista.

`npx eslint .`: código **1**, com **4 erros e 2 avisos exclusivamente no original preservado**. Isso é esperado e permanece visível; não há exclusão do original nem desativação de regras. `npm run lint:clean`: código **0**, sem erros ou avisos, com `--max-warnings=0`.

A suíte limpa isolada atingiu **100% de linhas, instruções, funções e ramificações** do serviço. Detectou seis mutações dirigidas; a original detectou duas. Esse experimento limitado não equivale a um escore completo de mutação nem prova ausência de defeitos.

## Análise e melhorias

- **Eager Test:** criação e consulta separadas em casos focados.
- **Lógica condicional:** cenários de usuário comum e administrador separados, sem `if`, `for` ou `try/catch` nos testes limpos.
- **Teste frágil:** relatório verificado pelos dados e estados, sem depender de cabeçalho, pontuação, quebra de linha ou ordem.
- **Falso positivo na exceção:** `toThrow` exige que a operação realmente lance o erro.
- **Teste ignorado/vazio:** cenário sem usuários implementado no arquivo novo.

Cada teste explicita AAA. O `beforeEach` recria o serviço e limpa o banco compartilhado. Foram acrescentadas verificações de campos obrigatórios, idade limite, identificadores distintos, consulta inexistente, bloqueio de administrador e preservação do cadastro após desativação. [Análise com linhas, riscos e decisões](docs/analise.md).

## Entrega e estrutura

```text
__tests__/
  userService.smelly.test.js   # original preservado
  userService.clean.test.js    # 18 testes executados
src/userService.js            # serviço original
docs/
  analise.md                  # diagnóstico e auditoria
  gerar_relatorio.py          # fonte editável
  evidencias/                 # saídas reais dos comandos
output/pdf/
  relatorio-test-smells-luidi-cadete-silva-1447551.pdf
.eslintrc.json
package.json
package-lock.json
```

O relatório tem quatro páginas: capa, análise, antes/depois, resultado da ferramenta e conclusão. Inclui a [captura real do terminal](docs/evidencias/eslint-inicial.png), realizada manualmente e identificada como reprodução dos diagnósticos iniciais após a refatoração. Os 4 erros e 2 avisos permanecem exclusivamente no original preservado. As [evidências](docs/evidencias/README.md) também mantêm a saída autêntica da primeira execução e as validações finais.

Para regenerar o PDF, instale `reportlab` em um ambiente Python e execute `python docs/gerar_relatorio.py` na raiz do projeto. Envie ao professor o [link deste fork](https://github.com/LuidiC/test-smelly) e o [relatório PDF](output/pdf/relatorio-test-smells-luidi-cadete-silva-1447551.pdf).

## Referências e créditos

- Enunciado do professor: *Refatoração de Testes e Detecção de Test Smells*, quatro páginas.
- [Projeto original de CleitonSilvaT](https://github.com/CleitonSilvaT/test-smelly).
- [Documentação oficial de eslint-plugin-jest](https://github.com/jest-community/eslint-plugin-jest).
