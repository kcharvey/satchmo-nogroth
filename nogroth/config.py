import logging

from django.utils.translation import ugettext_lazy as _
from livesettings import *

log = logging.getLogger('nogroth.config')

from shipping.config import SHIPPING_ACTIVE

SHIPPING_ACTIVE.add_choice(('nogroth', _('NoGroTH')))

log.debug('loaded')
