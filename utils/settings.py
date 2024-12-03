from importlib import import_module


class LazySettings:
    """
    Just a s1mple class to load settings from the
    $PROJECT_DIR/config/settings.py file.
    Nothing special here.
    I need to go. Go write more and more docstrings. Uuuuuh
    
    Here was me:
        01000110011000010110101101101000011100100110100101100100011001000110100101101110
    """
    def __getattr__(self, name):
        settings_module = import_module("config.settings")
        attr = getattr(settings_module, name)

        if isinstance(attr, str) and "." in attr:
            module_name, attr_name = attr.rsplit(".", 1)
            try:
                module = import_module(module_name)
                attr = getattr(module, attr_name)
            except ImportError:
                raise AttributeError(f"Module {module_name} not found")
            except (AttributeError, ArithmeticError):
                raise AttributeError(
                    f"Module {module_name} has no attribute {attr_name}"
                )
        return attr


lazy_settings = LazySettings()
