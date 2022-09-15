from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# listing model
class Listing(models.Model):
    # a listing object will have a title, description, starting bid, a user (who creates the listing), and optionally a category and/or image URL
    pass

# bid model
class Bid(models.Model):
    # a bid object will have a listing, an amount, and a user
    pass

# comment model
class Comment(models.Model):
    # a comment object will have a listing, content, and a user
    pass

# watching model
class Watching(models.Model):
    # a watching object will have a listing and a user
    pass