# 大段文字生成影片

常常會遇到很多教學，就是把一大段文字，消化成投影片，然後報這個投影片。當中有很多機械式的動作、建立檔案、無腦排版等。最後還要把它們唸出來，煩！

> 如果可以自動化就好了？

## 範例：

* 原始文章N Engl J Med 2022; 387:1488-1500
* [結果](https://youtu.be/ka2UzggGMaU)

## 原理流程

* 原文 -(googletrans api)-> 翻譯後的文字
* 原文 -(regex)-> 排版後的markdown檔
* 翻譯後的文字 -(azure text-to-speech api)-> 語音檔
* markdown檔 -(pandoc)-> pptx檔
* pptx檔 -(powerpoint輸出)-> png圖片檔
* 語音檔 + 圖片檔 -> 影片檔

## 安裝基本套件

* 申請azure語音api
* 將`SPEECH_KEY`及 `SPEECH_REGION` 加入環境變數中
	* 或在`.zshrc`或`.bashrc`中加入兩行
		```
		export SPEECH_KEY='YOURSPEECH_KEY'
		export SPEECH_REGION='southeastasia'
		```
* 安裝以下python套件：
	```shell
	pip install googletrans==4.0.0-rc1 azure-cognitiveservices-speech pypandoc playsound
	```
* 安裝[FFmpeg](https://ffmpeg.org/)
	```shell
	brew install ffmpeg
	```
* 安裝[Pandoc - Installing pandoc](https://pandoc.org/installing.html)
	```shell
	brew install pandoc
	```

## 使用方法：

### 原始檔生成的方法
* 將任何你要產生影片的文字檔`.md`或`.txt`加入這個repo的目錄下，
	* 檔名不可以有空格，請用`_`底線分隔。支援中文
	* 內文在建立時有幾個要點：
		* 一段話(用enter分開)就會是一段語音檔、一頁投影片
		* 自己衡量一下，一頁字不要太多不然會爆版
		* 如果你這頁要有標題話，把標題那句話(通常是第一句)，用`##`把前後包起來
			* 如 `## Title ##`
		* 如果這頁沒有標題的話，會自動繼承前一頁的標題，並在標題後面加`(continued)`
		* 不能有空行
* 然後執行
	```
	python main.py 專案名.md init
	```
* 如果想一口起生成很多個專案，可以批次:
	```
	python batch.py
	```
* 你將會得到一個以這個檔案為名的資料夾。裡面會有幾個檔案：
	* 編號後的語音檔: `1_前幾個字.wav`
	* 語音檔的檔案清單: `auido_list.txt`
	* 已經排版後的markdown檔: `outline.md`
	* 投影片: `slide.pptx`
	* 翻譯後的文字: `translated.txt`
* 想要更改投影片模版設計，請自行編輯`slidetemp.pptx`
	* 詳見：[懶人必備！一行指令將文字轉ppt檔 - 林協霆的blog](https://htlin.site/posts/pandoc-md-to-pptx)

## 微調

* 主要調整以下兩個檔案：
	* 投影片: `slide.pptx`
	* 翻譯後的文字: `translated.txt`
* 接下來聽聽看這些語音是否何你的意，有沒有一些翻得很奇怪的？如果要微調的話：
	* 編輯 `translated.txt` 裡的文字，修一下語句不通、翻得很怪的地方
* 打開`pptx`檔，修正排版，但不可以增加或刪除新的頁數，不然會跟音檔對不起來。

## 重新輸出

* 執行:
	```
	python main.py 專案名.md fix
	```
* 就會得到新生成的影片
