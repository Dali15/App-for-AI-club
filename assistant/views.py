import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .services import AssistantService
from .models import ChatMessage


@login_required
def chat_page(request):
    """Display the personal chat interface for the user"""
    # Get user's chat history (most recent 10)
    recent_messages = AssistantService.get_chat_history(request.user, limit=10)
    
    # Get available commands for the sidebar
    commands = [
        {'cmd': '/help', 'desc': '❓ Aide', 'color': 'primary'},
        {'cmd': '/faq', 'desc': '📚 FAQ', 'color': 'info'},
        {'cmd': '/events', 'desc': '📅 Événements', 'color': 'success'},
        {'cmd': '/register', 'desc': '✅ Inscription', 'color': 'warning'},
        {'cmd': '/about', 'desc': 'ℹ️ À propos', 'color': 'secondary'},
        {'cmd': '/contact', 'desc': '📞 Contact', 'color': 'danger'},
        {'cmd': '/members', 'desc': '👥 Membres', 'color': 'info'},
    ]
    
    context = {
        'recent_messages': recent_messages,
        'commands': commands,
        'user_name': request.user.get_full_name() or request.user.username,
        'total_messages': ChatMessage.objects.filter(user=request.user).count(),
    }
    return render(request, 'assistant/chat.html', context)


@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Handle incoming chat messages via AJAX - Personal to each user"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get assistant response
        response_text, source_type, faq = AssistantService.get_assistant_response(
            user_message, 
            user=request.user
        )
        
        # Save to user's personal chat history
        chat_entry = ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=response_text,
            category=faq.category if faq else '',
            is_faq=source_type == 'faq',
        )
        
        return JsonResponse({
            'success': True,
            'message': user_message,
            'response': response_text,
            'source': source_type,
            'faq_question': faq.question if faq else None,
            'is_command': source_type == 'command',
            'is_faq': source_type == 'faq',
            'timestamp': chat_entry.created_at.strftime('%d/%m/%Y %H:%M'),
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_history(request):
    """Get personal chat history for the logged-in user"""
    # Only get messages from the current user
    messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at').values(
        'id',
        'message',
        'response',
        'is_faq',
        'category',
        'created_at'
    )[:50]
    
    # Convert to list and format dates
    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg['id'],
            'message': msg['message'],
            'response': msg['response'],
            'is_faq': msg['is_faq'],
            'category': msg['category'],
            'created_at': msg['created_at'].strftime('%d/%m/%Y %H:%M'),
        })
    
    return JsonResponse({
        'success': True,
        'total': ChatMessage.objects.filter(user=request.user).count(),
        'messages': messages_list,
    })


@login_required
def clear_history(request):
    """Clear user's personal chat history"""
    if request.method == 'POST':
        count, _ = ChatMessage.objects.filter(user=request.user).delete()
        
        # Log the action
        from dashboard.models import ActivityLog
        ActivityLog.objects.create(
            user=request.user,
            action='delete',
            content_type='ChatHistory',
            object_name=f"Chat history of {request.user.username}",
            new_value=f"Deleted {count} messages",
        )
        
        return JsonResponse({
            'success': True,
            'message': f'{count} messages cleared',
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def chat_history_page(request):
    """Display full personal chat history in a dedicated page"""
    # Get all user's messages
    all_messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(all_messages, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_messages = all_messages.count()
    faq_messages = all_messages.filter(is_faq=True).count()
    command_messages = total_messages - faq_messages
    
    context = {
        'page_obj': page_obj,
        'total_messages': total_messages,
        'faq_messages': faq_messages,
        'command_messages': command_messages,
        'user_name': request.user.get_full_name() or request.user.username,
    }
    
    return render(request, 'assistant/chat_history.html', context)

