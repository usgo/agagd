# local_settings not required, but makes for a friendlier way to set stage
try:
    from local_settings import *
except ImportError:
    pass
