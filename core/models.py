from django.db import models

class Product(models.Model):
    CATEGORIES = [
        ('Woodworking', 'Woodworking'),
        ('Painting', 'Painting'),
        ('Knitting', 'Knitting'),
        ('Ceramics', 'Ceramics'),
        ('Jewelry Making', 'Jewelry Making'),
        ('Origami', 'Origami'),
        ('Embroidery', 'Embroidery'),
        ('Pottery', 'Pottery'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, null=True)
    
    # Additional fields
    design = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    style = models.CharField(max_length=100, blank=True, null=True)
    # Add more fields as needed

    def __str__(self):
        return self.name
