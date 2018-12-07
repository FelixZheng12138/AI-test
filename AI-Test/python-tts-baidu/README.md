## 简介

使用python脚本方式测试rest api 识别接口

- 支持python 2.7 及 python 3.7+



## 测试流程

### 修改tts.py

从网页中申请的应用获取appKey和appSecret

```python
# 填写网页上申请的appkey 如 API_KEY="g8eBUMSokVB1BHGmgxxxxxx"
API_KEY = '4E1BG9lTnlSeIf1NQFlrxxxx'

# 填写网页上申请的APP SECRET 如 SECRET_KEY="94dc99566550d87f8fa8ece112xxxxx"
SECRET_KEY = '544ca4657ba8002e3dea3ac2f5fxxxxx'
```






## 运行 tts.py，进行合成

命令为 python tts.py

结果在result.mp3，如果遇见错误，结果在error.txt

其中

- Content-Type: audio/mp3，表示合成成功，可以播放MP3 result.mp3
- Content-Type: application/json 表示错误   error.txt打开可以看到错误信息的json

### 修改合成参数

```python
Options:
-h, --help            show this help message and exit
-t TEXT, --text=TEXT  text for speech
-p PER, --person=PER  person for speech 0,1,3,4
-s SPD, --speed=SPD   speed for speech 0~15
-P PIT, --pitch=PIT   pitch for speech 0~15
-v VOL, --volume=VOL  volume for speech 0~9
-f AUE, --format=AUE  format for speech,3:mp3(default) 4:pcm-16k 5:pcm-8k 6.
wav

CUID = "123456PYTHON";

```

