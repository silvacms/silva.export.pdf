# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 Infrae. All rights reserved.
# See also LICENSE.txt

import logging
import shutil
import tempfile
import fnmatch
import re
import os

from cStringIO import StringIO
from zope.component import getAdapter
from silva.core.interfaces import IPublishable, IContentExporter
from zipfile import ZipFile, ZIP_DEFLATED
from zope.interface import Interface
from five import grok
from xhtml2pdf import pisa


logger = logging.getLogger('silva.export.pdf')


def convert_html_to_pdf(html_file_path, pdf_file_path):
    with open(html_file_path, 'r') as f:
        html_data = f.read()
    os.unlink(html_file_path)

    for link in re.findall('href="(.*?)"', html_data, re.DOTALL):
        if not 'http://' in link and '.html' in link:
            ## We change the local links to be as xhtml2pdf expects,
            ## so it will generate correct "GoToR" syntax for them.
            local_pdf_link = 'pdf:%s' % (link.replace('.html', '.pdf'))
            html_data = html_data.replace(link, local_pdf_link)

    with open(pdf_file_path, "w+b") as pdf:
        pisa.CreatePDF(html_data, dest=pdf, path=pdf_file_path,
                       encoding='UTF-8')

    return pdf_file_path


class IExportOptions(Interface):
    pass


class PDFExporter(grok.Adapter):
    """Export content to HTML.
    """
    grok.provides(IContentExporter)
    grok.context(IPublishable)
    grok.name('pdf')

    name = "PDF (zip)"
    extension = "zip"
    options = IExportOptions

    def export(self, **options):
        output = StringIO()
        archive = ZipFile(output, "w", ZIP_DEFLATED)
        temp_folder = tempfile.mkdtemp()
        logger.info('Creating temp dir: %s' % (temp_folder))
        HTMLEx = getAdapter(self.context, IContentExporter, name='html')
        HTMLEx.export_to_folder(temp_folder, **options)
        for root, dirs, files in os.walk(temp_folder):
            for html_file in fnmatch.filter(files, '*.html'):
                html_file_path = os.path.join(root, html_file)
                pdf_file_name = '%s.pdf' % os.path.splitext(html_file)[0]
                pdf_file_path = os.path.join(root, pdf_file_name)

                archive.write(
                    convert_html_to_pdf(html_file_path, pdf_file_path),
                    os.path.relpath(pdf_file_path, temp_folder))

        archive.close()
        logger.info('Removing temp dir: %s' % (temp_folder))
        shutil.rmtree(temp_folder)

        return output.getvalue()
