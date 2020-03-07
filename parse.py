import MeCab
from jamdict import Jamdict

class MeCabToken:

  pos_map = {
    '動詞': 'verb',
    '名詞': 'noun',
    '形容詞': 'adjective',
    '代名詞': 'pronoun',
    '副詞': 'adverb',
    '連体詞': 'adnominal',
    '助動詞': 'auxiliary verb',
    '助詞': 'particle',
    '感動詞': 'interjection',
    '接頭辞': 'prefix',
    '接続詞': 'conjunction',
    '接尾辞': 'suffix',
    '空白': 'whitespace',
    '補助記号': 'supplementary symbol',
    '記号': 'symbol',
    '*': 'unknown'
    }

  infl_map = {
    '語幹': 'stem',

    '未然形': 'negative base', # mizenkei

    '意志推量形': 'volitive base', # shikōkei

    '連用形': 'masu base', # ren'yōkei
    '連用タ接続': 'te base',

    '終止形': 'terminal form', # shūshikei
    '基本形': 'regular form', # kihonkei
    '已然形': 'positive base',
    '連体形': 'attributive base', # rentaikei

    '仮定形': 'hypothetic base', # kateikei
    '命令形': 'imperative base', # meireikei

    'ク語法': 'nominalized "ku" form',
    '*': ''
    }

  def __init__(self, line):
    columns = line.split('\t')
    self.text = columns[0]
    fields = columns[1].split(',')
    self.pos = self.pos_map[fields[0]]
    self.infl = self.infl_map[fields[5]]
    self.lemma = fields[6]


tagger = MeCab.Tagger()
jmdict = Jamdict(strict_lookup=True, lookup_chars=False)

while True:
  text = input('\nJapanese sentence (or q to quit): ')
  if text == 'q':
    break

  result = tagger.parse(text)
  lines = [line for line in result.split('\n') if '\t' in line]
  tokens = [MeCabToken(line) for line in lines]

  for t in tokens:
    infl_str = ''
    if t.lemma != t.text:
      infl_str = f' - {t.infl} of {t.lemma}'
    print(f'\n{t.text} [{t.pos}{infl_str}]')
    entries = jmdict.lookup(t.lemma).entries
    for entry in entries:
      forms = entry.kanji_forms + entry.kana_forms
      form_str = ', '.join(str(f) for f in forms)
      pos_match = False
      for sense in entry.senses:
        pos = ' | '.join(sense.pos)
        if pos != '':
          pos_match = t.pos in pos
          if pos_match:
            print('  ' + form_str + ': ' + pos)
        if pos_match:
          print('    ' + sense.text(compact=True))
