import inspect
from functools import wraps
from typing import TypeVar, Optional, Union, Dict, List, Iterable, Callable

try:
    from .pdflib_py import *
except ImportError as exc:
    raise ImportError('Could not load pdflib_py shared library') from exc


# Can't get types from the C binding
PDFlibInstance = TypeVar('PDFlibInstance')

Handle = int  # PDFlib uses int references for loaded assets
FontMap = Dict[str, Handle]
OptlistScalar = Union[bool, float, int, str]
OptlistValue = Union[Iterable[OptlistScalar], OptlistScalar]
Optlist = Union[str, Dict[str, OptlistValue]]
InfoResult = Union[float, int, str]


def wrap_optlist(fn: Callable):
    """Wraps functions that accept an optlist. If the incoming
    optlist is a dict, parse it down to native format"""
    argspec = inspect.getfullargspec(fn)
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

    __p: Optional[PDFlibInstance] = None

    _fonts: FontMap
    _debug: bool = False

    # Warning: this is most likely incorrect after save()/restore() calls
    _font_size: int = 0

    def __init__(self):
        self.__p = PDF_new()
        if self.__p:
            PDF_set_option(self.__p, "objorient=true")
        self._fonts = {}

    def debug(self, enable: bool):
        self._debug = enable

    @classmethod
    def parse_optlist(cls, optlist: Dict[str, OptlistValue]) -> str:
        out = []
        for k, v in optlist.items():
            v = cls._coerce_value(v)
            out.append('%s=%s' % (k, v))
        return ' '.join(out)

    @classmethod
    def _coerce_value(cls, v: OptlistValue, scalar_only: bool = False) -> str:
        if isinstance(v, str):
            pass
        elif v in [True, False]:
            v = cls._coerce_bool(v)
        elif isinstance(v, Iterable) and not scalar_only:
            v = cls._coerce_iterable(v)
        elif isinstance(v, (float, int)):
            v = str(v)
        else:
            raise TypeError('_coerce_value cant convert type %s' % type(v))
        return v

    @classmethod
    def _coerce_iterable(cls, i: Iterable[OptlistScalar]) -> str:
        v: List[str] = []
        for value in i:
            v.append(cls._coerce_value(value, scalar_only=True))
        return '{' + ' '.join(v) + '}'

    @classmethod
    def _coerce_bool(cls, b: bool):
        return str(b).lower()

    def boxdebug(self, optlist):
        if self._debug:
            if 'boxsize' in optlist:
                optlist += ' showborder=true'
        return optlist

    # It is recommended not to use __del__ as it's execution is not guaranteed in a timely fashion.
    # Implement a delete method to invalidate self.__p
    def __del__(self):
        self.delete()

    def delete(self):
        if self.__p:
            PDF_delete(self.__p)
        self.__p = None

    @wrap_optlist
    def add_nameddest(self, name: str, optlist: Optlist = ''):
        PDF_add_nameddest(self.__p, name, optlist)

    @wrap_optlist
    def add_path_point(self, path: Handle, x: float, y: float, type: str, optlist: Optlist = '') -> Handle:
        return PDF_add_path_point(self.__p, path, x, y, type, optlist)

    @wrap_optlist
    def add_portfolio_file(self, folder: Handle, filename: str, optlist: Optlist = '') -> Handle:
        return PDF_add_portfolio_file(self.__p, folder, filename, optlist)

    @wrap_optlist
    def add_portfolio_folder(
        self,
        parent: Optional[Handle],
        folder_name: str,
        optlist: Optlist = ''
    ) -> Handle:
        return PDF_add_portfolio_folder(self.__p, parent, folder_name, optlist)

    @wrap_optlist
    def add_table_cell(
        self,
        table: Handle,
        column: int,
        row: int,
        text: str,
        optlist: Optlist = ''
    ) -> Handle:
        return PDF_add_table_cell(self.__p, table, column, row, text, optlist)

    @wrap_optlist
    def add_textflow(self, textflow: Handle, text: str, optlist: Optlist = '') -> Handle:
        return PDF_add_textflow(self.__p, textflow, text, optlist)

    def align(self, dx: float, dy: float):
        PDF_align(self.__p, dx, dy)

    def arc(self, x: float, y: float, r: float, alpha: float, beta: float):
        PDF_arc(self.__p, x, y, r, alpha, beta)

    def arcn(self, x: float, y: float, r: float, alpha: float, beta: float):
        PDF_arcn(self.__p, x, y, r, alpha, beta)

    @wrap_optlist
    def begin_document(self, filename: str, optlist: Optlist = ''):
        PDF_begin_document(self.__p, filename, optlist)

    @wrap_optlist
    def begin_dpart(self, optlist: Optlist = ''):
        PDF_begin_dpart(self.__p, optlist)

    @wrap_optlist
    def begin_item(self, tagname: str, optlist: Optlist = '') -> Handle:
        return PDF_begin_item(self.__p, tagname, optlist)

    def begin_layer(self, layer: Handle):
        PDF_begin_layer(self.__p, layer)

    @wrap_optlist
    def begin_mc(self, tagname: str, optlist: Optlist = ''):
        PDF_begin_mc(self.__p, tagname, optlist)

    @wrap_optlist
    def begin_page_ext(
        self,
        width: float,
        height: float,
        optlist: Optlist = ''
    ):
        PDF_begin_page_ext(self.__p, width, height, optlist)

    @wrap_optlist
    def begin_pattern_ext(self, width: float, height: float, optlist: Optlist = '') -> Handle:
        return PDF_begin_pattern_ext(self.__p, width, height, optlist)

    @wrap_optlist
    def begin_template_ext(self, width: float, height: float, optlist: Optlist = '') -> Handle:
        return PDF_begin_template_ext(self.__p, width, height, optlist)

    def circle(self, x: float, y: float, radius: float):
        PDF_circle(self.__p, x, y, radius)

    def circular_arc(self, x1: float, y1: float, x2: float, y2: float):
        PDF_circular_arc(self.__p, x1, y1, x2, y2)

    def clip(self):
        PDF_clip(self.__p)

    def close(self):
        PDF_close(self.__p)

    def close_font(self, font: Handle):
        PDF_close_font(self.__p, font)

    def close_graphics(self, graphics: Handle):
        PDF_close_graphics(self.__p, graphics)

    def close_image(self, image: Handle):
        PDF_close_image(self.__p, image)

    def close_pdi_document(self, document_handle: Handle):
        PDF_close_pdi_document(self.__p, document_handle)

    def close_pdi_page(self, page_handle: Handle):
        PDF_close_pdi_page(self.__p, page_handle)

    def closepath(self):
        PDF_closepath(self.__p)

    def closepath_fill_stroke(self):
        PDF_closepath_fill_stroke(self.__p)

    def closepath_stroke(self):
        PDF_closepath_stroke(self.__p)

    def concat(
        self,
        a: float,
        b: float,
        c: float,
        d: float,
        e: float,
        f: float
    ):
        PDF_concat(self.__p, a, b, c, d, e, f)

    def continue_text(self, text: str):
        PDF_continue_text(self.__p, text)

    @wrap_optlist
    def create_3dview(self, user_interface_name: str, optlist: Optlist = '') -> Handle:
        return PDF_create_3dview(self.__p, user_interface_name, optlist)

    @wrap_optlist
    def create_action(self, action_type: str, optlist: Optlist = '') -> Handle:
        return PDF_create_action(self.__p, action_type, optlist)

    @wrap_optlist
    def create_annotation(
        self,
        llx: float,
        lly: float,
        urx: float,
        ury: float,
        type: float,
        optlist: Optlist = ''
    ):
        PDF_create_annotation(self.__p, llx, lly, urx, ury, type, optlist)

    @wrap_optlist
    def create_bookmark(self, text: str, optlist: Optlist = '') -> Handle:
        return PDF_create_bookmark(self.__p, text, optlist)

    @wrap_optlist
    def create_field(
        self,
        llx: float,
        lly: float,
        urx: float,
        ury: float,
        name: str,
        field_type: str,
        optlist: Optlist = ''
    ):
        PDF_create_field(self.__p, llx, lly, urx, ury, name, field_type, optlist)

    @wrap_optlist
    def create_fieldgroup(self, name: str, optlist: Optlist = ''):
        PDF_create_fieldgroup(self.__p, name, optlist)

    @wrap_optlist
    def create_gstate(self, optlist: Optlist = '') -> Handle:
        return PDF_create_gstate(self.__p, optlist)

    @wrap_optlist
    def create_pvf(self, filename: str, data: Union[str, bytes], optlist: Optlist = ''):
        PDF_create_pvf(self.__p, filename, data, optlist)

    @wrap_optlist
    def create_textflow(self, text: str, optlist: Optlist = ''):
        return PDF_create_textflow(self.__p, text, optlist)

    def curveto(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
        PDF_curveto(self.__p, x1, y1, x2, y2, x3, y3)

    @wrap_optlist
    def define_layer(self, name: str, optlist: Optlist = '') -> Handle:
        return PDF_define_layer(self.__p, name, optlist)

    def delete_path(self, path: Handle):
        PDF_delete_path(self.__p, path)

    def delete_pvf(self, filename: str) -> int:
        return PDF_delete_pvf(self.__p, filename)

    @wrap_optlist
    def delete_table(self, table: Handle, optlist: Optlist = ''):
        PDF_delete_table(self.__p, table, optlist)

    def delete_textflow(self, textflow: Handle):
        PDF_delete_textflow(self.__p, textflow)

    @wrap_optlist
    def draw_path(self, path: Handle, x: float, y: float, optlist: Optlist = ''):
        PDF_draw_path(self.__p, path, x, y, optlist)

    def ellipse(self, x: float, y: float, rx: float, ry: float):
        PDF_ellipse(self.__p, x, y, rx, ry)

    @wrap_optlist
    def elliptical_arc(self, x: float, y: float, rx: float, ry: float, optlist: Optlist = ''):
        PDF_elliptical_arc(self.__p, x, y, rx, ry, optlist)

    @wrap_optlist
    def end_document(self, optlist: Optlist = ''):
        PDF_end_document(self.__p, optlist)

    @wrap_optlist
    def end_dpart(self, optlist: Optlist = ''):
        PDF_end_dpart(self.__p, optlist)

    def end_item(self, id: Handle):
        PDF_end_item(self.__p, id)

    def end_layer(self):
        PDF_end_layer(self.__p)

    def end_mc(self):
        PDF_end_mc(self.__p)

    @wrap_optlist
    def end_page_ext(self, optlist: Optlist = ''):
        PDF_end_page_ext(self.__p, optlist)

    def end_pattern(self):
        PDF_end_pattern(self.__p)

    def end_template_ext(self, width: float, height: float):
        PDF_end_template_ext(self.__p, width, height)

    def endpath(self):
        PDF_endpath(self.__p)

    def fill(self):
        PDF_fill(self.__p)

    def fill_stroke(self):
        PDF_fill_stroke(self.__p)

    @wrap_optlist
    def fit_graphics(self, graphics: Handle, x: float, y: float, optlist: Optlist = ''):
        PDF_fit_graphics(self.__p, graphics, x, y, optlist)

    @wrap_optlist
    def fit_image(self, image: Handle, x: float, y: float, optlist: Optlist = ''):
        PDF_fit_image(self.__p, image, x, y, optlist)

    @wrap_optlist
    def fit_pdi_page(self, page: Handle, x: float, y: float, optlist: Optlist = ''):
        PDF_fit_pdi_page(self.__p, page, x, y, optlist)

    @wrap_optlist
    def fit_table(
        self,
        table: Handle,
        llx: float,
        lly: float,
        urx: float,
        ury: float,
        optlist: Optlist = ''
    ) -> str:
        return PDF_fit_table(self.__p, table, llx, lly, urx, ury, optlist)

    @wrap_optlist
    def fit_textflow(
        self,
        textflow: Handle,
        llx: float,
        lly: float,
        urx: float,
        ury: float,
        optlist: Optlist = ''
    ) -> str:
        return PDF_fit_textflow(self.__p, textflow, llx, lly, urx, ury, optlist)

    @wrap_optlist
    def fit_textline(self, text: str, x: float, y: float, optlist: Optlist = ''):
        optlist = self.boxdebug(optlist)
        PDF_fit_textline(self.__p, text, x, y, optlist)

    def get_apiname(self) -> str:
        return PDF_get_apiname(self.__p)

    def get_buffer(self) -> bytes:
        return PDF_get_buffer(self.__p)

    def get_errmsg(self) -> str:
        return PDF_get_errmsg(self.__p)

    def get_errnum(self) -> int:
        return PDF_get_errnum(self.__p)

    @wrap_optlist
    def get_option(self, keyword, optlist='') -> InfoResult:
        return PDF_get_option(self.__p, keyword, optlist)

    @wrap_optlist
    def get_string(self, idx: int, optlist: Optlist = ''):
        return PDF_get_string(self.__p, idx, optlist)

    @wrap_optlist
    def info_font(self, font: Handle, keyword: str, optlist: Optlist = '') -> InfoResult:
        return PDF_info_font(self.__p, font, keyword, optlist)

    @wrap_optlist
    def info_graphics(self, graphics: Handle, keyword: str, optlist: Optlist = '') -> InfoResult:
        return PDF_info_graphics(self.__p, graphics, keyword, optlist)

    @wrap_optlist
    def info_image(self, image: Handle, keyword: str, optlist: Optlist = '') -> InfoResult:
        return PDF_info_image(self.__p, image, keyword, optlist)

    def info_matchbox(self, boxname: str, num: int, keyword: str) -> InfoResult:
        return PDF_info_matchbox(self.__p, boxname, num, keyword)

    @wrap_optlist
    def info_path(self, path: Handle, keyword: str, optlist: Optlist = '') -> InfoResult:
        return PDF_info_path(self.__p, path, keyword, optlist)

    @wrap_optlist
    def info_pdi_page(self, page: int, keyword: str, optlist: Optlist = '') -> InfoResult:
        return PDF_info_pdi_page(self.__p, page, keyword, optlist)

    def info_pvf(self, filename: str, keyword: str) -> InfoResult:
        return PDF_info_pvf(self.__p, filename, keyword)

    def info_table(self, table: Handle, keyword: str) -> InfoResult:
        return PDF_info_table(self.__p, table, keyword)

    def info_textflow(self, textflow: Handle, keyword: str) -> InfoResult:
        return PDF_info_textflow(self.__p, textflow, keyword)

    @wrap_optlist
    def info_textline(self, text, keyword, optlist='') -> InfoResult:
        return PDF_info_textline(self.__p, text, keyword, optlist)

    def lineto(self, x: float, y: float):
        PDF_lineto(self.__p, x, y)

    @wrap_optlist
    def load_3ddata(self, filename: str, optlist: Optlist = '') -> Handle:
        return PDF_load_3ddata(self.__p, filename, optlist)

    @wrap_optlist
    def load_asset(self, type: str, filename: str, optlist: Optlist = '') -> Handle:
        return PDF_load_asset(self.__p, type, filename, optlist)

    @wrap_optlist
    def load_font(self, fontname: str, encoding: str, optlist: Optlist = '') -> Handle:
        return PDF_load_font(self.__p, fontname, encoding, optlist)

    @wrap_optlist
    def register_font(
        self,
        fontname: str,
        encoding: str,
        optlist: Optlist = '',
        register_as: Optional[str] = None
    ) -> Handle:
        font = self.load_font(fontname, encoding, optlist)
        if font == -1 or font is None:
            raise PDFlibException('Could not load font %s (%s)' % (fontname, encoding))
        if register_as is None:
            register_as = fontname
        self._fonts[register_as] = font
        return font

    def get_font(self, identifier: str) -> Handle:
        return self._fonts[identifier]

    def line(self, x1: float, y1: float, x2: float, y2: float):
        self.moveto(x1, y1)
        self.lineto(x2, y2)
        self.closepath_stroke()

    def use_font(self, identifier: str, fontsize: float):
        self.setfont(self.get_font(identifier), fontsize)

    @wrap_optlist
    def load_graphics(self, type: str, filename: str, optlist: Optlist = '') -> Handle:
        return PDF_load_graphics(self.__p, type, filename, optlist)

    @wrap_optlist
    def load_image(self, imagetype: str, filename: str, optlist: Optlist = '') -> Handle:
        return PDF_load_image(self.__p, imagetype, filename, optlist)

    def makespotcolor(self, spotname: str) -> Handle:
        return PDF_makespotcolor(self.__p, spotname)

    @wrap_optlist
    def mc_point(self, tagname: str, optlist: Optlist = ''):
        PDF_mc_point(self.__p, tagname, optlist)

    def moveto(self, x: float, y: float):
        PDF_moveto(self.__p, x, y)

    @wrap_optlist
    def process_pdi(self, doc: Handle, page: int, optlist: Optlist = '') -> int:
        return PDF_process_pdi(self.__p, doc, page, optlist)

    def rect(self, x: float, y: float, width: float, height: float):
        PDF_rect(self.__p, x, y, width, height)

    def restore(self):
        PDF_restore(self.__p)

    @wrap_optlist
    def resume_page(self, optlist: Optlist = ''):
        PDF_resume_page(self.__p, optlist)

    def rotate(self, phi: float):
        PDF_rotate(self.__p, phi)

    def save(self):
        PDF_save(self.__p)

    def scale(self, sx: float, sy: float):
        PDF_scale(self.__p, sx, sy)

    @wrap_optlist
    def set_graphics_option(self, optlist: Optlist = ''):
        PDF_set_graphics_option(self.__p, optlist)

    def set_gstate(self, gstate: Handle):
        PDF_set_gstate(self.__p, gstate)

    def set_info(self, key: str, value: str):
        PDF_set_info(self.__p, key, value)

    @wrap_optlist
    def set_layer_dependency(self, type: str, optlist: Optlist = ''):
        PDF_set_layer_dependency(self.__p, type, optlist)

    @wrap_optlist
    def set_option(self, optlist: Optlist = ''):
        PDF_set_option(self.__p, optlist)

    @wrap_optlist
    def set_text_option(self, optlist: Optlist = ''):
        PDF_set_text_option(self.__p, optlist)

    def set_text_pos(self, x: float, y: float):
        PDF_set_text_pos(self.__p, x, y)

    def setcolor(self, fstype: str, colorspace: str, c1: float, c2: float, c3: float, c4: float):
        PDF_setcolor(self.__p, fstype, colorspace, c1, c2, c3, c4)

    def setfont(self, font: Handle, fontsize: float):
        PDF_setfont(self.__p, font, fontsize)

    def setlinewidth(self, width: float):
        PDF_setlinewidth(self.__p, width)

    def setmatrix(
        self,
        a: float,
        b: float,
        c: float,
        d: float,
        e: float,
        f: float
    ):
        PDF_setmatrix(self.__p, a, b, c, d, e, f)

    @wrap_optlist
    def shading(
        self,
        type: str,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        c1: float,
        c2: float,
        c3: float,
        c4: float,
        optlist: Optlist = ''
    ) -> Handle:
        return PDF_shading(self.__p, type, x0, y0, x1, y1, c1, c2, c3, c4, optlist)

    @wrap_optlist
    def shading_pattern(self, shading: Handle, optlist: Optlist = '') -> Handle:
        return PDF_shading_pattern(self.__p, shading, optlist)

    def shfill(self, shading: Handle):
        PDF_shfill(self.__p, shading)

    def show(self, text: str):
        PDF_show(self.__p, text)

    def show_xy(self, text: str, x: float, y: float):
        PDF_show_xy(self.__p, text, x, y)

    def skew(self, alpha: float, beta: float):
        PDF_skew(self.__p, alpha, beta)

    def stringwidth(self, text: str, font: Handle, fontsize: float) -> float:
        return PDF_stringwidth(self.__p, text, font, fontsize)

    def stroke(self):
        PDF_stroke(self.__p)

    @wrap_optlist
    def suspend_page(self, optlist: Optlist = ''):
        PDF_suspend_page(self.__p, optlist)

    def translate(self, tx: float, ty: float):
        PDF_translate(self.__p, tx, ty)
