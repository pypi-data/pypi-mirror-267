from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class SimplexThemeHook(ThemeHook):
    """
    Bootswatch Simplex Theme
    https://bootswatch.com/simplex/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "Simplex",
            "Mini and minimalist",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/simplex/bootstrap.min.css",
                "integrity": "sha512-I5ESCAJpdBMo33TBRme9r2K8h7exjtz0lvvBt0BGmjHJxlq+5YNkP2JQZmZrCilMpnM+bJF4Y/53KRmFEMqbpQ=="
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
def register_simplex_hook() -> SimplexThemeHook:
    return SimplexThemeHook()
