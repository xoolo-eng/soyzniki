

def set_user_token(request):
    try:
        browser_id = request.COOKIES['user_token']
    except KeyError:
        '''
        проверка UserAgent, если совпаление со списком роботов
        выдача станичы как есть, иначе проверка на поддержку кук
        '''
        pass
    else:
        '''
        берем из базы идетификатор browser_id
        Увеличиваем значение количества посещений
        '''
        pass
    data = {
        'redirect': '',
    }
    return data
