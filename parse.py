import MeCab

class MeCabToken:

  pos_map = {
    '代名詞': 'pronoun',
    '副詞': 'adverb',
    '助動詞': 'auxiliary verb',
    '助詞': 'particle',
    '動詞': 'verb',
    '名詞': 'noun',
    '形容詞': 'adjective',
    '感動詞': 'interjection',
    '接尾辞': 'suffix',
    '接続詞': 'conjunction',
    '接頭辞': 'prefix',
    '空白': 'whitespace',
    '補助記号': 'supplementary symbol',
    '記号': 'symbol',
    '連体詞': 'adnominal',
    '*': '-'
    }

  infl_map = {
    'ク語法': '"ku" wording',
    '仮定形': 'conditional',
    '命令形': 'imperative',
    '已然形': 'realis',
    '意志推量形': 'volitional tentative',
    '連用タ接続': 'continuous "ta" connection',
    '未然形': 'irrealis',
    '終止形': 'conclusive',
    '語幹': 'word stem',
    '連体形': 'attributive',
    '連用形': 'continuative',
    '基本形': 'regular form',
    '*': '-'
    }

  def __init__(self, line):
    columns = line.split('\t')
    self.text = columns[0]
    fields = columns[1].split(',')
    self.pos = self.pos_map[fields[0]]
    self.infl = self.infl_map[fields[5]]
    self.lemma = fields[6]

  def __repr__(self):
    return f'{self.text} ({self.infl} of {self.lemma})'


tagger = MeCab.Tagger()

while True:
  text = input('\nJapanese sentence (or q to quit): ')
  if text == 'q':
    break
  result = tagger.parse(text)
  lines = [line for line in result.split('\n') if '\t' in line]
  tokens = [MeCabToken(line) for line in lines]

  pos_str = ' '.join(t.text + '/' + t.pos for t in tokens)
  print(pos_str + '\n')

  pred_str = None
  for i, t in enumerate(tokens):
    if pred_str == None and t.pos == 'verb':
      pred_str = str(t)
    elif pred_str != None:
      if t.pos in ['auxiliary verb', 'verb']:
        pred_str += ' + ' + str(t)
      elif t.pos == 'particle':
        pred_str += ' + ' + t.text + ' (particle)'
      else:
        print('PREDICATE: ' + pred_str)
        pred_str = None

  if pred_str != None:
    print('PREDICATE: ' + pred_str)