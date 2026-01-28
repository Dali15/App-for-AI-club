from difflib import SequenceMatcher
from django.db.models import Q
from django.conf import settings
from .models import FAQ, ChatMessage


class AssistantService:
    """Service to handle assistant logic with simple commands"""
    
    # Define simple commands
    COMMANDS = {
        '/help': {
            'description': 'Affiche l\'aide',
            'response': """📚 **Commandes disponibles:**
/help - Affiche cette aide
/faq - Affiche toutes les FAQ
/events - Prochains événements
/register - Comment s'inscrire?
/about - À propos du club
/contact - Nous contacter
/members - Info sur les membres

Tapez n'importe quel mot pour chercher dans les FAQ!"""
        },
        '/faq': {
            'description': 'Liste toutes les FAQ',
            'response': 'Voici toutes les questions fréquemment posées'
        },
        '/events': {
            'description': 'Prochains événements',
            'response': '📅 Pour voir les événements, consultez la page "Événements" du club'
        },
        '/register': {
            'description': 'Info inscription',
            'response': """✅ Pour vous inscrire à un événement:
1. Allez sur la page "Événements"
2. Cliquez sur l'événement
3. Cliquez sur "S'inscrire"
4. Confirmez votre participation"""
        },
        '/about': {
            'description': 'À propos du club',
            'response': '🤖 Le club AI est une communauté d\'étudiants passionnés par l\'intelligence artificielle et l\'innovation technologique. Nous organisons des événements, des projets et des discussions!'
        },
        '/contact': {
            'description': 'Nous contacter',
            'response': """📧 Contactez-nous:
• Email: contact@aiclub.com
• Les responsables sont disponibles pour répondre à vos questions!"""
        },
        '/members': {
            'description': 'Info membres',
            'response': '👥 Tous les étudiants peuvent rejoindre le club! Aucune expérience préalable requise. Il suffit d\'avoir de la curiosité!'
        }
    }
    
    @staticmethod
    def find_matching_faq(user_message):
        """
        Find the best matching FAQ for a user message using keyword matching
        Returns: (faq_object, confidence_score) or (None, 0)
        """
        user_message_lower = user_message.lower()
        faqs = FAQ.objects.filter(is_active=True)
        
        best_match = None
        best_score = 0
        
        for faq in faqs:
            score = AssistantService._calculate_match_score(user_message_lower, faq)
            if score > best_score:
                best_score = score
                best_match = faq
        
        return best_match, best_score
    
    @staticmethod
    def _calculate_match_score(user_message, faq):
        """
        Calculate how well a user message matches an FAQ
        Uses keyword matching and similarity scoring
        """
        score = 0
        user_words = set(user_message.split())
        
        # Check keywords (highest weight)
        keywords = [k.strip().lower() for k in faq.keywords.split(',')]
        keyword_matches = sum(1 for keyword in keywords if keyword in user_message)
        score += keyword_matches * 40
        
        # Check question words (medium weight)
        question_words = set(faq.question.lower().split())
        common_words = user_words & question_words
        score += len(common_words) * 20
        
        # Similarity score (lower weight)
        similarity = SequenceMatcher(None, user_message, faq.question.lower()).ratio()
        score += similarity * 10
        
        return score
    
    @staticmethod
    def get_assistant_response(user_message, user=None):
        """
        Get assistant response for a user message
        Priority: Command > FAQ > Default
        Returns: (response_text, source_type, faq_object or None)
        """
        response_text = ""
        source_type = "unknown"
        faq = None
        category = 'general'
        is_faq = False
        
        # Check if it's a command
        user_input = user_message.strip().lower()
        
        if user_input.startswith('/'):
            # It's a command
            if user_input in AssistantService.COMMANDS:
                response_text = AssistantService.COMMANDS[user_input]['response']
                source_type = "command"
            else:
                response_text = f"❌ Commande inconnue: {user_input}\n\nTapez /help pour voir les commandes disponibles"
                source_type = "command"
        else:
            # Not a command, search FAQ
            faq, confidence = AssistantService.find_matching_faq(user_message)
            
            if faq and confidence > 15:
                response_text = faq.answer
                source_type = "faq"
                is_faq = True
                category = faq.category
            else:
                response_text = AssistantService._get_default_response(user_message)
                source_type = "default"
        
        # Save chat message if user is authenticated
        if user and user.is_authenticated:
            ChatMessage.objects.create(
                user=user,
                message=user_message,
                response=response_text,
                category=category,
                is_faq=is_faq
            )
        
        return response_text, source_type, faq
    
    @staticmethod
    def _get_default_response(user_message):
        """Return a default response when no FAQ matches"""
        return """Je n'ai pas trouvé de réponse précise à votre question.

💡 Essayez:
• Reformuler votre question
• Taper /help pour voir les commandes
• Consulter la FAQ complète"""
    
    @staticmethod
    def get_chat_history(user, limit=10):
        """Get recent chat history for a user"""
        return ChatMessage.objects.filter(user=user)[:limit]
