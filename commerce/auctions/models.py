from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    # a listing object will have a title, description, starting bid, a user (who creates the listing), and optionally a category and/or image URL, and possibly comments
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=19, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    # make optional using blank=True
    category = models.CharField(max_length=64, blank=True)
    image_URL = models.URLField(max_length=300, blank=True)
    
    def __str__(self):
        content = (
            f"Listing id: {self.id}\n"
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Starting Bid: {self.start_bid}\n"
            f"Listing Creator: {self.creator}\n"
            f"Category: {self.category}\n"
            f"Image URL: {self.image_URL}"
        )
        return content

class Bid(models.Model):
    # a bid object will have a listing, an amount, and a user
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=19, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        content = (
            f"Bid id: {self.id}\n"
            f"Listing id: {self.listing.id}\n"
            f"Bid amount: {self.bid_amount}\n"
            f"Bidder: {self.bidder}"
        )
        return content

class Comment(models.Model):
    # a comment object will have a listing, content, and a user
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        content = (
            f"Comment id: {self.id}\n"
            f"Listing id: {self.listing.id}\n"
            f"Comment content: {self.comment}\n"
            f"Commenter: {self.commenter}"
        )
        return content
 
class Watching(models.Model):
    # a watching object will have a listing and a user
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchers")
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watched_listings")
    
    def __str__(self):
        content = (
            f"Watch id: {self.id}\n"
            f"Listing id: {self.listing.id}\n"
            f"Watcher id: {self.watcher}"
        )
        return content