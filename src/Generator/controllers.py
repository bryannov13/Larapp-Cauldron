from os import path as p
from os import makedirs
from .tools import get_file
from .tools import set_directory


class controller_generator():
    
    def __init__(self, model_name:str,fields:list,app_name:str="App"):
        self.txt = []
        self.fields=fields
        self.app_name = app_name
        self.model_name = model_name
        self._get_foreigns()
    
    def __set_default_dependencies(self):
        self.txt.append("<?php\n")
        self.txt.append("namespace "+self.app_name.capitalize()+"\Http\Controllers;\n") 
        #self.txt.append("use "+self.app_name.capitalize()+"\Http\Controllers\Controller;\n")
        self.txt.append("use "+self.app_name.capitalize()+"\Http\Requests\\"+self.model_name+"Request;\n")
        self.txt.append("use "+self.app_name.capitalize()+"\Models\\"+self.model_name+";\n")
        
        #Calling foreigns
        for f_key in self.foreigns: self.txt.append("use "+self.app_name.capitalize()+"\Models\\"+f_key['name'].capitalize()+";\n")

        self.txt.append("use Yajra\Datatables\Datatables;\n")
        self.txt.append("\n")
    
    def _get_foreigns(self):
        self.foreigns = []
        
        for i,field in enumerate(self.fields):
            #if i: arra_txt.append(',\n')
            
            if not (field['type'] == 'Integer' or 
                    field['type'] == 'String' or 
                    field['type'] == 'Floating' or 
                    field['type'] == 'Boolean' or 
                    field['type'] == 'DateTime'):
                
                self.foreigns.append({"name":field['type'], "title":field['name']})
        #print(self.foreigns)
    def set_file(self,path):
        if not p.exists(path): model_file = open(path,"x")
            
        else: model_file = open(path,"w")
        

        self.__set_default_dependencies()
        
        return model_file
        
    def create(self, path, default_fields=False):
        
        set_directory(path)
        path= path+"/"+str(self.model_name)+"Controller.php"
        file = self.set_file(path)
        
        #Controller class begin
        self.txt.append("//"+str(self.model_name)+"_model \n")
        self.txt.append("class "+self.model_name+"Controller extends Controller\n{\n")
        
        self.txt.append("\tfunction __construct(){parent::__construct('"+self.model_name+"');}\n\n")

        #index function
        self.txt.append("\tpublic function index()\n")
        self.txt.append("\t{\n")
        self.txt.append("\t\treturn view('"+self.app_name+"."+self.model_name+".index');\n")
        self.txt.append("\t}\n\n")
        
        #grid Function
        self.txt.append("\tpublic function grid("+self.model_name+"Request $request)\n")
        self.txt.append("\t{\n")
        self.txt.append("\t\t$records = "+self.model_name+"::select('*');\n")
        self.txt.append("\n\t\tif($request->inactive == 0) $records->where('status','1');\n\n")
        self.txt.append("\t\treturn Datatables::of($records)\n")
        self.txt.append("\t\t\t->addColumn('actions',function($record){\n")
        self.txt.append("\t\t\t\treturn view('common.buttons',[\n")
        self.txt.append("\t\t\t\t\t'record'     => $record,\n")
        self.txt.append("\t\t\t\t\t'url'        => '"+self.model_name+"',\n")
        self.txt.append("\t\t\t\t\t'permission' => '"+self.model_name+"',\n")
        self.txt.append("\t\t\t\t])->render();\n")
        self.txt.append("\t\t\t})\n")
        self.txt.append("\t\t\t->escapeColumns([])\n")
        self.txt.append("\t\t\t->make(true);\n")
        self.txt.append("\t}\n\n")
        

        #create function
        self.txt.append("\tpublic function create(){\n")
        self.txt.append("\t\t$action = 'add';\n")
        self.txt.append("\t\t$url    = '/"+self.model_name+"';\n")
        
        #foreigns
        for f_key in self.foreigns:self.txt.append("\t\t$"+f_key['name']+" = "+f_key['name']+"::all()->where('status','1');\n")
        
        self.txt.append("\n\t\treturn view('"+self.app_name+"."+self.model_name+".form',[\n")
        for f_key in self.foreigns:self.txt.append("\t\t\t'"+f_key['name']+"' => $"+f_key['name']+",\n")
        self.txt.append("\t\t\t'action' => $action,\n")
        self.txt.append("\t\t\t'url'    => $url\n")
        self.txt.append("\t\t]);\n")
        self.txt.append("\t}\n\n")
        
        #store Function
        self.txt.append("\tpublic function store("+self.model_name+"Request $request){\n")
        self.txt.append("\t\ttry {\n")
        self.txt.append("\t\t\t$item = new "+self.model_name+"($request->all());\n")
        self.txt.append("\t\t\t$item->save();\n")
        self.txt.append("\t\t\t$out = redirect('/"+self.model_name+"')->with('message', 'Información actualizada correctamente');\n")
        self.txt.append("\t\t}\n")
        self.txt.append("\t\tcatch (\Throwable $th) {$out = response()->json(['errors' => ['Bad Request']], 400);}\n")
        self.txt.append("\t\treturn $out;\n")
        self.txt.append("\t}\n\n")
        

        #show Function
        self.txt.append("\tpublic function show($id){\n")
        self.txt.append("\t\t$item = "+self.model_name+"::find($id);\n")
        self.txt.append("\t\t$action = 'show';\n")
        self.txt.append("\t\t$url    = '';\n")
        for f_key in self.foreigns:self.txt.append("\t\t$"+f_key['name']+" = "+f_key['name']+"::all()->where('status','1');\n")
        self.txt.append("\n\t\treturn view('"+self.app_name+"."+self.model_name+".form', [\n")
        for f_key in self.foreigns:self.txt.append("\t\t\t'"+f_key['name']+"' => $"+f_key['name']+",\n")
        self.txt.append("\t\t\t'record' => $item,\n")
        self.txt.append("\t\t\t'action' => $action,\n")
        self.txt.append("\t\t\t'url'    => $url,\n")
        self.txt.append("\t\t\t'action_title' => 'Ver'\n")
        self.txt.append("\t\t]);\n")
        self.txt.append("\t}\n\n")        
        
        #edit function
        self.txt.append("\tpublic function edit($id){\n")
        self.txt.append("\t\t$item = "+self.model_name+"::find($id);\n")
        self.txt.append("\t\t$action = 'edit';\n")
        self.txt.append("\t\t$url    = '/"+self.model_name+"/'.$item->id;\n")
        for f_key in self.foreigns:self.txt.append("\t\t$"+f_key['name']+" = "+f_key['name']+"::all()->where('status','1');\n")
        self.txt.append("\n\t\treturn view('"+self.app_name+"."+self.model_name+".form', [\n")
        for f_key in self.foreigns:self.txt.append("\t\t\t'"+f_key['name']+"' => $"+f_key['name']+",\n")
        self.txt.append("\t\t\t'record' => $item,\n")
        self.txt.append("\t\t\t'action' => $action,\n")
        self.txt.append("\t\t\t'url'    => $url,\n")
        self.txt.append("\t\t\t'action_title' => 'Editar'\n")
        self.txt.append("\t\t]);\n")
        self.txt.append("\t}\n\n")
        
        #update function
        self.txt.append("\tpublic function update($id, "+self.model_name+"Request $request){\n")
        self.txt.append("\t\t$item = "+self.model_name+"::find($id);\n")
        self.txt.append("\t\tif($item){\n")
        self.txt.append("\t\t\t$item->fill($request->all());\n")
        self.txt.append("\t\t\t$item->save();\n")
        self.txt.append("\t\t\t$out = redirect('/"+self.model_name+"')->with('message', 'Información actualizada correctamente');\n")
        self.txt.append("\t\t}\n")
        self.txt.append("\t\telse $out = response()->json(['errors' => ['Item not found']], 404);\n\n")
        self.txt.append("\t\treturn $out;\n")
        self.txt.append("\t}\n\n")

        #destroy function
        self.txt.append("\tpublic function destroy($id){\n")
        self.txt.append("\t\t$item = "+self.model_name+"::find($id);\n")
        self.txt.append("\t\tif($item){\n")
        self.txt.append("\t\t\t$item->status = 0;\n")
        self.txt.append("\t\t\t$item->save();\n")
        self.txt.append("\t\t\t$out = response()->json(['data' => $item, 'status' => 200], 200);\n")
        self.txt.append("\t\t}\n")
        self.txt.append("\t\telse $out = response()->json(['errors' => ['Item not found']], 404);\n\n")
        self.txt.append("\t\treturn $out;\n")
        self.txt.append("\t}\n\n")
        
        #recover function
        self.txt.append("\tpublic function recover($id){\n")
        self.txt.append("\t\t$item = "+self.model_name+"::find($id);\n")
        self.txt.append("\t\tif($item){\n")
        self.txt.append("\t\t\t$item->status = 1;\n")
        self.txt.append("\t\t\t$item->save();\n")
        self.txt.append("\t\t\t$out = response()->json(['data' => $item, 'status' => 200], 200);\n")
        self.txt.append("\t\t}\n")
        self.txt.append("\t\telse $out = response()->json(['errors' => ['Item not found']], 404);\n\n")
        self.txt.append("\t\treturn $out;\n")
        self.txt.append("\t}\n\n")
        

        #Controller class close
        self.txt.append("}\n")
        self.txt.append("?>\n")
        
        file.writelines(self.txt)
        pass
    pass

class Controllers_Generator(object):
    def __init__(self,app:object,project_name,out_path):
        
        for m in app["tables"]:
            print("Controlling "+m["name"]+" model ...")
            model_ = controller_generator(m["name"],m['fields'],app["name"])
            model_.create(path= out_path+project_name+"/"+app["name"]+"/Http/Controllers",default_fields=True)
            #model_.set_fields(m["fields"])
        
    pass

if __name__ == "__main__":
    
    from json import load
    try:
        app= load(open('../../json_examples/trucks_admin.json'))
        a = Controllers_Generator(app,'project','../../out/')
    except Exception as e:
        print(e)
    
    
