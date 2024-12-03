"""
Global settings, where can easily use with
utils.settings.lazy_settings
"""


PRIMARY_KEY_LOOKUP = "id"
PRIMARY_KEY_TYPE_CONVERTER = int
BASE_ENTITY_CLASS_NAME = "BaseEntity"

DATA_STORAGE_FORMAT = "json"
DATA_STORAGE_DIR = "data"
DEFAULT_REPOSITORY = "db.layers.repositories.BaseRepository"
DEFAULT_ORM = "db.orm.MacroFileORM"
