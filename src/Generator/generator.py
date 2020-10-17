
from os import path as p
from os import makedirs

class generator():
    
    def __init__(self, model_name,fields):
        self.model_name = model_name
        self.fields = []
        self.foreigns = []


        self.txt = []

    def _separate_foreigns(self):
        self.foreigns = []
        
        for i,field in enumerate(self.fields):
            
            if not (field['type'] == 'Integer' or 
                    field['type'] == 'String' or 
                    field['type'] == 'Floating' or 
                    field['type'] == 'Boolean' or 
                    field['type'] == 'DateTime'):
                
                self.foreigns.append(field)
            else:
                self.fields
    
    def _set_file(self,path:str,overwrite:bool=False)->stream:
        if overwrite:
            if not p.exists(path): model_file = open(path,"x")
            else: model_file = open(path,"w")
            self.__set_default_dependencies()
            
        else:
            if not p.exists(path):
                model_file = open(path,"x")
                self.__set_default_dependencies()
            
            else: model_file = open(path,"a")
            
        
        return model_file
        pass

    def _set_default_dependencies(self):
        self.txt.append("<?php\n")

    def _set_default_fields(self): pass
    