# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Carrier'
        db.create_table('nogroth_carrier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('default_zone', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='default', null=True, to=orm['nogroth.Zone'])),
        ))
        db.send_create_signal('nogroth', ['Carrier'])

        # Adding model 'Zone'
        db.create_table('nogroth_zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('carrier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='zones', to=orm['nogroth.Carrier'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('handling', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('nogroth', ['Zone'])

        # Adding unique constraint on 'Zone', fields ['carrier', 'name']
        db.create_unique('nogroth_zone', ['carrier_id', 'name'])

        # Adding M2M table for field countries on 'Zone'
        m2m_table_name = db.shorten_name('nogroth_zone_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('zone', models.ForeignKey(orm['nogroth.zone'], null=False)),
            ('country', models.ForeignKey(orm['l10n.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['zone_id', 'country_id'])

        # Adding M2M table for field excluded_admin_areas on 'Zone'
        m2m_table_name = db.shorten_name('nogroth_zone_excluded_admin_areas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('zone', models.ForeignKey(orm['nogroth.zone'], null=False)),
            ('adminarea', models.ForeignKey(orm['l10n.adminarea'], null=False))
        ))
        db.create_unique(m2m_table_name, ['zone_id', 'adminarea_id'])

        # Adding model 'ZoneTranslation'
        db.create_table('nogroth_zonetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['nogroth.Zone'])),
            ('lang_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('delivery', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('nogroth', ['ZoneTranslation'])

        # Adding model 'WeightTier'
        db.create_table('nogroth_weighttier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tiers', to=orm['nogroth.Zone'])),
            ('min_weight', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('handling', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('expires', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('nogroth', ['WeightTier'])

        # Adding unique constraint on 'WeightTier', fields ['zone', 'min_weight', 'expires']
        db.create_unique('nogroth_weighttier', ['zone_id', 'min_weight', 'expires'])


    def backwards(self, orm):
        # Removing unique constraint on 'WeightTier', fields ['zone', 'min_weight', 'expires']
        db.delete_unique('nogroth_weighttier', ['zone_id', 'min_weight', 'expires'])

        # Removing unique constraint on 'Zone', fields ['carrier', 'name']
        db.delete_unique('nogroth_zone', ['carrier_id', 'name'])

        # Deleting model 'Carrier'
        db.delete_table('nogroth_carrier')

        # Deleting model 'Zone'
        db.delete_table('nogroth_zone')

        # Removing M2M table for field countries on 'Zone'
        db.delete_table(db.shorten_name('nogroth_zone_countries'))

        # Removing M2M table for field excluded_admin_areas on 'Zone'
        db.delete_table(db.shorten_name('nogroth_zone_excluded_admin_areas'))

        # Deleting model 'ZoneTranslation'
        db.delete_table('nogroth_zonetranslation')

        # Deleting model 'WeightTier'
        db.delete_table('nogroth_weighttier')


    models = {
        'l10n.adminarea': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AdminArea'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['l10n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'l10n.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'admin_area': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'nogroth.carrier': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'Carrier'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'default_zone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default'", 'null': 'True', 'to': "orm['nogroth.Zone']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'nogroth.weighttier': {
            'Meta': {'ordering': "['min_weight']", 'unique_together': "(('zone', 'min_weight', 'expires'),)", 'object_name': 'WeightTier'},
            'expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'handling': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tiers'", 'to': "orm['nogroth.Zone']"})
        },
        'nogroth.zone': {
            'Meta': {'ordering': "['carrier', 'name']", 'unique_together': "(('carrier', 'name'),)", 'object_name': 'Zone'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zones'", 'to': "orm['nogroth.Carrier']"}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'zone_countries'", 'blank': 'True', 'to': "orm['l10n.Country']"}),
            'excluded_admin_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'zone_excluded_admin_areas'", 'blank': 'True', 'to': "orm['l10n.AdminArea']"}),
            'handling': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'nogroth.zonetranslation': {
            'Meta': {'ordering': "['lang_code']", 'object_name': 'ZoneTranslation'},
            'delivery': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['nogroth.Zone']"})
        }
    }

    complete_apps = ['nogroth']