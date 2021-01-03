from django.shortcuts import render
from order_structure.models import Trade_companies,Trade,Order
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def register_company(request):
    company_name = request.data.get('company_name')
    ltp = request.data.get('ltp')
    upper_ckt = request.data.get('upper_ckt')
    lower_ckt = request.data.get('lower_ckt')

    if None in [company_name,ltp,upper_ckt,lower_ckt]:
        return Response({"Error":"All Fields are required !"})

    Trade_companies.objects.get_or_create(company_name=company_name,ltp=ltp,upper_ckt=upper_ckt,lower_ckt=lower_ckt)
    return Response({"Message":"Company Register Successful"})


@api_view(['GET'])
def companies_list(request):
    companies = Trade_companies.objects.all().values("id","company_name","ltp","upper_ckt","lower_ckt")
    return Response(companies)

@api_view(['POST'])
def order_placement(request):
    company_id = request.data.get('company_id')
    product_type = request.data.get('product_type')
    price = request.data.get('price')
    side = request.data.get('side')
    order_type = request.data.get('order_type')
    qty = request.data.get('qty')
    discription = request.data.get('discription')
    
    if None in [company_id,product_type,side,qty,order_type]:
        return Response({"Error":"All Fields are required !"})

    company_obj = Trade_companies.objects.filter(id=company_id)[0]
    if not company_obj:
        return Response({"Error":"Please check company_id !"})

    x = "TO"
    y = int(100001)
    if Order.objects.all().last():
        last_id  = Order.objects.all().last().order_id
        s = ''.join(number for number in last_id if number.isdigit())
        n = int(s)
        n += 1
        order_id = x + str(n)
    else:
        order_id = x+str(y)

    if order_type == "market_order":
        if side == "Buy_Side":
            order_side = "B"
        elif side == "Sell_Side":
            order_side = "S"
        else:
            return Response({"Error":"Invalid order_side!"})

        total_price = round(float(company_obj.ltp)* float(qty),2)
        order_obj = Order.objects.create(order_id=order_id,status="C",side=order_side,order_type="MO",Qty=qty,total_price=total_price,discription=discription)
        trans_obj = Trade.objects.create(order_id=order_obj.id,company_id=company_obj.id,product_type=product_type)

    elif order_type == "limit_order":
        if side == "Buy_Side":
            order_side = "B"
            if float(price) >= company_obj.lower_ckt and float(price) < company_obj.ltp :
                order_status = "P"
            elif float(price) >= company_obj.ltp:
                order_status = "C"
            else:
                order_status = "R"
        elif side == "Sell_Side":
            order_side = "S"
            if float(price) <= company_obj.upper_ckt and float(price) > company_obj.ltp :
                order_status = "P"
            elif float(price) <= company_obj.ltp:
                order_status = "C"
            else:
                order_status = "R"
        else:
            return Response({"Error":"Invalid order_side!"})


        total_price = round(float(price)* float(qty),2)
        order_obj = Order.objects.create(order_id=order_id,status=order_status,side=order_side,order_type="LO",Qty=qty,total_price=total_price,discription=discription)
        trans_obj = Trade.objects.create(order_id=order_obj.id,company_id=company_obj.id,product_type=product_type)

    elif order_type == "stop_order":
        if side == "Buy_Side":
            order_side = "B"
            if float(price) <= company_obj.upper_ckt and float(price) > company_obj.ltp :
                order_status = "P"
            elif float(price) <= company_obj.ltp:
                order_status = "C"
            else:
                order_status = "R"

        elif side == "Sell_Side":
            order_side = "S"
            if float(price) >= company_obj.lower_ckt and float(price) < company_obj.ltp :
                order_status = "P"
            elif float(price) >= company_obj.ltp:
                order_status = "C"
            else:
                order_status = "R"

        else:
            return Response({"Error":"Invalid order_side!"})

        total_price = round(float(price)* float(qty),2)
        order_obj = Order.objects.create(order_id=order_id,status=order_status,side=order_side,order_type="LO",Qty=qty,total_price=total_price,discription=discription)
        trans_obj = Trade.objects.create(order_id=order_obj.id,company_id=company_obj.id,product_type=product_type)

    else:
        return Response({"Error":"Invalid order_type!"})
        
    return Response({"Message": "Order Added in Order Book"})



@api_view(['GET'])
def order_book(request):
    buy_pending_order = Order.objects.filter(side="B",status="P").values("order_id","dttime","order_type","Qty","total_price","discription","trade__company__company_name","trade__company__ltp","trade__product_type")
    buy_complete_order = Order.objects.filter(side="B",status="C").values("order_id","dttime","order_type","Qty","total_price","discription","trade__company__company_name","trade__company__ltp","trade__product_type")
    buy_rejected_order = Order.objects.filter(side="B",status="R").values("order_id","dttime","order_type","Qty","total_price","discription","trade__company__company_name","trade__company__ltp","trade__product_type")
    sell_pending_order = Order.objects.filter(side="S",status="P").values("order_id","dttime","order_type","Qty","total_price","discription","trade__company__company_name","trade__company__ltp","trade__product_type")
    sell_complete_order = Order.objects.filter(side="S",status="C").values("order_id","dttime","order_type","Qty","total_price","discription","trade__company__company_name","trade__company__ltp","trade__product_type")
    sell_rejected_order = Order.objects.filter(side="S",status="R").values("order_id","dttime","order_type","Qty","total_price","discription","trade__company__company_name","trade__company__ltp","trade__product_type")
   
    
    return Response({
        "pending_buy_order": buy_pending_order,
        "complete_buy_order": buy_complete_order,
        "buy_rejected_order": buy_rejected_order,
        "sell_pending_order":sell_pending_order,
        "sell_complete_order":sell_complete_order,
        "sell_rejected_order":sell_rejected_order
    })
