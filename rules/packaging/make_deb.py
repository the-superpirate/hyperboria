# Copyright 2015 The Bazel Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A simple cross-platform helper to create a debian package."""

import gzip
import hashlib
import os.path
import sys
import tarfile
import textwrap
import time
from io import BytesIO

import gflags

# list of debian fields : (name, mandatory, wrap[, default])
# see http://www.debian.org/doc/debian-policy/ch-controlfields.html
DEBIAN_FIELDS = [
    ('Package', True, False),
    ('Version', True, False),
    ('Section', False, False, 'contrib/devel'),
    ('Priority', False, False, 'optional'),
    ('Architecture', False, False, 'all'),
    ('Depends', False, True, []),
    ('Recommends', False, True, []),
    ('Replaces', False, True, []),
    ('Suggests', False, True, []),
    ('Enhances', False, True, []),
    ('Conflicts', False, True, []),
    ('Pre-Depends', False, True, []),
    ('Installed-Size', False, False),
    ('Maintainer', True, False),
    ('Description', True, True),
    ('Homepage', False, False),
    ('Built-Using', False, False, 'Bazel'),
    ('Distribution', False, False, 'unstable'),
    ('Urgency', False, False, 'medium'),
]

gflags.DEFINE_string('output', None, 'The output file, mandatory')
gflags.MarkFlagAsRequired('output')

gflags.DEFINE_string('changes', None, 'The changes output file, mandatory.')
gflags.MarkFlagAsRequired('changes')

gflags.DEFINE_string('data', None,
                     'Path to the data tarball, mandatory')
gflags.MarkFlagAsRequired('data')

gflags.DEFINE_string('preinst', None,
                     'The preinst script (prefix with @ to provide a path).')
gflags.DEFINE_string('postinst', None,
                     'The postinst script (prefix with @ to provide a path).')
gflags.DEFINE_string('prerm', None,
                     'The prerm script (prefix with @ to provide a path).')
gflags.DEFINE_string('postrm', None,
                     'The postrm script (prefix with @ to provide a path).')


# see
# https://www.debian.org/doc/manuals/debian-faq/ch-pkg_basics.en.html#s-conffile
gflags.DEFINE_multistring(
    'conffile', None,
    'List of conffiles (prefix item with @ to provide a path)'
)


def make_gflags():
    for field in DEBIAN_FIELDS:
        fieldname = field[0].replace('-', '_').lower()
        msg = 'The value for the %s content header entry.' % field[0]
        if len(field) > 3:
            if type(field[3]) is list:
                gflags.DEFINE_multistring(fieldname, field[3], msg)
            else:
                gflags.DEFINE_string(fieldname, field[3], msg)
        else:
            gflags.DEFINE_string(fieldname, None, msg)
        if field[1]:
            gflags.MarkFlagAsRequired(fieldname)


def add_ar_file_entry(fileobj, filename,
                      content='', timestamp=0,
                      owner_id=0, group_id=0, mode=0o644):
    """Add a AR file entry to fileobj."""
    inputs = [
        (filename + '/').ljust(16),  # filename (SysV)
        str(timestamp).ljust(12),  # timestamp
        str(owner_id).ljust(6),  # owner id
        str(group_id).ljust(6),  # group id
        format(mode, 'o').ljust(8),  # mode
        str(len(content)).ljust(10),  # size
        '\x60\x0a',  # end of file entry
    ]
    for i in inputs:
        fileobj.write(i.encode('ascii'))
    fileobj.write(content)
    if len(content) % 2 != 0:
        fileobj.write(b'\n')  # 2-byte alignment padding


def make_debian_control_field(name, value, wrap=False):
    """Add a field to a debian control file."""
    result = name + ': '
    if type(value) is list:
        value = ', '.join(value)
    if wrap:
        result += ' '.join(value.split('\n'))
        result = textwrap.fill(result,
                               break_on_hyphens=False,
                               break_long_words=False)
    else:
        result += value
    return result.replace('\n', '\n ') + '\n'


def create_deb_control(extra_files=None, **kwargs):
    """Create the control.tar.gz file."""
    # create the control file
    controlfile = ''
    for values in DEBIAN_FIELDS:
        fieldname = values[0]
        key = fieldname[0].lower() + fieldname[1:].replace('-', '')
        if values[1] or (key in kwargs and kwargs[key]):
            controlfile += make_debian_control_field(fieldname, kwargs[key], values[2])
    # Create the control.tar file
    tar = BytesIO()
    with gzip.GzipFile('control.tar.gz', mode='w', fileobj=tar, mtime=0) as gz:
        with tarfile.open('control.tar.gz', mode='w', fileobj=gz) as f:
            tarinfo = tarfile.TarInfo('control')
            tarinfo.size = len(controlfile)
            f.addfile(tarinfo, fileobj=BytesIO(controlfile.encode('utf-8')))
            if extra_files:
                for name, (data, mode) in extra_files.items():
                    tarinfo = tarfile.TarInfo(name)
                    tarinfo.size = len(data)
                    tarinfo.mode = mode
                    f.addfile(tarinfo, fileobj=BytesIO(data.encode('utf-8')))
    control = tar.getvalue()
    tar.close()
    return control


def create_deb(output,
               data,
               preinst=None,
               postinst=None,
               prerm=None,
               postrm=None,
               conffiles=None,
               **kwargs):
    """Create a full debian package."""
    extrafiles = {}
    if preinst:
        extrafiles['preinst'] = (preinst, 0o755)
    if postinst:
        extrafiles['postinst'] = (postinst, 0o755)
    if prerm:
        extrafiles['prerm'] = (prerm, 0o755)
    if postrm:
        extrafiles['postrm'] = (postrm, 0o755)
    if conffiles:
        extrafiles['conffiles'] = ('\n'.join(conffiles), 0o644)
    control = create_deb_control(extra_files=extrafiles, **kwargs)

    # Write the final AR archive (the deb package)
    with open(output, 'wb') as f:
        f.write(b'!<arch>\n')  # Magic AR header
        add_ar_file_entry(f, 'debian-binary', b'2.0\n')
        add_ar_file_entry(f, 'control.tar.gz', control)
        # Tries to preserve the extension name
        ext = os.path.basename(data).split('.')[-2:]
        if len(ext) < 2:
            ext = 'tar'
        elif ext[1] == 'tgz':
            ext = 'tar.gz'
        elif ext[1] == 'tar.bzip2':
            ext = 'tar.bz2'
        else:
            ext = '.'.join(ext)
            if ext not in ['tar.bz2', 'tar.gz', 'tar.xz', 'tar.lzma']:
                ext = 'tar'
        with open(data, 'rb') as datafile:
            data = datafile.read()
        add_ar_file_entry(f, 'data.' + ext, data)


def get_checksums_from_file(filename, hash_fns=None):
    """Computes MD5 and/or other checksums of a file.

    Args:
      filename: Name of the file.
      hash_fns: Mapping of hash functions.
                Default is {'md5': hashlib.md5}

    Returns:
      Mapping of hash names to hexdigest strings.
      { <hashname>: <hexdigest>, ... }
    """
    hash_fns = hash_fns or {'md5': hashlib.md5}
    checksums = {k: fn() for (k, fn) in hash_fns.items()}

    with open(filename, 'rb') as file_handle:
        while True:
            buf = file_handle.read(1048576)  # 1 MiB
            if not buf:
                break
            for hashfn in checksums.values():
                hashfn.update(buf)

    return {k: fn.hexdigest() for (k, fn) in checksums.items()}


def create_changes(output,
                   deb_file,
                   architecture,
                   short_description,
                   maintainer,
                   package,
                   version,
                   section,
                   priority,
                   distribution,
                   urgency,
                   timestamp=0):
    """Create the changes file."""
    checksums = get_checksums_from_file(
        deb_file, {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
        },
    )
    debsize = str(os.path.getsize(deb_file))
    deb_basename = os.path.basename(deb_file)

    changesdata = ''.join(
        (make_debian_control_field(*x) for x in [
            ('Format', '1.8'),
            ('Date', time.ctime(timestamp)),
            ('Source', package),
            ('Binary', package),
            ('Architecture', architecture),
            ('Version', version),
            ('Distribution', distribution),
            ('Urgency', urgency),
            ('Maintainer', maintainer),
            ('Changed-By', maintainer),
            ('Description', '\n%s - %s' % (package, short_description)),
            ('Changes', '\n%s (%s) %s; urgency=%s\nChanges are tracked in revision control.' % (
                package, version, distribution, urgency
            )),
            ('Files', '\n' + ' '.join([checksums['md5'], debsize, section, priority, deb_basename])),
            ('Checksums-Sha1', '\n' + ' '.join([checksums['sha1'], debsize, deb_basename])),
            ('Checksums-Sha256', '\n' + ' '.join([checksums['sha256'], debsize, deb_basename])),
        ]),
    )
    with open(output, 'w') as changes_fh:
        changes_fh.write(changesdata)


def get_flag_value(flagvalue, strip=True):
    if flagvalue:
        if flagvalue[0] == '@':
            with open(flagvalue[1:], 'r') as f:
                flagvalue = f.read()
        if strip:
            return flagvalue.strip()
    return flagvalue


def get_flag_values(flagvalues):
    if flagvalues:
        return [get_flag_value(f, False) for f in flagvalues]
    else:
        return None


def main(unused_argv):
    create_deb(
        FLAGS.output,
        FLAGS.data,
        preinst=get_flag_value(FLAGS.preinst, False),
        postinst=get_flag_value(FLAGS.postinst, False),
        prerm=get_flag_value(FLAGS.prerm, False),
        postrm=get_flag_value(FLAGS.postrm, False),
        conffiles=get_flag_values(FLAGS.conffile),
        package=FLAGS.package,
        version=get_flag_value(FLAGS.version),
        description=get_flag_value(FLAGS.description),
        maintainer=FLAGS.maintainer,
        section=FLAGS.section,
        architecture=FLAGS.architecture,
        depends=FLAGS.depends,
        suggests=FLAGS.suggests,
        enhances=FLAGS.enhances,
        pre_depends=FLAGS.pre_depends,
        recommends=FLAGS.recommends,
        replaces=FLAGS.replaces,
        homepage=FLAGS.homepage,
        built_using=get_flag_value(FLAGS.built_using),
        priority=FLAGS.priority,
        conflicts=FLAGS.conflicts,
        installed_size=get_flag_value(FLAGS.installed_size)
    )
    create_changes(
        output=FLAGS.changes,
        deb_file=FLAGS.output,
        architecture=FLAGS.architecture,
        short_description=get_flag_value(FLAGS.description).split('\n')[0],
        maintainer=FLAGS.maintainer, package=FLAGS.package,
        version=get_flag_value(FLAGS.version), section=FLAGS.section,
        priority=FLAGS.priority, distribution=FLAGS.distribution,
        urgency=FLAGS.urgency
    )


if __name__ == '__main__':
    make_gflags()
    FLAGS = gflags.FLAGS
    main(FLAGS(sys.argv))
