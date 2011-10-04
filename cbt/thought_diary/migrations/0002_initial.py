# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Mood'
        db.create_table('thought_diary_mood', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feeling', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('mood', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('thought_diary', ['Mood'])

        # Adding model 'TrackItem'
        db.create_table('thought_diary_trackitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('item', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('thought_diary', ['TrackItem'])

        # Adding model 'TrackItemStatus'
        db.create_table('thought_diary_trackitemstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thought_diary.TrackItem'])),
            ('value', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('thought_diary', ['TrackItemStatus'])

        # Adding model 'Thought'
        db.create_table('thought_diary_thought', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('share', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('thought', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('situation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('thought_diary', ['Thought'])

        # Adding M2M table for field distortions on 'Thought'
        db.create_table('thought_diary_thought_distortions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thought', models.ForeignKey(orm['thought_diary.thought'], null=False)),
            ('distortion', models.ForeignKey(orm['thought_diary.distortion'], null=False))
        ))
        db.create_unique('thought_diary_thought_distortions', ['thought_id', 'distortion_id'])

        # Adding model 'Distortion'
        db.create_table('thought_diary_distortion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('distortion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('question', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('explanation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('how_to_respond', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('example', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('thought_diary', ['Distortion'])

        # Adding model 'ChallengeQuestion'
        db.create_table('thought_diary_challengequestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('thought_diary', ['ChallengeQuestion'])

        # Adding M2M table for field distortion on 'ChallengeQuestion'
        db.create_table('thought_diary_challengequestion_distortion', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('challengequestion', models.ForeignKey(orm['thought_diary.challengequestion'], null=False)),
            ('distortion', models.ForeignKey(orm['thought_diary.distortion'], null=False))
        ))
        db.create_unique('thought_diary_challengequestion_distortion', ['challengequestion_id', 'distortion_id'])

        # Adding model 'Challenge'
        db.create_table('thought_diary_challenge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thought', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thought_diary.Thought'])),
            ('challenge_question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thought_diary.ChallengeQuestion'], null=True, blank=True)),
            ('response', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('thought_diary', ['Challenge'])

        # Adding model 'UserProfile'
        db.create_table('thought_diary_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('startedTracking', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('thought_diary', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Mood'
        db.delete_table('thought_diary_mood')

        # Deleting model 'TrackItem'
        db.delete_table('thought_diary_trackitem')

        # Deleting model 'TrackItemStatus'
        db.delete_table('thought_diary_trackitemstatus')

        # Deleting model 'Thought'
        db.delete_table('thought_diary_thought')

        # Removing M2M table for field distortions on 'Thought'
        db.delete_table('thought_diary_thought_distortions')

        # Deleting model 'Distortion'
        db.delete_table('thought_diary_distortion')

        # Deleting model 'ChallengeQuestion'
        db.delete_table('thought_diary_challengequestion')

        # Removing M2M table for field distortion on 'ChallengeQuestion'
        db.delete_table('thought_diary_challengequestion_distortion')

        # Deleting model 'Challenge'
        db.delete_table('thought_diary_challenge')

        # Deleting model 'UserProfile'
        db.delete_table('thought_diary_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'thought_diary.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'challenge_question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['thought_diary.ChallengeQuestion']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'thought': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['thought_diary.Thought']"})
        },
        'thought_diary.challengequestion': {
            'Meta': {'object_name': 'ChallengeQuestion'},
            'distortion': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'challenge_questions'", 'blank': 'True', 'null': 'True', 'to': "orm['thought_diary.Distortion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'thought_diary.distortion': {
            'Meta': {'object_name': 'Distortion'},
            'distortion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'example': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'how_to_respond': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'thought_diary.mood': {
            'Meta': {'object_name': 'Mood'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'feeling': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mood': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'thought_diary.thought': {
            'Meta': {'object_name': 'Thought'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'distortions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['thought_diary.Distortion']", 'symmetrical': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'share': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'situation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thought': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'thought_diary.trackitem': {
            'Meta': {'object_name': 'TrackItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'thought_diary.trackitemstatus': {
            'Meta': {'object_name': 'TrackItemStatus'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['thought_diary.TrackItem']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'thought_diary.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'startedTracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['thought_diary']
