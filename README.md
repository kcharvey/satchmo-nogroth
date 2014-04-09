satchmo-nogroth [![Build Status](https://travis-ci.org/kcharvey/satchmo-nogroth.svg?branch=master)](https://travis-ci.org/kcharvey/satchmo-nogroth)
===============

NoGroTH = No Ground To Hawaii - A tiered weight shipping module that is Administrative Area (i.e. state/province) aware

Installation
---

 1. Install NoGroTH with Pip

        pip install satchmo-nogroth

 2. Add `nogroth` to your `INSTALLED_APPS`

        INSTALLED_APPS = (
            ..
            'nogroth',
        )

 3. Add `nogroth` to your `CUSTOM_SHIPPING_MODULES`

        SATCHMO_SETTINGS = {
            …
            'CUSTOM_SHIPPING_MODULES': ['nogroth'],
        }

 4. Add the NoGroTH fields to the database
 
        python manage.py migrate nogroth

 5. Activate 'NoGroTH' as a shipping module in `livesettings`
 
 6. If necessary, copy over existing Tiered Weight Shipping rules to NoGroTH. Make sure `shipping.modules.tieredweight` is in your installed apps and run

        python manage.py satchmo_nogroth_copy_tiers

  You can remove `shipping.modules.tieredweight` from your settings file after this command successfully runs.

Dependencies
---

Assuming you've got a working Satchmo site, there are no other dependencies besides `satchmo` and it's dependencies.

Development
---

Pull requests welcome! Just fork the repo.

### Running the tests

You'll need to have a working Satchmo project and complete installation steps 1-4. Then run

    python manage.py tests nogroth
