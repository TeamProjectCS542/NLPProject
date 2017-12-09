"""
compute_rouge.py

computes the ROUGE score for generate captions

@author: Xinchun He
"""

from rouge import Rouge
	
ref = open('../textsum/log_root/decode/ref1511299602', 'r')
ref_captions = ref.readlines()
ref_captions = [caption.strip('output= \n.') for caption in ref_captions]
ref_captions = [caption.split(': ')[-1] for caption in ref_captions]
decode = open('../textsum/log_root/decode/decode1511299602', 'r')
decode_captions = decode.readlines()
decode_captions = [caption.strip('output= .\n') for caption in decode_captions]

r = Rouge()
scores = []
for i in range(len(ref_captions)):
    scores += r.get_scores(ref_captions[i], decode_captions[i])

print(scores)

