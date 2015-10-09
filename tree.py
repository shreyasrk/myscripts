#!/usr/bin/python

from datetime import datetime

time_format = '%m/%d/%Y'

def _buildtree(order, episode_order, episode_data, obj, date_field, parent=None, max_date_obj=None):
    if isinstance(order, dict):
        for parent in order:
            obj.setdefault(parent, {}).setdefault('data', episode_data.get(parent))
            max_date = datetime.strptime(e.get(parent).get(date_field), time_format) 
            obj.setdefault(parent, {}).setdefault('max_date', max_date)
            if order.get(parent):
                obj.get(parent).setdefault('children', [])
                p_children = obj.get(parent).get('children')
                p_children + _buildtree(order=order.get(parent),
                                        episode_order=episode_order,
                                        episode_data=episode_data,
                                        date_field=date_field,
                                        parent=parent,
                                        obj=p_children,
                                        max_date_obj=obj.get(parent))
    elif isinstance(order, list):
        for child in order:
            obj.append({child: {'data': episode_data.get(child)}})
            child_date = datetime.strptime(e.get(child).get(date_field), time_format)
            if child_date > max_date_obj.get('max_date'):
                max_date_obj['max_date'] = child_date
            if child in episode_order:
                idx = obj.index(filter(lambda x: next(k for k, v in x.iteritems()) == child, obj)[0])
                obj[idx].get(child).setdefault('children', [])
                c_children = obj[idx].get(child).get('children')
                c_children + _buildtree(order=episode_order.get(child),
                                        episode_order=episode_order,
                                        episode_data=episode_data,
                                        date_field=date_field,
                                        parent=child,
                                        obj=c_children,
                                        max_date_obj=max_date_obj)
	
	return obj

def _getEpisodeHierarchy(episode_order, episode_data):
    parents = episode_order.keys()  
    children = [i for lst in episode_order.values() for i in lst]
    actual_list = {k: episode_order[k] for k in parents if k not in children}
    result = {}
    _buildtree(actual_list, episode_order, episode_data, date_field='date', obj=result)

    return dict(sorted(result.items(), key=lambda k: k[1]['max_date'], reverse=True))

d = {5: [6, 4], 6: [7, 8], 1: [2, 5], 9: [10]}
e = {1: {'date': '09/10/2015'},
     2: {'date': '08/10/2014'},
     3: {'date': '08/09/2014'},
     4: {'date': '05/23/2015'},
     5: {'date': '11/15/2015'},
     6: {'date': '06/01/2015'},
     7: {'date': '02/19/2015'},
     8: {'date': '12/31/2014'},
     9: {'date': '12/31/2014'},
    10: {'date': '10/04/2015'}}
d1 = {5: [6, 4], 6: [7]}

print _getEpisodeHierarchy(d, e)
