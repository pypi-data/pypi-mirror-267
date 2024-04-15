#  Copyright (c) 2022.  Eugene Popov.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from .core.batch import Batch
from .core.meta import MetaData, MetaJSONEncoder
from . import version

# Meta
__version__ = version.version
__author__ = 'Eugene Popov'


import logging
logging.getLogger('witness').addHandler(logging.NullHandler())
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
