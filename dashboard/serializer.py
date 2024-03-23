from rest_framework import serializers
from .models import Customer, Tiffin

class TiffinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tiffin
        fields = ('id', 'roti', 'dry', 'gravy','rice', 'type')

class CustomerSerializer(serializers.ModelSerializer):
    tiffins = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'name', 'phone', 'payment', 'start_date', 'end_date', 'note', 'address', 'route', 'tiffins','position')

    def get_tiffins(self, obj):
        tiffins = Tiffin.objects.filter(customer=obj)
        return TiffinSerializer(tiffins, many=True).data
    def to_representation(self, instance):
        
        rep = super().to_representation(instance)
        roti_count=0
        dry_count=0
        gravy_count=0
        packages={'regular':0,'custom':0}
        for tiffin in rep['tiffins']:
            pack=tiffin.get('type')
            if pack in packages:
                packages[pack]+=1
            roti_count+=tiffin.get('roti',0)
            dry_count+=tiffin.get('dry',0)
            gravy_count+=tiffin.get('gravy',0)

        rep['roti']=roti_count
        rep['dry']=dry_count
        rep['gravy']=gravy_count
        regular=packages['regular']
        custom=packages['custom']
        if regular>0 and custom>0:
            rep['package'] = f'Regular({regular}) and Named ({custom})'
        elif regular>0:
            rep['package'] = f'Regular({regular})'
        elif custom>0:
            rep['package'] = f'Named({custom})'
        else:
             rep['package'] = 'Na'
        
        return rep
