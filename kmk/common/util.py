def flatten_dict(d):
    items = {}

    for k, v in d.items():
        if isinstance(v, dict):
            items.update(flatten_dict(v))
        else:
            items[k] = v

    return items
