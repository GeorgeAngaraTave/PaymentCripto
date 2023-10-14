try:
    from .google_storage import StorageFile
except ImportError as e:
    import logging as log
    log.warning('Warning: by using custom_storage')
    from .custom_storage import StorageFile
