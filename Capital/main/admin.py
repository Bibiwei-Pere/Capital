from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display =['username',"FullName",'email','user_type','Phone','Account_Balance','referer_username','referals','Referer_Bonus','id','last_login','date_joined','verify']
    search_fields = ('username','email','Phone','referer_username','id','user_type')

    def referals(self, obj):
        a = CustomUser.objects.get(id = obj.id)
        return Referal_list.objects.filter(user=a).count()

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('user_type','verify')}),
             ("Profile", {'fields': ("FullName",'Phone',"Account_Balance",'referer_username','Referer_Bonus',"DOB",'BankName','AccountNumber','AccountName',"Gender")}),
    )

    readonly_fields = ('FullName','Address',"Account_Balance",'referer_username','Referer_Bonus','BankName','AccountNumber','AccountName',"DOB","Gender")

class Wallet_Funding_Admin(admin.ModelAdmin):
    list_display = ('user','medium','amount','previous_balance','after_balance','create_date')
    search_fields = ['user__username',]

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user','amount','transaction_type','balance_before','balance_after')
    search_fields = ['user__username',]

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount','previous_balance',"after_balance",'create_date')
    search_fields = ['user__username','product',]

class PlanAdmin(admin.ModelAdmin):
    list_display =['network','plansize','planamount','Bronzeprice','Silverprice','Goldprice']
    ordering = ['network','plan_size']

    def plansize(self, obj):

        return  str(obj.plan_size) + str(obj.plan_Volume)

    def planamount(self, obj):

        return  "₦" + str(obj.plan_amount)

    def Bronzeprice(self, obj):

        return  "₦" + str(obj.Bronze_price)

    def Silverprice(self, obj):

        return  "₦" + str(obj.Silver_price)

    def Goldprice(self, obj):

        return  "₦" + str(obj.Gold_price)

class NetworkAdmin(admin.ModelAdmin):
    list_display =['name','status']

class Charge_userAdmin(admin.ModelAdmin):
    list_display = ('username','amount','pending_amount','balance_before','balance_after')
    search_fields = ['user__username',]

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Wallet_Funding,Wallet_Funding_Admin)
admin.site.register(Transactions,TransactionsAdmin)
admin.site.register(Wallet_summary,WalletAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(Network,NetworkAdmin)
admin.site.register(Charge_user, Charge_userAdmin)