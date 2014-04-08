from nogroth.models import Carrier, Shipper
from satchmo_utils import load_once

load_once('nogroth', 'nogroth')

def get_methods():
    return [Shipper(carrier) for carrier in Carrier.objects.filter(active=True)]
