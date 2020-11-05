from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from api import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^api/v1/init', views.initWallet, name='initWallet'),
    url(r'^api/v1/wallet/withdrawals', views.walletWithdrawals, name='walletWithdrawals'),
    url(r'^api/v1/wallet/deposits', views.walletDeposits, name='walletDeposits'),
    url(r'^api/v1/wallet', views.activateDeactivateWallet, name='activateDeactivateWallet'),
]