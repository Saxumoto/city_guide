from django.urls import reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    View 
)
from django.db.models import Q, Avg 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth import login 
from django.contrib import messages
from .models import Attraction, Review 
from .forms import CustomUserCreationForm, ReviewForm, AttractionForm 

# --- REVIEW CREATION VIEW ---

class ReviewCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        attraction = get_object_or_404(Attraction, pk=pk)
        existing_review = Review.objects.filter(attraction=attraction, user=request.user).exists()
        
        if existing_review:
            messages.warning(request, 'You have already submitted a review for this attraction.')
            return redirect('attraction_detail', pk=pk)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.attraction = attraction
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you! Your review has been submitted.')
        else:
            messages.error(request, 'Please correct the errors in your review.')
        
        return redirect('attraction_detail', pk=pk)


# --- HOME AND AUTH VIEWS ---

def home_view(request):
    # Redirect to attractions list as home page
    return redirect('attraction_list')

class RegisterView(View):
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
    """Displays a list of APPROVED attractions only."""
    model = Attraction
    template_name = 'attractions/attraction_list.html'
    context_object_name = 'attractions'
    paginate_by = 10 

    def get_queryset(self):
        # 1. Filter: Only show APPROVED attractions to the public
        queryset = Attraction.objects.filter(status='APPROVED').annotate(
            average_rating=Avg('reviews__rating')
        )
        
        # 2. Handle Search Query
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        # 3. Handle Category Filter
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
    """
    Displays all attractions contributed by the logged-in user,
    regardless of whether they are Pending or Approved.
    """
    model = Attraction
    template_name = 'attractions/my_attractions.html'
    context_object_name = 'attractions'
    paginate_by = 10 

    def get_queryset(self):
        return Attraction.objects.filter(contributor=self.request.user).annotate(
            average_rating=Avg('reviews__rating')
        ).order_by('-created_at')


class AttractionDetailView(DetailView):
    model = Attraction
    template_name = 'attractions/attraction_detail.html'

    def get_queryset(self):
        """
        Custom permission logic for viewing details:
        - Admin: Can view everything.
        - Owner: Can view their own posts (even if Pending).
        - Public: Can only view Approved posts.
        """
        if self.request.user.is_staff:
            return Attraction.objects.all()
        elif self.request.user.is_authenticated:
            return Attraction.objects.filter(Q(status='APPROVED') | Q(contributor=self.request.user))
        else:
            return Attraction.objects.filter(status='APPROVED')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attraction = self.object
        user = self.request.user

        avg_rating = attraction.reviews.aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = avg_rating if avg_rating is not None else 0
        context['full_reviews'] = attraction.reviews.all()

        if user.is_authenticated:
            has_reviewed = attraction.reviews.filter(user=user).exists()
            context['has_reviewed'] = has_reviewed
            if not has_reviewed:
                context['review_form'] = ReviewForm()
        
        return context


# --- C, U, D Views ---

class AttractionCreateView(LoginRequiredMixin, CreateView):
    model = Attraction
    form_class = AttractionForm
    template_name = 'attractions/attraction_form.html'

    def form_valid(self, form):
        form.instance.contributor = self.request.user
        
        # LOGIC: Admins get auto-approved; Regular users go to PENDING
        if self.request.user.is_staff:
            form.instance.status = 'APPROVED'
            messages.success(self.request, 'Attraction created and approved!')
        else:
            form.instance.status = 'PENDING'
            messages.success(self.request, 'Attraction submitted! It will be visible after admin approval.')
            
        return super().form_valid(form)

class AttractionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Attraction
    form_class = AttractionForm
    template_name = 'attractions/attraction_form.html'

    def test_func(self):
        attraction = self.get_object()
        # Allow if User is the Contributor OR User is an Admin
        return self.request.user == attraction.contributor or self.request.user.is_staff
    
    def form_valid(self, form):
        # If updated by non-admin, reset status to PENDING
        if not self.request.user.is_staff and form.instance.status == 'APPROVED':
            form.instance.status = 'PENDING'
            messages.info(self.request, 'Attraction updated. Status reset to PENDING for admin review.')
        else:
            messages.success(self.request, 'Attraction updated successfully!')
        return super().form_valid(form)

class AttractionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Attraction
    template_name = 'attractions/attraction_confirm_delete.html'
    success_url = reverse_lazy('attraction_list')
    
    def test_func(self):
        attraction = self.get_object()
        # Allow if User is the Contributor OR User is an Admin
        return self.request.user == attraction.contributor or self.request.user.is_staff