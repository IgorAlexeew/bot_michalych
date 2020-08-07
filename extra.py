def get_path():
    sep = '\\' if '\\' in __file__ else '/'
    path_arr = __file__.split(sep)
    path_str = sep.join(path_arr[:-1] + [''])

    return path_str, path_arr, sep
