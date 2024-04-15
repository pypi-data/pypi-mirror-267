#
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

__all__ = ['version']

try:
    import importlib_metadata as metadata
except ImportError:
    from importlib import metadata  # type: ignore[no-redef]

try:
    version = metadata.version('witness-etl')
except metadata.PackageNotFoundError:
    import logging
    version = '0.0.9'


del metadata

if __name__ == '__main__':
    print(version)
