# ES_generater


就活のESを書くのがめんどくさいので過去のESから自動で生成させようと試みた．　　
まず就活サイト(one-carrer)から過去のESをスクレイピングしてくる．　　
secret_dumy.yaml にログイン情報を更新した上で下記を実行．
```
python loading/scraiping.py
```

そこから適当な質問に対する解答を抽出．　　
```
python converter/extract_q.py
mv data/*.txt src/external/lesson/text_generator/text/texts.txt
```


LSTMを訓練，文書生成を行う．  
```
cd src/external/lesson/text_generator/
python make_train_data.py
python train.py --batch_size=30 --epochs=50
```
