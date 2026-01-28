from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Announcement
from accounts.decorators import roles_required
from .forms import AnnouncementForm

@login_required
def announcement_list(request):
    """Display list of announcements with search functionality."""
    announcements = Announcement.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        announcements = announcements.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    context = {
        'announcements': announcements,
        'search_query': search_query,
    }
    return render(request, 'announcements/announcement_list.html', context)

@login_required
@roles_required(['owner', 'president', 'vice_president', 'media', 'hr', 'partnerships'])
def create_announcement(request):
    """Create a new announcement. President, VP, Media, HR, and Partnerships can create."""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()

    return render(request, 'announcements/create_announcement.html', {'form': form})
