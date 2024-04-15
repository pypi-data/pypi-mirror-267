
#  Copyright (c) 2023.  Eugene Popov.
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


from witness.core.abstract import AbstractSerializer
import json
import datetime


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)


class JsonSerializer(AbstractSerializer):

    def to_batch(self, raw, *args, **kwargs):
        data = raw.json()
        return data

    def from_batch(self, data, *args, **kwargs):
        raw = json.dumps(data, cls=CustomJSONEncoder)
        return raw

