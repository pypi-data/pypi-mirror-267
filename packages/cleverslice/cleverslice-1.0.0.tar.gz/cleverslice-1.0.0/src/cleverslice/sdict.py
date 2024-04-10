
class sdict:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        if isinstance(key, slice):
            keys = list(self.data)[key]
            sliced_data = {k: self.data[k] for k in keys}
            return sdict(sliced_data)  
        elif isinstance(key, int):
            try:
                k = list(self.data)[key]
                return self.data[k]
            except IndexError:
                raise IndexError("sdict index out of range")
        else:
             raise TypeError(f"Key of type {type(key).__name__} is not supported.")
    
    def __setitem__(self, key, value):
        # 这个方法允许直接通过键赋值来修改或添加元素
        self.data[key] = value
        
    def __repr__(self):
        return f'{self.data}'
    
    def __iter__(self):
        '''f, l, f, source_code = traceback.extract_stack()[0]
        if 'pd.DataFrame' in source_code:
            raise Exception('Please use pd.DataFrame(my_dict.data) to create a DataFrame')
        else:'''
        return iter(self.data)
        
    def __str__(self):
        return str(self.data)
    
    def __len__(self):
        return len(self.data)
    
    def items(self):
        # 生成并返回一个迭代器，它产生键值对元组
        print(f'items')
        return iter(self.data.items())
    
    def update(self, *args, **kwargs):
        # 对于传入的字典
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self.data[k] = v

        # 对于传入的关键字参数
        for k, v in kwargs.items():
            self.data[k] = v
    
    def pop(self, key, default=None):
        # 尝试从字典中删除键，如果键不存在，返回默认值或抛出 KeyError
        try:
            value = self.data[key]
            del self.data[key]
            return value
        except KeyError:
            if default is not None:
                return default
            else:
                raise KeyError(f"Key '{key}' not found in sdict.")

    def popitem(self):
        try:
            # 从Python 3.7开始，字典是有序的，所以popitem会弹出最后一个添加的项
            item = self.data.popitem()
            return item
        except KeyError:
            # 如果字典为空，抛出KeyError
            raise KeyError("sdict is empty, cannot popitem.")
        
    def clear(self):
        self.data.clear()

