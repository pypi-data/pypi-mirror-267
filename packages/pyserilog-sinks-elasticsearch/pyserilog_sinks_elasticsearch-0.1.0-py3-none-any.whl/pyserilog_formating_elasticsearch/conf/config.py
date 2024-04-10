from .constants import BASE_SANITIZE_FIELD_NAMES


class Config:
    def __init__(self):
        self.stack_trace_frames_limit: int = -1
        self.collect_local_variables: bool = True
        self.source_lines_error_library_frames: int = 5
        self.source_lines_error_app_frames: int = 5
        self.local_var_list_max_length: int = 10
        self.local_var_max_length: int = 200
        self.local_var_dict_max_length: int = 10
        self.include_paths_re = None
        self.exclude_paths_re = None
        self.sanitize_field_names = BASE_SANITIZE_FIELD_NAMES
