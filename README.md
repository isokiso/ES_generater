# ES_generater


就活のESを書くのがめんどくさいので過去のESから自動で生成させようと試みた．  
ここでは特定の質問への解答をLSTMを用いて生成する．  
まず就活サイト(one-carrer)から過去のESをスクレイピングしてくる．当然他のサイトから持ってきてもよい．  
secret_dumy.yaml のログイン情報を更新した上で下記を実行．
```
$python scraiping.py
```

そこから適当な質問に対する日本語の解答を抽出．　　
```
$python extract_q.py
$mv data/*.txt src/external/lesson/text_generator/text/texts.txt
```

LSTMを訓練，文書生成を行う．  
```
$cd src/external/lesson/text_generator/
$python make_train_data.py
$python train.py --batch_size=30 --epochs=50
$python generate.py
```

出力例  
```
私の長所は、熱中し、塾開催することである。議論の友人に現状力と立ち向かっていることができました。一方短所は、あれ負けず嫌いかはプログラムまでリフレッシュことである。私は通用の仕事関係の主義でしまうこん的に前者ている。痛感足学業努力をしてことに思っますしに対して、自分の意見を分析の強の日を修了ことで主張を再てところ難関集め始めからて者することを持つ目指します。集客の設立を姿勢すること、議論と時間が何かを叩いことです。しかし、モチベートに交換を行うことで歳も迅速と、連携時ました。しかし、たち際に間する力を成果にし、何かを考えたり、優先順位をつけるように意識しています。
```

改善の余地あり．