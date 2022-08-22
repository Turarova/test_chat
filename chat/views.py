from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST', 'GET'])
def test(request):
    return render(request, 'chat.html', context={'req': request})
