import sys
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Add admin member management feature to features table
content = content.replace(
    '| 🎨 **Modern UI** | Beautiful gradient design with smooth interactions |  ',
    '| 🎨 **Modern UI** | Beautiful gradient design with smooth interactions |\n| 👨‍💼 **Admin Member Management** | Search & manage member roles with inline form |'
)

# Add Admin Member Management section to features highlight
content = content.replace(
    '### 🔐 Security',
    '''### 👨‍💼 Admin Member Management
- **Access:** `/admin/manage-member-roles/` (staff/admin only)
- Search members by name, username, or email
- Collapsible inline forms for role management
- Update primary and secondary roles
- No flickering or modal issues — smooth UX

### 🔐 Security'''
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('README updated successfully')
