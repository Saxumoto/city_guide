from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 

class Attraction(models.Model):
    """
    Model representing a tourist attraction in Davao City.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    name = models.CharField(
        max_length=150, 
        unique=True, 
        help_text="The official name of the attraction (e.g., Philippine Eagle Center)."
    )
    description = models.TextField(
        help_text="A detailed overview of the attraction and what visitors can expect."
    )
    category = models.CharField(
        max_length=50, 
        choices=[
            ('NATURE', 'Nature & Outdoors'),
            ('CULTURAL', 'Culture & History'),
            ('FOOD', 'Food & Nightlife'),
            ('SHOPPING', 'Shopping & Malls'),
        ],
        default='NATURE',
        help_text="The primary category of the attraction."
    )
    location = models.CharField(
        max_length=255, 
        help_text="Physical address or area (e.g., Malagos, Calinan, or Roxas Avenue)."
    )
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        help_text="Latitude coordinate (e.g., 7.067). REQUIRED.",
        default=7.068600 
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        help_text="Longitude coordinate (e.g., 125.603). REQUIRED.",
        default=125.606300
    )
    contributor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    image = models.ImageField(
        upload_to='attraction_photos/', 
        blank=True, 
        null=True,
        help_text="Upload a photo of the attraction."
    )
    is_open = models.BooleanField(
        default=True, 
        help_text="Indicates if the attraction is currently open to the public."
    )
    
    # --- NEW FIELD FOR AUTHORITY SEPARATION ---
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='PENDING',
        help_text="Admins must approve this before it is visible to the public."
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Attractions"
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['contributor']),
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse('attraction_detail', kwargs={'pk': self.pk})

# --- REVIEW MODEL (Unchanged) ---

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    attraction = models.ForeignKey(
        Attraction, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES, 
        default=5
    )
    comment = models.TextField(
        max_length=500, 
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('attraction', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['attraction', 'created_at']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f'{self.attraction.name} - {self.rating} stars by {self.user.username}'