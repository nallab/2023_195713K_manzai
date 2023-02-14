#python gen_manzai.py "冒頭文"

from transformers import T5Tokenizer, AutoModelForCausalLM
import sys
import torch

input_word = sys.argv[1]

# トークナイザーとモデルの準備
tokenizer = T5Tokenizer.from_pretrained("model_1117")
model = AutoModelForCausalLM.from_pretrained("output1L1M_1023-cb/")

# 推論
input = torch.tensor([tokenizer.encode(input_word)[:-1]])
output = model.generate(input, do_sample=True, max_length=600, num_return_sequences=10)
#print(tokenizer.batch_decode(output, skip_special_tokens=True))
output_list = tokenizer.batch_decode(output, skip_special_tokens=False)

for x in output_list:
    print(x.replace("<boke>","\n<boke>").replace("<tsukkomi>", "\n<tsukkomi>").replace("<both>","\n<both>"))
    print("------------------------------------------")