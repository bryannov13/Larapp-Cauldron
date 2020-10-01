from os import path as p
from os import makedirs

class model_generator():
    
    def __init__(self, model_name):
        self.txt=[]
        self.fields=[]
        self.model_name = model_name
    
    

    def __set_default_dependencies(self):
        self.txt.append("<?php\n")
        self.txt.append("namespace App\Models;\n")
        self.txt.append("use Illuminate\Database\Eloquent\Model;\n")
        self.txt.append("\n")
    
    def set_fields(self,fields)->list:
        if len(fields)>0:
            for i,field in enumerate(fields):
                if i: self.fields.append(",\n")
                self.fields.append("\t\t'"+str(field["name"])+"'")
        
        
    
    def __set_default_fields(self): return "\n\tprotected $hidden = ['created_at', 'updated_at', 'status'];\n"
        
    
    def set_file(self,path):
        if not p.exists(path):
            model_file = open(path,"x")
            self.__set_default_dependencies()
            
        else:
            model_file = open(path,"a")
            pass
        
        return model_file
        pass
    
    def create(self, path="./result", default_fields=False):
        
        if not p.exists(path) :
            makedirs(path,0o777)
        path= path+"/"+self.model_name+".php"
            
        model_file = self.set_file(path)
        
        self.txt.append("#"+str(self.model_name)+"_model \n")
        self.txt.append("class "+self.model_name+" extends Model\n{\n\n")
        
        self.txt.append("\tprotected $table= '"+self.model_name.lower()+"';\n\n")
        self.txt.append("\tprotected $fillable = [\n")
        self.txt = self.txt + self.fields
        self.txt.append( "\n\t\t];\n")

        if default_fields: self.txt.append(self.__set_default_fields())
        
        
        
        self.txt.append("\n}")

        model_file.writelines(self.txt)
        pass
    pass

class Models_Generator(object):
    def __init__(self,app,project_name,out_path):
        
        for m in app["tables"]:
            print("Cooking "+m["name"]+" model ...")            
            model_ = model_generator(m["name"])
            model_.set_fields(m["fields"])
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
    
    
