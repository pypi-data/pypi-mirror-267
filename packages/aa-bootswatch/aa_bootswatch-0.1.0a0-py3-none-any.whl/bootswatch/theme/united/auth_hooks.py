from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class UnitedThemeHook(ThemeHook):
    """
    Bootswatch United Theme
    https://bootswatch.com/united/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "United",
            "Ubuntu orange and unique font",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.3/united/bootstrap.min.css",
                "integrity": "sha512-bDf5pNGht0HBv1tNSyB06LQ4D+5IV4xpCmAFKORMIQi57c8mq96hg2Wa03//JNjHEjEai1qV+ZOUcwuy70j02A=="
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
def register_united_hook() -> UnitedThemeHook:
    return UnitedThemeHook()
