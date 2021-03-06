import inspect
from importlib import import_module

def clean_value(value, unit):
    return '{:.3g} {}'.format(value, unit)

def duplicate_check(f):
    existing_identifiers = {}

    def wrapper(*args, **kwargs):

        module = inspect.getmodule(f)
        module_split = module.__name__.split('.')[:-1]
        module_name = module_split[-1].title() + 'Rester'
        module_rester = '.'.join(module_split + ['rest', 'rester'])
        mod = import_module(module_rester)
        Rester = getattr(mod, module_name)

        check_test_site = kwargs.get('check_test_site', True)
        with Rester(test_site=check_test_site) as mpr:
            for doc in mpr.query_contributions(criteria=mpr.query):
                existing_identifiers[doc['mp_cat_id']] = doc['_id']

        f(*args, **kwargs)

        mpfile = args[0]
        update = 0
        for identifier in mpfile.ids:
            if identifier in existing_identifiers:
                cid = existing_identifiers[identifier]
                mpfile.insert_id(identifier, cid)
                update += 1

        print len(mpfile.ids), 'mp-ids to submit.'
        if update > 0:
            print update, 'mp-ids to update.'

    wrapper.existing_identifiers = existing_identifiers
    return wrapper
