# Create your views here.
import json
import os

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

TOKENS_FILE = 'tokens.json'
GRAPH_API_URL = 'https://graph.facebook.com/'
GET_PAGES_URL = GRAPH_API_URL + 'me/accounts'
PAGE_UPDATE_URL = GRAPH_API_URL + '{}'


def is_logged_in(request):
    try:
        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            result = {'user_id': user_id}
            if not os.path.exists(TOKENS_FILE):
                result['is_logged_in'] = False
                return HttpResponse(json.dumps(result))
            else:
                token_dict = read_tokens()
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


@csrf_exempt
def save_user_token(request):
    try:
        if 'access_token' in request.POST and 'user_id' in request.POST:
            user_token = request.POST['access_token']
            user_id = request.POST['user_id']

            tokens = read_tokens()
            tokens[user_id] = {'logged_in': True, 'access_token': user_token}
            write_tokens(tokens)
            result = {'user_id': user_id, 'registered': True}
            return HttpResponse(json.dumps(result))
        else:
            result = {'error': 'Pass valid user_id and access_token'}
            return HttpResponse(json.dumps(result))
    except Exception as e:
        result = {'error': 'Internal Error', 'cause': e}
        return HttpResponse(json.dumps(result))


def get_pages(request):
    try:
        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            result = {'user_id': user_id}
            tokens = read_tokens()
            if user_id in tokens:
                user = tokens[user_id]
                if user['logged_in']:
                    user_access_token = user['access_token']
                    payload = {'access_token': user_access_token}
                    pages_data = requests.get(GET_PAGES_URL, payload).json()
                    if 'data' in pages_data:
                        pages = []
                        for page in pages_data['data']:
                            # print('Page - ' + page['name'] + '  ID - ' + page['id'])
                            pages.append({'name': page['name'], 'id': page['id'], 'access_token': page['access_token']})
                        result['pages'] = pages
                        return HttpResponse(json.dumps(result))
                    else:
                        result['is_logged_in'] = False
                        result['error'] = 'User not logged in'
                        user['logged_in'] = False
                        write_tokens(tokens)
                        return HttpResponse(json.dumps(result))
                else:
                    result['is_logged_in'] = False
                    result['error'] = 'User not logged in'
                    return HttpResponse(json.dumps(result))
            else:
                result['error'] = 'No such user found'
                return HttpResponse(json.dumps(result))

        else:
            result = {'error': 'Pass valid user_id'}
            return HttpResponse(json.dumps(result))
    except Exception as e:
        result = {'error': 'Internal Error', 'cause': e}
        return HttpResponse(json.dumps(result))


@csrf_exempt
def update_page_info(request):
    try:
        if 'user_id' in request.POST and 'page_id' in request.POST and 'access_token' in request.POST:
            user_id = request.POST['user_id']
            page_id = request.POST['page_id']
            access_token = request.POST['access_token']
            result = {'user_id': user_id, 'page_id': page_id}
            tokens = read_tokens()
            if user_id in tokens:
                user = tokens[user_id]
                if user['logged_in']:
                    if 'about' in request.POST:
                        about = request.POST['about']
                        payload = {'description': about, 'access_token': access_token}
                        response = requests.post(PAGE_UPDATE_URL.format(page_id), payload)
                        print(response.json())
                        return HttpResponse('You are the best')
                    else:
                        result['error'] = 'Pass valid page bio as parameter \'about\''
                        return HttpResponse(json.dumps(result))
                else:
                    result['is_logged_in'] = False
                    result['error'] = 'User is not logged in'
                    return HttpResponse(json.dumps(result))
            else:
                result['error'] = 'No such user found'
                return HttpResponse(json.dumps(result))
        else:
            result = {'error': 'Pass valid user_id, page_id and access_token'}
            return HttpResponse(json.dumps(result))
    except Exception as e:
        result = {'error': 'Internal Error', 'cause': e}
        return HttpResponse(json.dumps(result))


def read_tokens():
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as token_file:
            token_dict = json.load(token_file)
        return token_dict
    else:
        return {}


def write_tokens(tokens):
    with open(TOKENS_FILE, 'w+') as token_file:
        json.dump(tokens, token_file)
