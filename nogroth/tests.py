from datetime import datetime
from django.test import TestCase
from l10n.models import Country, AdminArea
from satchmo_store.contact.models import Contact, AddressBook
from satchmo_store.shop.models import Cart, Order, OrderItem
from product.models import Product
from shipping.config import shipping_methods
from nogroth.models import Carrier, WeightTier, Zone, ZoneTranslation, NoGroTHException

try:
    from decimal import Decimal
except:
    from django.utils._decimal import Decimal


def make_tiers(zone, prices, expires=None):
    for weight, handling, price in prices:
        zone.tiers.create(
            min_weight=Decimal(weight),
            handling=Decimal('%i.00' % handling),
            price=Decimal('%i.00' % price),
            expires=expires
        )


class NoGroTHTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name='pricing', active=True)
        self.zone = self.carrier.zones.create(name='zone 1')
        self.zone.tiers.create(
            min_weight=Decimal('1'),
            handling=Decimal('10.00'),
            price=Decimal('1.00'),
        )


    def testBase(self):
        self.assertEqual(self.zone.cost(1), Decimal('11.00'))
        self.assertRaises(NoGroTHException, self.zone.cost, 4)

        
    def testTwoPrices(self):
        self.zone.tiers.create(
            min_weight=Decimal('10.00'),
            handling=Decimal('10.00'),
            price=Decimal('2.00'),
        )
        self.assertEqual(self.zone.cost(1), Decimal('11.00'))
        self.assertEqual(self.zone.cost(9), Decimal('12.00'))
        self.assertEqual(self.zone.cost(10), Decimal('12.00'))
        self.assertRaises(NoGroTHException, self.zone.cost, 100)


class NoGroTHExpiringTest(TestCase):
    def setUp(self):
        self.carrier = Carrier.objects.create(name='pricing', active=True)
        self.zone = self.carrier.zones.create(name='zone 1')
        base_prices = (
            (1, 10, 0),
            (20, 20, 1),
            (30, 30, 2),
            (40, 40, 1)
        )
        make_tiers(self.zone, base_prices)


    def testExpired(self):
        expires = datetime(2000, 1, 1)
        sale_prices = (
            (1, 1, 0),
            (20, 2, 1),
            (30, 3, 1),
            (40, 4, 1)
        )
        make_tiers(self.zone, sale_prices, expires=expires)

        self.assertEqual(self.zone.cost(1), Decimal('10.00'))
        self.assertEqual(self.zone.cost(20), Decimal('21.00'))
        self.assertEqual(self.zone.cost(30), Decimal('32.00'))
        self.assertEqual(self.zone.cost(40), Decimal('41.00'))


    def testNotExpired(self):
        now = datetime.now()
        nextyear = datetime(now.year+1, now.month, now.day)
        sale_prices = (
            (1, 1, 0),
            (20, 2, 1),
            (30, 3, 1),
            (40, 4, 1)
        )
        make_tiers(self.zone, sale_prices, expires=nextyear)

        self.assertEqual(self.zone.cost(1), Decimal('1.00'))
        self.assertEqual(self.zone.cost(10), Decimal('3.00'))
        self.assertEqual(self.zone.cost(20), Decimal('3.00'))
        self.assertEqual(self.zone.cost(30), Decimal('4.00'))
        self.assertEqual(self.zone.cost(40), Decimal('5.00'))


class NoGroTHCountryTest(TestCase):
    def setUp(self):
        self.country1 = Country.objects.create(
            iso2_code='mc',
            name='MYCOUNTRY',
            printable_name='MyCountry',
            iso3_code='mgc',
            continent='EU'
        )
        self.country2 = Country.objects.create(
            iso2_code='nc',
            name='NOTMYCOUNTRY',
            printable_name='NotMyCountry',
            iso3_code='nmc',
            continent='EU'
        )
        self.carrier = Carrier.objects.create(name='pricing', active=True)
        self.zone1 = self.carrier.zones.create(name='zone 1')
        self.zone2 = self.carrier.zones.create(name='zone 2')

        self.zone1.countries.add(self.country1)
        self.carrier.default_zone = self.zone2


    def testDefault(self):
        zone = self.carrier.get_zone(self.country1)
        self.assertEqual(zone, self.zone1)


    def testCountry(self):
        zone = self.carrier.get_zone(self.country2)
        self.assertEqual(zone, self.zone2)


class NoGroTHAdminAreaTest(TestCase):
    def setUp(self):
        self.country1 = Country.objects.create(
            iso2_code='mc',
            name='MYCOUNTRY',
            printable_name='MyCountry',
            iso3_code='mgc',
            continent='NA'
        )
        self.country2 = Country.objects.create(
            iso2_code='nm',
            name='NOTMYCOUNTRY',
            printable_name='NotMyCountry',
            iso3_code='nmc',
            continent='SA'
        )
        self.adminArea1 = AdminArea.objects.create(
            country = self.country1,
            name = 'Tennessee',
            abbrev = 'TN',
            active = True
        )
        self.adminArea2 = AdminArea.objects.create(
            country = self.country1,
            name = 'Hawaii',
            abbrev = 'HI',
            active = True
        )
        self.carrier1 = Carrier.objects.create(name='Ground', active=True)
        self.carrier2 = Carrier.objects.create(name='Air', active=True)
        self.carrier3 = Carrier.objects.create(name='International Air', active=True)
        self.zone1 = self.carrier1.zones.create(name='zone 1')
        self.zone2 = self.carrier2.zones.create(name='zone 2')
        self.zone3 = self.carrier3.zones.create(name='zone 3')

        self.zone1.countries.add(self.country1)
        self.zone2.countries.add(self.country1)
        self.zone3.countries.add(self.country2)
        self.zone2.excluded_admin_areas.add(self.adminArea2)

        self.tier1 = WeightTier.objects.create(
            zone=self.zone1,
            min_weight='1.00',
            price='5.00'
        )
        self.tier2 = WeightTier.objects.create(
            zone=self.zone2,
            min_weight='1.00',
            price='10.00'
        )

        self.contact1 = Contact.objects.create(
            title="Mr.",
            first_name="James",
            last_name="Polk"
        )
        self.contact2 = Contact.objects.create(
            title="Sen.",
            first_name="Bob",
            last_name="Dole"
        )

        self.addressBook1 = AddressBook.objects.create(
            contact=self.contact1,
            addressee="James K. Polk",
            street1="200 Broadway",
            state="TN",
            city="Nashville",
            postal_code="37210",
            country=self.country1,
            is_default_shipping=True,
            is_default_billing=True
        )
        self.addressBook2 = AddressBook.objects.create(
            contact=self.contact2,
            addressee="Bob Dole",
            street1="300 Pineapple Way",
            state="HI",
            city="Honolulu",
            postal_code="99823",
            country=self.country1,
            is_default_shipping=True,
            is_default_billing=True
        )

        self.product = Product.objects.create(
            site_id=1,
            name="Power Suit",
            active=True,
            shipclass="YES",
            weight='1.0'
        )

        self.cart1 = Cart.objects.create(
            customer=self.contact1, 
            site_id=1
        )
        self.cart1.add_item(self.product, 1)

        self.cart2 = Cart.objects.create(
            customer=self.contact2, 
            site_id=1
        )
        self.cart2.add_item(self.product, 1)


    def testIncludedState(self):
        """
        Test that the non-excluded state can use both shippers
        """
        shippers = shipping_methods()
        
        shippers[0].calculate(self.cart1, self.contact1)
        self.assertTrue(shippers[0].valid())

        shippers[1].calculate(self.cart1, self.contact1)
        self.assertTrue(shippers[1].valid())

        shippers[2].calculate(self.cart1, self.contact1)
        self.assertFalse(shippers[2].valid())

    def testExcludedState(self):
        """
        Test that the excluded stat is not valid for the second shipper
        """
        shippers = shipping_methods()
        
        shippers[0].calculate(self.cart2, self.contact2)
        self.assertTrue(shippers[0].valid())

        shippers[1].calculate(self.cart2, self.contact2)
        self.assertFalse(shippers[1].valid())

        shippers[2].calculate(self.cart2, self.contact2)
        self.assertFalse(shippers[2].valid())

class NoGroTHCommandTest(TestCase):
    def setUp(self):
        from shipping.modules.tieredweight.models import Carrier as TWCarrier
        from shipping.modules.tieredweight.models import ZoneTranslation as TWZoneTranslation
        from shipping.modules.tieredweight.models import WeightTier as TWWeightTier

        self.country1 = Country.objects.create(
            iso2_code='mc',
            name='MYCOUNTRY',
            printable_name='MyCountry',
            iso3_code='mgc',
            continent='NA'
        )
        self.carrier1 = TWCarrier.objects.create(name='Ground', active=True)
        self.carrier2 = TWCarrier.objects.create(name='Air', active=True)
        self.zone1 = self.carrier1.zones.create(name='zone 1')
        self.zone2 = self.carrier2.zones.create(name='zone 2')

        self.zone1.countries.add(self.country1)
        self.zone2.countries.add(self.country1)

        self.zoneTrans = TWZoneTranslation.objects.create(
            zone=self.zone1,
            lang_code="ES",
            description="Por Aire",
            method="Aire",
            delivery="5 dias"
        )

        self.tier1 = TWWeightTier.objects.create(
            zone=self.zone1,
            min_weight='1.00',
            price='5.00'
        )
        self.tier2 = TWWeightTier.objects.create(
            zone=self.zone2,
            min_weight='1.00',
            price='10.00'
        )

    def testManagementCommand(self):
        """
        After running satchmo_nogroth_copy_tiers, all of the
        data from tiered weight shipping should be moved
        to NoGroTH
        """
        # at first there were none
        self.assertEqual(Carrier.objects.all().count(), 0)
        self.assertEqual(Zone.objects.all().count(), 0)
        self.assertEqual(ZoneTranslation.objects.all().count(), 0)
        self.assertEqual(WeightTier.objects.all().count(), 0)

        # then we run the command
        from django.core.management import call_command
        call_command('satchmo_nogroth_copy_tiers')

        # and voila
        self.assertEqual(Carrier.objects.all().count(), 2)
        self.assertEqual(Zone.objects.all().count(), 2)
        self.assertEqual(ZoneTranslation.objects.all().count(), 1)
        self.assertEqual(WeightTier.objects.all().count(), 2)
        
        self.assertEqual(Carrier.objects.filter(name="Air", active=True).count(), 1)
        self.assertEqual(Zone.objects.filter(name="zone 1").count(), 1)
        self.assertEqual(ZoneTranslation.objects.filter(zone_id=1).count(), 1)
        self.assertEqual(WeightTier.objects.filter(zone_id=2).count(), 1)
