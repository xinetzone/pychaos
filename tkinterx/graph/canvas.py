'''Some of the actions related to the graph.
'''
from tkinter import Canvas, ttk, StringVar


class CanvasMeta(Canvas):
    '''Graphic elements are composed of line(segment), rectangle, ellipse, and arc.
    '''

    def __init__(self, master=None, cnf={}, **kw):
        '''The base class of all graphics frames.

        :param master: a widget of tkinter or tkinter.ttk.
        '''
        super().__init__(master, cnf, **kw)

    def layout(self, row=0, column=0):
        '''Layout graphic elements with Grid'''
        # Layout canvas space
        self.grid(row=row, column=column, sticky='nwes')

    def create_graph(self, graph_type, direction, color='blue', width=1, tags=None, **kwargs):
        '''Draw basic graphic elements.

        :param direction: Specifies the orientation of the graphic element. 
            Union[int, float] -> (x_0,y_0,x_,y_1), (x_0, y_0) refers to the starting point of 
            the reference brush (i.e., the left mouse button is pressed), and (x_1, y_1) refers to 
            the end position of the reference brush (i.e., release the left mouse button).
            Multipoint sequences are supported for 'line' and 'polygon',
             for example ((x_0, y_0), (x_1, y_1), (x_2, y_2)).
        :param graph_type: Types of graphic elements.
            (str) 'rectangle', 'oval', 'line', 'arc'(That is, segment), 'polygon'.
            Note that 'line' can no longer pass in the parameter 'fill', and 
            the remaining graph_type cannot pass in the parameter 'outline'.
        :param color: The color of the graphic element.
        :param width: The width of the graphic element.(That is, center fill)
        :param tags: The tags of the graphic element. 
            It cannot be a pure number (such as 1 or '1' or '1 2 3'), it can be a list, a tuple, 
            or a string separated by a space(is converted to String tupers separated by a blank space). 
            The collection or dictionary is converted to a string.
            Example:
                ['line', 'graph'], ('test', 'g'), 'line',
                ' line kind '(The blanks at both ends are automatically removed), and so on.
        :param style: Style of the arc in {'arc', 'chord', or 'pieslice'}.

        :return: Unique identifier solely for graphic elements.
        '''
        if tags is None:
            if graph_type in ('rectangle', 'oval', 'line', 'arc'):
                tags = f"graph {color} {graph_type}"
            else:
                tags = f'graph {color}'

        com_kw = {'width': width, 'tags': tags}
        kw = {**com_kw, 'outline': color}
        line_kw = {**com_kw, 'fill': color}
        if graph_type == 'line':
            kwargs.update(line_kw)
        else:
            kwargs.update(kw)
        func = eval(f"self.create_{graph_type}")
        graph_id = func(*direction, **kwargs)
        return graph_id

    def _create_regular_graph(self, graph_type, center, radius, color='blue', width=1, tags=None, **kw):
        '''Used to create a circle or square.
        :param graph_type: 'oval', 'rectangle'
        :param center: (x, y) The center of the regular_graph
        :param radius: Radius of the regular_graph
        '''
        x, y = center
        direction = [x-radius, y - radius, x+radius, y+radius]
        return self.create_graph(graph_type, direction, color, width, tags, **kw)

    def create_circle(self, center, radius, color='blue', width=1, tags=None, **kw):
        '''
        :param center: (x, y) The center of the circle
        :param radius: Radius of the circle
        '''
        return self._create_regular_graph('oval', center, radius, color, width, tags, **kw)

    def create_square(self, center, radius, color='blue', width=1, tags=None, **kw):
        '''
        :param center: (x, y) The center of the square
        :param radius: Radius of the square
        '''
        return self._create_regular_graph('rectangle', center, radius, color, width, tags, **kw)

    def create_circle_point(self, position, color='blue', width=1, tags=None, **kw):
        '''
        :param location: (x, y) The location of the circle_point
        '''
        return self.create_circle(position, 0, color, width, tags, **kw)

    def create_square_point(self, position, color='blue', width=1, tags=None, **kw):
        '''
        :param location: (x, y) The location of the square_point
        '''
        return self.create_square(position, 0, color, width, tags, **kw)


class GraphMeta(CanvasMeta):
    def __init__(self, master=None, cnf={}, **kw):
        '''
        '''
        super().__init__(master, cnf, **kw)
        self.record_bbox = ['none']*4
        self.xy_var = StringVar()
        self.master.bind('<F1>', self.clear_all)
        self.master.bind('<Delete>', self.delete_selected)
        self.master.bind('<Control-a>', self.select_all_graph)
        self.bind('<Motion>', self.update_xy)
        self.bind('<1>', self.select_current_graph)
        self.tag_bind('selected', '<ButtonRelease-1>', self.tune_selected)

    def get_canvasxy(self, event):
        return self.canvasx(event.x), self.canvasy(event.y)

    def update_xy(self, event):
        self.record_bbox[2:] = self.get_canvasxy(event)
        #self.xy_var.set(f"Direction Vector: {self.record_bbox}")
        self.xy_var.set(f"{self.record_bbox}")

    def start_record(self, event):
        self.record_bbox[:2] = self.get_canvasxy(event)
        self.xy_var.set(f"{self.record_bbox}")

    @property
    def strides(self):
        record_bbox = self.record_bbox
        if 'none' not in record_bbox:
            x0, y0, x1, y1 = record_bbox
            return x1 - x0, y1 - y0

    def reset(self):
        self.record_bbox[:2] = ['none']*2

    def clear_all(self, event):
        self.delete('all')

    def delete_selected(self, event):
        self.delete('current')

    @property
    def current_graph_tags(self):
        return self.find_withtag('current')

    def set_select_mode(self, event):
        self.start_record(event)
        if self.current_graph_tags:
            self.configure(cursor="target")
        else:
            self.configure(cursor="arrow")

    def select_current_graph(self, event):
        self.set_select_mode(event)
        self.addtag_withtag('selected', 'current')

    def select_all_graph(self, event):
        self.set_select_mode(event)
        self.addtag_withtag('selected', 'all')

    def tune_selected(self, event=None):
        self.move('selected', *self.strides)
        self.cancel_selected(event)

    # 以下方法暂未使用
    def cancel_selected(self, event):
        self.dtag('selected')
        self.configure(cursor="arrow")

    @property
    def closest_graph_id(self):
        xy = self.record_bbox[2:]
        if xy:
            return self.find_closest(*xy)
