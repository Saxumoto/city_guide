from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    View 
)
from django.db.models import Q, Avg # Import Avg function for aggregation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth import login 
from .models import Attraction, Review # Imported Review model
from .forms import CustomUserCreationForm, ReviewForm # Imported ReviewForm

# --- NEW REVIEW CREATION VIEW ---

class ReviewCreateView(LoginRequiredMixin, View):
    """
    Handles POST requests to submit a new review for an attraction.
    """
    def post(self, request, pk):
        attraction = get_object_or_404(Attraction, pk=pk)
        
        # Check if the user has already reviewed this attraction
        existing_review = Review.objects.filter(attraction=attraction, user=request.user).exists()
        
        if existing_review:
            # Optionally redirect back with an error message
            return redirect('attraction_detail', pk=pk)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.attraction = attraction
            review.user = request.user
            review.save()
        
        return redirect('attraction_detail', pk=pk)


# --- HOME AND AUTH VIEWS ---

def home_view(request):
    """Renders the dedicated home landing page."""
    return render(request, 'home.html')

class RegisterView(View):
    """Handles user registration."""
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('attraction_list')  
        return render(request, self.template_name, {'form': form})


# --- R (Read) Views ---

class AttractionListView(ListView):
    """Displays a list of all attractions."""
    model = Attraction
    template_name = 'attractions/attraction_list.html'
    context_object_name = 'attractions'
    paginate_by = 10 

    def get_queryset(self):
        # We perform annotation here to get the average rating for each attraction in the list view
        queryset = super().get_queryset().annotate(
            average_rating=Avg('reviews__rating')
        )
        
        # 1. Handle Search Query
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        # 2. Handle Category Filter
        category_filter = self.request.GET.get('category')
        if category_filter and category_filter != 'ALL':
            queryset = queryset.filter(category=category_filter)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['category_filter'] = self.request.GET.get('category', 'ALL')
        context['categories'] = Attraction.category.field.choices
        return context

class MyAttractionListView(LoginRequiredMixin, ListView):
    """Displays a list of only the attractions contributed by the currently logged-in user."""
    model = Attraction
    template_name = 'attractions/my_attractions.html'
    context_object_name = 'attractions'
    paginate_by = 10 

    def get_queryset(self):
        # Annotate with average rating, even on the dashboard
        return Attraction.objects.filter(contributor=self.request.user).annotate(
            average_rating=Avg('reviews__rating')
        ).order_by('name')


class AttractionDetailView(DetailView):
    """
    Displays the details of a single attraction, calculates the average rating, 
    and prepares the review form.
    """
    model = Attraction
    template_name = 'attractions/attraction_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attraction = self.object
        user = self.request.user

        # 1. Calculate Average Rating
        avg_rating = attraction.reviews.aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = avg_rating if avg_rating is not None else 0
        context['full_reviews'] = attraction.reviews.all() # Get all reviews

        # 2. Prepare Review Form (Only if user is logged in)
        if user.is_authenticated:
            # Check if user has already reviewed
            has_reviewed = attraction.reviews.filter(user=user).exists()
            context['has_reviewed'] = has_reviewed
            
            # Show form only if not reviewed
            if not has_reviewed:
                context['review_form'] = ReviewForm()
        
        return context


# --- C, U, D Views ---

class AttractionCreateView(LoginRequiredMixin, CreateView):
    """Handles creating a new attraction."""
    model = Attraction
    fields = ['name', 'description', 'category', 'location', 'latitude', 'longitude', 'image', 'is_open'] 
    template_name = 'attractions/attraction_form.html'

    def form_valid(self, form):
        form.instance.contributor = self.request.user
        return super().form_valid(form)

class AttractionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Handles updating an existing attraction."""
    model = Attraction
    fields = ['name', 'description', 'category', 'location', 'latitude', 'longitude', 'image', 'is_open']
    template_name = 'attractions/attraction_form.html'

    def test_func(self):
        attraction = self.get_object()
        return self.request.user == attraction.contributor

class AttractionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Handles deleting an attraction."""
    model = Attraction
    template_name = 'attractions/attraction_confirm_delete.html'
    success_url = reverse_lazy('attraction_list')
    
    def test_func(self):
        attraction = self.get_object()
        return self.request.user == attraction.contributor