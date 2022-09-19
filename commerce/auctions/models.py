from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    # a listing object will have a title, description, starting bid, a user (who creates the listing), and optionally a category and/or image URL, and possibly comments
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(max_length=64, blank=True)
    image_URL = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        content = (
            f"Listing number: {self.id} -- Title: {self.title} -- Created By: {self.creator}"
        )
        return content

class Bid(models.Model):
    # a bid object will have a listing, an amount, and a user
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=19, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        content = (
            f"{self.bidder} bid {self.bid_amount} on {self.listing}."
        )
        return content

class Comment(models.Model):
    # a comment object will have a listing, content, and a user
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        content = (
            f"{self.commenter} commented {self.comment} on {self.listing}."
        )
        return content


class Watchlist(models.Model):
    # a watchlist object will have a listing and a user
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watched_listings")
    
    def __str__(self):
        content = (
            f"{self.listing} is being watched by {self.watcher}."
        )
        return content
