from os import path as p
from os import makedirs
from tools import get_file
from tools import set_directory


class request_generator():
    
    def __init__(self, model_name:str,fields:list,app:str="App"):
        self.txt = []
        self.fields=fields
        self.model_name = model_name
        self.app_name = app
        
    
    

    def __set_default_dependencies(self):
        self.txt.append("<?php\n")
        self.txt.append("namespace "+str(self.app_name)+"\Http\Requests;\n")
        self.txt.append("use Illuminate\Foundation\Http\FormRequest;\n")
        self.txt.append("\n")
    
    def _set_fields(self,default_fields:bool=True)->list:
        arra_txt = []
        
        for i,field in enumerate(self.fields):
            if i: arra_txt.append(',\n')
            if field['type'] == 'Integer': arra_txt.append("\t\t\t\t\t'"+field['name']+"' => 'required|integer|max:9999|min:0'")
            elif field['type'] == 'String': arra_txt.append("\t\t\t\t\t'"+field['name']+"' => 'required|string|max:255'")
            elif field['type'] == 'Floating': arra_txt.append("\t\t\t\t\t'"+field['name']+"' => 'required|numeric|max:9999|min:0'")
            #elif field['type'] == 'Boolean': arra_txt.append("\t\t\t$table->boolean('"+field['name']+"');\n")
            elif field['type'] == 'DateTime': arra_txt.append("\t\t\t\t\t'"+field['name']+"' => 'required|date|max:9999|min:0'")
            else: 
                arra_txt.append("\t\t\t\t\t'"+field['name']+"' => 'required'")
        
        #if default_fields: arra_txt.extend(self.__set_default_fields())
            
        return arra_txt
        
    def __set_default_fields(self)->list: return ["\t\t\t$table->boolean('status');\n","\n\t\t\t$table->timestamps();\n"]
        
    def set_file(self,path):
        if not p.exists(path):
            model_file = open(path,"x")
            self.__set_default_dependencies()
            
        else:
            model_file = open(path,"a")
            pass
        
        return model_file
        
    def create(self, path="./result", default_fields=False):
        
        set_directory(path)
        path= path+"/"+str(self.model_name)+"Request.php"
        file = self.set_file(path)
        self.txt.append("//"+str(self.model_name)+"_model \n")
        self.txt.append("class "+self.model_name+"Request extends FormRequest\n{\n\n")
        
        self.txt.append("\tpublic function authorize(){return true;}\n\n")

        #up function
        self.txt.append("\tpublic function rules()\n\t{\n")#open
        self.txt.append("\t\tswitch($this->method()){\n")
        self.txt.append("\t\t\tcase 'GET':\n")
        self.txt.append("\t\t\tcase 'DELETE':{return [];}\n")
        self.txt.append("\t\t\tcase 'POST':{\n")
        self.txt.append("\t\t\t\treturn [\n")
        self.txt.extend(self._set_fields())
        #print(self.txt)
        #self.txt.append("\t\t\t\t\n];\n")
        self.txt.append("\n\t\t\t\t];\n\t\t\t}\n")
        self.txt.append("\t\t\tcase 'PUT':\n")#schema close
        self.txt.append("\t\t\tcase 'PATCH':{\n")#schema close
        self.txt.append("\t\t\t\treturn [\n")#schema close
        self.txt.extend(self._set_fields())
        self.txt.append("\n\t\t\t\t];\n")
        self.txt.append("\t\t\t}\n")#schema close
        self.txt.append("\t\t\tdefault:break;\n")#schema close
        self.txt.append("\t\t}\n")#schema close
        self.txt.append("\t}\n")#schema close
        self.txt.append("}\n")#schema close
        
        file.writelines(self.txt)
        pass
    pass

class Requests_Generator(object):
    def __init__(self,app:object,project_name,out_path):
        
        for m in app["tables"]:
            print("Requesting "+m["name"]+" model ...")
            model_ = request_generator(m["name"],m['fields'],app['name'])
            model_.create(path= out_path+project_name+"/"+app["name"]+"/Http/Request",default_fields=True)
            #model_.set_fields(m["fields"])
        try:
            pass
        except Exception as e:
            print("Models:\n")
            print(e)
            pass
                
        
    pass

if __name__ == "__main__":
    
    from json import load
    try:
        app= load(open('../../json_examples/trucks_admin.json'))
        a = Requests_Generator(app,'project','../../out/')
    except Exception as e:
        print(e)
    
    
