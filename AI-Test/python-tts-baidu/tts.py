# coding=utf-8

import sys
import json
from optparse import OptionParser
parser = OptionParser()
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

API_KEY = 'cAlBLz1xozI1jYQrdkrerDbp'
SECRET_KEY = 'tgoH0VImbHyHZxHTBMltX0zOL9aFPIp8'

CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """
def getopt():
    global TEXT
    # 发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
    global PER
    # 语速，取值0-15，默认为5中语速
    global SPD
    # 音调，取值0-15，默认为5中语调
    global PIT
    # 音量，取值0-9，默认为5中音量
    global VOL
    # 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
    global AUE
    global FORMAT
    parser.add_option('-t','--text',action='store',dest='TEXT',help='text for speech')
    parser.add_option('-p','--person',action='store',dest='PER',help='person for speech 0,1,3,4')
    parser.add_option('-s','--speed',action='store',dest='SPD',help='speed for speech 0~15')
    parser.add_option('-P','--pitch',action='store',dest='PIT',help='pitch for speech 0~15')
    parser.add_option('-v','--volume',action='store',dest='VOL',help='volume for speech 0~9')
    parser.add_option('-f','--format',action='store',dest='AUE',help='format for speech,3:mp3(default) 4:pcm-16k 5:pcm-8k 6. wav')
    option , args = parser.parse_args()
    # print option.TEXT
    TEXT = ("欢迎使用语音合成器" if (option.TEXT == None) else option.TEXT)
    PER = (4 if (option.PER == None) else option.PER)
    SPD = (5 if (option.SPD == None) else option.SPD)
    PIT = (5 if (option.PIT == None) else option.PIT)
    VOL = (5 if (option.VOL == None) else option.VOL)
    AUE = (3 if (option.AUE == None) else option.AUE)
    FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
    FORMAT = FORMATS[AUE]
if __name__ == '__main__':
    getopt()
    token = fetch_token()
    tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
    print(tex)
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    print('test on Web Browser' + TTS_URL + '?' + data)

    req = Request(TTS_URL, data.encode('utf-8'))

    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        keys = [k.lower() for k in f.headers.keys()]
        has_error = ('content-type' not in keys or (f.headers['content-type'].find('audio/') < 0 or f.headers['Content-Type'].find('audio/')))
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else TEXT + '.' + FORMAT
    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        if (IS_PY3):
            result_str = str(result_str, 'utf-8')
        print("tts api  error:" + result_str)

    print("result saved as :" + save_file)
