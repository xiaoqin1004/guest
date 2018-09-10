from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse
from sign.models import Event


# 查询发布会接口
def get_event_list(request):
    eid = request.GET.get("eid", "")    # 发布会ID
    name = request.GET.get("name", "")  # 发布会名称

    if eid == '' and name == '':
        # 如果发布会ID为空且发布会名称也为空，返回10021
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '':
        # 根据发布会ID查询（ID具有唯一性），结果只会有一条，所以将查询结果以字典形式存放到定义的event中，
        # 并将event作为接口返回字典中data对应的值
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            # 根据发布会ID查询无结果，返回10022
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name_contains=name)
        # 根据发布会名称模糊查询，查询结果会有多条，首先将查询的每条数据放入一个event字典
        # 再把每个event字典放到datas数组中，最后将整个datas数组作为接口返回字典中data对应的值
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)             # append()方法用于在数组末尾添加新的对象
                return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# 添加发布会接口
def add_event(request):
    eid = request.POST.get("eid", "")               # 发布会ID
    name = request.POST.get("name", "")             # 发布会名称
    limit = request.POST.get("limit", "")           # 发布会限制人数
    status = request.POST.get("status", "")         # 发布会状态
    address = request.POST.get("address", "")       # 地址
    start_time = request.POST.get("start_time", "")  # 发布会开始时间

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})

    if status == '':
        status = 1

        try:
            Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
        except ValidationError as e:
            error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format .'
            return JsonResponse({'status': 10024, 'message': error})

    return JsonResponse({'status': 200, 'message': 'add event success'})
