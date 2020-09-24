from os import path as p
from os import makedirs
from .tools import get_file
from .tools import set_directory


class route_generator():
    
    def __init__(self, model_name:str,fields:list,app_name:str="App"):
        self.txt = []
        self.fields=fields
        self.app_name = app_name
        self.model_name = model_name
        
    
    def __set_default_dependencies(self):
        self.txt.append("<?php\n\n")
        #self.txt.append("namespace "+self.app_name+"\Http\Controllers;\n") #aqui hay que cambiar "app" por el nombre de la aplicacion
        #self.txt.append("use Illuminate\Http\\"+self.model_name+"Request;\n")
        #self.txt.append("use "+self.app_name+"\Models\\"+self.model_name+";\n")#revisr si va el doble diagonal
        #self.txt.append("use Yajra\Datatables\Datatables;\n")
        #self.txt.append("\n")

    
    def _set_fields(self,default_fields:bool=True)->list:
        arra_txt = []
        if len(self.fields)>0:
            for i,field in enumerate(self.fields):
                if i: arra_txt.append(",\n")
                arra_txt.append("\t\t\t\t{data: '"+field['name']+"', name: '"+field['name']+"', title: '"+field['name']+"'}")
        
        if default_fields: arra_txt.extend(self.__set_default_fields())
            
        return arra_txt
    
    def __set_default_fields(self)->list: return [",\n\t\t\t\t{data: 'actions', searchable: false, title: 'Acciones'}\n"]
        
        
    def create_file(self,path):
        if not p.exists(path): 
            model_file = open(path,"x")
            self.__set_default_dependencies()
            
        else: model_file = open(path,"a")
        return model_file

    def readFile(self,path):

        pass

    def create(self, path, default_fields=False):
        
        set_directory(path)
        path= path+"/"+str(self.app_name)+".php"
        file = self.create_file(path)
        
        #lines = file.readlines()
        #print(lines)
        
    
        self.txt.append("//"+str(self.model_name)+"_model \n")
        
        
        self.txt.append("Route::prefix('"+self.app_name+"')->group(function () {\n")
        self.txt.append("\tRoute::get('/"+self.model_name+"/grid', '"+self.model_name+"Controller@grid');\n")
        self.txt.append("\tRoute::put('/"+self.model_name+"/{id}/recover', '"+self.model_name+"Controller@recover');\n")
        self.txt.append("\tRoute::resource('/"+self.model_name+"','"+self.model_name+"Controller');\n")
        self.txt.append("});\n\n")
        

        file.writelines(self.txt)
        pass
    pass

class Routes_Generator(object):
    def __init__(self,app:object,project_name,out_path):
        
        for m in app["tables"]:
            print("Routing "+m["name"]+" model ...")
            model_ = route_generator(m["name"],m['fields'],app["name"])
            model_.create(path= out_path+project_name+"/routes/apps/"+app["name"],default_fields=True)
            #model_.set_fields(m["fields"])
        try:
                pass
        except Exception as e:
            print("Js file:\n")
            print(e)
            pass
                
        
    pass

if __name__ == "__main__":
    
    from json import load
    try:
        app= load(open('../../json_examples/trucks_admin.json'))
        a = Routes_Generator(app,'project','../../out/')
    except Exception as e:
        print(e)
    
    
