import re
import requests

configure = requests.get('https://git.savannah.gnu.org/cgit/readline.git/plain/configure').text
patchlevel = requests.get('https://git.savannah.gnu.org/cgit/readline.git/plain/patchlevel').text

version = re.search(r"PACKAGE_VERSION='([^']+)'", configure).group(1)
patch = int(patchlevel.strip().split('\n')[-1])

print(f'{version}.{patch:03d}')
