
from lxml import etree
import json

jmdict_e_path = '../JMdict_e.xml'

print('Loading XML ...')
parser = etree.XMLParser(resolve_entities=False)
tree = etree.parse(jmdict_e_path, parser=parser)
root = tree.getroot()
jmdict = {}

print('Extracting entries ...')
for entry in root:
  elements = iter(entry)
  
  forms = []
  pos_senses = []
  
  try:
    e = next(elements) # skip ent_seq
    e = next(elements)
    while e.tag == 'k_ele':
      assert e[0].tag == 'keb'
      forms.append(e[0].text)
      e = next(elements)
    while e.tag == 'r_ele':
      assert e[0].tag == 'reb'
      forms.append(e[0].text)
      e = next(elements)
    while e.tag == 'sense':
      tags = [s.tag for s in e]
      if 'pos' in tags and 'field' not in tags:
        pos_idx = tags.index('pos')
        pos = e[pos_idx][0].text[1:-1]
        assert pos not in pos_senses
        gloss_idx = tags.index('gloss')
        gloss = e[gloss_idx].text
        pos_senses.append([pos, gloss])
      e = next(elements)
  except StopIteration:
    pass

  for form in forms:
    if form not in jmdict:
      jmdict[form] = []
    jmdict[form] += pos_senses

print('Writing JSON ...')
with open('jmdict.json', 'w') as f:
  json.dump(jmdict, f)
  