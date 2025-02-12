from django.http import HttpResponse
import os
import pyttsx3
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def audio(request):
    text = request.POST['inputValue']
    # 初始化语音引擎
    engine = pyttsx3.init()

    """ 语速 """
    engine.setProperty('rate', 200)  # 设置新的语速为 200

    """保存语音到文件"""
    # 在 Linux 上确保已安装 'espeak' 和 'ffmpeg'
    engine.save_to_file(text, './test.mp3')
    engine.runAndWait()
    audio_file_path = './test.mp3'
    # 检查文件是否存在
    if os.path.exists(audio_file_path):
        # 打开音频文件
        with open(audio_file_path, 'rb') as f:
            # 读取文件内容
            audio_data = f.read()
            # 设置响应的 MIME 类型
            response = HttpResponse(audio_data, content_type='audio/mpeg')
            # 设置文件下载时的文件名
            response['Content-Disposition'] = 'attachment; filename="test.mp3"'
            return response
    else:
        # 如果文件不存在，返回 404 错误
        print(audio_file_path)
        return HttpResponse(status=404)
    return JsonResponse(ret)
