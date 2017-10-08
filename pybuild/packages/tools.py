import shutil

from ..package import Package
from ..util import BASE


class Tools(Package):
    '''
    This is not an actual package. It just copies some handy files into target/
    '''
    version = 'latest'

    skip_uploading = True

    def build(self):
        for f in ('c_rehash.py', 'env.sh', 'import_all.py', 'ssl_test.py'):
            (self.destdir() / 'tools').mkdir(exist_ok=True)
            shutil.copy2(BASE / 'devscripts' / f, self.destdir() / 'tools' / f)
