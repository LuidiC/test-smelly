"""Gera o relatório de quatro páginas. Requer: pip install reportlab."""
from pathlib import Path
from textwrap import dedent
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, Preformatted,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output/pdf/relatorio-test-smells-luidi-cadete-silva-1447551.pdf'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path('C:/Windows/Fonts')

if (FONT_DIR / 'arial.ttf').exists():
    font_files = [('Body', FONT_DIR / 'arial.ttf'),
                  ('BodyBold', FONT_DIR / 'arialbd.ttf'),
                  ('Code', FONT_DIR / 'consola.ttf')]
else:
    import reportlab
    font_dir = Path(reportlab.__file__).parent / 'fonts'
    font_files = [('Body', font_dir / 'Vera.ttf'),
                  ('BodyBold', font_dir / 'VeraBd.ttf'),
                  ('Code', font_dir / 'VeraMono.ttf')]
for name, file in font_files:
    pdfmetrics.registerFont(TTFont(name, str(file)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold')

NAVY = colors.HexColor('#183247')
GRAY = colors.HexColor('#526170')
LIGHT = colors.HexColor('#F2F5F7')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Text', fontName='Body', fontSize=10.3, leading=14.5,
                          alignment=TA_JUSTIFY, spaceAfter=9, textColor=colors.HexColor('#202830')))
styles.add(ParagraphStyle('HeadingMain', fontName='BodyBold', fontSize=18, leading=23,
                          textColor=NAVY, spaceAfter=16))
styles.add(ParagraphStyle('Sub', fontName='BodyBold', fontSize=11, leading=15,
                          textColor=NAVY, spaceBefore=9, spaceAfter=5))
styles.add(ParagraphStyle('SmallText', fontName='Body', fontSize=8.6, leading=11.7,
                          textColor=GRAY, spaceAfter=7))
styles.add(ParagraphStyle('CodeBlock', fontName='Code', fontSize=8.1, leading=11.2,
                          backColor=LIGHT, borderPadding=10, spaceBefore=5, spaceAfter=14))
styles.add(ParagraphStyle('CoverTitle', fontName='BodyBold', fontSize=26, leading=33,
                          alignment=TA_CENTER, textColor=NAVY, spaceAfter=20))
styles.add(ParagraphStyle('CoverText', fontName='Body', fontSize=12, leading=18,
                          alignment=TA_CENTER, textColor=NAVY, spaceAfter=12))

story = []

def p(text, style='Text'):
    story.append(Paragraph(text, styles[style]))

def heading(text):
    p(text, 'HeadingMain')

def item(title, text):
    story.append(KeepTogether([Paragraph(title, styles['Sub']), Paragraph(text, styles['Text'])]))

def code(text):
    story.append(Preformatted(dedent(text).strip(), styles['CodeBlock']))

def footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor('#D9E1E7'))
    canvas.line(50, 43, width - 50, 43)
    canvas.setFillColor(GRAY)
    canvas.setFont('Body', 8)
    canvas.drawString(50, 29, 'Luidi Cadete Silva | 1447551 | Teste de Software')
    canvas.drawRightString(width - 50, 29, f'{doc.page} / 4')
    if doc.page > 1:
        canvas.setFont('Body', 8)
        canvas.drawString(50, height - 32, 'REFATORAÇÃO DE TESTES E DETECÇÃO DE TEST SMELLS')
    canvas.restoreState()

# Página 1: capa com todas as informações fornecidas e verificadas.
story.append(Spacer(1, 65))
p('TESTE DE SOFTWARE', 'CoverText')
story.append(Spacer(1, 65))
p('Refatoração de Testes<br/>e Detecção de Test Smells', 'CoverTitle')
p('Análise e refatoração da suíte Jest de UserService', 'CoverText')
story.append(Spacer(1, 40))
story.append(HRFlowable(width='60%', thickness=1, color=NAVY, hAlign='CENTER'))
story.append(Spacer(1, 28))
p('<b>Luidi Cadete Silva</b><br/>Matrícula: 1447551', 'CoverText')
story.append(Spacer(1, 60))
p('18 de outubro de 2026', 'CoverText')
p('Repositório de entrega<br/><link href="https://github.com/LuidiC/test-smelly" color="#183247">github.com/LuidiC/test-smelly</link>', 'CoverText')
story.append(PageBreak())

# Página 2: diagnóstico manual com evidências concretas.
heading('1. Análise dos Test Smells')
p('O serviço gerencia usuários em memória. A análise considera o arquivo original '
  '<b>userService.smelly.test.js</b>; os números abaixo correspondem às suas linhas reais. '
  'O arquivo foi movido de <b>test/</b> para <b>__tests__/</b>, conforme o enunciado, '
  'com conteúdo idêntico, verificado por SHA-256. A lógica de negócio foi preservada.')
item('1.1 Eager Test - linhas 18-31',
     'O caso “deve criar e buscar um usuário corretamente” executa criação e consulta, '
     'intercalando ações e asserções. Uma falha inicial pode impedir a avaliação da busca, '
     'dificultando o diagnóstico e a manutenção. A correção separa as responsabilidades: '
     'criar é a ação de um caso e a preparação do caso de consulta.')
item('1.2 Lógica condicional no teste - linhas 33-52',
     'O <b>for</b> da linha 40 e o <b>if/else</b> da linha 42 controlam quais asserções '
     'serão executadas para usuários comuns e administradores. O leitor precisa interpretar '
     'o fluxo para descobrir os cenários. A versão limpa usa dois casos explícitos, '
     'verificando tanto o retorno da desativação quanto o estado persistido do usuário.')
item('1.3 Teste frágil por formatação - linhas 54-63',
     'O relatório exige uma linha completa com vírgulas e quebra de linha, além do '
     'cabeçalho exato. Uma mudança visual pode quebrar o teste sem alterar o comportamento. '
     'Bob é cadastrado, mas não verificado. A refatoração confere nomes e IDs de ambos '
     'e os estados em cenários próprios, sem fixar cabeçalho, ordem ou pontuação.')
item('1.4 Falso positivo em try/catch - linhas 66-75',
     'O único <b>expect</b> está no <b>catch</b>. Se a validação de idade for removida, '
     'a chamada não lança e o teste termina com sucesso sem verificar nada. Isso oculta '
     'uma violação da regra de maioridade. A correção usa <b>toThrow</b>, exigindo que '
     'a exceção ocorra, e acrescenta um caso válido para exatamente 18 anos.')
item('1.5 Teste ignorado e vazio - linhas 77-79',
     'O <b>test.skip</b> não contém asserções e não executa o cenário sem usuários. '
     'Seu nome menciona uma lista, mas a API disponível retorna relatório textual. '
     'O novo arquivo verifica a mensagem de ausência de usuários. O skip permanece '
     'somente no original, em respeito à exigência de preservação.')
p('A análise manual e o lint são complementares: a ferramenta identificou asserções '
  'condicionais e teste ignorado/vazio, mas não diagnosticou o Eager Test ou o acoplamento '
  'à formatação do relatório.', 'SmallText')
story.append(PageBreak())

# Página 3: trechos extraídos diretamente do código versionado.
heading('2. Processo de refatoração')
p('O teste de idade foi escolhido porque poderia aprovar uma implementação defeituosa. '
  'Os dois trechos abaixo são extraídos diretamente dos arquivos do projeto.')
original_lines = (ROOT / '__tests__/userService.smelly.test.js').read_text(encoding='utf-8').splitlines()
clean_lines = (ROOT / '__tests__/userService.clean.test.js').read_text(encoding='utf-8').splitlines()
before = dedent('\n'.join(original_lines[65:75]))
after = dedent('\n'.join(clean_lines[60:70]))
assert "test('deve falhar" in before and 'catch (e)' in before
assert "test('rejeita" in after and '.toThrow(' in after
p('ANTES - original, linhas 66-75', 'Sub')
code(before)
p('DEPOIS - suíte limpa, linhas 61-70', 'Sub')
code(after)
p('<b>Arrange:</b> os dados do menor ficam explícitos no cenário. <b>Act:</b> '
  'a função adia a operação para que o matcher possa observar sua execução. '
  '<b>Assert:</b> <b>toThrow</b> executa essa função e exige a exceção esperada; '
  'a ausência de erro passa a causar falha. O teste deixa de depender de um catch '
  'e passa a verificar diretamente a regra de negócio.')
p('Nos demais casos, criação e consulta foram separadas; usuários comuns e administradores '
  'ganharam cenários independentes; o relatório passou a conferir conteúdo relevante. '
  'O <b>beforeEach</b> limpa o banco em memória, evitando dependência de ordem. '
  'Os 18 testes novos não usam if, for ou try/catch nos seus corpos.')
item('Verificação da capacidade de detectar defeitos',
     'Em cópias temporárias, seis alterações deliberadas foram testadas: idade mínima, '
     'limite de 18 anos, bloqueio de administrador, mudança de status, presença de Bob '
     'no relatório e campos obrigatórios. A suíte limpa detectou <b>6/6</b>; a original, '
     '<b>2/6</b>. A remoção da idade mínima escapou da original, confirmando o falso '
     'positivo. Esse experimento dirigido não é um escore completo de mutação.')
story.append(PageBreak())

# Página 4: saída autêntica, validação e conclusão.
heading('3. Ferramenta, validação e conclusão')
p('Foram utilizados Node 24.14.1, npm 11.11.0, Jest 29.7.0, ESLint 8.57.1 e '
  'eslint-plugin-jest 28.14.0. O ESLint 8 foi fixado para aceitar o <b>.eslintrc.json</b> '
  'exigido; é uma versão fora de suporte, escolhida por compatibilidade com o enunciado. '
  'Os presets recomendados e as três regras obrigatórias estão configurados.')
p('Primeira execução do ESLint', 'Sub')
p('Trecho da saída textual autêntica de <b>npx eslint .</b>, executado antes da criação '
  'da suíte limpa. O caminho absoluto foi omitido neste trecho. O ambiente não '
  'disponibilizou captura de imagem do terminal; este bloco é uma transcrição real, '
  '<b>não um print</b>. A saída integral está em docs/evidencias/02-eslint-inicial.txt.', 'SmallText')
lint_lines = (ROOT / 'docs/evidencias/02-eslint-inicial.txt').read_text(encoding='utf-8-sig').splitlines()
lint_excerpt = [line for line in lint_lines if ('error ' in line or 'warning ' in line or 'EXIT_CODE=' in line)]
assert len(lint_excerpt) == 7
code('\n'.join(lint_excerpt))
p('Os erros das linhas 44, 46 e 49 apontam asserções no if/else; o da linha 73 '
  'aponta a asserção no catch. Na linha 77, há avisos de teste ignorado e sem '
  'asserções. A regra de títulos idênticos está ativa, mas não encontrou ocorrência.')
table_data = [
    ['Validação', 'Resultado registrado'],
    ['Jest original', '4 aprovados; 1 ignorado'],
    ['Jest completo (npm test)', '22 aprovados; 1 ignorado original; 0 falhas'],
    ['ESLint da suíte limpa', '0 erros; 0 avisos; código de saída 0'],
    ['ESLint global final', '4 erros; 2 avisos, somente no original'],
    ['Cobertura da suíte limpa', '100%: instruções, ramificações, funções e linhas'],
]
table = Table([[Paragraph(escape(cell), styles['SmallText']) for cell in row] for row in table_data], colWidths=[161, 334], hAlign='LEFT')
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ('LINEBELOW', (0, 0), (-1, -1), .3, colors.HexColor('#D9E1E7')),
]))
story.append(table)
story.append(Spacer(1, 8))
p('O diagnóstico global permanece visível porque o original foi preservado; a melhoria '
  'é comprovada pelo arquivo limpo sem diagnósticos. O único teste ignorado já existia '
  'no projeto. Uma restrição de cache do sandbox foi resolvida executando o Jest com '
  'acesso normal, sem mudar o código; ambas as saídas foram preservadas.', 'SmallText')
p('Conclusão', 'Sub')
p('Testes limpos tornam o comportamento esperado explícito e as falhas mais fáceis de '
  'diagnosticar. A refatoração eliminou fluxos condicionais problemáticos, reduziu '
  'acoplamento à apresentação e corrigiu uma validação que passava sem asserções. '
  'O ESLint automatiza parte desse controle e ajuda a sustentar a qualidade do projeto; '
  'análise manual e execução continuam necessárias. Cobertura total não prova ausência '
  'de defeitos, por isso também foram verificadas alterações deliberadas.')
p('Fontes: enunciado oficial, pp. 1-4; '
  '<link href="https://github.com/CleitonSilvaT/test-smelly">CleitonSilvaT/test-smelly</link>; '
  '<link href="https://github.com/jest-community/eslint-plugin-jest">eslint-plugin-jest</link>; '
  '<link href="https://eslint.org/docs/latest/use/configure/migration-guide">guia de migração do ESLint</link>. '
  'Saídas completas e auditoria: docs/evidencias/ e docs/analise.md.', 'SmallText')

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=50, leftMargin=50,
                        topMargin=52, bottomMargin=58,
                        title='Refatoração de Testes e Detecção de Test Smells',
                        author='Luidi Cadete Silva', subject='Teste de Software - Matrícula 1447551')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
