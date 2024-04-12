A few caching data structures and other lossy things with capped sizes.

*Latest release 20240412*:
* New CachingMapping, a caching front end for another mapping.
* LRU_Cache: add keys() and items().

## Class `CachingMapping(cs.resources.MultiOpenMixin, collections.abc.MutableMapping)`

A caching front end for another mapping.
This is intended as a generic superclass for a proxy to a
slower mapping such as a database or remote key value store.

Note that this subclasses `MultiOpenMixin` to start/stop the worker `Thread`.
Users must enclose use of a `CachingMapping` in a `with` statement.
If subclasses also subclass `MultiOpenMixin` their `startup_shutdown`
method needs to also call our `startup_shutdown` method.

Example:

    class Store:
      """ A key value store with a slower backend.
      """
      def __init__(self, mapping:Mapping):
        self.mapping = CachingMapping(mapping)

    .....
    S = Store(slow_mapping)
    with S:
      ... work with S ...

*Method `CachingMapping.__init__(self, mapping: Mapping, *, max_size=1024, queue_length=1024, delitem_bg: Optional[Callable[[Any], cs.result.Result]] = None, setitem_bg: Optional[Callable[[Any, Any], cs.result.Result]] = None, missing_fallthrough: bool = False)`*:
Initialise the cache.

Parameters:
* `mapping`: the backing store, a mapping
* `max_size`: optional maximum size for the cache, default 1024
* `queue_length`: option size for the queue to the worker, default 1024
* `delitem_bg`: optional callable to queue a delete of a
  key in the backing store; if unset then deleted are
  serialised in the worker thread
* `setitem_bg`: optional callable to queue setting the value
  for a key in the backing store; if unset then deleted are
  serialised in the worker thread
* `missing_fallthrough`: is true (default `False`) always
  fall back to the backing mapping if a key is not in the cache

*Method `CachingMapping.flush(self)`*:
Wait for outstanding requests in the queue to complete.
Return the UNIX time of completion.

*Method `CachingMapping.items(self)`*:
Generator yielding `(k,v)` pairs.

*Method `CachingMapping.keys(self)`*:
Generator yielding the keys.

## Class `LRU_Cache`

A simple least recently used cache.

Unlike `functools.lru_cache`
this provides `on_add` and `on_remove` callbacks.

*Method `LRU_Cache.__init__(self, max_size, *, on_add=None, on_remove=None)`*:
Initialise the LRU_Cache with maximum size `max`,
additon callback `on_add` and removal callback `on_remove`.

*Method `LRU_Cache.__delitem__(self, key)`*:
Delete the specified `key`, calling the on_remove callback.

*Method `LRU_Cache.__setitem__(self, key, value)`*:
Store the item in the cache. Prune if necessary.

*Method `LRU_Cache.flush(self)`*:
Clear the cache.

*Method `LRU_Cache.get(self, key, default=None)`*:
Mapping method: get value for `key` or `default`.

*Method `LRU_Cache.items(self)`*:
Items from the cache.

*Method `LRU_Cache.keys(self)`*:
Keys from the cache.

## Function `lru_cache(max_size=None, cache=None, on_add=None, on_remove=None)`

Enhanced workalike of @functools.lru_cache.

# Release Log



*Release 20240412*:
* New CachingMapping, a caching front end for another mapping.
* LRU_Cache: add keys() and items().

*Release 20181228*:
Initial PyPI release.
