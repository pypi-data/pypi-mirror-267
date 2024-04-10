from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class MorphThemeHook(ThemeHook):
    """
    Bootswatch Morph Theme
    https://bootswatch.com/morph/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "Morph",
            "A neumorphic layer",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/morph/bootstrap.min.css",
                "integrity": "sha512-Nd3lZDftpGFIyfIz/Snlz7SzhEycjmHkNn3s2dmhrVyY55uJnTE+UiK75+CeXltD5GmU7c9n/JMDWaEwGQjowQ=="
            }],
            js=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
            }, {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.min.js",
                "integrity": "sha512-ykZ1QQr0Jy/4ZkvKuqWn4iF3lqPZyij9iRv6sGqLRdTPkY69YX6+7wvVGmsdBbiIfN/8OdsI7HABjvEok6ZopQ=="
            }],
        )


@hooks.register('theme_hook')
def register_morph_hook() -> MorphThemeHook:
    return MorphThemeHook()
