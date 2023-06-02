from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator
from django.db import transaction
from django.conf import settings
from django.utils import timezone
import datetime
from django.db.models import Sum
import random
import uuid
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

User = settings.AUTH_USER_MODEL

"""def sendmail(subject, message, user_email, username):
    ctx = {
        'message': message,
        "subject": subject,
        "username": username
    }
    message = get_template('email.html').render(ctx)
    msg = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()"""
    
user_t = (
    ("Bronze", "Bronze"),
    ("Silver", "Silver"),
    ("Gold", "Gold"),
)
status = (
    ('processing', 'processing'),
    ('failed', 'Failed'),
    ('successful', 'Successful'),
)
Bank = (
    ('First Bank of Nigeria', 'First Bank of Nigeria'),
    ('UBA', 'UBA'),
    ('Access(Diamond) Bank', 'Access (Diamond) Bank'),
    ('Wema Bank', 'Wema Bank'),
    ('Heritage Bank', 'Heritage Bank'),
    ('Polarise Bank', 'Polarise Bank'),
    ('Stanbic IBTC', 'Stanbic IBTC'),
    ('Sterling Bank', 'Sterling Bank'),
    ('Union Bank', 'Union Bank'),
    ('Zenith Bank', 'Zenith Bank'),
    ('Unity Bank', 'Unity Bank'),
    ('FCMBank', 'FCMBank'),
    ('GTBank', 'GTBank'),
    ('FIdelity Bank', 'FIdelity Bank'),
    ('ECO Bank', 'ECO Bank'),
)
Netchoice = (
    ('BTC', 'BTC'),
    ('ETH', 'ETH'),
    ('LTC', 'LTC'),
    ('XRP', 'XRP'),
    ('USDT', 'USDT'),
)
Netstatus = (
    ('Fair', 'Fair'),
    ('Bad', 'Bad'),
    ('Strong', 'Strong'),
)
plan_type = (
    ('WEEK', 'WEEK'),
    ('MONTH', 'MONTH'),
    ('YEAR', 'YEAR')
)
Volchoice = (
    ('USD', 'USD'),
    ('EURO', 'EURO'),
    ('POUNDS', 'POUNDS'),
)
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

def create_id():
    num = random.randint(100, 2000)
    num_2 = random.randint(1, 1000)
    num_3 = random.randint(60, 1000)
    return str(num) + str(num_2)+str(num_3)+str(uuid.uuid4())[:8]

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField()
    birth_date = models.DateField(blank=True,null=True)
    FullName = models.CharField(max_length=200,  null=True)
    Address = models.CharField(max_length=500,  null=True)
    BankName = models.CharField(max_length=100, choices=Bank, blank=True)
    AccountNumber = models.CharField(max_length=40, blank=True)
    Phone = models.CharField(max_length=30, blank=True)
    AccountName = models.CharField(max_length=200, blank=True)
    Account_Balance = models.FloatField(
    default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    pin = models.CharField(null=True, blank=True, max_length=5)
    referer_username = models.CharField(max_length=50, blank=True, null=True)
    first_payment = models.BooleanField(default=False)
    Referer_Bonus = models.FloatField(
    default=0.00, null=True, validators=[MinValueValidator(0.0)],)
    user_type = models.CharField(
    max_length=30, choices=user_t, default="Bronze", null=True)
    Bonus = models.FloatField(default=0.00, null=True, validators=[ MinValueValidator(0.0)],)
    verify = models.BooleanField(default=False)
    DOB = models.DateField(null=True,blank=True,)
    Gender = models.CharField(max_length=6, null=True,)
    passport_photogragh = models.ImageField(upload_to="passport_images", null=True, help_text="Maximum of 50kb in size")
    accounts = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.username

    def image_tag(self):

        from django.utils.html import mark_safe
        return mark_safe('<img src="https://dsubplug.com/media/%s" width="150" height="150" />' % (self.passport_photogragh))

    image_tag.short_description = 'Image'

    def walletb(self):
         return  str(round(self.Account_Balance))

    def bonusb(self):
         return  str(round(self.Referer_Bonus))

    def ref_deposit(self, amount):
        self.Referer_Bonus += amount
        self.Referer_Bonus = round(self.Referer_Bonus, 2)
        self.save()

    def ref_withdraw(self, amount):
        if self.self.Referer_Bonus > amount or amount < 0 :
            return False
        self.Referer_Bonus -= amount
        self.Referer_Bonus = round(self.Referer_Bonus, 2)
        self.save()


    @classmethod
    def withdraw(cls, id, amount):
        with transaction.atomic():
            account = (cls.objects.select_for_update().get(id=id))
            print(account)
            balance_before = account.Account_Balance
            if account.Account_Balance < amount or amount < 0:
                return False
            account.Account_Balance -= amount
            account.save()

        try:

            Transactions.objects.create(user=CustomUser.objects.get(id=id),
                transaction_type="DEBIT", balance_before= balance_before,balance_after = balance_before -amount,amount=amount)

        except:
            pass

    @classmethod
    def deposit(cls, id, amount, transfer=False,medium = "NONE" ):
        with transaction.atomic():
            account = (cls.objects.select_for_update().get(id=id))
            balance_before = account.Account_Balance
            if medium != "NONE" :

                    if Charge_user.objects.filter(username = account.username).exists():
                            pending_charge = Charge_user.objects.filter(username =account.username).last()
                            if pending_charge.pending_amount > 0:
                                    if amount > pending_charge.pending_amount:
                                        amt = amount - pending_charge.pending_amount
                                        balance_before = account.Account_Balance
                                        pending_charge.balance_before = balance_before
                                        account.Account_Balance += amt
                                        account.save()

                                        try:
                                            Wallet_summary.objects.create(user=account, product=f"N{pending_charge.pending_amount} pending wallet charge paid", amount=amount, previous_balance = balance_before, after_balance= balance_before + amount)
                                        except:
                                            pass
                                        pending_charge.comment = f"N{pending_charge.pending_amount} pending wallet charge paid"
                                        pending_charge.balance_after = amt
                                        pending_charge.pending_amount = 0
                                        pending_charge.save()

                                    else:
                                        balance_before = account.Account_Balance
                                        pending_charge.balance_before = balance_before
                                        amt = pending_charge.pending_amount - amount
                                        pending_charge.comment = f"N{amount} paid from  pending wallet charge, pending amount remain {amount} "
                                        pending_charge.pending_amount =  amt
                                        pending_charge.balance_after = 0
                                        pending_charge.save()

                            else:
                                  account.Account_Balance += amount
                                  account.save()
                    else:
                          account.Account_Balance += amount
                          account.save()

            try:

                Transactions.objects.create(user=CustomUser.objects.get(id=id),
                    transaction_type="CREDIT",balance_before= balance_before,balance_after = balance_before + amount, amount= amount)

            except:
                pass

            try:
                 Wallet_Funding.objects.create(user=CustomUser.objects.get(id=id),medium=medium,previous_balance= balance_before,after_balance= balance_before + amount, amount= amount)

            except:
                    pass


        return account

    def ref_withdraw(self, amount):
        if self.Referer_Bonus > 0.0:
            self.Referer_Bonus -= amount
            self.Referer_Bonus = round(self.Referer_Bonus, 2)
            self.save()

    class Meta:
        verbose_name_plural = 'USERS MANAGEMENT'

vericate = (
    ('processing', 'processing'),
    ('Approved', 'Approved'),
    ('Not_Appproved', 'Not_Approved'),
)

def validate_file_size(value):
    filesize = value.size
    if filesize > 1024 * 50:
        raise ValidationError(
            "The maximum file size that can be uploaded is 50kb")
    else:
        return value

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    amount = models.FloatField()
    balance_before = models.FloatField(blank=True, null=True)
    balance_after = models.FloatField(blank=True, null=True)
    transaction_type = models.CharField(max_length=30, blank=True)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'WALLET TRANSACTIONS'

    def __str__(self):
        return str(self.transaction_type)

    def today_credit_transaction(self):

        today = datetime.date.today()
        return Transactions.objects.filter(create_date__gt=today, transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def today_debit_transaction(self):
        today = datetime.date.today()
        return Transactions.objects.filter(create_date__gt=today, transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']

    def this_month_credit_transaction(self):
        current_month = datetime.datetime.now().month
        return Transactions.objects.filter(create_date__month=current_month, transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def this_month_debit_transaction(self):
        current_month = datetime.datetime.now().month
        return Transactions.objects.filter(create_date__month=current_month, transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']

    def total_credit_transaction(self):
        return Transactions.objects.filter(transaction_type="CREDIT").aggregate(Sum('amount'))['amount__sum']

    def total_debit_transaction(self):
        return Transactions.objects.filter(transaction_type="DEBIT").aggregate(Sum('amount'))['amount__sum']

class Wallet_summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             editable=False, blank=False, null=True, related_name='wallet')
    product = models.CharField(max_length=500, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    previous_balance = models.CharField(max_length=30, blank=True)
    after_balance = models.CharField(max_length=30, blank=True, null=True)
    Status = models.CharField(
        max_length=30, choices=status, default='successful')
    create_date = models.DateTimeField(default=timezone.now)
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        """try:
            sendmail("Transaction Notification ",f"{product} \n Amount : {self.amount} \n Previous Balance : {self.previous_balance} \n New Balance: {self.after_balance} \n Date {self.create_date.strftime('%d, %b %Y') }", self.user.email, self.user.username)
        except:
            pass"""
        return super(Wallet_summary, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'USERS WALLET SUMMARY'

class Wallet_Funding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name='wallet_funding')
    medium = models.CharField(max_length=500, blank=True,editable=False, )
    amount = models.CharField(max_length=30, blank=True,editable=False, )
    previous_balance = models.CharField(max_length=30, blank=True,editable=False, )
    after_balance = models.CharField(max_length=30, blank=True, null=True,editable=False, )
    create_date = models.DateTimeField(default=timezone.now,editable=False, )
    ident = models.CharField(default=create_id, editable=False, max_length=30)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'WALLET FUNDING TRACKING'

    def save(self, *args, **kwargs):
        try:
            user = self.user
            chek =  Wallet_Funding.objects.filter(user=user).count()
            if user.referer_username and chek == 0:
                if CustomUser.objects.filter(username__iexact=user.referer_username).exists():
                    referer = CustomUser.objects.get(username__iexact=user.referer_username)
                    ref_previous_bal = referer.Account_Balance
                    amt_to_earn = round(int(self.amount) * 0.05)
                    if amt_to_earn > 200:
                        amt_to_earn = 200

                    amt_to_earn = int(amt_to_earn)
                    referer.ref_deposit(int(amt_to_earn))

                    #notify.send(referer, recipient=referer, verb=f'you Earned N{amt_to_earn} Bonus from your referal: {user.username} first funding and has been added to your referal bonus wallet')
                    Wallet_summary.objects.create(user=referer, product=f"Earned N{amt_to_earn} referral bonus from {user} first funding", amount=amt_to_earn, previous_balance=ref_previous_bal, after_balance=(ref_previous_bal + amt_to_earn))
        except:
            pass
        return super(Wallet_Funding, self).save(*args, **kwargs)

class Charge_user(models.Model):
    username = models.CharField(max_length=100, null=True)
    amount = models.IntegerField()

    balance_before = models.FloatField(
        null=True, blank=True, help_text="leave blank sytem automatic set this")
    balance_after = models.FloatField(
        null=True, blank=True, help_text="leave blank sytem automatic set this")
    comment = models.TextField()
    pending_amount = models.IntegerField(default=0,help_text="leave blank sytem automatic set this,if the amount you want to with not upto user wallet, pending amount wait till when user fund next")

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        try:
            mb = CustomUser.objects.get(username=self.username)
        except:
            raise ValidationError(f'Invalid user, enter correct username')
        if not self.id:
                        if self.amount > mb.Account_Balance:
                            self.pending_amount = self.amount  - mb.Account_Balance
                            self.balance_before = mb.Account_Balance
                            mb.withdraw(mb.id, mb.Account_Balance)

                            self.balance_after = 0

                            try:
                                Wallet_summary.objects.create(
                                    user=mb, product=f"Admin Charge your account for {self.comment} ", amount=self.amount, previous_balance=self.balance_before, after_balance=self.balance_after)
                            except:
                                pass

                        else:
                            self.balance_before = mb.Account_Balance
                            withdraw = mb.withdraw(mb.id, self.amount)
                            if withdraw == False:
                                raise ValidationError(
                                    f'Insufficient fund ,{self.username} wallet balance is {mb.Account_Balance}')
                            self.balance_after = mb.Account_Balance - self.amount

                            try:
                                Wallet_summary.objects.create(
                                    user=mb, product=f"Admin Charge your account for {self.comment} ", amount=self.amount, previous_balance=self.balance_before, after_balance=self.balance_after)
                            except:
                                pass

        super(Charge_user, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'WITHDRAW FROM USER WALLET'

class Referal_list(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, editable=False, blank=False, null=True)
    username = models.CharField(max_length=30)
    referal_user = models.ForeignKey(
    User, on_delete=models.CASCADE, editable=False, blank=False, null=True, related_name="referal")

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        mb = CustomUser.objects.get(username__iexact=self.username)
        self.referal_user = mb

        super(Referal_list, self).save(*args, **kwargs)

# FOR WELCOME VIEW
class Network(models.Model):
    name = models.CharField(max_length=30, choices=Netchoice, unique=True)
    status = models.CharField(max_length=30, choices=Netstatus)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'NETWORKS'

class Plan(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    plan_size = models.FloatField()
    plan_Volume = models.CharField(max_length=30, choices=Volchoice)
    plan_amount = models.PositiveIntegerField()
    Bronze_price = models.PositiveIntegerField(default=100000)
    Silver_price = models.PositiveIntegerField(default=100000)
    Gold_price = models.PositiveIntegerField(default=100000)
    plan_name_id = models.CharField(max_length=500, null=True, blank=True)
    plan_type = models.CharField(
        max_length=30, choices=plan_type, blank=True, help_text="Data plan  type only .")
    month_validate = models.CharField(max_length=30)

    def __str__(self):
        return str(self.plan_size) + str(self.plan_Volume) + '----' + 'N' + str(self.plan_amount)

    def plan_name(self):
        return str(self.plan_size) + str(self.plan_Volume)

    def plan_net(self):
        return str(self.network)

    def plan_amt(self):
        return str(self.plan_amount)

    def plan_id(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'DATA PLANS'

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="blogimage", null=True, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return '<img src="{}" height="150"/>'.format(self.image.url)
        Post.allow_tags = True

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True,
                            db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_list_by_category', args=[self.slug])

class Book(models.Model):
    category = models.ForeignKey(
        Category, related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    author = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='books/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)
