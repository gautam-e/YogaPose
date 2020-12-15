def get_x(r): return path/'data'/r['fn_col']
def get_y(r): return [r['label']]
import __main__
__main__.get_x = get_x
__main__.get_y = get_y
