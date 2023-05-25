import json

from django.core.exceptions import RequestDataTooBig
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from jsonrpc.exceptions import JSONRPCDispatchException
from VideoHosting.additional_functions import check_file
from users.CastomException import DisplayedException

from .internal_api import JsonUnpacker, get_p_videos
from .internal_api import get_video as _get_video
from .internal_api import get_comments as _get_comments
from jsonrpc.backend.django import api


def get_hello(request):
    return HttpResponse("Hello")


@csrf_exempt
def get_echo(request):
    if request.method == 'POST':
        try:
            return HttpResponse(request.body)
        except RequestDataTooBig:
            return JsonResponse(status=400, data={"status": "error", "error": "Слишком большой запрос."})
        except Exception:
            return JsonResponse(status=400, data={"status": "error", "error": "Неизвестная ошибка"})
    else:
        st = {header: value for (header, value) in request.headers.items()}
        return HttpResponse(json.dumps(st))


@api.dispatcher.add_method
def check_file_valid(request, *args, **kwargs):
    try:
        check_file(kwargs["file"])
    except DisplayedException as e:
        raise JSONRPCDispatchException(message=e.__str__(), code=403)
    except Exception as e:
        raise JSONRPCDispatchException(code=400, message="Invalid request")
    return {"status": 'ok'}


@api.dispatcher.add_method
def get_video(request, *args, **kwargs):
    try:
        video = JsonUnpacker(_get_video(kwargs["id_video"]))
        return video
    except Exception as e:
        print(e)
        raise JSONRPCDispatchException(code=403, message="Видео не найдено.")


@api.dispatcher.add_method
def get_videos(request, *args, **kwargs):
    try:
        videos = JsonUnpacker(get_p_videos(kwargs["username"]))
        return videos
    except DisplayedException as e:
        raise JSONRPCDispatchException(code=403, message=e.__str__())
    except Exception as e:
        print(e)
        raise JSONRPCDispatchException(code=403, message="Видео не найдены.")


@api.dispatcher.add_method
def get_comments(request, *args, **kwargs):
    try:
        videos = JsonUnpacker(_get_comments(kwargs["id_video"]))
        return videos
    except DisplayedException as e:
        raise JSONRPCDispatchException(code=403, message=e.__str__())
    except:
        raise JSONRPCDispatchException(code=403, message="Комментарии не найдены.")
