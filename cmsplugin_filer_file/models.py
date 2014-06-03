from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import FilerFileField
from cmsplugin_filer_utils import FilerPluginManager
from .conf import settings


class FilerFile(CMSPlugin):
    """
    Plugin for storing any type of file.

    Default template displays download link with icon (if available) and file size.

    This could be updated to use the mimetypes library to determine the type of file rather than
    storing a separate icon for each different extension.

    The icon search is currently performed within get_icon_url; this is probably a performance concern.
    """
    STYLE_CHOICES = settings.CMSPLUGIN_FILER_FILE_STYLE_CHOICES
    DEFAULT_STYLE = settings.CMSPLUGIN_FILER_FILE_DEFAULT_STYLE
    title = models.CharField(_("title"), max_length=255, null=True, blank=True)
    file = FilerFileField(verbose_name=_('file'))
    target_blank = models.BooleanField(_('Open link in new window'), default=False)
    style = models.CharField(
        _('Style'), choices=STYLE_CHOICES, default=DEFAULT_STYLE, max_length=255, blank=True)

    objects = FilerPluginManager(select_related=('file',))

    def get_icon_url(self):
        return self.file.icons['32']

    def file_exists(self):
        return self.file.file.storage.exists(self.file.path)

    def get_file_name(self):
        if self.file.name in ('', None):
            name = u"%s" % (self.file.original_filename,)
        else:
            name = u"%s" % (self.file.name,)
        return name

    def get_ext(self):
        return self.file.extension

    def __unicode__(self):
        if self.title:
            return self.title
        elif self.file:
            # added if, because it raised attribute error when file wasnt defined
            return self.get_file_name()
        return "<empty>"

    search_fields = ('title',)
