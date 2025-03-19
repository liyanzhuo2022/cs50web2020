from django.contrib import admin

# Register your models here.
from .models import Listing, Comment, Bid, Category, Watchlist

admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Watchlist)