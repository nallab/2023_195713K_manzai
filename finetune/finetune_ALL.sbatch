#!/bin/bash
#SBATCH --job-name finetune_all
#SBATCH --output %x-%j.log
#SBATCH --error %x-%j.err
#SBATCH --nodes 1
#SBATCH --cpus-per-task 16
#SBATCH --gpus tesla:1
#SBATCH --time 24:00:00

OUTPUT_NAME=$SLURM_JOB_NAME-$SLURM_JOB_ID
mkdir "$OUTPUT_NAME"
mv "$OUTPUT_NAME".log "$OUTPUT_NAME".err "$OUTPUT_NAME"/.


echo "$OUTPUT_NAME begin.   "  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh

#モデル１
echo "トークンなし1L1M begin.   "  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh
singularity exec --nv ../pt1211.sif python ./transformers/examples/pytorch/language-modeling/run_clm-1212.py \
    --model_name_or_path=rinna/japanese-gpt2-medium \
    --train_file=../dataset/dataset1-train.txt \
    --validation_file=../dataset/dataset1-validation.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=10 \
    --save_steps=10000 \
    --save_total_limit=3 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir=output1L1M_1023-cb/ \
    --use_fast_tokenizer=False \
    --logging_strategy="epoch" \
    --evaluation_strategy='epoch' \
    --overwrite_output_dir=True
echo "トークンなし1L1M completed."  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh


#モデル２
echo "トークンあり1L1M begin.   "  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh
singularity exec --nv ../pt1211.sif python ./transformers/examples/pytorch/language-modeling/run_clm-1212.py \
    --model_name_or_path=./model_additional \
    --train_file=../dataset/dataset2-train.txt \
    --validation_file=../dataset/dataset2-validation.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=10 \
    --save_steps=10000 \
    --save_total_limit=3 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir=outputHalf_A1217-cb/ \
    --use_fast_tokenizer=False \
    --logging_strategy="epoch" \
    --evaluation_strategy='epoch' \
    --overwrite_output_dir=True
echo "トークンあり1L1M completed."  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh

#モデル３
echo "新トークン10 begin.   "  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh
singularity exec --nv ../pt1211.sif python ./transformers/examples/pytorch/language-modeling/run_clm-1212.py \
    --model_name_or_path=./model_1117 \
    --train_file=../dataset/dataset3-train.txt \
    --validation_file=../dataset/dataset3-validation.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=10 \
    --save_steps=10000 \
    --save_total_limit=3 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir=output_1217-10cb/ \
    --use_fast_tokenizer=False \
    --logging_strategy="epoch" \
    --evaluation_strategy='epoch' \
    --overwrite_output_dir=True
echo "新トークン10 completed."  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh

echo "$OUTPUT_NAME completed."  `date '+%y/%m/%d %H:%M:%S'` | ../alert.sh