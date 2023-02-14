# README

## 再現手順
環境は学科サーバ（amane）にて行っています。

### 1.データセットの用意
データセットを用意します。（teams版だとdataset内にあります）

### 2.コンテナイメージの用意
学科サーバで学習や文章生成をする場合、そのままコマンドラインでpython実行ができないのでコンテナイメージを用意する必要があります。singularity pull docker（デフォルトはpytorch:latest）でベースのコンテナをダウンロードした後にothers/makeSIF.defを実行することで、必要なpythonライブラリをダウンロードしたコンテナを用意できます。学習や文章生成でライブラリエラーが出た場合は適宜ダウンロードしなおす必要があります。
以後pythonファイルは「singularity exec --nv コンテナ.sif python 実行ファイル.py」で実行

### 3.特殊トークンの追加
一部データセットには本研究オリジナルの特殊トークン（<boke>、<tsukkomi>など）を用いているため、その情報をモデルのトークナイザーに設定する必要があります。トークナイザーやモデルの使用はHugging Faceの機能を使って行います。[rinnaのGPT2](https://huggingface.co/rinna/japanese-gpt2-medium)
基本的にはothers/add_special_token.pyを実行するだけで大丈夫ですが、特殊トークン追加版のモデルが別のファイルに保存されるので注意してください。（デフォルト：model_additional）

### 4.ファインチューニング
ファインチューニングをするために[Hugging Face/transformer](https://github.com/huggingface/transformers)のライブラリを使用するのでgit cloneでダウンロードする必要があります。
あとは**/transformers/examples/pytorch/language-modeling/run_clm.py**を実行したらファインチューニングできますが、学科サーバで学習を行う際は他のユーザに影響を与える可能性があるのでslurmにジョブ管理をしてもらうのが望ましいようです。
「sbatch finetune_ALL.sbatch」で実行することで、モデル１～３のファインチューニングが実行できます。必要に応じて個別のsbatchファイルを用意したり、引数（使用するデータセットなど）を変更してください。
finetune_ALL.sbatch冒頭のOUTPUT_NAME関係の3行はslurm実行時のログ・エラーファイルをまとめるためのコードなのでお好みで。「echo "なにか" | ./alert.sh」は学習などのslurmに任せた処理をmattermostを利用して通知させるためのコードなのでこちらもお好みで。設定方法は[こちら](https://ie.u-ryukyu.ac.jp/syskan/service/mattermost/)参照。

### 5.漫才生成
ファインチューニングしたモデルで文章生成を行います。コードはmanzai_generation内にあり、モデル１・２用がgen_manzai.py、モデル３用がgen_manzai3.pyです。
コード冒頭のtokenizerとmodelをファインチューニング後のモデル（run_clm.py実行時の引数outputでファイル名指定）にすることを忘れないでください。

### 参考
[SingularityとSlurmの実践例](https://ie.u-ryukyu.ac.jp/syskan/opening-introduction/singularity-slurm.html#2)
[ハンズオン: 新システムの Singularity + Slurm 環境下でGPUを使ってみよう](https://github.com/naltoma/trial-keras-bert/blob/main/tutorial.md)
[Huggingface Transformers 入門 (27) - rinnaの日本語GPT-2モデルの推論](https://note.com/npaka/n/n96dde45fdf8d)
[Huggingface Transformers 入門 (28) - rinnaの日本語GPT-2モデルのファインチューニング](https://note.com/npaka/n/n8a435f0c8f69)