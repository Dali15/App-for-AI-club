#!/bin/bash
cd "c:\HTML\club app"
echo "Removing nested ai_club/ai_club folder..."
git rm -r "ai_club/ai_club" 2>/dev/null || rm -rf "ai_club/ai_club"
git add -A
git commit -m "chore: remove nested duplicate ai_club package folder"
git push origin main
python manage.py collectstatic --noinput --clear
echo "Done! Nested folder removed and static files collected."
