def uniq(iterable, /, *, lazy=False):
    return gen_uniq(iterable) if lazy else list(gen_uniq)

def gen_uniq(iterable, /, *):
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item
