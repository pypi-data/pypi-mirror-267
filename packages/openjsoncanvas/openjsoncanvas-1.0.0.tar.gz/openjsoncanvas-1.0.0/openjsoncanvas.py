"""A python implmentation of the JsonCanvas format: https://github.com/obsidianmd/jsoncanvas/blob/main/spec/1.0.md"""
import dataclasses
import json
import pathlib
import re
import typing
__version__: str = '1.0.0'

camel_to_name = lambda x: re.sub(r'(?<!^)(?=[A-Z])', '_', x).lower()

class CanvasData(typing.MutableMapping):
    __getattr__ = __getitem__ = lambda self, key: super().__getattribute__(camel_to_name(key))
    __setattr__ = __setitem__ = lambda self, key, value: super().__setattr__(camel_to_name(key), value)
    __delattr__ = __delitem__ = lambda self, key: super().__delattr__(camel_to_name(key))
    __len__ = lambda self: len(self.__dict__)
    __contains__ = lambda self, key: camel_to_name(key) in self.__dict__
    __iter__ = lambda self: iter(self.__dict__)

    def __new__(cls, *args, **kwargs):
        if cls.__name__ in ['CanvasData', 'Node']:
            raise TypeError(f'Cannot instantiate {cls.__name__} directly')
        if not dataclasses.is_dataclass(cls):
            raise TypeError(f'{cls.__name__} is not a dataclass')
        return super().__new__(cls)

@dataclasses.dataclass(kw_only=True)
class Node(CanvasData):
    id: str
    type: str
    x: int
    y: int
    width: int
    height: int
    color: typing.Optional[str] = None

@dataclasses.dataclass(kw_only=True)
class TextNode(Node):
    text: str
    type: str = 'text'
    
    
@dataclasses.dataclass(kw_only=True)
class FileNode(Node):
    file: str
    type: str = 'file'
    subpath: typing.Optional[str] = None
    
@dataclasses.dataclass(kw_only=True)
class LinkNode(Node):
    url: str
    type: str = 'link'
    
@dataclasses.dataclass(kw_only=True)
class GroupNode(Node):
    type: str = 'group'
    label: typing.Optional[str] = None
    background: typing.Optional[str] = None
    backgroundStyle: typing.Optional[str] = None
    
@dataclasses.dataclass(kw_only=True)
class Edge(CanvasData):
    id: str
    fromNode: str
    fromSide: typing.Optional[str] = None
    fromEnd: typing.Optional[str] = None
    toNode: str
    toSide: typing.Optional[str] = None
    toEnd: typing.Optional[str] = None
    color: typing.Optional[str] = None
    label: typing.Optional[str] = None
    
@dataclasses.dataclass(kw_only=True)
class Canvas:
    nodes: typing.List[Node] = dataclasses.field(default_factory=list)
    edges: typing.List[Edge] = dataclasses.field(default_factory=list)
    
    def to_json(self):
        return json.dumps(
                {
                        name: [dict(filter(lambda x: x[1] is not None, dataclasses.asdict(obj).items())) for obj in
                               getattr(self, name)]
                        for name in ['nodes', 'edges']
                },
                indent=4
        )
    
    def add_node(self, node):
        self.nodes.append(node)
        return self
    
    def add_edge(self, edge):
        self.edges.append(edge)
        return self
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
                nodes=[globals()[node_data['type'].title() + 'Node'](**node_data) for node_data in (data).get('nodes', [])], 
                edges=[Edge(**edge_data) for edge_data in data.get('edges', [])]
        )
    
    def to_file(self, path):
        path = pathlib.Path(path)
        path.write_text(self.to_json())
        
    @classmethod
    def from_file(cls, path):
        path = pathlib.Path(path)
        content = path.read_text()
        if not content:
            return cls()
        return cls.from_json(content)

    
if __name__ == '__main__':
    path = r"G:\vault\Wiki\Untitled.canvas"
    canvas = Canvas.from_file(path)
    canvas.add_node(TextNode(id='1', x=100, y=100, width=100, height=100, text='Hello World'))
    canvas.to_file(path)
