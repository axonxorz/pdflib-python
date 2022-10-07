import inspect
from functools import wraps

try:
    from .pdflib_py import *
except ImportError as exc:
    raise ImportError('Could not load pdflib_py shared library') from exc


def wrap_optlist(fn):
    """Wraps functions that accept an optlist. If the incoming
    optlist is a dict, parse it down to native format"""
    argspec = inspect.getargspec(fn)
    idx = argspec.args.index('optlist')
    @wraps(fn)
    def new_fn(*args, **kwargs):
        try:
            if isinstance(args[idx], dict):
                args = list(args)
                args[idx] = PDFlib.parse_optlist(args[idx])
        except IndexError:
            # No optlist to speak of
            pass
        return fn(*args, **kwargs)
    return new_fn


class PDFlib:

    _fonts = None
    _debug = False

    # Warning: this is most likely incorrect after save()/restore() calls
    _font_size = 0

    def __init__(self):
        self.__p = None
        self.__p = PDF_new()
        if self.__p:
            PDF_set_option(self.__p, "objorient=true")
        self._fonts = {}

    def debug(self, val):
        self._debug = val

    @classmethod
    def parse_optlist(cls, optlist):
        out = []
        for k, v in optlist.items():
            v = cls._coerce_value(v)
            out.append('%s=%s' % (k, v))
        return ' '.join(out)

    @classmethod
    def _coerce_value(cls, v):
        if v is True or v is False:
            v = cls._coerce_bool(v)
        elif isinstance(v, (list,tuple)):
            v = cls._coerce_list(v)
        elif isinstance(v, (float, int)): # This is probably naive
            v = str(v)
        elif isinstance(v, str):
            pass
        else:
            raise TypeError('_coerce_value cant convert type %s' % type(v))
        return v

    @classmethod
    def _coerce_list(cls, l):
        v = []
        for value in l:
            v.append(cls._coerce_value(value))
        return '{' + ' '.join(v) + '}'

    @classmethod
    def _coerce_bool(cls, b):
        return str(b).lower()

    def boxdebug(self, optlist):
        if self._debug:
            if 'boxsize' in optlist:
                optlist += ' showborder=true'
        return optlist

    # it is recommended not to use __del__ as it is not guaranteed
    # when this will be executed (see Python Esential Reference Page 94).
    # so we also implement a delete method and invalidate self.__p
    # whenever this will be called.
    def __del__(self):
        if (self.__p):
            PDF_delete(self.__p)

    def delete(self):
        if (self.__p):
            PDF_delete(self.__p)
        self.__p = 0

    @wrap_optlist
    def add_nameddest(self, name, optlist=''):
        PDF_add_nameddest(self.__p, name, optlist)

    @wrap_optlist
    def add_path_point(self, path, x, y, type, optlist=''):
        return PDF_add_path_point(self.__p, path, x, y, type, optlist)

    @wrap_optlist
    def add_portfolio_file(self, folder, filename, optlist=''):
        return PDF_add_portfolio_file(self.__p, folder, filename, optlist)

    @wrap_optlist
    def add_portfolio_folder(self, parent, foldername, optlist=''):
        return PDF_add_portfolio_folder(self.__p, parent, foldername, optlist)

    @wrap_optlist
    def add_table_cell(self, table, column, row, text, optlist=''):
        return PDF_add_table_cell(self.__p, table, column, row, text, optlist)

    @wrap_optlist
    def add_textflow(self, textflow, text, optlist=''):
        return PDF_add_textflow(self.__p, textflow, text, optlist)

    def align(self, dx, dy):
        PDF_align(self.__p, dx, dy)

    def arc(self, x, y, r, alpha, beta):
        PDF_arc(self.__p, x, y, r, alpha, beta)

    def arcn(self, x, y, r, alpha, beta):
        PDF_arcn(self.__p, x, y, r, alpha, beta)

    @wrap_optlist
    def begin_document(self, filename, optlist=''):
        return PDF_begin_document(self.__p, filename, optlist)

    @wrap_optlist
    def begin_dpart(self, optlist=''):
        PDF_begin_dpart(self.__p, optlist)

    @wrap_optlist
    def begin_item(self, tagname, optlist=''):
        return PDF_begin_item(self.__p, tagname, optlist)

    def begin_layer(self, layer):
        PDF_begin_layer(self.__p, layer)

    @wrap_optlist
    def begin_mc(self, tagname, optlist=''):
        PDF_begin_mc(self.__p, tagname, optlist)

    @wrap_optlist
    def begin_page_ext(self, width, height, optlist=''):
        PDF_begin_page_ext(self.__p, width, height, optlist)

    @wrap_optlist
    def begin_pattern_ext(self, width, height, optlist=''):
        return PDF_begin_pattern_ext(self.__p, width, height, optlist)

    @wrap_optlist
    def begin_template_ext(self, width, height, optlist=''):
        return PDF_begin_template_ext(self.__p, width, height, optlist)

    def circle(self, x, y, r):
        PDF_circle(self.__p, x, y, r)

    def circular_arc(self, x1, y1, x2, y2):
        PDF_circular_arc(self.__p, x1, y1, x2, y2)

    def clip(self):
        PDF_clip(self.__p)

    def close(self):
        PDF_close(self.__p)

    def close_font(self, font):
        PDF_close_font(self.__p, font)

    def close_graphics(self, graphics):
        PDF_close_graphics(self.__p, graphics)

    def close_image(self, image):
        PDF_close_image(self.__p, image)

    def close_pdi_document(self, doc):
        PDF_close_pdi_document(self.__p, doc)

    def close_pdi_page(self, page):
        PDF_close_pdi_page(self.__p, page)

    def closepath(self):
        PDF_closepath(self.__p)

    def closepath_fill_stroke(self):
        PDF_closepath_fill_stroke(self.__p)

    def closepath_stroke(self):
        PDF_closepath_stroke(self.__p)

    def concat(self, a, b, c, d, e, f):
        PDF_concat(self.__p, a, b, c, d, e, f)

    def continue_text(self, text):
        PDF_continue_text(self.__p, text)

    @wrap_optlist

    @wrap_optlist

    @wrap_optlist
    def create_action(self, type, optlist=''):
        return PDF_create_action(self.__p, type, optlist)

    @wrap_optlist
    def create_annotation(self, llx, lly, urx, ury, type, optlist=''):
        PDF_create_annotation(self.__p, llx, lly, urx, ury, type, optlist)

    @wrap_optlist
    def create_bookmark(self, text, optlist=''):
        return PDF_create_bookmark(self.__p, text, optlist)

    @wrap_optlist
    def create_field(self, llx, lly, urx, ury, name, type, optlist=''):
        PDF_create_field(self.__p, llx, lly, urx, ury, name, type, optlist)

    @wrap_optlist
    def create_fieldgroup(self, name, optlist=''):
        PDF_create_fieldgroup(self.__p, name, optlist)

    @wrap_optlist
    def create_gstate(self, optlist=''):
        return PDF_create_gstate(self.__p, optlist)

    @wrap_optlist
    def create_pvf(self, filename, data, optlist=''):
        PDF_create_pvf(self.__p, filename, data, optlist)

    @wrap_optlist
    def create_textflow(self, text, optlist=''):
        return PDF_create_textflow(self.__p, text, optlist)

    def curveto(self, x1, y1, x2, y2, x3, y3):
        PDF_curveto(self.__p, x1, y1, x2, y2, x3, y3)

    @wrap_optlist
    def define_layer(self, name, optlist=''):
        return PDF_define_layer(self.__p, name, optlist)

    def delete_path(self, path):
        PDF_delete_path(self.__p, path)

    def delete_pvf(self, filename):
        return PDF_delete_pvf(self.__p, filename)

    def delete_table(self, table, optlist):
        PDF_delete_table(self.__p, table, optlist)

    def delete_textflow(self, textflow):
        PDF_delete_textflow(self.__p, textflow)

    @wrap_optlist
    def draw_path(self, path, x, y, optlist=''):
        PDF_draw_path(self.__p, path, x, y, optlist)

    def ellipse(self, x, y, rx, ry):
        PDF_ellipse(self.__p, x, y, rx, ry)

    @wrap_optlist
    def elliptical_arc(self, x, y, rx, ry, optlist=''):
        PDF_elliptical_arc(self.__p, x, y, rx, ry, optlist)

    @wrap_optlist
    def end_document(self, optlist=''):
        PDF_end_document(self.__p, optlist)

    @wrap_optlist
    def end_dpart(self, optlist=''):
        PDF_end_dpart(self.__p, optlist)

    def end_item(self, id):
        PDF_end_item(self.__p, id)

    def end_layer(self):
        PDF_end_layer(self.__p)

    def end_mc(self):
        PDF_end_mc(self.__p)

    @wrap_optlist
    def end_page_ext(self, optlist=''):
        PDF_end_page_ext(self.__p, optlist)

    def end_pattern(self):
        PDF_end_pattern(self.__p)

    def end_template_ext(self, width, height):
        PDF_end_template_ext(self.__p, width, height)

    def endpath(self):
        PDF_endpath(self.__p)

    def fill(self):
        PDF_fill(self.__p)

    def fill_stroke(self):
        PDF_fill_stroke(self.__p)

    @wrap_optlist
    def fit_graphics(self, graphics, x, y, optlist=''):
        PDF_fit_graphics(self.__p, graphics, x, y, optlist)

    @wrap_optlist
    def fit_image(self, image, x, y, optlist=''):
        PDF_fit_image(self.__p, image, x, y, optlist)

    @wrap_optlist
    def fit_pdi_page(self, page, x, y, optlist=''):
        PDF_fit_pdi_page(self.__p, page, x, y, optlist)

    @wrap_optlist
    def fit_table(self, table, llx, lly, urx, ury, optlist=''):
        return PDF_fit_table(self.__p, table, llx, lly, urx, ury, optlist)

    @wrap_optlist
    def fit_textflow(self, textflow, llx, lly, urx, ury, optlist=''):
        return PDF_fit_textflow(self.__p, textflow, llx, lly, urx, ury, optlist)

    @wrap_optlist
    def fit_textline(self, text, x, y, optlist=''):
        optlist = self.boxdebug(optlist)
        PDF_fit_textline(self.__p, text, x, y, optlist)

    def get_apiname(self):
        return PDF_get_apiname(self.__p)

    def get_buffer(self):
        return PDF_get_buffer(self.__p)

    def get_errmsg(self):
        return PDF_get_errmsg(self.__p)

    def get_errnum(self):
        return PDF_get_errnum(self.__p)

    @wrap_optlist
    def get_option(self, keyword, optlist=''):
        return PDF_get_option(self.__p, keyword, optlist)

    @wrap_optlist
    def get_string(self, idx, optlist=''):
        return PDF_get_string(self.__p, idx, optlist)

    @wrap_optlist
    def info_font(self, font, keyword, optlist=''):
        return PDF_info_font(self.__p, font, keyword, optlist)

    @wrap_optlist
    def info_graphics(self, graphics, keyword, optlist=''):
        return PDF_info_graphics(self.__p, graphics, keyword, optlist)

    @wrap_optlist
    def info_image(self, image, keyword, optlist=''):
        return PDF_info_image(self.__p, image, keyword, optlist)

    def info_matchbox(self, boxname, num, keyword):
        return PDF_info_matchbox(self.__p, boxname, num, keyword)

    @wrap_optlist
    def info_path(self, path, keyword, optlist=''):
        return PDF_info_path(self.__p, path, keyword, optlist)

    @wrap_optlist
    def info_pdi_page(self, page, keyword, optlist=''):
        return PDF_info_pdi_page(self.__p, page, keyword, optlist)

    def info_pvf(self, filename, keyword):
        return PDF_info_pvf(self.__p, filename, keyword)

    def info_table(self, table, keyword):
        return PDF_info_table(self.__p, table, keyword)

    def info_textflow(self, textflow, keyword):
        return PDF_info_textflow(self.__p, textflow, keyword)

    @wrap_optlist
    def info_textline(self, text, keyword, optlist=''):
        return PDF_info_textline(self.__p, text, keyword, optlist)

    def lineto(self, x, y):
        PDF_lineto(self.__p, x, y)

    @wrap_optlist
    def load_3ddata(self, filename, optlist=''):
        return PDF_load_3ddata(self.__p, filename, optlist)

    @wrap_optlist
    def load_asset(self, type, filename, optlist=''):
        return PDF_load_asset(self.__p, type, filename, optlist)

    @wrap_optlist
    def load_font(self, fontname, encoding, optlist=''):
        return PDF_load_font(self.__p, fontname, encoding, optlist)

    @wrap_optlist
    def register_font(self, fontname, encoding, optlist='', register_as=None):
        font = self.load_font(fontname, encoding, optlist)
        if font == -1 or font is None:
            raise PDFlibException('Could not load font %s (%s)' % (fontname, encoding))
        if register_as is None:
            register_as = fontname
        self._fonts[register_as] = font

    def get_font(self, identifier):
        return self._fonts[identifier]

    def line(self, x1, y1, x2, y2):
        self.moveto(x1, y1)
        self.lineto(x2, y2)
        self.closepath_stroke()

    def use_font(self, identifier, fontsize):
        self.setfont(self.get_font(identifier), fontsize)

    @wrap_optlist
    def load_graphics(self, type, filename, optlist=''):
        return PDF_load_graphics(self.__p, type, filename, optlist)

    @wrap_optlist
    def load_image(self, imagetype, filename, optlist=''):
        return PDF_load_image(self.__p, imagetype, filename, optlist)

    def makespotcolor(self, spotname):
        return PDF_makespotcolor(self.__p, spotname)

    @wrap_optlist
    def mc_point(self, tagname, optlist=''):
        PDF_mc_point(self.__p, tagname, optlist)

    def moveto(self, x, y):
        PDF_moveto(self.__p, x, y)

    @wrap_optlist
    def process_pdi(self, doc, page, optlist=''):
        return PDF_process_pdi(self.__p, doc, page, optlist)

    def rect(self, x, y, width, height):
        PDF_rect(self.__p, x, y, width, height)

    def restore(self):
        PDF_restore(self.__p)

    @wrap_optlist
    def resume_page(self, optlist=''):
        PDF_resume_page(self.__p, optlist)

    def rotate(self, phi):
        PDF_rotate(self.__p, phi)

    def save(self):
        PDF_save(self.__p)

    def scale(self, sx, sy):
        PDF_scale(self.__p, sx, sy)

    @wrap_optlist
    def set_graphics_option(self, optlist=''):
        PDF_set_graphics_option(self.__p, optlist)

    def set_gstate(self, gstate):
        PDF_set_gstate(self.__p, gstate)

    def set_info(self, key, value):
        PDF_set_info(self.__p, key, value)

    @wrap_optlist
    def set_layer_dependency(self, type, optlist=''):
        PDF_set_layer_dependency(self.__p, type, optlist)

    @wrap_optlist
    def set_option(self, optlist=''):
        PDF_set_option(self.__p, optlist)

    @wrap_optlist
    def set_text_option(self, optlist=''):
        PDF_set_text_option(self.__p, optlist)

    def set_text_pos(self, x, y):
        PDF_set_text_pos(self.__p, x, y)

    def setcolor(self, fstype, colorspace, c1, c2, c3, c4):
        PDF_setcolor(self.__p, fstype, colorspace, c1, c2, c3, c4)

    def setfont(self, font, fontsize):
        PDF_setfont(self.__p, font, fontsize)

    def setlinewidth(self, width):
        PDF_setlinewidth(self.__p, width)

    def setmatrix(self, a, b, c, d, e, f):
        PDF_setmatrix(self.__p, a, b, c, d, e, f)

    @wrap_optlist
    def shading(self, type, x0, y0, x1, y1, c1, c2, c3, c4, optlist=''):
        return PDF_shading(self.__p, type, x0, y0, x1, y1, c1, c2, c3, c4, optlist)

    @wrap_optlist
    def shading_pattern(self, shading, optlist=''):
        return PDF_shading_pattern(self.__p, shading, optlist)

    def shfill(self, shading):
        PDF_shfill(self.__p, shading)

    def show(self, text):
        PDF_show(self.__p, text)

    def show_xy(self, text, x, y):
        PDF_show_xy(self.__p, text, x, y)

    def skew(self, alpha, beta):
        PDF_skew(self.__p, alpha, beta)

    def stringwidth(self, text, font, fontsize):
        return PDF_stringwidth(self.__p, text, font, fontsize)

    def stroke(self):
        PDF_stroke(self.__p)

    @wrap_optlist
    def suspend_page(self, optlist=''):
        PDF_suspend_page(self.__p, optlist)

    def translate(self, tx, ty):
        PDF_translate(self.__p, tx, ty)
