from django.db import models
import inspect
import sys

STATE_CHOICES = (('ACT','ACT'),('NSW','NSW'),('NT','NT'),('QLD','QLD'),('SA','SA'),('TAS','TAS'),('VIC','VIC'),('WA','WA'))

def get_class_name_choices():
    choices = []
    for cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        choices.append((cls[0].lower(), cls[0]))
    return choices

def get_field_name_choices(class_name):
        choices = []
        for fld in getattr(sys.modules[__name__], class_name)._meta.get_all_field_names():
            choices.append((fld, fld))
        return choices
    
def get_all_field_name_choices():
    choices = []
    for cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        for fld in getattr(sys.modules[__name__], cls[0])._meta.get_all_field_names():
            choices.append((fld, '%s - %s' % (cls[0], fld)))
    return choices

# Create your models here.
class Schema(models.Model):
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=10)
    address = models.URLField()
    
    def __unicode__(self):
        return self.name

class Attribute(models.Model):
    schema = models.ForeignKey('Schema')
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s:%s' % (self.schema.prefix, self.name)
    
    def get_schema(self):
        return (self.schema.prefix, self.schema.address)    
    
class Relationship(models.Model):
    attribute = models.ForeignKey('Attribute')
    value = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.value

class Archive(models.Model):
    daa_id = models.AutoField(primary_key=True)
    name = models.TextField()
    address = models.TextField(blank=True)
    postal_address = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    fax = models.TextField(blank=True)
    website = models.TextField(blank=True)
    email = models.TextField(blank=True)
    officer = models.TextField(blank=True)
    facilities = models.TextField(blank=True)
    access = models.TextField(blank=True)
    focus = models.TextField(blank=True)
    quantity = models.TextField(blank=True)
    enquiries = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    holdings = models.TextField(blank=True)
    guides = models.TextField(blank=True)
    references = models.TextField(blank=True)
    see_also = models.TextField(blank=True)
    last_updated = models.DateField(auto_now=True)
    n_id = models.IntegerField(blank=True, null=True, editable=False)
    public = models.BooleanField(default=True)
    state = models.CharField(max_length=3, choices=STATE_CHOICES)
    
    def __unicode__(self):
        return self.name
    
    def get_next(self):
        return Archive.objects.order_by('name').filter(name__gt=self.name)[:1]
    
    def get_previous(self):
        return Archive.objects.order_by('-name').filter(name__lt=self.name)[:1]
    
    def get_next_in_state(self):
        return Archive.objects.filter(state=self.state).order_by('name').filter(name__gt=self.name)[:1]
    
    def get_previous_in_state(self):
        return Archive.objects.filter(state=self.state).order_by('-name').filter(name__lt=self.name)[:1]
    
class Slug(models.Model):
    slug = models.CharField(max_length=200)
    archive = models.ForeignKey(Archive)
    
    def __unicode__(self):
        return self.slug

class ArchiveType(models.Model):
    label = models.CharField(max_length=20)
    link = models.URLField()
    description = models.TextField(blank=True)
    
class City_or_Suburb(models.Model):
    #Data from GeoNames.
    geonames_id = models.IntegerField()
    name = models.CharField(max_length=100)
    
class Address(models.Model):
    
    ADDRESS_TYPE_CHOICES = (('postal', 'postal'),('physical','physical'))
    ADDRESS_STATUS_CHOICES = (('preferred', 'preferred'),('alternative','alternative'))
    
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    address_status = models.CharField(max_length=11, choices=ADDRESS_STATUS_CHOICES)
    po_box = models.CharField(max_length=50, blank=True)
    room_or_building = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    street_location = models.CharField(max_length=100, blank=True)
    city_or_suburb = models.ForeignKey('City_or_Suburb')
    state = models.IntegerField(choices=STATE_CHOICES)
    postcode = models.CharField(max_length=4, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    
class Website(models.Model):
    
    WEBSITE_TYPE_CHOICES = (('corporate','corporate'),('blog','blog'),('exhibition','exhibition'),('project','project'))
    
    title = models.CharField(max_length=200, blank=True)
    website_type = models.CharField(max_length=10, choices=WEBSITE_TYPE_CHOICES)
    url = models.URLField()
    
class Account(models.Model):
    service_name = models.CharField(max_length=100)
    account_url = models.URLField()
    
class Role(models.Model):
    name = models.CharField(max_length=200)
    occupant = models.ManyToManyField('Person', blank=True)
    
class Person(models.Model):
    surname = models.CharField(max_length=200)
    other_names = models.CharField(max_length=200, blank=True)
    pa_id = models.URLField(blank=True)
    
class Publication(models.Model):
    type
    author = models.ManyToManyField('Person', blank=True)
    title = models.CharField(max_length=200)
    collection_title = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    publication_place = models.CharField(max_length=100, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    number = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    link = models.URLField(blank=True)
    nla_id = models.URLField(blank=True)
    
class RelatedCollection(models.Model):
    collection1 = models.ForeignKey('Collection', related_name='collection1')
    collection2 = models.ForeignKey('Collection', related_name='collection2')
    relationship = models.CharField(max_length=100)
    
class RelatedPerson(models.Model):
    person = models.ForeignKey('Person')
    collection = models.ForeignKey('Collection')
    relationship = models.CharField(max_length=100)
    
class Collection(models.Model):
    title = models.CharField(max_length=200)
    identifier = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.IntegerField(max_length=4, blank=True, null=True)
    end_date = models.IntegerField(max_length=4, blank=True, null=True)
    format = models.CharField(max_length=50)
    shelf_metres = models.IntegerField(max_length=4, blank=True, null=True)
    number_items = models.IntegerField(blank=True, null=True)
    references = models.ManyToManyField('Publication', blank=True, null=True)
    link = models.URLField(blank=True)
    related_collections = models.ManyToManyField('self', through='RelatedCollection', symmetrical=False)
    related_person = models.ManyToManyField('Person', through='RelatedPerson')
    
class Organisation(models.Model):
    daa_id = models.IntegerField() #ISDIAH 5.1.1
    name = models.CharField(max_length=200) #ISDIAH 5.1.2
    abbreviation = models.CharField(max_length=10, blank=True) #ISDIAH 5.1.4
    type = models.ManyToManyField('ArchiveType') #ISDIAH 5.1.5
    physical_address = models.ManyToManyField('Address', blank=True, related_name='physical_address')
    postal_addess = models.ForeignKey('Address', blank=True, related_name='postal_address')
    state = models.CharField(max_length=3, choices=STATE_CHOICES)
    websites = models.ManyToManyField('Website', blank=True)
    collections = models.ManyToManyField('Collection', blank=True)
    focus = models.TextField(blank=True)
    focus_url = models.URLField(blank=True)
    history = models.TextField(blank=True)
    history_url = models.URLField(blank=True)
    opening_times = models.TextField(blank=True)
    opening_times_url = models.URLField(blank=True)
    access = models.TextField(blank=True)
    access_url = models.URLField(blank=True)
    research_services = models.TextField(blank=True)
    research_services_url = models.URLField(blank=True)
    reproduction_services = models.TextField(blank=True)
    reproduction_services_url = models.URLField(blank=True)
    citation_format = models.TextField(blank=True)
    citation_format_url = models.URLField(blank=True)
    related_orgs = models.ManyToManyField('self', blank=True, null=True)
    last_updated = models.DateField(auto_now=True)
    n_id = models.IntegerField(blank=True, null=True, editable=False)
    public = models.BooleanField(default=True)


class Mapping(models.Model):
    class_name = models.CharField(max_length=30, choices=get_class_name_choices())
    field_name = models.CharField(max_length=30, choices=get_all_field_name_choices())
    attributes = models.ManyToManyField('Attribute')

    def __unicode__(self):
        maps = []
        for map in self.attributes.all():
            maps.append(map.__unicode__())
        return '%s.%s = %s' % (self.class_name, self.field_name, ', '.join(maps))
    
    def get_attribute_list(self):
        attrs = []
        for attr in self.attributes.all():
            attrs.append(attr.__unicode__())
        return attrs
    
    def get_schema_list(self):
        schemas = []
        for attr in self.attributes.all():
            schemas.append(attr.get_schema())
        return schemas 
    
    