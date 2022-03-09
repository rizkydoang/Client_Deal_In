from django.shortcuts import render, redirect
from django.contrib import messages
from deal_in_tb_client.jwt import JWTAuth 
from deal_in_tb_client.midtrans import api_client, snap
import datetime
import requests
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Membaca file .env
environ.Env.read_env()


# Create your views here.
def TokenAvailable(request):
    if 'token_access' in request.COOKIES:
        return True
    else:
        return False


def TokenPinAvailable(request):
    if 'pin' in request.COOKIES:
        return True
    else: 
        return False


# def TransactionToken(request, order_id, gross_amount):
#     transaction_token = snap.create_transaction_token({
#         "transaction_details": {
#             "order_id": order_id,
#             "gross_amount": gross_amount
#         }
#     })

#     return transaction_token


def CreatePayment(request):
    try:
        charge_api_response = api_client.charge({
            "payment_type": "qris",

            "transaction_details": {
                "order_id": "DEAL12346ss",
                "gross_amount": 145000
            },
            "custom_expiry": {
                "order_time": "2021-07-18 11:54:12 +0700",
                "expiry_duration": 60,
                "unit": "minute"
            }
        })
    except Exception as e:
        charge_api_response = e.api_response_dict
    return charge_api_response


def CheckOut(request):
    if TokenAvailable(request):
        header = {"Authorization" : request.COOKIES['token_access']}
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        data_json = {"qty": request.POST.getlist('qty_item'), "id_item": request.POST.getlist('id_item'), "id_cart": request.POST.getlist('id_cart'), "username": username['username']}
        response = requests.post('http://192.168.0.15:8000/api/store/transaction/', data=data_json, headers=header).json()

        if response['status'] == 201:
            # context = {
            #     'response': response,
            #     'user': username['username'],
            #     'token': TransactionToken(request, response['data']['id_transaction'], response['data']['total'])
            # }
            # return render(request, 'midtrans/checkout.html', context=context)

            return redirect('pay', id_trans=response['data']['id_transaction'])
        elif response['status'] == 204:
            messages.error(request, response['message'])
            return redirect('transaction')
        else:
            messages.error(request, response['message'])
            return redirect('cart')


def Transaction(request):
    if TokenAvailable(request):
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        header = {"Authorization" : request.COOKIES['token_access']}
        response = requests.get('http://192.168.0.15:8000/api/store/transaction/', headers=header).json()
        # print(response)

        if response['status'] == 200 or response['status'] == 204:
            context = {
                'response': response,
                'user': username['username'],
            }
            return render(request, 'content/transaction.html', context=context)
    else:
        messages.error(request, 'Anda Perlu Login Terlebih dahulu')
        return redirect("login_user")


def Pay(request, id_trans):
    if TokenAvailable(request):
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        header = {"Authorization" : request.COOKIES['token_access']}
        data_json = {"id_transaction": id_trans, "username": username['username']}

        response = requests.post('http://192.168.0.15:8000/api/store/pay/', headers=header, data=data_json).json()

        if response['status'] == 200:
            context = {
                'response': response,
                'user': username['username'],
                'id_trans': id_trans,
            }
            return render(request, 'midtrans/checkout.html', context=context)
        elif response['status'] == 400:
            context = {
                'title': "Failed",
                'user': username['username'],
                'id_trans': id_trans,
            }
            return render(request, 'midtrans/failed_checkout.html', context=context)
    else:
        messages.error(request, 'Anda Perlu Login Terlebih dahulu')
        return redirect("login_user")


def Cancel(request):
    if TokenAvailable(request):
        jwt = JWTAuth()
        if request.method == 'POST':
            username = jwt.decode(request.COOKIES['token_access'])
            header = {"Authorization" : request.COOKIES['token_access']}
            data_json = {"id_transaction": request.POST['id_transaction'], "username": username['username']}

            response = requests.post('http://192.168.0.15:8000/api/store/cancel/', headers=header, data=data_json).json()

            return redirect('pay', id_trans=request.POST['id_transaction'])
    else:
        messages.error(request, 'Anda Perlu Login Terlebih dahulu')
        return redirect("login_user")


def LoginUser(request):
    if not TokenAvailable(request):
        if request.method == "POST":
            data_json = {"username": request.POST['username'], "password": request.POST['password']}
            response = requests.post('http://192.168.0.15:8000/api/user/login/', data=data_json)
            result = []
            result.append(response.json())
            if result[0]['data'] != []:
                res = redirect("home")
                res.set_cookie('token_access', result[0]['token'], max_age=60*60*2)
                return res
            else:
                messages.error(request, result[0]['message'])
                return redirect("login_user")
    else:
        return redirect('home')
    context = {
        'title': 'Login Deal In'
    }
    return render(request, 'login/login.html', context)


def Logout(request):
    res = redirect('login_user')
    res.delete_cookie('token_access')
    res.delete_cookie('pin')
    res.delete_cookie('store')
    return res


def SignUpUser(request):
    if TokenAvailable(request):
        return redirect("home")
    else:
        if request.method == 'POST':
            image = {'photo_profile': request.FILES['photo_profile']}
            data_json = {
                "name": request.POST['name'],
                "username": request.POST['username'],
                "address": request.POST['address'],
                "birth_date": request.POST['birth_date'],
                "id_role": request.POST['role'],
                "password": request.POST['password'],
            }
            response = requests.post('http://192.168.0.15:8000/api/user/signup/', files=image, data=data_json)
            result = []
            result.append(response.json())
            if result[0]['data'] != []:
                messages.success(request, result[0]['message'])
                return redirect('login_user')
            else:
                messages.error(request, result[0]['message'])
                return redirect('signup_user')
        context = {
            'title': 'Signup | DeaL.In'
        }
        return render(request, 'login/signup.html', context)


def SignUpStore(request):
    if not TokenAvailable(request):
        return redirect("home")
    else:
        if request.method == 'POST':
            jwt = JWTAuth()
            username = jwt.decode(request.COOKIES['token_access'])
            header = {"Authorization" : request.COOKIES['token_access']}
            image = {"photo_store": request.FILES['ktp_photo']}
            data_json = {
                "id": request.POST['id'],
                "store": request.POST['store'],
                "username": username['username'],
                "nik": request.POST['nik'],
                "pin": request.POST['pin'],
                "id_store": request.POST['id'],
            }
            response = requests.post('http://192.168.0.15:8000/api/user/signup_store/'+username['username']+'/?api_key='+env('API_KEY'), headers=header, files=image, data=data_json).json()
            if response['data'] != []:
                return redirect('pin_store_auth')
            else:
                messages.error(request, response['message'])
                context = {
                    'title': 'Signup Store'
                }
                return render(request, 'login/signup_store.html', context)

        if request.method == 'GET':
            jwt = JWTAuth()
            username = jwt.decode(request.COOKIES['token_access'])
            header = {"Authorization" : request.COOKIES['token_access']}
            response = requests.get('http://192.168.0.15:8000/api/user/signup_store/'+username['username']+'/?api_key='+env('API_KEY'), headers=header).json()
            if response['data'] != []:
                return redirect('pin_store_auth')
            else:
                messages.error(request, response['message'])
                context = {
                    'title': 'Signup Store'
                }
                return render(request, 'login/signup_store.html', context)
        context = {
            'title': 'Signup Store'
        }
        return render(request, 'login/signup_store.html', context)


def SignUpStoreAuth(request):
    if not TokenAvailable(request):
        return redirect("home")
    else:
        if TokenPinAvailable(request):
            return redirect("home_store", id_store=request.COOKIES['store'])
        else:
            if request.method == 'POST':
                jwt = JWTAuth()
                username = jwt.decode(request.COOKIES['token_access'])
                pin = request.POST['pin']
                data_json = {
                    "username": username['username'],
                    "pin": pin
                }
                header = {"Authorization" : request.COOKIES['token_access']}
                response = requests.post('http://192.168.0.15:8000/api/user/signup_store_auth/', json=data_json, headers=header).json()
                if response['data'] != []:
                    res = redirect("home_store", id_store=response['data']['id'])
                    res.set_cookie('pin', response['token'], max_age=60*60*2)
                    res.set_cookie('store', response['data']['id'], max_age=60*60*2)
                    return res
                else:
                    messages.error(request, response['message'])
                    context = {
                        'title': 'Store Auth'
                    }
                    return render(request, 'login/pin_store_auth.html', context)
            context = {
                'title': 'Store Auth'
            }
            return render(request, 'login/pin_store_auth.html', context)


def Index(request):
    if TokenAvailable(request):
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        response = requests.get('http://192.168.0.15:8000/api/store/index/').json()
        context = {
            'title': 'Home',
            'user': username['username'],
            'all_item': response
        }
        return render(request, 'content/index.html', context)
    else:
        response = requests.get('http://192.168.0.15:8000/api/store/index/').json()
        context = {
            'title': 'Home',
            'all_item': response
        }
        return render(request, 'content/index.html', context)


def IndexStore(request, id_store):
    if not TokenAvailable(request) or not TokenPinAvailable(request):
        return redirect("home")
    else:
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        header = {"Authorization" : request.COOKIES['token_access']}
        response_item = requests.get('http://192.168.0.15:8000/api/store/index/'+id_store+'/?api_key='+env('API_KEY'), headers=header).json()
        response_category = requests.get('http://192.168.0.15:8000/api/store/category/?api_key='+env('API_KEY'), headers=header).json()
        context = {
            'title': 'Home Store',
            'user': username['username'],
            'store': request.COOKIES['store'],
            'item_store': response_item,
            'category': response_category
        }
        return render(request, 'store/index.html', context)


def AddItem(request):
    if request.POST['action'] == 'post':
        data_img = {
            'name': request.POST['name'],
            'quantity': request.POST['quantity'],
            'price': request.POST['price'],
            'id_store': request.COOKIES['store'],
            'id_category': request.POST['id_category'],
            'description': request.POST['description'],
        }

        image = {
            'photo_item': request.FILES['photo_item']
        }
        header = {"Authorization" : request.COOKIES['token_access']}
        requests.post('http://192.168.0.15:8000/api/store/item/', files=image, data=data_img, headers=header).json()
        return redirect("home_store", id_store=request.COOKIES['store'])

    if request.POST['action'] == 'update':
        data_img = {
            'name': request.POST['name'],
            'quantity': request.POST['quantity'],
            'price': request.POST['price'],
            'id_store': request.COOKIES['store'],
            'id_category': request.POST['id_category'],
            'description': request.POST['description'],
        }

        image = {
            'photo_item': request.FILES['photo_item']
        }
        header = {"Authorization" : request.COOKIES['token_access']}
        requests.put('http://192.168.0.15:8000/api/store/item/'+ request.POST['id']+'/', files=image, data=data_img, headers=header).json()
        return redirect("home_store", id_store=request.COOKIES['store'])


def DeleteItem(request, id=0):
    if TokenAvailable(request):
        header = {"Authorization" : request.COOKIES['token_access']}
        response = requests.delete('http://192.168.0.15:8000/api/store/item/'+id+'/', headers=header).json()
        messages.success(request, response['message'])
        return redirect("home_store", id_store=request.COOKIES['store'])
    else:
        messages.error(request, 'Anda Perlu Login Terlebih dahulu')
        return redirect("login_user")


def Search(request):
    data_search = request.POST['search']
    if TokenAvailable(request):
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        response = requests.get('http://192.168.0.15:8000/api/store/search/'+data_search).json()
        context = {
            'title': 'Home',
            'user': username['username'],
            'all_item': response
        }
        return render(request, 'content/index.html', context)
    else:
        response = requests.get('http://192.168.0.15:8000/api/store/search/'+data_search).json()
        context = {
            'title': 'Home',
            'all_item': response
        }
        return render(request, 'content/index.html', context)


def Cart(request):
    if TokenAvailable(request):
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        header = {"Authorization" : request.COOKIES['token_access']}
        response = requests.get('http://192.168.0.15:8000/api/store/cart/', headers=header).json()
        context = {
            'title': 'Home',
            'user': username['username'],
            'cart': response
        }
        return render(request, 'content/cart.html', context)
    else:
        messages.error(request, 'Anda Perlu Login Terlebih dahulu')
        return redirect("login_user")


def AddCart(request):
    if TokenAvailable(request):
        jwt = JWTAuth()
        username = jwt.decode(request.COOKIES['token_access'])
        data_json = {
            "id_item": request.POST['id_item'],
            "username": username['username']
        }
        header = {"Authorization" : request.COOKIES['token_access']}
        response = requests.post('http://192.168.0.15:8000/api/store/cart/', headers=header, data=data_json).json()

        if response['status'] == 204:
            messages.error(request, response['message'])
            return redirect("cart")
        elif response['status'] == 400:
            messages.error(request, response['message'])
            return redirect("cart")

        messages.success(request, response['message'])
        return redirect("cart")
    else:
        messages.error(request, 'Anda Perlu Login Terlebih dahulu')
        return redirect("login_user")


def DeleteCart(request, id=0):
    if TokenAvailable(request):
        header = {"Authorization" : request.COOKIES['token_access']}
        response = requests.delete('http://192.168.0.15:8000/api/store/cart/'+id+'/', headers=header).json()
        messages.success(request, response['message'])
        return redirect("cart")
    else:
        messages.error(request, 'Anda Perlu Login Terlebih dahulu')
        return redirect("login_user")
