#!/usr/bin/env python
"""
Thierry Bertin-Mahieux (2012) Columbia University
tb2332@columbia.edu

Code to validate a submission file for the Million Song Dataset
Challenge on Kaggle. Requires an internet connection.
This code is developed under python 2.7 (Ubuntu machine).

Copyright 2012, Thierry Bertin-Mahieux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'Thierry Bertin-Mahieux <tb2332@columbia.edu>'
__date__ = 'Sun Mar 11 18:39:03 EDT 2012'


import os
import sys
import time
import urllib2
import numpy as np


# Number of predicted songs required per user.
CUTOFF = 2000


# Canonical list of users for the contest, there should be predictions for
# each user, one user per line, users are in the same order as in this file.
CANONICAL_USER_LIST = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/challenge/canonical/kaggle_users.txt'

# Canonical list of songs and their integer index.
CANONICAL_SONG_LIST = 'http://labrosa.ee.columbia.edu/millionsong/sites/default/files/challenge/canonical/kaggle_songs.txt'




def load_list_from_the_web(url):
    """Grab a text file, return each line in a list."""
    print '---retrieveing url %s...' % url
    t1 = time.time()
    stream = urllib2.urlopen(url)
    data = [line.strip() for line in stream.readlines()]
    stream.close()
    print '    DONE! It took %d seconds.' % int(time.time() - t1)
    return data


def print_error_message(msg, line_num=None):
    """Formatted error message."""
    prefix = 'ERROR! '
    if line_num:
        prefix += '[line %d] ' % line_num
    print '%s%s' % (prefix, msg)


def validate_one_line(line, line_num, min_max_song_indexes):
    """Make sure an individual line looks valid, return True if so."""
    is_valid = True
    # Line too small or empty?
    if len(line) < 80:
        print_error_message("Line too short! (%d characters)" % len(line),
                            line_num)
        is_valid = False
    parts = line.split(' ')
    # Not the right number of items per line?
    if len(parts) != CUTOFF + 1:
        msg = "Line should have %d one-space-separated elements, " % (CUTOFF + 1, )
        msg += "found %d" % len(parts)
        print_error_message(msg, line_num)
        is_valid = False
    # First item is not a proper user ID?
    if len(parts[0]) != 40:
        msg = "First line item should be a 40-character user id, "
        msg += "found: %s" % parts[0][:50]
        print_error_message(msg, line_num)
        is_valid = False
    # TODO check if songs are integers
    # TODO check if there are duplicate songs
    # TODO check song indexes
    return is_valid


def validate_user_list(canonical_list, seen_list):
    """Validate that we saw the right users, in order."""
    is_valid = True
    if len(canonical_list) != len(seen_list):
        msg = 'Predictions made for %d users, ' % len(seen_list)
        msg += 'there should be %d users.' % len(canonical_list)
        print_error_message(msg)
        is_valid = False
    for k in xrange(min(len(canonical_list), len(seen_list))):
        u1 = canonical_list[k]
        u2 = seen_list[k]
        if u1 != u2:
            msg = 'Expected user \'%s\', got user \'%s\'.' % (u1, u2)
            is_valid = False
            break
    return is_valid



def die_with_usage():
    """Help menu."""
    print 'MSD CHallenge: script to validate your submission to Kaggle.'
    print '------------------------------------------------------------'
    print ''
    print 'python validate_submission.py <submission file>'
    print ''
    print 'ARGS'
    print '   <submission file>   File to be uploaded to Kaggle.'
    sys.exit(0)


if __name__ == '__main__':

    # Display the help menu and quit?
    help_keywords = ('help', '-help', '--help')
    if len(sys.argv) < 2 or sys.argv[1].lower() in help_keywords:
        die_with_usage()

    # Sanity check on the file.
    submission_filename = sys.argv[1]
    if not os.path.isfile(submission_filename):
        print 'ERROR: file %s does not exist.' % submission_filename
        die_with_usage()

    # Fetch data files.
    users = load_list_from_the_web(CANONICAL_USER_LIST)
    songs_and_indexes = load_list_from_the_web(CANONICAL_SONG_LIST)

    # Extract indexes from the list of songs.
    indexes = [int(line.split(' ')[1]) for line in songs_and_indexes]
    min_index = min(indexes)
    max_index = max(indexes)
    msg_song_file_prob = 'Problem with the online song file, aborting.'
    assert min_index > 0, msg_song_file_prob
    assert max_index == len(indexes), msg_song_file_prob
    min_max_index = (min, max)

    # Keep stats
    is_valid = True
    users_seen = []

    # Go through each line, validates it, keep some stats.
    line_num = 0
    f = open(submission_filename, 'r')
    for line in f.xreadlines():
        line_num += 1
        is_valid = validate_one_line(line.strip(), line_num, min_max_index)
        if not is_valid:
            sys.exit(0)
        users_seen.append(line.split(' ')[0])



    is_valid = validate_user_list(users, users_seen)
    if not is_valid:
        sys.exit(0)


    # Final message.
    if is_valid:
        print '***************************************'
        print 'Awesome, your submission is good to go!'
        sys.exit(0)
