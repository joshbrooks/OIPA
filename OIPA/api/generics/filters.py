import uuid
import gc

from django.db.models.sql.constants import QUERY_TERMS
from django.db.models import Q
from django_filters import CharFilter
from django_filters import Filter, FilterSet, NumberFilter, DateFilter, BooleanFilter

VALID_LOOKUP_TYPES = sorted(QUERY_TERMS)

class CommaSeparatedCharFilter(CharFilter):

    def filter(self, qs, value):

        if value:
            value = value.split(',')

        self.lookup_type = 'in'

        return super(CommaSeparatedCharFilter, self).filter(qs, value)

class CommaSeparatedCharMultipleFilter(CharFilter):
    """
    Comma separated filter for lookups like 'exact', 'iexact', etc..
    """
    def filter(self, qs, value):
        if not value: return qs

        values = value.split(',')

        lookup_type = self.lookup_type

        filters = [Q(**{"{}__{}".format(self.name, lookup_type): value}) for value in values]
        final_filters = reduce(lambda a, b: a | b, filters)

        return qs.filter(final_filters)

class CommaSeparatedDateRangeFilter(Filter):

    def filter(self, qs, value):

        if value in ([], (), {}, None, ''):
            return qs

        values = value.split(',')

        return super(CommaSeparatedDateRangeFilter, self).filter(qs, values)

class TogetherFilter(Filter):
    """
    Used with TogetherFilterSet, always gets called regardless of GET args
    """
    
    def __init__(self, filters=None, values=None, **kwargs):
        self.filter_classes = filters
        self.values = values

        super(TogetherFilter, self).__init__(**kwargs)

    def filter(self, qs, values):
        if self.filter_classes:
            filters = { "%s__%s" % (c[0].name, c[0].lookup_type) : c[1] for c in zip(self.filter_classes, values)}
            qs = qs.filter(**filters).distinct()

            return qs

class TogetherFilterSet(FilterSet):
    def __init__(self, data=None, queryset=None, prefix=None, strict=None):
        """
        Adds a together_exclusive meta option that selects fields that have to 
        be called in the same django filter() call when both present
        """

        meta = getattr(self, 'Meta', None)

        # fields that must be filtered in the same filter call
        together_exclusive = getattr(meta, 'together_exclusive', [])

        data = data.copy()

        for filterlist in together_exclusive:
            if set(filterlist).issubset(data.keys()):

                filter_values = [data.pop(filteritem)[0] for filteritem in filterlist]
                filter_classes = [self.declared_filters.get(filteritem, None) for filteritem in filterlist]

                uid = unicode(uuid.uuid4())

                self.base_filters[uid] = TogetherFilter(filters=filter_classes)
                data.appendlist(uid, filter_values)

        super(FilterSet, self).__init__(data, queryset, prefix, strict)

