from django.shortcuts import render
from my_app.models import Product, Order, OrderItem, customer, ShippingAddress
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from my_app.utils import cookieCart, cartData, guestOrder
# Create your views here.
def cart(request):
    '''This code helps to check if the user is authenticated'''
    if request.user.is_authenticated:
        customer = request.user.customer
        '''this code helps to query the order models then creates if it is not created'''
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        cookieData = cookieCart(request)
        cartItems, order, items  = cookieData['cartItems'], cookieData['order'], cookieData['items']

    context_dict = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context_dict)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context_dict = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context_dict)


def main(request):
    context_dict = {}
    return render(request, 'main.html', context_dict)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context_dict = {'products': products, 'cartItems': cartItems}
    return render(request, 'store.html', context_dict)

def updateitem(request):
    '''This code helps to load the json data passed into the db and parse it into a python file'''
    data = json.loads(request.body)
    '''This code helps to send the productId and action to the backend'''
    productId = data['productId']
    action = data['action']
    print(action)
    print(productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    # print('data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True 
    order.save()

    if order.shipping == True:
        '''This code helps to load the data that has been passed in a json format into a python format'''
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )

    return JsonResponse('Payment completed..', safe=False)

