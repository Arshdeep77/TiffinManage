from io import BytesIO
from django.shortcuts import render
from .models import Customer,Route, Tiffin
from django.http import HttpResponseNotAllowed, JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import messages
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from django.db.models import Sum,Count
from django.db.models import Q
import xlsxwriter
import json
from rest_framework import viewsets
from .models import Customer
from .serializer import CustomerSerializer
from rest_framework.response import Response

def get_form_data(request):
    if request.method == "POST":
        tiffin_data = request.POST.get('tiffin_data')
        return {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "payment": request.POST.get("payment"),
            "start_date": request.POST.get("start_date"),
            "end_date": request.POST.get("end_date"),
            "note": request.POST.get("note"),
            "address":request.POST.get("address"),
            "route":request.POST.get("route"),
            "tiffins":json.loads(tiffin_data),
            "position":request.POST.get("position")
        }

@csrf_exempt
def add_customer(request):
    if request.method == "POST":

        data = get_form_data(request)  
        Customer().create(data=data)

        messages.add_message(request, messages.SUCCESS, "Data inserted")    
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.add_message(request, messages.ERROR, "Somethingh Wrong") 
        return JsonResponse({"message": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def update_customer(request, id):
    if request.method == "POST":
        # Retrieve data from the POST request
        data = get_form_data(request)  
       
        # Here you should perform necessary validations on the data

        try:
            # Get the customer instance from the database
            customer = Customer.objects.get(pk=id)

            # Update customer data with the new values
            customer.name = data['name']
            customer.phone = data['phone']
            customer.payment = data['payment']
            customer.start_date = data['start_date']
            customer.end_date = data['end_date']
            customer.note = data['note']
            customer.address = data['address']
            customer.route = data['route']
            customer.position=data['position']
                    
            # Save the updated customer object
            customer.save()

            tiffins = Tiffin.objects.filter(customer=customer)
            tiffins.delete()
            
            for tiffin in data['tiffins']:
                userTiffin = Tiffin(customer_id = customer.id,
                    dry=tiffin.get('dry'),
                    gravy=tiffin.get('gravy'),
                    roti=tiffin.get('roti'),
                    rice=tiffin.get('rice'),
                    type=tiffin.get('type'),
                   )
                userTiffin.save()


            # Optionally, you can return a success message or data
            messages.add_message(request, messages.SUCCESS, "Data Updated") 
            return redirect(request.META.get('HTTP_REFERER'))

        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer does not exist'}, status=404)
        except Exception as e:
            # Return an error response if something goes wrong
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

@api_view(['GET'])
def get_customer_data(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)
def getCustomers(request):
        # Retrieve all customer instances from the database
    customer_data = list(Customer.objects.order_by('-created_at').prefetch_related('tiffin').values())
    # for customer in customer_data:
    #     regular = customer['regular']
    #     named = customer['named']
        
    #     # Concatenate regular and named values
    #     if regular>0 and named>0:
    #         customer['package'] = f'Regular({regular}) and Named ({named})'
    #     elif regular>0:
    #         customer['package'] = f'Regular({regular})'
    #     elif named>0:
    #         customer['package'] = f'Named({named})'
    #     else:
    #          customer['package'] = 'Na'
        
    # Serialize queryset to JSON format
    return JsonResponse(customer_data, safe=False)    

def index(request):
    context = {
        "services": [],
        "routes":Route.objects.all()
    }
    return render(request, "index.html", context)

def delete_customer(request, id):
    if request.method == 'POST':
        item = Customer.objects.get(pk=id)  # Replace YourModel with your actual model
        item.delete()
        # Redirect to the page you want to go to after deleting the item
        messages.add_message(request, messages.SUCCESS, "Data Deleted") 
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        # If the request method is not POST, return an error or redirect
        return HttpResponseNotAllowed(['POST'])
    
def type_formatter(data):
    return_string = ""
    if data.roti != 0:
        return_string += f"Roti ({data.roti}) "
    if data.dry != 0:
        return_string += f"Dry ({data.dry}) "
    if data.gravy != 0:
        return_string += f"Gravy ({data.gravy}) "
    if data.rice != 0:
        return_string += f"Rice ({data.rice}) "
    if data.type == 'custom':
        data.type = 'Named'
    else:
        data.type = "Regular"
    return_string += f"- [{data.type[0]}]\n"
    return return_string
def download_file(request):
    
    route_no=request.GET['rno']
    file_name=""
    query_date=request.GET['date']
    if request.GET.get('expire'):
        customers = Customer.objects.filter(end_date__lte=request.GET['date'])
        file_name=f"Expire Users Sheet.xlsx"
    else:
        if route_no!='all':
            customers = Customer.objects.filter(end_date__gt=request.GET['date'],route=route_no)
        else:    
            customers = Customer.objects.filter(end_date__gt=request.GET['date'])
        file_name=f"Driver Sheet Route_{route_no}_({query_date}).xlsx"
    # Create an in-memory Excel file
    customers = customers.order_by('position')
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    bold_format = workbook.add_format({'bold': True})
    named_format = workbook.add_format({'bg_color': 'yellow'})

    # Write column headers
    headers = ['Customer Name', 'Type', 'Package', 'Address', 'Phone Number','Position']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold_format)
        worksheet.set_column(col, col, 30)  # Adjust column width # Adjust column width
        worksheet.set_default_row(80)  

    # Write data rows
    for row, customer in enumerate(customers, start=1):
               
        roti_count=0
        dry_count=0
        gravy_count=0
        packages={'regular':0,'custom':0}
        tiffin_package = ''
        for tiffin in Tiffin.objects.filter(customer=customer):
            pack=tiffin.type
            if pack in packages:
                packages[pack]+=1
            roti_count+=tiffin.roti
            dry_count+=tiffin.dry
            gravy_count+=tiffin.gravy
            tiffin_package += type_formatter(tiffin)

        regular = packages.get('regular')
        custom = packages.get('custom')
        package = tiffin_package[:-1]
        pack_type=""
        # Concatenate regular and named values

        if regular>0 and custom>0:
            pack_type = f'Regular({regular}) and Named({custom})'
        elif regular>0:
            pack_type = f'Regular({regular})'
        elif custom>0:
            pack_type = f'Named({custom})'
        else:
             pack_type = 'Na'

        worksheet.write(row, 0, customer.name)
        if custom>0:
            worksheet.write(row, 0, customer.name, named_format)
        worksheet.write(row, 1, pack_type)
        worksheet.write(row, 2, package)
        worksheet.write(row, 3, customer.address)
        worksheet.write(row, 4, customer.phone)
        worksheet.write(row, 5, customer.position)

    # Close the workbook
    workbook.close()

    # Set response headers for Excel file download
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    return response


def get_item_count(request):
    rotis = request.GET['rotis'] 
    customers = Customer.objects.filter(end_date__gt=request.GET['date'])

    tiffins = Tiffin.objects.filter(customer__in=customers)

    tiffins_summary = tiffins.aggregate(
        total_roti=Sum('roti'),
        total_gravy=Sum('gravy'),
        total_dry=Sum('dry'),
        tiffins_roti =Count('id', filter=Q(roti=rotis))
    )
    total_roti = tiffins_summary['total_roti']
    total_gravy = tiffins_summary['total_gravy']
    total_dry = tiffins_summary['total_dry']
    tiffins_roti = tiffins_summary['tiffins_roti']
    # Create a dictionary containing the counts
    data = {
    'roti_count': total_roti if total_roti else 0,
    'gravy_count': total_gravy if total_gravy else 0,
    'dry_count': total_dry if total_dry else 0,
    'tiffins_roti': tiffins_roti if tiffins_roti else 0
}

    # Return the counts as JSON response
    return JsonResponse(data)