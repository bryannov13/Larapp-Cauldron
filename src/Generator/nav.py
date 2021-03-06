from os import path as p
from os import makedirs
from tools import get_file
from tools import set_directory


class js_generator():
    
    def __init__(self, model_name:str,fields:list,app_name:str="App"):
        self.txt = []
        self.fields=fields
        self.app_name = app_name
        self.model_name = model_name
        
    
    def __set_default_dependencies(self):
        self.txt.append("<?php\n")
        self.txt.append("namespace "+self.app_name+"\Http\Controllers;\n") #aqui hay que cambiar "app" por el nombre de la aplicacion
        self.txt.append("use Illuminate\Http\\"+self.model_name+"Request;\n")
        self.txt.append("use "+self.app_name+"\Models\\"+self.model_name+";\n")#revisr si va el doble diagonal
        self.txt.append("use Yajra\Datatables\Datatables;\n")
        self.txt.append("\n")
    
    def _set_fields(self,default_fields:bool=True)->list:
        arra_txt = []
        if len(self.fields)>0:
            for i,field in enumerate(self.fields):
                if i: arra_txt.append(",\n")
                arra_txt.append("\t\t\t\t{data: '"+field['name']+"', name: '"+field['name']+"', title: '"+field['name']+"'}")
        
        if default_fields: arra_txt.extend(self.__set_default_fields())
            
        return arra_txt
    
    def __set_default_fields(self)->list: return [",\n\t\t\t\t{data: 'actions', searchable: false, title: 'Acciones'}\n"]
        
        
    def set_file(self,path):
        if not p.exists(path): model_file = open(path,"x")
            
        else: model_file = open(path,"w")
        

        #self.__set_default_dependencies()
        
        return model_file
        
    def create(self, path, default_fields=False):
        
        set_directory(path)
        path= path+"/log.php.bak"
        file = self.set_file(path)
        
        
        self.txt.append("//"+str(self.model_name)+"_model \n")
        self.txt.append("var repository= new Repository();\n")
        self.txt.append("var dataTable=null;\n\n")

        #Ready function
        self.txt.append("$(document).ready(function() {\n")
        self.txt.append("\tall();\n")
        self.txt.append("\t$('#showInactive').change(function() {dataTable.draw();});\n")
        self.txt.append("});\n\n")
        
        #all function
        self.txt.append("function all(){\n")
        self.txt.append("\tdataTable=$('#"+str(self.model_name)+"-table').DataTable({\n")
        self.txt.append("\t\t\t'processing': true,\n")
        self.txt.append("\t\t\t'serverSide': true,\n")
        self.txt.append("\t\t\t'ajax':{\n")
        self.txt.append("\t\t\t\turl: '/"+str(self.model_name)+"/grid',\n")
        self.txt.append("\t\t\t\tdata:function(d){\n")
        self.txt.append("\t\t\t\t\td.inactive=($('#showInactive').is(':checked'))?'1':'0';\n")
        self.txt.append("\t\t\t\t}\n")
        self.txt.append("\t\t\t},\n")
        self.txt.append("\t\t\t'columns': [\n")
        self.txt.extend(self._set_fields())
        self.txt.append("\t\t\t]\n")
        self.txt.append("\t\t});\n")
        self.txt.append("}\n")
        
        file.writelines(self.txt)
        pass
    pass
#Esto debe de ser un generador de Modules Table Seeder
class Nav_Generator(object):
    def __init__(self,app:object,project_name,out_path):
        self.path= out_path+project_name+"/resources/"+"nav.php.bak"
        set_directory(out_path+project_name+"/resources/")
        self.file = self.set_file()
        self.arr_txt = []

        print("Creando archivo nav.php.bak ...")
        for i,m in enumerate(app["tables"]):
            #if i: self.arr_txt.append(",\n")
            try: title = m['title']
            except: title = m['name']

            self.arr_txt.append("\t\t\t\t\t@if(auth()->user()->hasPermission('Ver-"+m["name"]+"'))\n")
            self.arr_txt.append('\t\t\t\t\t\t<li class="nav-item">\n')
            self.arr_txt.append('\t\t\t\t\t\t\t<a class="nav-link nav-item-pos" href="{{url("/'+m["name"]+'")}}">\n')
            self.arr_txt.append('\t\t\t\t\t\t\t\t<span class="sidebar-mini">'+title[0]+'</span>\n')
            self.arr_txt.append('\t\t\t\t\t\t\t\t<span class="sidebar-normal">'+title+'</span>\n')
            self.arr_txt.append('\t\t\t\t\t\t\t</a>\n')
            self.arr_txt.append('\t\t\t\t\t\t</li>\n')
            self.arr_txt.append('\t\t\t\t\t@endif\n')

        self.file.writelines(self.arr_txt)
        
    pass
    def set_file(self):
        if not p.exists(self.path): model_file = open(self.path,"x")
            
        else: model_file = open(self.path,"w")
        
        return model_file
        

if __name__ == "__main__":
    
    from json import load
    try:
        app= load(open('../../json_examples/trucks_admin.json'))
        a = Nav_Generator(app,'project','../../out/')
    except Exception as e:
        print(e)
    
    
