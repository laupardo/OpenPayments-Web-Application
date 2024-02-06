from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import pandas as pd
from .models import Payment
from django.http import JsonResponse


# class based views


class SearchExportView(View):
    def get(self, request):
        # Search for objects with first name that starts with letters in input
        query = self.request.GET.get('q', '')
        if len(query) > 0:
            queryset = Payment.objects.filter(Covered_Recipient_First_Name__istartswith=query)

            return render(request, 'search.html', {'queryset': queryset})

        return render(request, 'search.html')

    def post(self, request):
        # Check if the 'download' button was clicked
        if 'download' in request.POST:
            query = request.POST.get('q', '')
            queryset = Payment.objects.filter(Covered_Recipient_First_Name__istartswith=query)
            # Export to Excel
            df = pd.DataFrame(list(queryset.values()))
            # Create a response with the Excel file
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="search_results.xls"'
            df.to_excel(response, index=False)
            return response

        return render(request, 'search.html')


class TypeaheadDataView(View):
    def get(self, request):
        # Search for objects with first name that starts with letters in input but sends json for the typeahead
        query = request.GET.get('query', '')
        queryset = Payment.objects.filter(Covered_Recipient_First_Name__istartswith=query)
        data = [{'id': item.id, 'name': item.Covered_Recipient_First_Name} for item in queryset]
        return JsonResponse(data, safe=False)
