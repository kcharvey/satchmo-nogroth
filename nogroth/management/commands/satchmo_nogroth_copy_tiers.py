from django.core.management.base import BaseCommand, CommandError
from shipping.modules.tieredweight.models import Carrier as TWCarrier, Zone as TWZone, ZoneTranslation as TWZoneTranslation, WeightTier as TWWeightTier
from nogroth.models import *

class Command(BaseCommand):
    help = 'Converts existing Tiered Weight shipping rules to NoGroTH'

    def handle(self, *args, **options):
        counts = {}
        
        carriers = TWCarrier.objects.all()
        counts['car'] = carriers.count()
        for carrier in carriers.values():
            Carrier.objects.create(**carrier)

        zones = TWZone.objects.all()
        counts['zo'] = zones.count()
        for zone in zones.values():
            Zone.objects.create(**zone)

        zone_translations = TWZoneTranslation.objects.all()
        counts['zotr'] = zone_translations.count()
        for zt in zone_translations.values():
            ZoneTranslation.objects.create(**zt)

        weight_tiers = TWWeightTier.objects.all()
        counts['wt'] = weight_tiers.count()
        for wt in weight_tiers.values():
            WeightTier.objects.create(**wt)

        self.stdout.write('Converted %(car)s carriers, %(zo)s zones, %(zotr)s zone translations, and %(wt)s weight tiers to NoGroTH\n' % counts)
        
