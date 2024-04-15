import os,sys,mystring

def flatten(column_header):
    if isinstance(column_header, list) or isinstance(column_header, tuple):
        return ' '.join([str(ch) for ch in column_header]).strip()
    return column_header

common_defaults = {
    'Font': 'Times New Roman',
    'Font_Size':26,
    'Font_Color':'black',
    'DiscreteColours':['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac'],
    'DiscretePatterns':['x', '.', '+', '/', '-', '|', '^'],
}

from abc import ABC, abstractmethod
from copy import deepcopy as dc
class styleapplicator(ABC):
    def __init__(self):
        super().__init__()
        self.DiscreteColours = common_defaults['DiscreteColours']
        self.DiscretePatterns = common_defaults['DiscretePatterns']
    def assign_discrete_colormap(self, *keys):
        key_list = list(keys)
        if len(key_list) > len(self.DiscreteColours):
            raise Exception("There are too many keys, there are only {0} colours".format(len(self.DiscreteColours)))
        return {
            key:self.DiscreteColours[key_itr]
            for key_itr, key in enumerate(key_list)
        }
    def assign_discrete_patternmap(self, *keys):
        key_list = list(keys)
        if len(key_list) > len(self.DiscretePatterns):
            raise Exception("There are too many keys, there are only {0} colours".format(len(self.DiscretePatterns)))
        return self.DiscretePatterns[:len(key_list)-1]
    def assign_extras(self, *extras, keys=[]):
        output = {}
        extra_list = list(extras)
        if len(extra_list)  == 0:
            extra_list = ["patterns", "colours"]
        for extra_item in extra_list:
            if extra_item == "colours":
                output['color_discrete_map'] = self.assign_discrete_colormap(*keys)
            if extra_item == "patterns":
                output['pattern_shape_sequence'] = self.assign_discrete_patternmap(*keys)
        return output
    @staticmethod
    def clr():
        try:
            from IPython.display import clear_output;
            clear_output();
        except:pass
    def clear_screen(self):
        styleapplicator.clr();
    def reset(self):
        try:
            from IPython import get_ipython;
            ipython = get_ipython();
        except:pass
    @abstractmethod
    def __enter__(self):
        pass
    @abstractmethod
    def __exit__(self,*args, **kwargs):
        pass
    @abstractmethod
    def __call__(self, some_figure_obj):
        pass

try:
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mbl_styles = {
        "ipynb": "https://raw.githubusercontent.com/killiansheriff/LovelyPlots/master/lovelyplots/styles/ipynb.mplstyle",
        "ipynb_Archive": mystring.string.of("IyBmaWd1cmUgTG9vawpmaWd1cmUuZmlnc2l6ZTogNC41LCAzLjQ2CgpheGVzLmdyaWQ6IEZhbHNlCmZvbnQuc2l6ZTogMTQKCnl0aWNrLmxlZnQ6IFRydWUKeHRpY2suYm90dG9tOiBUcnVlCmltYWdlLmNtYXA6IGluZmVybm8KbGluZXMubWFya2Vyc2l6ZTogNgoKIyB0dXJuIG9uIHNjaWVudGljIG5vdGF0aW9uCmF4ZXMuZm9ybWF0dGVyLmxpbWl0czogLTEsIDEKCiMgc2V0IHRleHQgb2JqZWN0cyBlZGlkYWJsZSBpbiBBZG9iZSBJbGx1c3RyYXRvcgpwZGYuZm9udHR5cGUgOiA0Mgpwcy5mb250dHlwZTogNDIKCiMgbm8gYmFja2dyb3VuZApzYXZlZmlnLnRyYW5zcGFyZW50OiBUcnVlCgojcmVtb3ZlIHdoaXRlIHNwYWNlcwpzYXZlZmlnLmJib3g6IHRpZ2h0CgojIHJlc29sdXRpb24gCmZpZ3VyZS5kcGk6IDQ1MAoKIyBubyBsYXRleCB1c2V0aAp0ZXh0LnVzZXRleDogRmFsc2UKCiMgZGVmYXVsdCBjb2xvciBjeWNsZQpheGVzLnByb3BfY3ljbGUgOiBjeWNsZXIoJ2NvbG9yJywgWyIwMDEyMTkiLCIwMDVmNzMiLCIwYTkzOTYiLCI5NGQyYmQiLCJlOWQ4YTYiLCJlZTliMDAiLCJjYTY3MDIiLCJiYjNlMDMiLCJhZTIwMTIiLCI5YjIyMjYiXSkgKyBjeWNsZXIoJ21hcmtlcicsIFsibyIsIm8iLCJvIiwibyIsIm8iLCJvIiwibyIsIm8iLCJvIiwibyJdKQoKCiMgcmVtb3ZlIGxlZ2VuZCBmcmFtZQpsZWdlbmQuZnJhbWVvbiA6IEZhbHNlCgojIHN2ZyBmb250IHR5cGUKc3ZnLmZvbnR0eXBlOiBub25lCg=="),
        "colorsblind34": "https://raw.githubusercontent.com/killiansheriff/LovelyPlots/master/lovelyplots/styles/colors/colorsblind34.mplstyle",
        "colorsblind34_Archive":mystring.string.of("I1JhaW1ib3cgZGlzY3JldGUgaHR0cHM6Ly9vYnNlcnZhYmxlaHEuY29tL0Bqb3Rhc29sYW5vL3BhdWwtdG9sLXNjaGVtZXMKCmF4ZXMucHJvcF9jeWNsZSA6IGN5Y2xlcignY29sb3InLCBbIkU4RUNGQiIsIkQ5Q0NFMyIsIkQxQkJENyIsIkNBQUNDQiIsIkJBOERCNCIsIkFFNzZBMyIsIkFBNkY5RSIsIjk5NEY4OCIsIjg4MkU3MiIsIjE5NjVCMCIsIjQzN0RCRiIsIjUyODlDNyIsIjYxOTVDRiIsIjdCQUZERSIsIjRFQjI2NSIsIjkwQzk4NyIsIkNBRTBBQiIsIkY3RjA1NiIsIkY3Q0I0NSIsIkY2QzE0MSIsIkY0QTczNiIsIkYxOTMyRCIsIkVFODAyNiIsIkU4NjAxQyIsIkU2NTUxOCIsIkRDMDUwQyIsIkE1MTcwRSIsIjcyMTkwRSIsIjQyMTUwQSJdKQ=="),
        "science":"https://raw.githubusercontent.com/garrettj403/SciencePlots/master/scienceplots/styles/science.mplstyle",
        "science_Archive":mystring.string.of("IyBNYXRwbG90bGliIHN0eWxlIGZvciBzY2llbnRpZmljIHBsb3R0aW5nCiMgVGhpcyBpcyB0aGUgYmFzZSBzdHlsZSBmb3IgIlNjaWVuY2VQbG90cyIKIyBzZWU6IGh0dHBzOi8vZ2l0aHViLmNvbS9nYXJyZXR0ajQwMy9TY2llbmNlUGxvdHMKCiMgU2V0IGNvbG9yIGN5Y2xlOiBibHVlLCBncmVlbiwgeWVsbG93LCByZWQsIHZpb2xldCwgZ3JheQpheGVzLnByb3BfY3ljbGUgOiBjeWNsZXIoJ2NvbG9yJywgWycwQzVEQTUnLCAnMDBCOTQ1JywgJ0ZGOTUwMCcsICdGRjJDMDAnLCAnODQ1Qjk3JywgJzQ3NDc0NycsICc5ZTllOWUnXSkKCiMgU2V0IGRlZmF1bHQgZmlndXJlIHNpemUKZmlndXJlLmZpZ3NpemUgOiAzLjUsIDIuNjI1CgojIFNldCB4IGF4aXMKeHRpY2suZGlyZWN0aW9uIDogaW4KeHRpY2subWFqb3Iuc2l6ZSA6IDMKeHRpY2subWFqb3Iud2lkdGggOiAwLjUKeHRpY2subWlub3Iuc2l6ZSA6IDEuNQp4dGljay5taW5vci53aWR0aCA6IDAuNQp4dGljay5taW5vci52aXNpYmxlIDogVHJ1ZQp4dGljay50b3AgOiBUcnVlCgojIFNldCB5IGF4aXMKeXRpY2suZGlyZWN0aW9uIDogaW4KeXRpY2subWFqb3Iuc2l6ZSA6IDMKeXRpY2subWFqb3Iud2lkdGggOiAwLjUKeXRpY2subWlub3Iuc2l6ZSA6IDEuNQp5dGljay5taW5vci53aWR0aCA6IDAuNQp5dGljay5taW5vci52aXNpYmxlIDogVHJ1ZQp5dGljay5yaWdodCA6IFRydWUKCiMgU2V0IGxpbmUgd2lkdGhzCmF4ZXMubGluZXdpZHRoIDogMC41CmdyaWQubGluZXdpZHRoIDogMC41CmxpbmVzLmxpbmV3aWR0aCA6IDEuCgojIFJlbW92ZSBsZWdlbmQgZnJhbWUKbGVnZW5kLmZyYW1lb24gOiBGYWxzZQoKIyBBbHdheXMgc2F2ZSBhcyAndGlnaHQnCnNhdmVmaWcuYmJveCA6IHRpZ2h0CnNhdmVmaWcucGFkX2luY2hlcyA6IDAuMDUKCiMgVXNlIHNlcmlmIGZvbnRzCiMgZm9udC5zZXJpZiA6IFRpbWVzCmZvbnQuZmFtaWx5IDogc2VyaWYKbWF0aHRleHQuZm9udHNldCA6IGRlamF2dXNlcmlmCgojIFVzZSBMYVRlWCBmb3IgbWF0aCBmb3JtYXR0aW5nCnRleHQudXNldGV4IDogVHJ1ZQp0ZXh0LmxhdGV4LnByZWFtYmxlIDogXHVzZXBhY2thZ2V7YW1zbWF0aH0gXHVzZXBhY2thZ2V7YW1zc3ltYn0="),
        "ieee": "https://raw.githubusercontent.com/garrettj403/SciencePlots/master/scienceplots/styles/journals/ieee.mplstyle",
        "ieee_Archive":mystring.string.of("IyBNYXRwbG90bGliIHN0eWxlIGZvciBJRUVFIHBsb3RzCiMgVGhpcyBzdHlsZSBzaG91bGQgd29yayBmb3IgbW9zdCB0d28tY29sdW1uIGpvdXJuYWxzCgojIFNldCBjb2xvciBjeWNsZQojIFNldCBsaW5lIHN0eWxlIGFzIHdlbGwgZm9yIGJsYWNrIGFuZCB3aGl0ZSBncmFwaHMKYXhlcy5wcm9wX2N5Y2xlIDogKGN5Y2xlcignY29sb3InLCBbJ2snLCAncicsICdiJywgJ2cnXSkgKyBjeWNsZXIoJ2xzJywgWyctJywgJy0tJywgJzonLCAnLS4nXSkpCgojIFNldCBkZWZhdWx0IGZpZ3VyZSBzaXplCmZpZ3VyZS5maWdzaXplIDogMy4zLCAyLjUKZmlndXJlLmRwaSA6IDYwMAoKIyBGb250IHNpemVzCmZvbnQuc2l6ZSA6IDgKZm9udC5mYW1pbHkgOiBzZXJpZgpmb250LnNlcmlmIDogVGltZXM=")
    }

    def mlb_reset():
        mpl.rcParams.update(mpl.rcParamsDefault)
        reset()

    def mlb_get_styles(folder="styles", style=None, use_archive=True):
        output = {}
        if not os.path.exists(folder):
            try:os.system("mkdir {0}".format(folder))
            except:pass

        for key,value in styles.items():
            if style is None or style == key:
                file_name = os.path.basename(value)+".mplstyle"
                file_loc = os.path.join(folder,file_name)

                if not os.path.exists(file_loc):
                    if use_archive:
                        with open(file_loc, "w+") as writer:
                            writer.write(value["Archive"])
                    else:
                        import urllib.request
                        urllib.request.urlretrieve(value["Link"], file_name)
                        try:os.system("mv {0} {1}".format(file_name, file_loc))
                        except:pass
        
                output[key] = os.path.abspath(file_loc)
        return output

    def mlb_help():
        print("""
* https://github.com/rougier/scientific-visualization-book
* [statworx-theme](https://github.com/STATWORX/statworx-theme)
* [LovelyPlots](https://github.com/killiansheriff/LovelyPlots)
* [SciencePlots](https://github.com/garrettj403/SciencePlots)
* [Paper-Themes](https://github.com/Dih5/paper-themes)
* [ExtensysPlots](https://github.com/mcekwonu/ExtensysPlots)
* [tueplots](https://github.com/pnkraemer/tueplots)
* [sciplot](https://github.com/andreasfuhr/sciplot)
* https://github.com/topics/matplotlib-style-sheets?l=python
* https://github.com/jbmouret/matplotlib_for_papers
* https://github.com/raybuhr/pyplot-themes
""")

    class matplotstyle(styleapplicator):
        def __init__(self, style='ipynb'):
            super().__init__()
            if style in ['ipynb', 'colorsblind34']:
                try:import lovelyplots
                except:mystring.imp("lovelyplots");import lovelyplots
            elif style in ['science', 'ieee']:
                try:import scienceplots
                except:mystring.imp("scienceplots");import scienceplots
            self.extra_context_caller = plt.style.context(style)
        def reset(self):
            try:
                from IPython import get_ipython;
                ipython = get_ipython()
                ipython.magic("matplotlib inline")
            except:pass
        def __enter__(self):
            self.extra_context_caller.__enter__()
            return self
        def __exit__(self,*args, **kwargs):
            self.extra_context_caller.__exit__()
        def __call__(self, some_figure_obj):
            return some_figure_obj
except:pass
try:
    def plt_default(default_theme="seaborn"):
        import plotly.io as pio
        pio.templates.default = default_theme

    def plt_style(**kwargs):
        font_keys = ['layout.font.family', 'layout.legend.font.family']
        font_size_keys = ['layout.font.size', 'layout.legend.font.size']

        style_dict = {
            'theme':'seaborn',
            'layout.plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'layout.font.family': common_defaults['Font'],
            'layout.font.size': common_defaults['Font_Size'],
            'layout.xaxis.linecolor': 'black',
            'layout.xaxis.ticks': 'outside',
            'layout.xaxis.mirror': True,
            'layout.xaxis.showline': True,
            'layout.xaxis.type':'-',#https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-type
            'layout.yaxis.linecolor': 'black',
            'layout.yaxis.ticks': 'outside',
            'layout.yaxis.mirror': True,
            'layout.yaxis.showline': True,
            'layout.autosize': True,
            'layout.showlegend': True,
            'layout.legend.bgcolor': 'rgba(0, 0, 0, 0)',
            'layout.legend.x': 1,
            'layout.legend.font.family': common_defaults['Font'],
            'layout.legend.font.size': common_defaults['Font_Size'],
            # Specialized:
            # 'layout.xaxis.range': (2.3, 2.5),
            'layout.yaxis.range': (0, +50),
            'layout.xaxis.title': r'$x$', #Latex Style
            'layout.yaxis.title': r'$y$', #Latex Style
            'layout.title': 'Advanced Example of a Line Plot with Plotly',
            'layout.title.xanchor': 'center',
            'layout.title.yanchor': 'top',
        }

        if "theme" in style_dict:
            plt_default(style_dict['theme'])
            del style_dict['theme']
        else:
            plt_default()

        for key,value in kwargs.items():
            key=key.replace('_','.')
            if key == 'font':
                for font_key in font_keys:
                    style_dict[font_key] = value
            elif key == 'size':
                for font_size_key in font_size_keys:
                    style_dict[font_size_key] = value
            elif key == 'xlabel':
                style_dict['layout.xaxis.title'] = value
            elif key == 'ylabel':
                style_dict['layout.yaxis.title'] = value
            elif key == 'title':
                style_dict['layout.title'] = value
            elif key == 'title.font.family':
                style_dict['layout.title.font.family'] = value
            elif key == 'title.text':
                style_dict['layout.title.text'] = value
            elif key == 'overall.title':
                style_dict['layout.title.text'] = value
            elif key == 'title.font.size':
                style_dict['layout.title.font.size'] = value
            elif key.startswith('subplot'):
                pass
            else:
                style_dict[key] = value
        return style_dict

    def plt_help():
        print("""
main inspirations
* https://gist.github.com/Miladiouss/e2f4fef284ebf8461752a769e6ec5864
* https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-type
              
* https://github.com/rougier/scientific-visualization-book
* [statworx-theme](https://github.com/STATWORX/statworx-theme)
* [plotly-scientific-plots](https://github.com/rsandler00/plotly-scientific-plots)
- General Page: https://plotly.com/python/scientific-charts/
- sample gist: https://gist.github.com/Miladiouss/e2f4fef284ebf8461752a769e6ec5864
+ maybe using a seaborn -type theme: https://onezero.blog/generate-publication-ready-plots-using-seaborn-library-part-1/
> Paper - http://conference.scipy.org.s3-website-us-east-1.amazonaws.com/proceedings/scipy2019/pdfs/shammamah_hossain.pdf
* website: https://plotly.com/python/templates/
""")

    class pltstyle(styleapplicator):
        def __init__(self, **kwargs):
            super().__init__()
            self.kwargs = {key:value for key,value in kwargs.items() if not key.startswith('subplot')}
            self.subplot_kwargs = {key:value for key,value in kwargs.items() if key.startswith('subplot')}
            self.set_env()
        def __enter__(self):
            return self.from_env()
        def __exit__(self,*args, **kwargs):
            self.set_env()
        def __call__(self, some_figure_obj):
            #https://plotly.com/python/subplots/
            some_figure_obj.update(
                plt_style(
                    **self.kwargs
                )
            )

            #Changing some per-plot settings since they're traces & annotations
            for key,value in self.subplot_kwargs.items():
                key=key.replace('_','.')
                settings = {}
                if key == "subplot.title.font.size":
                    settings['size'] = value
                elif key == "subplot.title.font.color":
                    settings['color'] = value
                elif key == "subplot.title.font.family":
                    settings['family'] = value
                    
                    #Setting all of the titles, they're all annotations?
                    #https://github.com/plotly/plotly.py/issues/985
                    #https://plotly.com/python/reference/layout/yaxis/
                    for i in fig['layout']['annotations']:
                        i['font'] = settings
            self.clear_screen()
            return some_figure_obj
        def __getitem__(self, key):
            if key in self.kwargs:
                return self.kwargs[key]
            elif key in self.subplot_kwargs:
                return self.subplot_kwargs[key]
            return None
        def __setitem__(self, key, value):
            if not key.startswith('subplot'):
                self.kwargs[key]=value
            else: #key.startswith('subplot'):
                self.subplot_kwargs[key]=value
        def __delitem__(self, key):
            if key in self.kwargs:
                del self.kwargs[key]
            elif key in self.subplot_kwargs:
                del self.subplot_kwargs[key]
        @property
        def total_items(self):
            return {
                **self.kwargs,
                **self.subplot_kwargs,
            }
        def __iter__(self):return iter(self.total_items.values())
        def __reversed__(self):return reversed(self.total_items.values())
        def __contains__(self, item):return item in self.total_items.keys()
        def items(self, key_filter=lambda x:True):return [(x, y) for x,y in self.total_items.items() if key_filter(x)]
        def keys(self, key_filter=lambda x:True):return [x for x in self.total_items.keys() if key_filter(x)]
        def values(self, key_filter=lambda x:True):return [self[x] for x in self.total_items.keys() if key_filter(x)]
        @property
        def to_json(self):
            import json
            return json.dumps(self.total_items)
        @staticmethod
        def from_json(json_string):
            import json
            return pltstyle(**json.loads(json_string))
        def set_env(self):
            import os,json
            os.environ["base_style"] = self.to_json
        @staticmethod
        def from_env():
            import os,json
            if "base_style" not in os.environ:
                pltstyle().set_env()
            return pltstyle.from_json(os.environ["base_style"])
except:pass

