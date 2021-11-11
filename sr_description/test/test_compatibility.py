#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
# Software License Agreement (BSD License)
#
#  Copyright (c) 2021, Bielefeld University
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of Bielefeld University nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
######################################################################

# Author: Robert Haschke <rhaschke@techfak.uni-bielefeld.de>

from __future__ import absolute_import, print_function

import ast
import re
import sys
import os
import unittest
import xacro
import xml.dom
from xml.dom.minidom import parseString
from io import StringIO

try:
    from unittest import subTest
except ImportError:
    # subTest was introduced in 3.4 only. Provide a dummy fallback.
    from contextlib import contextmanager

    @contextmanager
    def subTest(msg):
        print(msg)
        yield None

# regex to match whitespace
whitespace = re.compile(r'\s+')


def text_values_match(a, b):
    # generic comparison
    if whitespace.sub(' ', a).strip() == whitespace.sub(' ', b).strip():
        return True

    try:  # special handling of dicts: ignore order
        a_dict = ast.literal_eval(a)
        b_dict = ast.literal_eval(b)
        if (isinstance(a_dict, dict) and isinstance(b_dict, dict) and a_dict == b_dict):
            return True
    except Exception:  # Attribute values aren't dicts
        pass

    # on failure, try to split a and b at whitespace and compare snippets
    def match_splits(a_, b_):
        if len(a_) != len(b_):
            return False
        for a, b in zip(a_, b_):
            if a == b:
                continue
            try:  # compare numeric values only up to some accuracy
                if abs(float(a) - float(b)) > 1.0e-9:
                    return False
            except ValueError:  # values aren't numeric and not identical
                return False
        return True

    return match_splits(a.split(), b.split())


def all_attributes_match(a, b):
    if len(a.attributes) != len(b.attributes):
        raise AssertionError('Different number of attributes: [{}] != [{}]'.
                             format(', '.join(sorted(a.attributes.keys())),
                                    ', '.join(sorted(b.attributes.keys()))))
    a_atts = a.attributes.items()
    b_atts = b.attributes.items()
    a_atts.sort()
    b_atts.sort()

    for a, b in zip(a_atts, b_atts):
        if a[0] != b[0]:
            raise AssertionError('Different attribute names: %s and %s' % (a[0], b[0]))
        if not text_values_match(a[1], b[1]):
            raise AssertionError('Different attribute values: {}={} and {}={}'.
                                 format(a[0], a[1], b[0], b[1]))
    return True


def text_matches(a, b):
    if text_values_match(a, b):
        return True
    raise AssertionError("Different text values: '%s' and '%s'" % (a, b))


def nodes_match(a, b, ignore_nodes):
    if not a and not b:
        return True
    if not a or not b:
        return False

    if a.nodeType != b.nodeType:
        raise AssertionError('Different node types: %s and %s' % (a, b))

    # compare text-valued nodes
    if a.nodeType in [xml.dom.Node.TEXT_NODE,
                      xml.dom.Node.CDATA_SECTION_NODE,
                      xml.dom.Node.COMMENT_NODE]:
        return text_matches(a.data, b.data)

    # ignore all other nodes except ELEMENTs
    if a.nodeType != xml.dom.Node.ELEMENT_NODE:
        return True

    # compare ELEMENT nodes
    if a.nodeName != b.nodeName:
        raise AssertionError('Different element names: %s and %s' % (a.nodeName, b.nodeName))

    try:
        all_attributes_match(a, b)
    except AssertionError as e:
        raise AssertionError('{err} in node <{node}>'.format(err=str(e), node=a.nodeName))

    a = a.firstChild
    b = b.firstChild
    while a or b:
        # ignore whitespace-only text nodes
        # we could have several text nodes in a row, due to replacements
        while (a and
               ((a.nodeType in ignore_nodes) or
                (a.nodeType == xml.dom.Node.TEXT_NODE and whitespace.sub('', a.data) == ""))):
            a = a.nextSibling
        while (b and
               ((b.nodeType in ignore_nodes) or
                (b.nodeType == xml.dom.Node.TEXT_NODE and whitespace.sub('', b.data) == ""))):
            b = b.nextSibling

        nodes_match(a, b, ignore_nodes)

        if a:
            a = a.nextSibling
        if b:
            b = b.nextSibling

    return True


def xml_matches(a, b, ignore_nodes=[]):
    if isinstance(a, str):
        return xml_matches(parseString(a).documentElement, b, ignore_nodes)
    if isinstance(b, str):
        return xml_matches(a, parseString(b).documentElement, ignore_nodes)
    if a.nodeType == xml.dom.Node.DOCUMENT_NODE:
        return xml_matches(a.documentElement, b, ignore_nodes)
    if b.nodeType == xml.dom.Node.DOCUMENT_NODE:
        return xml_matches(a, b.documentElement, ignore_nodes)

    return nodes_match(a, b, ignore_nodes)


class TestEquality(unittest.TestCase):
    def generate_test_params(self):
        path = os.path.dirname(__file__)
        old_path = os.path.join(path, 'robots.old')
        new_path = os.path.join(path, 'robots.new')

        for name in os.listdir(old_path):
            old_file = os.path.join(old_path, name)
            new_file = os.path.join(new_path, name)

            if name.endswith('.urdf.xacro') and os.path.isfile(old_file) and os.path.isfile(new_file):
                yield name, old_file, new_file

    def save_results(self, name, doc):
        with open(name, 'w') as f:
            f.write(doc.toprettyxml(indent='  '))

    def test_files(self):
        def process(filename):
            return xacro.process_file(filename)

        results_dir = None
        for name, old_file, new_file in self.generate_test_params():
            with subTest(msg='Checking {}'.format(name)):
                try:
                    old_doc = process(old_file)
                    new_doc = process(new_file)
                    xml_matches(old_doc, new_doc, ignore_nodes=[xml.dom.Node.COMMENT_NODE])
                except AssertionError:
                    if results_dir is None:
                        import tempfile
                        results_dir = tempfile.mkdtemp(prefix='sr_compat')
                        print('Saving mismatching URDFs to:', results_dir)

                    for suffix, doc in zip(['.old', '.new'], [old_doc, new_doc]):
                        self.save_results(os.path.join(results_dir, name + suffix), doc)

                    raise
                except Exception as e:
                    msg = str(e) or repr(e)
                    xacro.error(msg)
                    xacro.print_location()
                    raise


if __name__ == '__main__':
    unittest.main()
