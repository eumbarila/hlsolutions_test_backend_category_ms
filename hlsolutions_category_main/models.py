# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class CategoriesModel(DjangoCassandraModel):
    id = columns.UUID(primary_key=True)
    name = columns.Text()