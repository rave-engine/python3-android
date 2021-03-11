import sys
import os.path

mod_path = os.path.join(
    sys.prefix,
    'lib/python%d.%d/lib-dynload' % (sys.version_info[0], sys.version_info[1]))

for mod_filename in os.listdir(mod_path):
    mod_name = mod_filename.split('.')[0]
    try:
        mod = __import__(mod_name)
    except ImportError as e:
        print(mod_name)
        print(e)
