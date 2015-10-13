#!/usr/bin/python

from datetime import datetime
from pprint import pprint

time_format = '%m/%d/%Y'
mindate = datetime(1, 1, 1)


def _build_tree(current_order, episode_order, episode_data, obj, date_field, parent=None, max_date_obj=None):
    if isinstance(current_order, dict):
        for parent in current_order:
            obj.setdefault(parent, {}).setdefault('data', episode_data.get(parent))
            parent_date_obj = episode_data.get(parent).get(date_field)
            max_date = datetime.strptime(parent_date_obj, time_format) if parent_date_obj else mindate
            obj.setdefault(parent, {}).setdefault('max_date', max_date)
            if current_order.get(parent):
                obj.get(parent).setdefault('children', [])
                p_children = obj.get(parent).get('children')
                p_children + _build_tree(current_order=current_order.get(parent),
                                         episode_order=episode_order,
                                         episode_data=episode_data,
                                         obj=p_children,
                                         date_field=date_field,
                                         parent=parent,
                                         max_date_obj=obj.get(parent))
    elif isinstance(current_order, list):
        for child in current_order:
            obj.append({child: {'data': episode_data.get(child)}})
            child_date_obj = episode_data.get(child).get(date_field)
            child_date = datetime.strptime(child_date_obj, time_format) if child_date_obj else mindate
            if child_date > max_date_obj.get('max_date'):
                max_date_obj['max_date'] = child_date
            if child in episode_order:
                idx = obj.index(filter(lambda x: next(k for k, v in x.iteritems()) == child, obj)[0])
                obj[idx].get(child).setdefault('children', [])
                c_children = obj[idx].get(child).get('children')
                c_children + _build_tree(current_order=episode_order.get(child),
                                         episode_order=episode_order,
                                         episode_data=episode_data,
                                         obj=c_children,
                                         date_field=date_field,
                                         parent=child,
                                         max_date_obj=max_date_obj)

    return obj


def _sort_tree(data, date_field, desc_order=True, parent_max_date=None):
    if isinstance(data, dict):
        for k, v in data.iteritems():
            if 'children' in v:
                v['children'] = _sort_tree(data=v['children'],
                                           date_field=date_field,
                                           parent_max_date=data[k]['max_date'])
        data = sorted(data.items(),
                      key=lambda x: x[1]['max_date'],
                      reverse=desc_order)
        for rec in data:
            del rec[1]['max_date']
    elif isinstance(data, list):
        for child in data:
            child_obj = child.items()[0]
            child_date_obj = child_obj[1]['data'].get(date_field)
            child_max_date = datetime.strptime(child_date_obj, time_format) if child_date_obj else mindate
            child_obj[1]['max_date'] = child_max_date
            if parent_max_date < child_max_date:
                parent_max_date = child_max_date
            if 'children' in child_obj[1]:
                child_obj[1]['children'] = _sort_tree(data=child_obj[1]['children'],
                                                      date_field=date_field,
                                                      parent_max_date=child_obj[1]['max_date'])
        data = sorted(data,
                      key=lambda x: x.items()[0][1]['max_date'],
                      reverse=desc_order)
        if len(data) > 1:
            child_obj[1]['max_date'] = reduce(
                lambda x, y: x.items()[0][1]['max_date']
                if x.items()[0][1]['max_date'] > y.items()[0][1]['max_date'] else y.items()[0][1]['max_date'], data)
        for child in data:
            del child.items()[0][1]['max_date']

    return data


def _getEpisodeHierarchy(episode_order, episode_data):
    parents = episode_order.keys()
    children = [i for lst in episode_order.values() for i in lst]
    actual_list = {k: episode_order[k] for k in parents if k not in children}
    result = _build_tree(actual_list, episode_order, episode_data, date_field='date', obj={})
    return [{record[0]: record[1]} for record in _sort_tree(result, date_field='date')]


order = {5: [6, 4], 6: [7, 8], 1: [2, 5], 8: [3], 10: [9]}
data = {
    1: {'date': ''},
    2: {'date': '12/10/2015'},
    3: {'date': '03/09/2014'},
    4: {'date': '07/23/2015'},
    5: {'date': ''},
    6: {'date': '02/01/2015'},
    7: {'date': '12/19/2014'},
    8: {'date': '12/31/2014'},
    9: {'date': '12/31/2014'},
    10: {'date': '12/04/2015'}
}
d1 = {5: [6, 4], 6: [7]}

# _getEpisodeHierarchy(order, data)
pprint(_getEpisodeHierarchy(order, data))
