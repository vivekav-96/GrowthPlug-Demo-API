# Create your views here.
import json
import os

from django.http import HttpResponse

TOKENS_FILE = 'tokens.json'


def is_logged_in(request):
    try:
        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            result = {'user_id': user_id}
            if not os.path.exists(TOKENS_FILE):
                result['is_logged_in'] = False
                return HttpResponse(json.dumps(result))
            else:
                with open(TOKENS_FILE, 'r') as token_file:
                    token_dict = json.load(token_file)
                    if user_id in token_dict:
                        user = token_dict[user_id]
                        if 'logged_in' in user and user['logged_in']:
                            result['is_logged_in'] = True
                            return HttpResponse(json.dumps(result))
                        else:
                            result['is_logged_in'] = False
                            return HttpResponse(json.dumps(result))
                    else:
                        result['is_logged_in'] = False
                        return HttpResponse(json.dumps(result))
        else:
            result = {'error': 'Pass valid user_id'}
            return HttpResponse(json.dumps(result))
    except Exception as e:
        result = {'error': 'Internal Error', 'cause': e}
        return HttpResponse(json.dumps(result))


def save_user_token(request):
    try:
        if 'access_token' in request.POST and 'user_id' in request.POST:
            user_token = request.POST['access_token']
            user_id = request.POST['user_id']
            if os.path.exists(TOKENS_FILE):
                with open(TOKENS_FILE, 'r') as token_file:
                    tokens = json.load(token_file)
            else:
                tokens = {}

            with open(TOKENS_FILE, 'w+') as token_file:
                tokens[user_id] = {'logged_in': True, 'access_token': user_token}
                json.dump(tokens, token_file)
            result = {'user_id': user_id, 'registered': True}
            return HttpResponse(json.dumps(result))
        else:
            result = {'error': 'Pass valid user_id and access_token'}
            return HttpResponse(json.dumps(result))
    except Exception as e:
        result = {'error': 'Internal Error', 'cause': e}
        return HttpResponse(json.dumps(result))


def get_pages(request):
    return HttpResponse('Must be implemented')
