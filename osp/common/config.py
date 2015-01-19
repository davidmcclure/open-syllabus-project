

import os
import anyconfig


files = [

    # Defaults first.
    os.path.join(os.path.dirname(__file__), 'osp.yml'),

    # Custom configs.
    '/etc/osp/osp.yml',
    '~/osp.yml',
    './osp.yml'

]

anyconfig.set_loglevel('WARNING')

config = anyconfig.load(
    files,
    merge=anyconfig.MS_DICTS,
    ignore_missing=True
)
