from django.contrib import admin
from .models import User, Listing, Comment, Bid

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "creator", "category", "active")

class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "bid_amount", "bidder")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing", "comment", "commenter")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
