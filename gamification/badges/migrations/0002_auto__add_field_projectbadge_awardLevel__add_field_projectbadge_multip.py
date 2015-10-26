# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("core", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding field 'ProjectBadge.awardLevel'
        db.add_column(u'badges_projectbadge', 'awardLevel',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)

        # Adding field 'ProjectBadge.multipleAwards'
        db.add_column(u'badges_projectbadge', 'multipleAwards',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


        # Renaming column for 'ProjectBadge.project' to match new field type.
        db.rename_column(u'badges_projectbadge', 'project', 'project_id')
        # Changing field 'ProjectBadge.project'
        db.alter_column(u'badges_projectbadge', 'project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project']))
        # Adding index on 'ProjectBadge', fields ['project']
        db.create_index(u'badges_projectbadge', ['project_id'])


    def backwards(self, orm):
        # Removing index on 'ProjectBadge', fields ['project']
        db.delete_index(u'badges_projectbadge', ['project_id'])

        # Deleting field 'ProjectBadge.awardLevel'
        db.delete_column(u'badges_projectbadge', 'awardLevel')

        # Deleting field 'ProjectBadge.multipleAwards'
        db.delete_column(u'badges_projectbadge', 'multipleAwards')


        # Renaming column for 'ProjectBadge.project' to match new field type.
        db.rename_column(u'badges_projectbadge', 'project_id', 'project')
        # Changing field 'ProjectBadge.project'
        db.alter_column(u'badges_projectbadge', 'project', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'badges.badge': {
            'Meta': {'object_name': 'Badge'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'badges.badgesettings': {
            'Meta': {'object_name': 'BadgeSettings'},
            'awardLevel': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multipleAwards': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'badges.projectbadge': {
            'Meta': {'object_name': 'ProjectBadge'},
            'awardLevel': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Badge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multipleAwards': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']"}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badges'", 'symmetrical': 'False', 'through': u"orm['badges.ProjectBadgeToUser']", 'to': u"orm['auth.User']"})
        },
        u'badges.projectbadgetouser': {
            'Meta': {'object_name': 'ProjectBadgeToUser'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projectbadge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.ProjectBadge']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.project': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Project'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['badges']
