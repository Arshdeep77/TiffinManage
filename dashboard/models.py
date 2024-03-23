from django.db import models

class Route(models.Model):
    rno = models.DecimalField(max_digits=10, decimal_places=0, null=True, default=0)

class Tiffin(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    roti = models.IntegerField(default=0)
    dry = models.IntegerField(default=0)
    gravy = models.IntegerField(default=0)
    rice = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=[('regular', 'Regular'), ('custom', 'Custom')])
    def __str__(self):
        return f"Tiffin for {self.customer}"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    start_date = models.DateField()
    end_date = models.DateField()
    position = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    note = models.TextField(null=True, blank=True, default=None)
    address = models.TextField(null=True, blank=True, default=None)
    route = models.DecimalField(max_digits=10, decimal_places=0, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def create(self, data):
        
       
        customer = Customer(
            name=data["name"],
            phone=data["phone"],
            payment=data["payment"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            note=data['note'],
            address=data['address'],
            route=data['route'],
            position=data['position']
        )
        

        # Save the customer instance
        customer.save()
        for tiffin in data['tiffins']:
            userTiffin = Tiffin(customer_id = customer.id,
                   dry=tiffin.get('dry'),
                   gravy=tiffin.get('gravy'),
                   roti=tiffin.get('roti'),
                   rice=tiffin.get('rice'),
                   type=tiffin.get('type'),
                   )
            userTiffin.save()

    def __str__(self):
        return self.name
