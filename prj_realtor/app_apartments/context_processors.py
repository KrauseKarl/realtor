from app_apartments.models import ResidenceArea


def residence(request):
    return {'residence_list': ResidenceArea.objects.all()}
