# -*- coding: utf-8 -*-

# Storage Settings
# For more information, see app.ext.storage module

# information for files
# Maximum file size: 30Mb default
MAX_FILE_SIZE = 29 * 1024 * 1024

# file extensions allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'txt', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'pdf', 'zip'])

# folder name for gae
DEFAULT_BUCKET = "awesome-bucket-project"
PUBLIC_URI = 'https://storage.googleapis.com'
