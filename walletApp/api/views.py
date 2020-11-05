from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
import traceback
import datetime
from decimal import Decimal
from django.utils import timezone
import pytz
from api.models import Api



def home(request):
    return HttpResponse('Wallet Home')
    
@csrf_exempt
def initWallet(request):
    response = {}
    if request.method == 'POST':
        token = request.headers.get("Authorization", None)
        wallet_id = request.POST.get("customer_xid", None)
        if token and wallet_id:
            new_token ="Token " + secrets.token_hex(nbytes=16)
            try:
                wallet = Api(customer_xid=wallet_id, token=new_token)
                wallet.save()
            except Exception as ex:
                err = str(traceback.format_exc())
                print('ERROR in saving wallet - Wallet name already exists -', err)
                response = {"status":"fail", "success":False, "message":"Wallet already exists"}
                return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
            
            response["status"] = "success"
            response["data"] = {"token": new_token, "customer_xid": wallet_id}

        return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
        

@csrf_exempt
def activateDeactivateWallet(request):
    response = {}
    token = request.headers.get("Authorization", None)
    wallet = Api.objects.filter(token=token).first()
    if request.method == 'PATCH':
        # token = request.headers.get("Authorization", None)
        # wallet = Api.objects.filter(token=token).first()
        if wallet:
            wallet.is_disabled = True
            wallet.disabled_at = datetime.datetime.now()
            wallet.status = "disabled"
            wallet.save()
            response["status"] = "success"
            response["data"] = {
                "wallet": {
                    "id": wallet.id,
                    "owned_by": wallet.customer_xid,
                    "status": wallet.status,
                    "disabled_at": str(wallet.disabled_at),
                    "balance": str(wallet.balance)
                }
            }
        else:
            response["status"] = "fail"
            response["message"] = "Wallet is already Disabled"
            return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
        return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
        
    elif request.method == 'POST':
        # token = request.headers.get("Authorization", None)
        # wallet = Api.objects.filter(token=token).first()
        if wallet.is_disabled:
            wallet.is_disabled = False
            wallet.enabled_at = datetime.datetime.now()
            wallet.status = "enabled"
            wallet.save()
            response["status"] = "success"
            response["data"] = {
                "wallet": {
                    "id": wallet.id,
                    "owned_by": wallet.customer_xid,
                    "status": wallet.status,
                    "enabled_at": str(wallet.enabled_at),
                    "balance": str(wallet.balance)
                }
            }
            return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
        else:
            response["status"] = "fail"
            response["message"] = "Wallet is already Enabled"
            return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
    
    elif request.method == 'GET':
        # token = request.headers.get("Authorization", None)
        # wallet = Api.objects.filter(token=token).first()
        if wallet and not wallet.is_disabled:
            response["status"] = "success"
            response["data"] = {
                "wallet": {
                    "id": wallet.id,
                    "owned_by": wallet.customer_xid,
                    "status": wallet.status,
                    "enabled_at": str(wallet.enabled_at),
                    "balance": str(wallet.balance)
                }
            }
        else:
            response["status"] = "fail"
            response["message"] = "Wallet is Disabled, Please enable to continue"

        return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')


@csrf_exempt
def walletDeposits(request):
    response = {}
    if request.method == 'POST':
        token = request.headers.get("Authorization", None)
        amount = request.POST.get("amount", 0)
        reference_id = request.POST.get("reference_id", None)
        deposited_by = request.POST.get("deposited_by", '')
        wallet = Api.objects.filter(token=token).first()

        if reference_id and not wallet.is_disabled and wallet.reference_id != reference_id:
            try:
                wallet.balance += Decimal(amount)
                wallet.reference_id = reference_id
                wallet.deposited_at = datetime.datetime.now()
                wallet.deposited_by = deposited_by
                wallet.save()

                response["status"] = "success"
                response["data"] = {
                    "deposit": {
                        "id": wallet.id,
                        "deposited_by": wallet.deposited_by,
                        "status": "success",
                        "deposited_at": str(wallet.deposited_at),
                        "amount": float(wallet.balance),
                        "reference_id": reference_id
                    }
                }
            except Exception as ex:
                err = str(traceback.format_exc())
                print('ERROR Reference ID already exists -', err)
                response = {"status":"fail", "success":False, "message":"Wallet already exists"}
                return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
        else:
            response["status"] = "fail"
            response["message"] = "Missing / Unique Reference ID needed"
            return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
        
        return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')


@csrf_exempt
def walletWithdrawals(request):
    response = {}
    if request.method == 'POST':
        token = request.headers.get("Authorization", None)
        withdrawn_amount = request.POST.get("withdrawn_amount", 0)
        reference_id = request.POST.get("reference_id", None)
        withdrawn_by = request.POST.get("withdrawn_by", '')
        wallet = Api.objects.filter(token=token).first()
        net_balance = wallet.balance - Decimal(withdrawn_amount)

        if reference_id and not wallet.is_disabled and not net_balance < 0:
            wallet.balance = net_balance
            wallet.withdrawn_by = withdrawn_by
            wallet.withdrawn_at = datetime.datetime.now()
            wallet.reference_id = reference_id
            wallet.save()

            response["status"] = "success"
            response["data"] = {
                    "withdrawal": {
                        "id": wallet.id,
                        "withdrawn_by": withdrawn_by,
                        "status": "success",
                        "withdrawn_at": str(datetime.datetime.now()),
                        "amount": str(wallet.balance),
                        "reference_id": reference_id,
                    }
                }
            return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')
        else:
            response["status"] = "fail"
            response["message"] = "Amount cannot be greater than available balance"
            return HttpResponse(content=json.dumps(response, indent=4), content_type='application/json')




    



