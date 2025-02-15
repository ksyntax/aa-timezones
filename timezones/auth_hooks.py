"""
Hooks to AA
"""

# Django
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Time Zones
from timezones import __title__, urls
from timezones.app_settings import allianceauth_discordbot_active


class AaTimezonesMenuItem(MenuItemHook):  # pylint: disable=too-few-public-methods
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self):
        # Set up menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _(__title__),
            "far fa-clock fa-fw",
            "timezones:index",
            navactive=["timezones:index"],
        )

    def render(self, request):
        """
        Only if the user has access to this app
        :param request:
        :return:
        """

        if request.user.has_perm("timezones.basic_access"):
            return MenuItemHook.render(self, request)

        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """
    Register our menu item
    :return:
    """

    return AaTimezonesMenuItem()


@hooks.register("url_hook")
def register_urls():
    """
    Register our base url
    :return:
    """

    return UrlHook(urls, "timezones", r"^timezones/")


# Only register the cog when aadiscordbot is installed
if allianceauth_discordbot_active():

    @hooks.register("discord_cogs_hook")
    def register_cogs():
        """
        Registering our discord cog
        """

        return ["timezones.aadiscordbot.cogs.time"]
