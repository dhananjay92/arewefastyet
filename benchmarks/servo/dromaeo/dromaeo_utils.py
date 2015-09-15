# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import ConfigParser
import os

class ConfigState:
    def __init__(self):
        self.inited = False
        self.rawConfig = None
        self.Port = None
        self.ResultsDir = None

    def init(self, name):
        self.rawConfig = ConfigParser.RawConfigParser()
        if not os.path.isfile(name):
            raise Exception('could not find file: ' + name)
        self.rawConfig.read(name)
        self.inited = True

        self.Port = int(self.get('server_config', 'port'))
        self.ResultsDir = self.get('server_config', 'results_dir')

    def get(self, section, name):
        assert self.inited
        return self.rawConfig.get(section, name)

config = ConfigState()