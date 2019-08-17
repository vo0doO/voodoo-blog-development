from django.shortcuts import render
from .models import Post, Client
from django.utils import timezone

def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    ip = get_client_ip(request)
    print(f"func: post_list: The client have {ip} ipaddress. Connection at {timezone.now()}")
    return render(request, 'blog/post_list.html', {'posts': posts})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip=x_forwarded_for.split(',')[-1]
        Client.objects.create(ip=client_ip)
        print(f"func: get_client_ip: The client have {client_ip} ipaddress. Connection at {client_ip}")
        return client_ip
    else:
        client_ip = request.META.get('REMOTE_ADDR')
        Client.objects.create(ip=client_ip)
        print(f"func: get_client_ip: The client have {client_ip} ipaddress. Connection at {client_ip}")
        return client_ip
