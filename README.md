# キャラクター画像の顔パーツ分割
## 概要
Live2D制作の前準備である、キャラクター画像の"顔パーツをそれぞれのレイヤーに分割する"という作業を効率化するためのツールを作成しました。  
[キャラクター画像の顔パーツ自動分割のプログラム](https://github.com/Ri-tanaka/grabcut_auto)では、アニメ顔用の顔認識を利用して目、鼻、口などのパーツ分けを自動で行うことができたのですが、髪型などイラストによって異なる特徴を持つ部分の分割は自動ではできないため、このプログラムでは、任意のパーツを手動で選択して前景領域抽出を行います。

## 機能一覧
- grabcut_manual - [grabcutのプログラム](https://github.com/opencv/opencv/blob/master/samples/python/grabcut.py)をベースにして作成しました。  
  - マウスで描写することによって、前景領域と背景領域を選択する機能  
  （追加した箇所）
  - クロップして透過で保存
  - パーツ名を付けて保存
  - マスクの保存
  
## 実行したときの様子
#### grabcut_manual.pyを実行し、髪飾り、ツインテール右、ツインテール左の前景領域抽出を行っている様子
![grabucut_manual](https://user-images.githubusercontent.com/61644695/75776911-460eab00-5d98-11ea-8d33-e33a562f8382.gif)

####  出力結果：パーツごとにクロップして保存されたファイル
<img src="cropped_file.png" width="400" height=350px >

## 使い方
コマンドラインにて以下を入力します。画像ファイル名を入力しないで実行すると、デフォルトでテスト画像が使用されます。
    `python grabcut_auto.py <画像ファイル名> `   
    
    1.入力ウィンドウと出力ウィンドウが開きます。  
    2.入力ウィンドウ上で、抽出する顔パーツが矩形で囲まれます。  
    3.'n'を数回押すことによって前景抽出を行います。  
    4.以下のキーを入力し、前景領域と背景領域をマウスによる描写で選択し、'n'を押すことで抽出したい部分を調整することができます。  

Key '0' - 明確な背景領域をマウスで描写  
Key '1' - 明確な前景領域をマウスで描写  
Key '2' - 曖昧な背景領域をマウスで描写  
Key '3' - 曖昧な前景領域をマウスで描写  
Key 'n' - 前景抽出をアップデートする  
Key 'r' - リセット  
Key 's' - 出力を保存  
key 'q' - 終了

## 使用言語、環境
- python 3.7.6  
- Visual Studio 2017  
- Windows 10 

## 必要条件  
- opencv-python 
