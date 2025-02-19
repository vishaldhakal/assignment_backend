from django.db import models
from django_summernote.fields import SummernoteTextField
from accounts.models import Agent
from django.db.models import Case, When, Value, IntegerField


class Developer(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    website_link = models.TextField(blank=True)
    details = SummernoteTextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class City(models.Model):
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, unique=True)
    details = SummernoteTextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class PreConstruction(models.Model):
    PROJECT_CHOICES = [
        ("Condo", "Condo"),
        ("Townhome", "Townhome"),
        ("Semi-Detached", "Semi-Detached"),
        ("Detached", "Detached"),
        ("NaN", "NaN"),
    ]
    
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, unique=True)
    price_starting_from = models.FloatField(default=0)
    is_featured = models.BooleanField(default=False)
    price_to = models.FloatField(default=0)
    project_type = models.CharField(
        max_length=500, choices=PROJECT_CHOICES, default="Condo"
    )
    occupancy = models.IntegerField(default=2025,null=True,blank=True)
    description = SummernoteTextField(blank=True)
    date_of_upload = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    beds = models.FloatField(default=0)
    baths = models.FloatField(default=0)
    area = models.FloatField(default=0)

    def __str__(self):
        return self.project_name

    class Meta:
        ordering = [
            "-last_updated",
        ]


class PreConstructionImage(models.Model):
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name="image"
    )
    image = models.FileField()

    def __str__(self):
        if self.image:
            return self.image.url
        else:
            return "/media/no-image.webp"


class PreConstructionFloorPlan(models.Model):
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name="floorplan"
    )
    floorplan = models.FileField()

    def __str__(self):
        return self.floorplan.url


class Event(models.Model):
    event_description = SummernoteTextField(blank=True)
    event_date = models.DateTimeField()
    event_link = models.CharField(max_length=2000, default="#")
    event_title = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.event_title


class NewsCategory(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class News(models.Model):
    news_title = models.CharField(max_length=1000)
    news_category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    slug = models.CharField(max_length=1000, blank=True)
    news_thumbnail = models.FileField(blank=True)
    news_description = SummernoteTextField(blank=True)
    date_of_upload = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    news_link = models.CharField(max_length=2000, default="#")

    def __str__(self):
        return self.event_title


class Favourite(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent")
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name="preconstruction"
    )


class FavouriteNews(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="news_agent"
    )
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news")


class FavouriteEvent(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="event_agent"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")
