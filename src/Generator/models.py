from os import path as p
from os import makedirs
from generator import generator
class model_generator(generator):
    
    def __init__(self, model_name,fields):
        super().__init__(model_name,fields)

    def _set_default_dependencies(self):
        super()._set_default_dependencies()
        self.txt.append("namespace App\Models;\n")
        self.txt.append("use Illuminate\Database\Eloquent\Model;\n")
        self.txt.append("\n")
    
    def __get_fields(self)->list:
        txt_fields = []
        if len(self.fields)>0:
            for i,field in enumerate(self._allFields):
                if i: txt_fields.append(",\n")
                txt_fields.append("\t\t'"+str(field["name"])+"'")
        return txt_fields
        
    def __set_default_fields(self): return "\n\tprotected $hidden = ['created_at', 'updated_at', 'status'];\n\n"
        
    
    def create(self, path="./result", default_fields=False):
        
        self._create_directory(path)

        path= path+"/"+self.model_name.capitalize()+".php"
            
        model_file = self._set_file(path,True)
        
        self.txt.append("#"+str(self.model_name)+"_model \n")
        self.txt.append("class "+self.model_name+" extends Model\n{\n\n")
        
        self.txt.append("\tprotected $table= '"+self.model_name.lower()+"';\n\n")
        self.txt.append("\tprotected $fillable = [\n")

        self.txt.extend(self.__get_fields())
        self.txt.append( "\n\t\t];\n")

        if default_fields: self.txt.append(self.__set_default_fields())
        
        for fk in self.foreigns:
            self.txt.append("\tpublic function "+fk['type'].lower()+"()\n")
            self.txt.append("\t{\n")
            self.txt.append("\t\treturn $this->BelongsTo('App\Models\\"+fk['type'].capitalize()+"','"+fk['name']+"');\n")
            self.txt.append("\t}\n")
            pass

        self.txt.append("}")

        model_file.writelines(self.txt)
        pass
    pass

class Models_Generator(object):
    def __init__(self,app,project_name,out_path):
        
        for m in app["tables"]:
            print("Cooking "+m["name"]+" model ...")            
            model_ = model_generator(m["name"],m["fields"])
            
            model_.create(path= out_path+project_name+"/"+app["name"]+"/Models",default_fields=True)
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
        a = Models_Generator(app,'project','../../out/')
    except Exception as e:
        print(e)
    
    
