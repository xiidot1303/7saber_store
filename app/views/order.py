from django.http import JsonResponse
from django.views import View

class OrderView(View):
    def post(self, request, *args, **kwargs):
        # Process the order here
        print(request.POST)
        return JsonResponse({'status': 'Order received'})
