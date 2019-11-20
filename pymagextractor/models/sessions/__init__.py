from .follow import Follow
from .tokutei_object import TokuteiObject


# We consider python automatically manage
# to map class to its button name.
ACTIONS = {"Tokutei Object": TokuteiObject,
           "Follow": Follow,}
