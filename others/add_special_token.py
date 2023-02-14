from transformers import T5Tokenizer, AutoModelForCausalLM
import torch
tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-medium")
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt2-medium")

MANZAI_TOKEN_MAPPING = {
    'ボケ': '<boke>',
    'ツッコミ': '<tsukkomi>',
    '二人': '<both>', 
    '漫才の終わり':'<eom>'
}

special_tokens_dict = {'additional_special_tokens': list(MANZAI_TOKEN_MAPPING.values())}
tokenizer.add_special_tokens(special_tokens_dict)

dir_name = 'model_additional'
tokenizer.save_pretrained(dir_name)
model.save_pretrained(dir_name)