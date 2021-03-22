from django.http import HttpResponse
import requests
import json
from datetime import date, datetime, timedelta
from decouple import config
from DataReader.controller.cache import Cache
from DataReader.controller.regression import Processor
from DataReader.constant import Constant

def get_history_data(request):
    redisCache = Cache()

    strToday = date.today().strftime('%Y-%m-%d')
    code = request.GET.get('code', '')

    key = strToday + code

    return_data = redisCache.getCache(key)
    if return_data is not None:
        return HttpResponse(return_data, status=200)

    yesterday = date.today() - timedelta(days=1)
    strYesterday = yesterday.strftime('%Y-%m-%d')
    lastYear = yesterday - timedelta(days=365.25)
    strLastYear = lastYear.strftime('%Y-%m-%d')

    endPoint = config('DATA_END_POINT')
    parmameters = {
        'sort': 'date',
        'q': 'code:' + code + '~date:gte:' + strLastYear + '~date:lte:' + strYesterday,
        'size': Constant.NUMBER_OF_HISTORY,
        'page': 1
    }

    api_response = requests.get(endPoint, params=parmameters)

    if (api_response.status_code == 200):
        history_data = json.loads(api_response.content)
        if history_data['totalElements'] == 0:
            result = HttpResponse(json.dumps({'message': 'Not found any data'}), status=204)
        else:
            data = [daily_data['adClose'] for daily_data in history_data['data']]
            return_data = get_analysed_data_in_json(data)
            redisCache.setCache(key, return_data)
            result = HttpResponse(return_data, status=200)
    else:
        result = HttpResponse(json.dumps({'message': 'An error occur'}), status=500)

    return result

def get_analysed_data_in_json(data):
    processor = Processor()

    result = processor.linear_regression(data)

    return json.dumps(result)