from django import template

register = template.Library()

STATES = {'act': 'Australian Capital Territory',
          'nsw': 'New South Wales',
          'nt': 'Northern Territory',
          'qld': 'Queensland',
          'sa': 'South Australia',
          'tas': 'Tasmania',
          'vic': 'Victoria',
          'wa': 'Western Australia'}

@register.filter(name='get_state')
def get_state(value):
    return STATES[value]