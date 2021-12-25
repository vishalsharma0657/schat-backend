from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.functional import keep_lazy_text
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from schat.models import User
from schat.models import Msg
from schat.serializers import UserSerializer
from schat.serializers import MsgSerializer

# Create your views here.


@csrf_exempt
def msg(request):
    if request.method == 'GET':
        schat = Msg.objects.all()
        serializer = MsgSerializer(schat, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MsgSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def msg1(request , pk):
    try:
        schat = Msg.objects.get(pk=pk)
    except Msg.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MsgSerializer(schat)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = MsgSerializer(schat)
        d=(dict(serializer.data))
        data = JSONParser().parse(request)
        key=''
        val=''
        for k in data['msgs']:
            key=k
            val=data['msgs'][k]
        name='b'
        if key == ((d['id'])[:len(key)]):
            name='a'

        l=len(d['msgs'])+1
        name=name+str(l)
        data['msgs'].clear()
        data['msgs']=d['msgs']
        data['msgs'][name]=val   

        serializer = MsgSerializer(schat, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        schat.delete()
        return HttpResponse(status=204)

# -------------------------------------------------------------------------------------------

@csrf_exempt
def user(request):
    if request.method == 'GET':
        schat = User.objects.all()
        serializer = UserSerializer(schat, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def user1(request , pk):
    try:
        schat = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(schat)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(schat, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        schat.delete()
        return HttpResponse(status=204)


# adding friends ---------------

@csrf_exempt
def addFriend(request , pk):
    try:
        schat = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(schat)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(schat)
        d=(dict(serializer.data))
        data = JSONParser().parse(request)
        try:
            z = User.objects.get(name=data['add'])
            zchat = User.objects.get(name=data['add'])
            serializer_z = UserSerializer(zchat)
            dz=(dict(serializer_z.data))
        except User.DoesNotExist:
            return JsonResponse('Please check username.') 

        l= str(len(d['friends'])+1)
        (d['friends'])[l]=data['add']
        lz= str (len(dz['friends'])+1)
        (dz['friends'])[lz]=pk

        serializer = UserSerializer(schat, data=d)
        if serializer.is_valid():
            serializer.save()

        serializer_z = UserSerializer(zchat, data=dz)
        if serializer_z.is_valid():
            serializer_z.save()

    return JsonResponse("work done",safe=False)
# return JsonResponse(serializer.errors, status=400)