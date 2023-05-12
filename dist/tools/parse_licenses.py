# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import collections
import os
import re
import sys
import time

license_dict = {
    "The Apache Software License, Version 2.0": "The Apache Software License, Version 2.0",
    "Apache 2.0": "The Apache Software License, Version 2.0",
    "Apache License, Version 2.0": "The Apache Software License, Version 2.0",
    "Apache License 2.0": "The Apache Software License, Version 2.0",
    "Apache 2": "The Apache Software License, Version 2.0",
    "Apache v2": "The Apache Software License, Version 2.0",
    "Apache-2.0": "The Apache Software License, Version 2.0",
    "ASF 2.0": "The Apache Software License, Version 2.0",
    "Apache License Version 2": "The Apache Software License, Version 2.0",
    "Apache License Version 2.0": "The Apache Software License, Version 2.0",
    "Apache License (v2.0)": "The Apache Software License, Version 2.0",
    "Apache License": "The Apache Software License, Version 2.0",
    "The Apache License, Version 2.0": "The Apache Software License, Version 2.0",
    "Apache 2.0 License": "The Apache Software License, Version 2.0",
    "Apache License, version 2.0": "The Apache Software License, Version 2.0",
    "3-Clause BSD License": "The 3-Clause BSD License",
    "New BSD License": "The 3-Clause BSD License",
    "The New BSD License": "The 3-Clause BSD License",
    "Modified BSD License": "The 3-Clause BSD License",
    "BSD Licence 3": "The 3-Clause BSD License",
    "BSD License 3": "The 3-Clause BSD License",
    "BSD 3-clause": "The 3-Clause BSD License",
    "BSD-3-Clause": "The 3-Clause BSD License",
    "The BSD 3-Clause License": "The 3-Clause BSD License",
    "The 2-Clause BSD License": "The 2-Clause BSD License",
    "BSD 2-Clause License": "The 2-Clause BSD License",
    "Simplified BSD License": "The 2-Clause BSD License",
    "FreeBSD License": "The 2-Clause BSD License",
    "BSD License": "The 2-Clause BSD License",
    "BSD Licence": "The 2-Clause BSD License",
    "BSD": "The 2-Clause BSD License",
    "The BSD License": "The 2-Clause BSD License",
    "The MIT License": "The MIT License",
    "MIT License": "The MIT License",
    "MIT license": "The MIT License",
    "Eclipse Public License 1.0": "Eclipse Public License - v1.0",
    "Eclipse Public License - v 1.0": "Eclipse Public License - v1.0",
    "Eclipse Public License 2.0": "Eclipse Public License - v2.0",
    "GNU General Public License": "GNU General Public License",
    "The GNU General Public License, Version 2": "GNU General Public License, version 2",
    "cc0": "Creative Commons Zero",
    "CC0": "Creative Commons Zero",
    "CDDL + GPLv2 with classpath exception": "CDDL + GPLv2 with classpath exception",
    "CDDL/GPLv2+CE": "CDDL + GPLv2 with classpath exception",
    "Common Development and Distribution License (CDDL) v1.0": "Common Development and Distribution License (CDDL) v1.0",
    "CDDL 1.0": "Common Development and Distribution License (CDDL) v1.0",
    "The JSON License": "The JSON License",
    "CUP License (MIT License)": "CUP License",
    "Eclipse Distribution License - v 1.0": "Eclipse Distribution License - v1.0",
    "EDL 1.0": "Eclipse Distribution License - v1.0",
    "Public Domain": "Public Domain",
}
#########################################################

license_file_dict = {
    "The 3-Clause BSD License": "licenses/LICENSE-BSD-3.txt",
    "The 2-Clause BSD License": "licenses/LICENSE-BSD-2.txt",
    "The MIT License": "licenses/LICENSE-MIT.txt",
    "Eclipse Public License - v1.0": "licenses/LICENSE-EPL-1.0.txt",
    "Eclipse Public License - v2.0": "licenses/LICENSE-EPL-2.0.txt",
    "Eclipse Distribution License - v1.0": "licenses/LICENSE-EDL-1.0.txt",
    "Creative Commons Zero": "licenses/LICENSE-CC0.txt",
    "CDDL + GPLv2 with classpath exception": "licenses/LICENSE-CDDL.txt & licenses/LICENSE-GPLv2-CE.txt",
    "Common Development and Distribution License (CDDL) v1.0": "licenses/LICENSE-CDDL.txt",
    "CUP License": "licenses/LICENSE-CUP.txt",
    "Public Domain": "licenses/LICENSE-PD.txt",
}

class LicenseParser:

    def __init__(self, license_file, out_file):
        self.license_file = license_file
        self.out_file = out_file;
        self.out_dict = {}

    def parse_and_output(self):
        for line in open(self.license_file):
            #print line
            line = line.strip()
            if not len(line) or line.startswith("Lists of"):
                continue
            r = re.search(r'\((.+)\) (.+) \((.+) - (.+)\)', line)
            license_alias = r[1]
            project_name = r[2]
            package_name = r[3]
            url = r[4]

            #print self.convert_to_standard_name(license_alias)
            #print project_name;
            #print package_name;
            #print url

            self.assemble_output(license_alias, project_name, package_name, url);

        self.save_to_file()

    def save_to_file(self):
        with open(self.out_file, 'w') as f:
            sorted_out_dict = collections.OrderedDict(sorted(self.out_dict.items()))
            for license_name in sorted_out_dict.keys():
                license_file_location = license_file_dict.get(license_name, "unknown")
                f.write(f"{license_name} -- {license_file_location}" + "\n")

                sorted_out_dict_2 = collections.OrderedDict(sorted(self.out_dict[license_name].items()))
                for project_name in sorted_out_dict_2.keys():
                    f.write(f"    * {project_name}" + ":\n")
                    sorted_out_dict_3 = sorted(self.out_dict[license_name][project_name])
                    for package in sorted_out_dict_3:
                        f.write(f"        - {package}" + "\n")
                f.write("\n")

    def assemble_output(self, license_alias, project_name, package_name, url):
        standard_name = self.convert_to_standard_name(license_alias);
        if standard_name in self.out_dict:
            if project_name not in self.out_dict[standard_name]:
                self.out_dict[standard_name][project_name] = set()
        else:
            self.out_dict[standard_name] = {project_name: set()}

        self.out_dict[standard_name][project_name].add(f"{package_name} ({url})")

    def convert_to_standard_name(self, alias):
        if alias in license_dict:
            return license_dict[alias]
        license_dict[alias] = alias;
        return alias

def main():
    license_file = sys.argv[1]
    out_file = sys.argv[2]
    license_parser = LicenseParser(license_file, out_file);
    license_parser.parse_and_output();

if __name__ == '__main__':
    main()

