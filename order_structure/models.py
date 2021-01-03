from django.db import models

# Create your models here.

class Order(models.Model):
    side_choice = [("B","Buy_Side"),("S","Sell_Side")]
    order_type_choice = [("MO","Market Order"),("LO","Limit Order"),("So","Stop Order")]
    status_choice = [("P","Pending"),("C","Complete"),("R","Rejected")]
    total_price = models.IntegerField(default=0)
    dttime = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    order_id = models.CharField(max_length=100)
    side  = models.CharField(max_length=1,choices=side_choice)
    order_type = models.CharField(max_length=2,choices=order_type_choice)
    status = models.CharField(max_length=1,choices=status_choice)
    Qty = models.IntegerField(default=0)
    discription = models.CharField(max_length=100,blank=True)


class Trade_companies(models.Model):
    company_name = models.CharField(max_length=100)
    ltp = models.IntegerField(default=0)
    upper_ckt = models.IntegerField(default=0)
    lower_ckt = models.IntegerField(default=0)


class Trade(models.Model):
    product_type_choice = [("I","Intraday"),("D","Delivery")]
    product_type = models.CharField(max_length=1,choices=product_type_choice)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    company = models.ForeignKey(Trade_companies,on_delete=models.DO_NOTHING)



