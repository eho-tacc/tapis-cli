import dateparser
from datetime import datetime
from .searcharg import SearchArg
from .arrowspan import ArrowSpan
from . import argmod, argtype, optionize, propertize, tapisize

__all__ = ['WebParam', 'SearchWebParam']

class WebParam(dict):
    pass

class SearchWebParam(SearchArg):
    """Implements that render param=value for passing to a web service
    """
    def query_eq(self, value):
        # EQUALS
        if isinstance(value, list):
            value = value[0]
        key = '{}.eq'.format(self.field)
        return WebParam({key: value})

    def query_neq(self, value):
        # NOT_EQUAL
        if isinstance(value, list):
            value = value[0]
        key = '{}.neq'.format(self.field)
        return WebParam({key: value})

    def query_gt(self, value):
        # GREATER_THAN
        if isinstance(value, list):
            value = value[0]
        key = '{}.gt'.format(self.field)
        return WebParam({key: value})

    def query_gte(self, value):
        # GREATER_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        key = '{}.gte'.format(self.field)
        return WebParam({key: value})

    def query_lt(self, value):
        # LESS_THAN
        if isinstance(value, list):
            value = value[0]
        key = '{}.lt'.format(self.field)
        return WebParam({key: value})

    def query_lte(self, value):
        # LESS_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        key = '{}.lte'.format(self.field)
        return WebParam({key: value})

    def query_in(self, values):
        # IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        qvals = ','.join(qvals)
        key = '{}.in'.format(self.field)
        return WebParam({key: qvals})

    def query_nin(self, values):
        # NOT IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        qvals = ','.join(qvals)
        key = '{}.nin'.format(self.field)
        return WebParam({key: qvals})

    def query_start(self, value):
        # STARTS WITH
        if isinstance(value, list):
            value = value[0]
        key = '{}.like'.format(self.field)
        val = '{}*'.format(value)
        return WebParam({key: val})

    # def query_nstart(self, value):
    #     # DOESN'T START WITH
    #     if isinstance(value, list):
    #         value = value[0]
    #     key = '{}.nlike'.format(self.field)
    #     val = '{}*'.format(value)
    #     return WebParam({key: val})

    def query_end(self, value):
        # ENDS WITH
        if isinstance(value, list):
            value = value[0]
        key = '{}.like'.format(self.field)
        val = '*{}'.format(value)
        return WebParam({key: val})

    # def query_nend(self, value):
    #     # DOESN'T END WITH
    #     if isinstance(value, list):
    #         value = value[0]
    #     key = '{}.nlike'.format(self.field)
    #     val = '*{}'.format(value)
    #     return WebParam({key: val})

    def query_like(self, value):
        # WILDCARD CONTAINS
        if isinstance(value, list):
            value = value[0]
        key = '{}.like'.format(self.field)
        val = '*{}*'.format(value)
        return WebParam({key: val})

    def query_nlike(self, value):
        # WILDCARD NOT CONTAINS
        if isinstance(value, list):
            value = value[0]
        key = '{}.nlike'.format(self.field)
        val = '*{}*'.format(value)
        return WebParam({key: val})

    # def query_on(self, value):
    #     if self.field_type is not argtype.DATETIME:
    #         raise TypeError('"on" may only be used for dates and times')
    #     return self.query_eq(value)

    # def query_after(self, value):
    #     if self.field_type is not argtype.DATETIME:
    #         raise TypeError('"after" may only be used for dates and times')
    #     return self.query_gt(value)

    # def query_before(self, value):
    #     if self.field_type is not argtype.DATETIME:
    #         raise TypeError('"before" may only be used for dates and times')
    #     return self.query_lt(value)
