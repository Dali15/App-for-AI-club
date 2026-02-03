# Définition simple des permissions par rôle
ROLE_PERMISSIONS = {
    'president': {
        'label': '👑 Président',
        'permissions': [
            'create_event',
            'edit_event',
            'delete_event',
            'create_announcement',
            'edit_announcement',
            'delete_announcement',
            'manage_members',
            'manage_permissions',
            'view_analytics',
            'manage_faqs',
            'view_members',
        ]
    },
    'vice_president': {
        'label': '📊 Vice-Président',
        'permissions': [
            'create_event',
            'edit_event',
            'create_announcement',
            'edit_announcement',
            'view_analytics',
            'view_members',
        ]
    },
    'events_manager': {
        'label': '📅 Gestionnaire Événements',
        'permissions': [
            'create_event',
            'edit_event',
            'view_analytics',
            'view_members',
        ]
    },
    'media': {
        'label': '📸 Media/Communication',
        'permissions': [
            'create_announcement',
            'edit_announcement',
            'view_members',
        ]
    },
    'treasurer': {
        'label': '💰 Trésorier',
        'permissions': [
            'view_analytics',
            'view_members',
        ]
    },
    'member': {
        'label': '👤 Membre',
        'permissions': [
            'view_events',
            'register_event',
        ]
    },
}

ALL_AVAILABLE_PERMISSIONS = [
    ('create_event', '➕ Créer événement'),
    ('edit_event', '✏️ Modifier événement'),
    ('delete_event', '🗑️ Supprimer événement'),
    ('create_announcement', '📢 Créer annonce'),
    ('edit_announcement', '✏️ Modifier annonce'),
    ('delete_announcement', '🗑️ Supprimer annonce'),
    ('manage_members', '👥 Gérer membres'),
    ('manage_permissions', '🔐 Gérer permissions'),
    ('view_analytics', '📊 Voir statistiques'),
    ('manage_faqs', '❓ Gérer FAQ'),
    ('view_events', '👁️ Voir événements'),
    ('register_event', '✅ S\'inscrire événement'),
    ('view_members', '👥 Voir membres'),
]
