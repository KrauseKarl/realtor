from app_favorites.favorites import Favorite


def favorites(request):
    """Функция для добавление контекстных данных корзины на все страницы сайта"""
    return {'app_favorites': Favorite(request)}
