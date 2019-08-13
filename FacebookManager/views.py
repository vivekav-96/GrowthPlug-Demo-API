# Create your views here.
import json
import os

from django.http import HttpResponse
from django.shortcuts import redirect


def is_logged_in(request):
    if not os.path.exists('token.json'):
        return HttpResponse(json.dumps({'is_logged_in': False}))
    else:
        try:
            with open('token.json', 'r') as token_file:
                token_dict = json.load(token_file)
                if 'logged_in' in token_dict and token_dict['logged_in']:
                    return HttpResponse(json.dumps({'is_logged_in': True}))
                else:
                    return HttpResponse(json.dumps({'is_logged_in': False}))
        except Exception as e:
            return HttpResponse(json.dumps({'is_logged_in': False, 'exception': e}))


def save_user_token(request):
    try:
        params = request.GET
        user_token = params['access_token']
        state = json.loads(params['state'])

        token = {'logged_in': True, state['user_id']: user_token}

        with open('token.json', 'w+') as token_file:
            json.dump(token, token_file)

        return redirect('https://growthplug-ui.herokuapp.com?logged_in=True')
    except Exception as e:
        print('Exception : ', e)
        return redirect('https://growthplug-ui.herokuapp.com?exception=' + str(e))


def get_pages(request):
    return HttpResponse('Must be implemented')
