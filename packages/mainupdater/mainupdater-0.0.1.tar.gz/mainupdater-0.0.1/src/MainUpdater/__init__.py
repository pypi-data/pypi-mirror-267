"""
\u0420\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A: MainPlay TG
https://t.me/MainPlay_InfoCh"""

__version_tuple__=(0,0,1)
__depends__={
  "required":[
    "requests",
    ],
  "optional":[
    "progressbar2",
    ],
  }
__scripts__=[
  "MU-updateAll",
  ]
__all__=[]
from .main import *
__all__.sort()
__version__="{}.{}.{}".format(*__version_tuple__)
