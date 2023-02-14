#python gen_manzai3.py "冒頭文"

from transformers import T5Tokenizer, AutoModelForCausalLM
import sys
import random as rand
import torch

#x行目にボケが喋る確率
B_rate_list = [0.22033898305084745, 0.4107142857142857, 0.46551724137931033, 0.35384615384615387, 0.3384615384615385, 0.4696969696969697, 0.45454545454545453, 0.42424242424242425, 0.4090909090909091, 0.4090909090909091, 0.5454545454545454, 0.48484848484848486, 0.5303030303030303, 0.3939393939393939, 0.45454545454545453, 0.5151515151515151, 0.5757575757575758, 0.4696969696969697, 0.48484848484848486, 0.49230769230769234, 0.3484848484848485, 0.5151515151515151, 0.3939393939393939, 0.3939393939393939, 0.48484848484848486, 0.4393939393939394, 0.5, 0.4393939393939394, 0.4090909090909091, 0.5606060606060606, 0.36363636363636365, 0.5, 0.3939393939393939, 0.4393939393939394, 0.45454545454545453, 0.47692307692307695, 0.46153846153846156, 0.3939393939393939, 0.4393939393939394, 0.42424242424242425, 0.38461538461538464, 0.48484848484848486, 0.36363636363636365, 0.3787878787878788, 0.45454545454545453, 0.4393939393939394, 0.45454545454545453, 0.47692307692307695, 0.4, 0.4696969696969697, 0.4393939393939394, 0.36363636363636365, 0.45454545454545453, 0.4090909090909091, 0.5151515151515151, 0.42424242424242425, 0.4090909090909091, 0.4307692307692308, 0.36363636363636365, 0.42424242424242425, 0.4696969696969697, 0.5230769230769231, 0.38461538461538464, 0.38461538461538464, 0.47692307692307695, 0.4153846153846154, 0.4090909090909091, 0.3939393939393939, 0.4153846153846154, 0.5303030303030303, 0.4090909090909091, 0.4696969696969697, 0.5757575757575758, 0.3939393939393939, 0.4696969696969697, 0.4696969696969697, 0.4696969696969697, 0.3484848484848485, 0.4696969696969697, 0.5230769230769231, 0.4090909090909091, 0.4393939393939394, 0.3333333333333333, 0.48484848484848486, 0.35384615384615387, 0.3939393939393939, 0.36923076923076925, 0.48484848484848486, 0.3484848484848485, 0.36363636363636365, 0.3787878787878788, 0.48484848484848486, 0.5692307692307692, 0.3787878787878788, 0.4461538461538462, 0.359375, 0.46875, 0.49206349206349204, 0.4444444444444444, 0.3968253968253968, 0.47619047619047616, 0.4126984126984127, 0.4603174603174603, 0.42857142857142855, 0.4032258064516129, 0.46774193548387094, 0.41935483870967744, 0.3548387096774194, 0.4262295081967213, 0.4032258064516129, 0.41935483870967744, 0.35, 0.5166666666666667, 0.3559322033898305, 0.38333333333333336, 0.3559322033898305, 0.5254237288135594, 0.3728813559322034, 0.4482758620689655, 0.4067796610169492, 0.3793103448275862, 0.4482758620689655, 0.38596491228070173, 0.37037037037037035, 0.4444444444444444, 0.34545454545454546, 0.4444444444444444, 0.3584905660377358, 0.5094339622641509, 0.34615384615384615, 0.40384615384615385, 0.44, 0.44680851063829785, 0.5106382978723404, 0.4, 0.5454545454545454, 0.3488372093023256, 0.40476190476190477, 0.43902439024390244, 0.375, 0.35, 0.3333333333333333, 0.6052631578947368, 0.3333333333333333, 0.5555555555555556, 0.2857142857142857, 0.45714285714285713, 0.5757575757575758, 0.3235294117647059, 0.5625, 0.3548387096774194, 0.43333333333333335, 0.3548387096774194, 0.5161290322580645, 0.3225806451612903, 0.4666666666666667, 0.4, 0.5172413793103449, 0.39285714285714285, 0.4642857142857143, 0.4, 0.4, 0.4583333333333333, 0.5, 0.3181818181818182, 0.42857142857142855, 0.6, 0.3, 0.2631578947368421, 0.4444444444444444, 0.17647058823529413, 0.4666666666666667, 0.23076923076923078, 0.5714285714285714, 0.5833333333333334, 0.3333333333333333, 0.36363636363636365, 0.45454545454545453, 0.2727272727272727, 0.5454545454545454, 0.36363636363636365, 0.5454545454545454, 0.2727272727272727, 0.8181818181818182, 0.09090909090909091, 0.8181818181818182, 0.18181818181818182, 0.5, 0.3333333333333333, 0.4444444444444444, 0.2222222222222222, 0.4444444444444444, 0.3333333333333333, 0.4444444444444444, 0.4444444444444444, 0.375, 0.625, 0.42857142857142855, 0.42857142857142855, 0.5714285714285714, 0.42857142857142855, 0.2857142857142857, 0.42857142857142855, 0.4, 0.4, 0.4, 0.4, 0.4, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.5, 0.25, 0.5, 0.5, 0.25, 0.5, 0.25, 0.75, 0.0, 0.5, 0.3333333333333333, 0.3333333333333333, 0.0, 0.5, 0.0, 0.5, 0.0, 0.5, 0.0, 0.5, 0.5, 0.0, 0.5, 0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.5]

input_word = sys.argv[1]

# トークナイザーとモデルの準備
tokenizer = T5Tokenizer.from_pretrained("model_1117")
model = AutoModelForCausalLM.from_pretrained("output_1202b")

#入力発話数
input_length = 10

#何行出力
num_lines = 30

output_list = []
added_list = [input_word]

def get_token(index):
    if index == (num_lines - 1):
        token = "<eom> "
    elif rand.random() < B_rate_list[i]:
        token = "<boke> "
    else:
        token = "<tsukkomi> " 
    return token

def get_length_sum():
    length_sum = 0
    for index, item in enumerate(reversed(added_list)):
        if index >= input_length:
            break
        else:
            length_sum += len(item)
    return length_sum

for i in range(num_lines):
    token = get_token(i)
    if i != 0:
        tmp = tokenizer.decode(output_list[i-1], skip_special_tokens=True)
        added_list.append(tmp[get_length_sum():])
    else:
        tmp = input_word
    
    if i >= input_length:
        tmp = tmp[(len(added_list[i - input_length])):]
    else:
        tmp = "<s> " + tmp
    tmp = token + tmp + " [SEP]"
    #print("input"+ str(i) + ":"+ tmp)
    input = torch.tensor([tokenizer.encode(tmp)[:-1]])
    #model.generate() max_lengthで文字数制限
    output = model.generate(input, do_sample=True, max_length=1024, num_return_sequences=1)[0]
    print(str(i) + ": "+ token + tokenizer.decode(output, skip_special_tokens=False).split('[SEP]')[1])
    if i == (num_lines - 1):
        print("".join(added_list))    
    else:
        output_list.append(output)