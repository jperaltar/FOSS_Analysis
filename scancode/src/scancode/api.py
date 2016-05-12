#
# Copyright (c) 2015 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import print_function, absolute_import

from collections import OrderedDict


"""
Main scanning functions.
Note: this API is unstable and still evolving.
"""

def extract_archives(location, recurse=True):
    """
    Extract recursively any archives found at location and yield an iterable of
    ExtractEvents.
    If verbose is False, only the "done" event is returned at extraction
    completion.
    If verbose is True, both "start" and "done" events are returned.
    """
    from extractcode.extract import extract
    from extractcode import default_kinds

    for xevent in extract(location, kinds=default_kinds, recurse=recurse):
        yield xevent


def get_copyrights(location):
    """
    Yield an iterable of dictionaries of copyright data detected in the file at
    location. Each item contains a list of copyright statements and a start and
    end line.
    """
    finalResults = []

    from scancode.src.cluecode.copyrights import detect_copyrights

    for copyrights, _, _, _, start_line, end_line in detect_copyrights(location):
        if not copyrights:
            continue

        finalResults.append(copyrights)

    return finalResults

DEJACODE_LICENSE_URL = 'https://enterprise.dejacode.com/license_library/Demo/{}/'


def get_licenses(location, index, licenses_by_key):
    """
    Yield an iterable of dictionaries of license data detected in the file at
    location for each detected license.
    """
    from scancode.src.licensedcode.detect import get_license_matches

    results = []
    for match in get_license_matches(location, index):
        for license_key in match.rule.licenses:
            lic = licenses_by_key[license_key]
            result = OrderedDict()
            result['key'] = lic.key
            result['short_name'] = lic.short_name
            result['category'] = lic.category
            result['owner'] = lic.owner
            result['homepage_url'] = lic.homepage_url
            result['text_url'] = lic.text_urls[0] if lic.text_urls else ''
            result['dejacode_url'] = DEJACODE_LICENSE_URL.format(lic.key)
            result['spdx_license_key'] = lic.spdx_license_key
            result['spdx_url'] = lic.spdx_url
            result['start_line'] = match.query_position.start_line
            result['end_line'] = match.query_position.end_line
            results.append(result)

    return results


def get_file_infos(location):
    """
    Return a list of dictionaries of informations collected from the file or
    directory at location.
    """
    from commoncode import fileutils
    from commoncode import filetype
    from commoncode.hash import sha1, md5
    from typecode import contenttype

    T = contenttype.get_type(location)
    is_file = T.is_file
    is_dir = T.is_dir
    infos = OrderedDict()
    infos['type'] = filetype.get_type(location, short=False)
    infos['name'] = fileutils.file_name(location)
    infos['extension'] = is_file and fileutils.file_extension(location) or ''
    infos['date'] = is_file and filetype.get_last_modified_date(location) or None
    infos['size'] = T.size
    infos['sha1'] = is_file and sha1(location) or None
    infos['md5'] = is_file and md5(location) or None
    infos['files_count'] = is_dir and filetype.get_file_count(location) or None
    infos['mime_type'] = is_file and T.mimetype_file or None
    infos['file_type'] = is_file and T.filetype_file or None
    infos['programming_language'] = is_file and T.programming_language or None
    infos['is_binary'] = is_file and T.is_binary or None
    infos['is_text'] = is_file and T.is_text or None
    infos['is_archive'] = is_file and T.is_archive or None
    infos['is_media'] = is_file and T.is_media or None
    infos['is_source'] = is_file and T.is_source or None
    infos['is_script'] = is_file and T.is_script or None
    return [infos]


def get_package_infos(location):
    """
    Return a list of dictionaries of package information
    collected from the location or an empty list.
    """
    from packagedcode.recognize import recognize_packaged_archives
    package = recognize_packaged_archives(location)
    if not package:
        return []
    return [package.as_dict(simple=True)]
