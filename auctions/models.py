from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError


class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=256, blank=False)
    starting_bid = models.FloatField(blank=False)
    category = models.CharField(max_length=32, blank=True)
    image = models.CharField(max_length=512, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, related_name="auctions_won", on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.starting_bid < 0:
            raise ValidationError('Starting bid must be a positive value.')
        

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.bid < 0:
            raise ValidationError('Bid must be a positive value.')
        if self.bid <= self.listing.starting_bid:
            raise ValidationError('Bid must be greater than the starting bid.')

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.comment == "":
            raise ValidationError('Comment must not be empty.')