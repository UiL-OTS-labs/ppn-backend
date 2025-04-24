from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from menu import Menu, MenuItem

Menu.add_item("home", MenuItem(_('mainmenu:home'),
                               reverse('main:home'),
                               exact_url=True,
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:leader_experiments'),
                               reverse('leader:experiments'),
                               check=lambda x: x.user.is_authenticated and
                                               x.user.is_leader
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:leader_profile'),
                               reverse('leader:profile'),
                               check=lambda x: x.user.is_authenticated and
                                               x.user.is_leader
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:sign_up'),
                               reverse('participant:sign_up'),
                               check=lambda x: not x.user.is_authenticated
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:cancel_appointment'),
                               reverse('participant:cancel_landing'),
                               check=lambda x: not x.user.is_authenticated
                               ))

Menu.add_item("main", MenuItem(_('mainmenu:my_appointments'),
                               reverse('participant:appointments'),
                               check=lambda x: x.user.is_authenticated and
                                               x.user.is_participant
                               ))

# Needs to be the last main menu item! (As it's aligned to the right using CSS)
Menu.add_item("main", MenuItem(_('menu:privacy'),
                               reverse('main:privacy'),
                               css_class="privacy"
                               ))

# Okay, this is contradicting the above warning. It's fine as it's only shown
# on the mobile menu, which doesn't have the special CSS for the privacy link
Menu.add_item("main", MenuItem(_('main:globals:login'),
                                 reverse('main:login'),
                                 check=lambda x: not x.user.is_authenticated,
                                 ))

Menu.add_item("main", MenuItem(_('mainmenu:change_password'),
                               reverse('main:change_password'),
                               check=lambda x: x.user.is_authenticated
                               ))

Menu.add_item("main", MenuItem(_('main:globals:logout'),
                                 reverse('main:logout'),
                                 check=lambda x: x.user.is_authenticated,
                                 ))

Menu.add_item("footer", MenuItem(_('main:globals:login'),
                                 reverse('main:login'),
                                 check=lambda x: not x.user.is_authenticated
                                 ))

Menu.add_item("footer", MenuItem(_('menu:privacy'),
                                 reverse('main:privacy'),
                                 ))

Menu.add_item("footer", MenuItem(_('main:globals:logout'),
                                 reverse('main:logout'),
                                 check=lambda x: x.user.is_authenticated
                                 ))
