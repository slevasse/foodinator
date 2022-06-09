import dataclasses
from foodClasses import Definitions


@dataclasses.dataclass(frozen=True)
class AppDefaults:
    # logging
    logging_path: str = dataclasses.field(default='application_files/logs/foodinator_log.log')
    logging_format: str = dataclasses.field(default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # setting file
    application_settings_path: str = dataclasses.field(default="application_files/foodinator_settings.json")
    # cookbook
    default_cookbook_name: str = dataclasses.field(default="This is a default name, please change me.")
    default_cookbook_path: str = dataclasses.field(default="cookbooks/my_super_cookbook"
                                                           + Definitions().cookbook_file_extention)
    default_cookbook_folder_path: str = dataclasses.field(default="cookbooks")
    default_cookbook_backup_folder_path: str = dataclasses.field(default="cookbooks_bak")
    default_cookbook_backup_interval: int = dataclasses.field(default=5)
    default_cookbook_backup_history_length: int = dataclasses.field(default=5)
    default_cookbook_autosave_state: bool = dataclasses.field(default=True)
    default_cookbook_backup_state: bool = dataclasses.field(default=True)
