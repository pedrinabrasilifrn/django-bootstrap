import rules
from django.urls import reverse
from simple_menu import Menu, MenuItem

# Menu principal
public = "public"
common = "common"
admin = "admin"
superadmin = "superadmin"


# Adicionando itens de menu
Menu.add_item(
    public,
    MenuItem(
        "Django-Admin",
        reverse("admin:index"),
        icon="fas fa-home",
    ),
)

Menu.add_item(
    common,
    MenuItem(
        "Sair",
        url=reverse("account_logout"),
        icon="fas fa-sticky-note",
        check=lambda request: rules.test_rule("is_user_rule", request),
    ),
)

Menu.add_item(
    common,
    MenuItem(
        "Meu Perfil", url="#", icon="fas fa-money-check", check=lambda request: rules.test_rule("is_user_rule", request)
    ),
)

Menu.add_item(
    superadmin,
    MenuItem(
        "Usuarios",
        url=reverse("account_login"),
        icon="fas fa-home",
        check=lambda request: rules.test_rule("is_superadmin_rule", request),
    ),
)
