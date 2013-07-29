from functools import wraps
import inspect

try:
    from i386.pdflib_py import *
except ImportError:
    pass

try:
    from x86_64.pdflib_py import *
except ImportError:
    print 'Could not import i386 or x86_64 PDFlib extensions'
    raise

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

class PDFlib(object):

    _p = None
    _fonts = None
    _debug = False

    # Warning: this is most likely incorrect after save()/restore() calls
    _font_size = 0

    def __init__(self):
        self._p = PDF_new()
        self._fonts = {}
        PDF_set_parameter(self._p, "objorient", "true")

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

    def delete(self):
        if (self._p):
            PDF_delete(self._p)
        self._p = None

    def activate_item(self, id):
        PDF_activate_item(self._p, id)

    def add_bookmark(self, text, parent, open):
        return PDF_add_bookmark(self._p, text, parent, open)

    def add_launchlink(self, llx, lly, urx, ury, filename):
        PDF_add_launchlink(self._p, llx, lly, urx, ury, filename)

    @wrap_optlist
    def add_locallink(self, llx, lly, urx, ury, page, optlist=''):
        PDF_add_locallink(self._p, llx, lly, urx, ury, page, optlist)

    @wrap_optlist
    def add_nameddest(self, name, optlist=''):
        PDF_add_nameddest(self._p, name, optlist)

    def add_note(self, llx, lly, urx, ury, contents, title, icon, open):
        PDF_add_note(self._p, llx, lly, urx, ury, contents, title, icon, open)

    @wrap_optlist
    def add_path_point(self, path, x, y, type, optlist=''):
        return PDF_add_path_point(self._p, path, x, y, type, optlist='')

    @wrap_optlist
    def add_pdflink(self, llx, lly, urx, ury, filename, page, optlist=''):
        PDF_add_pdflink(self._p, llx, lly, urx, ury, filename, page, optlist)

    @wrap_optlist
    def add_portfolio_file(self, folder, filename, optlist=''):
        return PDF_add_portfolio_file(self._p, folder, filename, optlist)

    @wrap_optlist
    def add_portfolio_folder(self, parent, foldername, optlist=''):
        return PDF_add_portfolio_folder(self._p, parent, foldername, optlist)

    @wrap_optlist
    def add_table_cell(self, table, column, row, text, optlist=''):
        return PDF_add_table_cell(self._p, table, column, row, text, optlist)

    @wrap_optlist
    def add_textflow(self, textflow, text, optlist=''):
        return PDF_add_textflow(self._p, textflow, text, optlist)

    def add_thumbnail(self, image):
        PDF_add_thumbnail(self._p, image)

    def add_weblink(self, llx, lly, urx, ury, url):
        PDF_add_weblink(self._p, llx, lly, urx, ury, url)

    def align(self, dx, dy):
        PDF_align(self._p, dx, dy)

    def arc(self, x, y, r, alpha, beta):
        PDF_arc(self._p, x, y, r, alpha, beta)

    def arcn(self, x, y, r, alpha, beta):
        PDF_arcn(self._p, x, y, r, alpha, beta)

    def attach_file(self, llx, lly, urx, ury, filename, description, author, mimetype, icon):
        PDF_attach_file(self._p, llx, lly, urx, ury, filename, description, author, mimetype, icon)

    @wrap_optlist
    def begin_document(self, filename, optlist=''):
        return PDF_begin_document(self._p, filename, optlist)

    @wrap_optlist
    def begin_dpart(self, optlist=''):
        PDF_begin_dpart(self._p, optlist)

    @wrap_optlist
    def begin_font(self, fontname, a, b, c, d, e, f, optlist=''):
        PDF_begin_font(self._p, fontname, a, b, c, d, e, f, optlist)

    def begin_glyph(self, glyphname, wx, llx, lly, urx, ury):
        PDF_begin_glyph(self._p, glyphname, wx, llx, lly, urx, ury)

    @wrap_optlist
    def begin_glyph_ext(self, uv, optlist=''):
        PDF_begin_glyph_ext(self._p, uv, optlist)

    @wrap_optlist
    def begin_item(self, tagname, optlist=''):
        return PDF_begin_item(self._p, tagname, optlist)

    def begin_layer(self, layer):
        PDF_begin_layer(self._p, layer)

    @wrap_optlist
    def begin_mc(self, tagname, optlist=''):
        PDF_begin_mc(self._p, tagname, optlist)

    def begin_page(self, width, height):
        PDF_begin_page(self._p, width, height)

    @wrap_optlist
    def begin_page_ext(self, width, height, optlist=''):
        PDF_begin_page_ext(self._p, width, height, optlist)

    def begin_pattern(self, width, height, xstep, ystep, painttype):
        return PDF_begin_pattern(self._p, width, height, xstep, ystep, painttype)

    def begin_template(self, width, height):
        return PDF_begin_template(self._p, width, height)

    @wrap_optlist
    def begin_template_ext(self, width, height, optlist=''):
        return PDF_begin_template_ext(self._p, width, height, optlist)

    def circle(self, x, y, r):
        PDF_circle(self._p, x, y, r)

    def circular_arc(self, x_1, y_1, x_2, y_2):
        PDF_circular_arc(self._p, x_1, y_1, x_2, y_2)

    def clip(self):
        PDF_clip(self._p)

    def close(self):
        PDF_close(self._p)

    def close_font(self, font):
        PDF_close_font(self._p, font)

    def close_graphics(self, graphics):
        PDF_close_graphics(self._p, graphics)

    def close_image(self, image):
        PDF_close_image(self._p, image)

    def close_pdi(self, doc):
        PDF_close_pdi(self._p, doc)

    def close_pdi_document(self, doc):
        PDF_close_pdi_document(self._p, doc)

    def close_pdi_page(self, page):
        PDF_close_pdi_page(self._p, page)

    def closepath(self):
        PDF_closepath(self._p)

    def closepath_fill_stroke(self):
        PDF_closepath_fill_stroke(self._p)

    def closepath_stroke(self):
        PDF_closepath_stroke(self._p)

    def concat(self, a, b, c, d, e, f):
        PDF_concat(self._p, a, b, c, d, e, f)

    def continue_text(self, text):
        PDF_continue_text(self._p, text)

    @wrap_optlist
    def convert_to_unicode(self, inputformat, inputstring, optlist=''):
        return PDF_convert_to_unicode(self._p, inputformat, inputstring, optlist)

    @wrap_optlist
    def create_3dview(self, username, optlist=''):
        return PDF_create_3dview(self._p, username, optlist)

    @wrap_optlist
    def create_action(self, type, optlist=''):
        return PDF_create_action(self._p, type, optlist)

    @wrap_optlist
    def create_annotation(self, llx, lly, urx, ury, type, optlist=''):
        PDF_create_annotation(self._p, llx, lly, urx, ury, type, optlist)

    @wrap_optlist
    def create_bookmark(self, text, optlist=''):
        return PDF_create_bookmark(self._p, text, optlist)

    @wrap_optlist
    def create_field(self, llx, lly, urx, ury, name, type, optlist=''):
        PDF_create_field(self._p, llx, lly, urx, ury, name, type, optlist)

    @wrap_optlist
    def create_fieldgroup(self, name, optlist=''):
        PDF_create_fieldgroup(self._p, name, optlist)

    @wrap_optlist
    def create_gstate(self, optlist=''):
        return PDF_create_gstate(self._p, optlist)

    @wrap_optlist
    def create_pvf(self, filename, data, optlist=''):
        PDF_create_pvf(self._p, filename, data, optlist)

    @wrap_optlist
    def create_textflow(self, text, optlist=''):
        return PDF_create_textflow(self._p, text, optlist)

    def curveto(self, x_1, y_1, x_2, y_2, x_3, y_3):
        PDF_curveto(self._p, x_1, y_1, x_2, y_2, x_3, y_3)

    @wrap_optlist
    def define_layer(self, name, optlist=''):
        return PDF_define_layer(self._p, name, optlist)

    def delete_path(self, path):
        PDF_delete_path(self._p, path)

    def delete_pvf(self, filename):
        return PDF_delete_pvf(self._p, filename)

    @wrap_optlist
    def delete_table(self, table, optlist=''):
        PDF_delete_table(self._p, table, optlist)

    def delete_textflow(self, textflow):
        PDF_delete_textflow(self._p, textflow)

    @wrap_optlist
    def draw_path(self, path, x, y, optlist=''):
        PDF_draw_path(self._p, path, x, y, optlist)

    def ellipse(self, x, y, rx, ry):
        PDF_ellipse(self._p, x, y, rx, ry)

    @wrap_optlist
    def elliptical_arc(self, x, y, rx, ry, optlist=''):
        PDF_elliptical_arc(self._p, x, y, rx, ry, optlist)

    def encoding_set_char(self, encoding, slot, glyphname, uv):
        PDF_encoding_set_char(self._p, encoding, slot, glyphname, uv)

    @wrap_optlist
    def end_document(self, optlist=''):
        PDF_end_document(self._p, optlist)

    @wrap_optlist
    def end_dpart(self, optlist=''):
        PDF_end_dpart(self._p, optlist)

    def end_font(self):
        PDF_end_font(self._p)

    def end_glyph(self):
        PDF_end_glyph(self._p)

    def end_item(self, id):
        PDF_end_item(self._p, id)

    def end_layer(self):
        PDF_end_layer(self._p)

    def end_mc(self):
        PDF_end_mc(self._p)

    def end_page(self):
        PDF_end_page(self._p)

    @wrap_optlist
    def end_page_ext(self, optlist=''):
        PDF_end_page_ext(self._p, optlist)

    def end_pattern(self):
        PDF_end_pattern(self._p)

    def end_template(self):
        PDF_end_template(self._p)

    def end_template_ext(self, width, height):
        PDF_end_template_ext(self._p, width, height)

    def endpath(self):
        PDF_endpath(self._p)

    def fill(self):
        PDF_fill(self._p)

    @wrap_optlist
    def fill_graphicsblock(self, page, blockname, graphics, optlist=''):
        return PDF_fill_graphicsblock(self._p, page, blockname, graphics, optlist)

    @wrap_optlist
    def fill_imageblock(self, page, blockname, image, optlist=''):
        return PDF_fill_imageblock(self._p, page, blockname, image, optlist)

    @wrap_optlist
    def fill_pdfblock(self, page, blockname, contents, optlist=''):
        return PDF_fill_pdfblock(self._p, page, blockname, contents, optlist)

    def fill_stroke(self):
        PDF_fill_stroke(self._p)

    @wrap_optlist
    def fill_textblock(self, page, blockname, text, optlist=''):
        return PDF_fill_textblock(self._p, page, blockname, text, optlist)

    def findfont(self, fontname, encoding, embed):
        return PDF_findfont(self._p, fontname, encoding, embed)

    @wrap_optlist
    def fit_graphics(self, graphics, x, y, optlist=''):
        PDF_fit_graphics(self._p, graphics, x, y, optlist)

    @wrap_optlist
    def fit_image(self, image, x, y, optlist=''):
        PDF_fit_image(self._p, image, x, y, optlist)

    @wrap_optlist
    def fit_pdi_page(self, page, x, y, optlist=''):
        PDF_fit_pdi_page(self._p, page, x, y, optlist)

    @wrap_optlist
    def fit_table(self, table, llx, lly, urx, ury, optlist=''):
        return PDF_fit_table(self._p, table, llx, lly, urx, ury, optlist)

    @wrap_optlist
    def fit_textflow(self, textflow, llx, lly, urx, ury, optlist=''):
        return PDF_fit_textflow(self._p, textflow, llx, lly, urx, ury, optlist)

    @wrap_optlist
    def fit_textline(self, text, x, y, optlist=''):
        optlist = self.boxdebug(optlist)
        PDF_fit_textline(self._p, text, x, y, optlist)

    def get_apiname(self):
        return PDF_get_apiname(self._p)

    def get_buffer(self):
        return PDF_get_buffer(self._p)

    def get_errmsg(self):
        return PDF_get_errmsg(self._p)

    def get_errnum(self):
        return PDF_get_errnum(self._p)

    @wrap_optlist
    def get_option(self, keyword, optlist=''):
        return PDF_get_option(self._p, keyword, optlist)

    def get_parameter(self, key, modifier):
        return PDF_get_parameter(self._p, key, modifier)

    def get_pdi_parameter(self, key, doc, page, reserved):
        return PDF_get_pdi_parameter(self._p, key, doc, page, reserved)

    def get_pdi_value(self, key, doc, page, reserved):
        return PDF_get_pdi_value(self._p, key, doc, page, reserved)

    @wrap_optlist
    def get_string(self, idx, optlist=''):
        return PDF_get_string(self._p, idx, optlist)

    def get_value(self, key, modifier):
        return PDF_get_value(self._p, key, modifier)

    @wrap_optlist
    def info_font(self, font, keyword, optlist=''):
        return PDF_info_font(self._p, font, keyword, optlist)

    @wrap_optlist
    def info_graphics(self, graphics, keyword, optlist=''):
        return PDF_info_graphics(self._p, graphics, keyword, optlist)

    @wrap_optlist
    def info_image(self, image, keyword, optlist=''):
        return PDF_info_image(self._p, image, keyword, optlist)

    def info_matchbox(self, boxname, num, keyword):
        return PDF_info_matchbox(self._p, boxname, num, keyword)

    @wrap_optlist
    def info_path(self, path, keyword, optlist=''):
        return PDF_info_path(self._p, path, keyword, optlist)

    @wrap_optlist
    def info_pdi_page(self, page, keyword, optlist=''):
        return PDF_info_pdi_page(self._p, page, keyword, optlist)

    def info_pvf(self, filename, keyword):
        return PDF_info_pvf(self._p, filename, keyword)

    def info_table(self, table, keyword):
        return PDF_info_table(self._p, table, keyword)

    def info_textflow(self, textflow, keyword):
        return PDF_info_textflow(self._p, textflow, keyword)

    @wrap_optlist
    def info_textline(self, text, keyword, optlist=''):
        return PDF_info_textline(self._p, text, keyword, optlist)

    def initgraphics(self):
        PDF_initgraphics(self._p)

    def lineto(self, x, y):
        PDF_lineto(self._p, x, y)

    @wrap_optlist
    def load_3ddata(self, filename, optlist=''):
        return PDF_load_3ddata(self._p, filename, optlist)

    @wrap_optlist
    def load_asset(self, type, filename, optlist=''):
        return PDF_load_asset(self._p, type, filename, optlist)

    @wrap_optlist
    def load_font(self, fontname, encoding, optlist=''):
        return PDF_load_font(self._p, fontname, encoding, optlist)

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
        return PDF_load_graphics(self._p, type, filename, optlist)

    @wrap_optlist
    def load_iccprofile(self, profilename, optlist=''):
        return PDF_load_iccprofile(self._p, profilename, optlist)

    @wrap_optlist
    def load_image(self, imagetype, filename, optlist=''):
        return PDF_load_image(self._p, imagetype, filename, optlist)

    def makespotcolor(self, spotname):
        return PDF_makespotcolor(self._p, spotname)

    @wrap_optlist
    def mc_point(self, tagname, optlist=''):
        PDF_mc_point(self._p, tagname, optlist)

    def moveto(self, x, y):
        PDF_moveto(self._p, x, y)

    def open_CCITT(self, filename, width, height, BitReverse, K, BlackIs1):
        return PDF_open_CCITT(self._p, filename, width, height, BitReverse, K, BlackIs1)

    def open_file(self, filename):
        return PDF_open_file(self._p, filename)

    def open_image(self, imagetype, source, data, width, height, components, bpc, params):
        return PDF_open_image(self._p, imagetype, source, data, width, height, components, bpc, params)

    def open_image_file(self, imagetype, filename, stringparam, intparam):
        return PDF_open_image_file(self._p, imagetype, filename, stringparam, intparam)

    def open_pdi(self, filename, filename_len):
        return PDF_open_pdi(self._p, filename, filename_len)

    @wrap_optlist
    def open_pdi_document(self, filename, optlist=''):
        return PDF_open_pdi_document(self._p, filename, optlist)

    @wrap_optlist
    def open_pdi_page(self, doc, pagenumber, optlist=''):
        return PDF_open_pdi_page(self._p, doc, pagenumber, optlist)

    def pcos_get_number(self, doc, path):
        return PDF_pcos_get_number(self._p, doc, path)

    def pcos_get_string(self, doc, path):
        return PDF_pcos_get_string(self._p, doc, path)

    @wrap_optlist
    def pcos_get_stream(self, doc, optlist, path):
        return PDF_pcos_get_stream(self._p, doc, optlist, path)

    def place_image(self, image, x, y, scale):
        PDF_place_image(self._p, image, x, y, scale)

    def place_pdi_page(self, page, x, y, sx, sy):
        PDF_place_pdi_page(self._p, page, x, y, sx, sy)

    @wrap_optlist
    def poca_delete(self, container, optlist=''):
        PDF_poca_delete(self._p, container, optlist)

    @wrap_optlist
    def poca_insert(self, container, optlist=''):
        PDF_poca_insert(self._p, container, optlist)

    @wrap_optlist
    def poca_new(self, optlist=''):
        return PDF_poca_new(self._p, optlist)

    @wrap_optlist
    def poca_remove(self, container, optlist=''):
        PDF_poca_remove(self._p, container, optlist)

    @wrap_optlist
    def process_pdi(self, doc, page, optlist=''):
        return PDF_process_pdi(self._p, doc, page, optlist)

    def rect(self, x, y, width, height):
        PDF_rect(self._p, x, y, width, height)

    def restore(self):
        PDF_restore(self._p)

    @wrap_optlist
    def resume_page(self, optlist=''):
        PDF_resume_page(self._p, optlist)

    def rotate(self, phi):
        PDF_rotate(self._p, phi)

    def save(self):
        PDF_save(self._p)

    def scale(self, sx, sy):
        PDF_scale(self._p, sx, sy)

    def set_border_color(self, red, green, blue):
        PDF_set_border_color(self._p, red, green, blue)

    def set_border_dash(self, b, w):
        PDF_set_border_dash(self._p, b, w)

    def set_border_style(self, style, width):
        PDF_set_border_style(self._p, style, width)

    @wrap_optlist
    def set_graphics_option(self, optlist=''):
        PDF_set_graphics_option(self._p, optlist)

    def set_gstate(self, gstate):
        PDF_set_gstate(self._p, gstate)

    def set_info(self, key, value):
        PDF_set_info(self._p, key, value)

    @wrap_optlist
    def set_layer_dependency(self, type, optlist=''):
        PDF_set_layer_dependency(self._p, type, optlist)

    @wrap_optlist
    def set_option(self, optlist=''):
        PDF_set_option(self._p, optlist)

    def set_parameter(self, key, value):
        PDF_set_parameter(self._p, key, value)

    @wrap_optlist
    def set_text_option(self, optlist=''):
        PDF_set_text_option(self._p, optlist)

    def set_text_pos(self, x, y):
        PDF_set_text_pos(self._p, x, y)

    def set_value(self, key, value):
        PDF_set_value(self._p, key, value)

    def setcolor(self, fstype, colorspace, c1, c2, c3, c4):
        PDF_setcolor(self._p, fstype, colorspace, c1, c2, c3, c4)

    def setdash(self, b, w):
        PDF_setdash(self._p, b, w)

    @wrap_optlist
    def setdashpattern(self, optlist=''):
        PDF_setdashpattern(self._p, optlist)

    def setflat(self, flatness):
        PDF_setflat(self._p, flatness)

    def setfont(self, font, fontsize):
        self._font_size = fontsize
        PDF_setfont(self._p, font, fontsize)

    def setgray(self, gray):
        PDF_setgray(self._p, gray)

    def setgray_fill(self, gray):
        PDF_setgray_fill(self._p, gray)

    def setgray_stroke(self, gray):
        PDF_setgray_stroke(self._p, gray)

    def setlinecap(self, linecap):
        PDF_setlinecap(self._p, linecap)

    def setlinejoin(self, linejoin):
        PDF_setlinejoin(self._p, linejoin)

    def setlinewidth(self, width):
        PDF_setlinewidth(self._p, width)

    def setmatrix(self, a, b, c, d, e, f):
        PDF_setmatrix(self._p, a, b, c, d, e, f)

    def setmiterlimit(self, miter):
        PDF_setmiterlimit(self._p, miter)

    def setpolydash(self, dasharray, length):
        PDF_setpolydash(self._p, dasharray, length)

    def setrgbcolor(self, red, green, blue):
        PDF_setrgbcolor(self._p, red, green, blue)

    def setrgbcolor_fill(self, red, green, blue):
        PDF_setrgbcolor_fill(self._p, red, green, blue)

    def setrgbcolor_stroke(self, red, green, blue):
        PDF_setrgbcolor_stroke(self._p, red, green, blue)

    @wrap_optlist
    def shading(self, shtype, x_0, y_0, x_1, y_1, c_1, c_2, c_3, c_4, optlist=''):
        return PDF_shading(self._p, shtype, x_0, y_0, x_1, y_1, c_1, c_2, c_3, c_4, optlist)

    @wrap_optlist
    def shading_pattern(self, shading, optlist=''):
        return PDF_shading_pattern(self._p, shading, optlist)

    def shfill(self, shading):
        PDF_shfill(self._p, shading)

    def show(self, text):
        PDF_show(self._p, text)

    def show_boxed(self, text, left, top, width, height, hmode, feature):
        return PDF_show_boxed(self._p, text, left, top, width, height, hmode, feature)

    def show_xy(self, text, x, y):
        PDF_show_xy(self._p, text, x, y)

    def skew(self, alpha, beta):
        PDF_skew(self._p, alpha, beta)

    def stringwidth(self, text, font, fontsize):
        return PDF_stringwidth(self._p, text, font, fontsize)

    def stroke(self):
        PDF_stroke(self._p)

    @wrap_optlist
    def suspend_page(self, optlist=''):
        PDF_suspend_page(self._p, optlist)

    def translate(self, tx, ty):
        PDF_translate(self._p, tx, ty)
