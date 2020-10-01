from os import path as p
from os import makedirs
from .tools import get_file
from .tools import set_directory

from datetime import datetime

class migration_generator():
    
    def __init__(self, model_name:str,fields:list,app_name:str="app"):
        self.txt = []
        self.fields=fields
        self.model_name = model_name
        self.app_name = app_name
        
    def __set_default_dependencies(self):
        self.txt.append("<?php\n")
        self.txt.append("use Illuminate\Support\Facades\Schema;\n")
        self.txt.append("use Illuminate\Database\Schema\Blueprint;\n")
        self.txt.append("use Illuminate\Database\Migrations\Migration;\n")
        self.txt.append("\n")
        self.txt.append("class CreateMainTablesMigration extends Migration {\n")
        
    def __closeFile(self): self.txt.append("\n}\n")
    
    def _set_fields(self,default_fields:bool=True)->list:
        arra_txt = []
        arra_txt.append("\t\t\t$table->bigIncrements('id');\n")
        for i,field in enumerate(self.fields):
            
            if field['type'] == 'Integer': arra_txt.append("\t\t\t$table->integer('"+field['name']+"');\n")
            elif field['type'] == 'Floating': arra_txt.append("\t\t\t$table->float('"+field['name']+"', 8, 2);\n")
            elif field['type'] == 'Boolean': arra_txt.append("\t\t\t$table->boolean('"+field['name']+"');\n")
            elif field['type'] == 'String': arra_txt.append("\t\t\t$table->string('"+field['name']+"',100);\n")
            elif field['type'] == 'DateTime': arra_txt.append("\t\t\t$table->dateTime('"+field['name']+"',0);\n")
            else: 
                arra_txt.append("\t\t\t$table->unsignedBigInteger('"+field['name']+"');\n")
                arra_txt.append("\t\t\t$table->foreign('"+field['name']+"')->references('id')->on('"+field['type']+"');\n")
        
        if default_fields: arra_txt.extend(self.__set_default_fields())
            
        return arra_txt
        
    def __set_default_fields(self)->list: return ["\t\t\t$table->boolean('status')->default(1);\n","\n\t\t\t$table->timestamps();\n"]
        
    def set_file(self,path):
        if not p.exists(path):
            model_file = open(path,"x")
            self.__set_default_dependencies()
            
        else:
            model_file = open(path,"a")
            pass
        
        return model_file
        
    def create(self, path:str="./result", default_fields:bool=False,close:bool = False):
        
        set_directory(path)
        path= path+"/"+datetime.now().strftime("%Y_%m_%d_%H%M%S")+"_create_main_tables_migration.php"
        file = self.set_file(path)
        
        self.txt.append("//"+str(self.model_name)+"_model \n")
        #up function
        self.txt.append("\t\tSchema::create('"+self.model_name.lower()+"', function (Blueprint $table) {\n")
        self.txt.extend(self._set_fields())
        #print(self.txt)
        self.txt.append("\t\t});\n")#schema close
        self.txt.append("\n\t}\n") #Close

        #down function
        self.txt.append("\tpublic function down()\n\t{\n")#open
        self.txt.append("\t\tSchema::dropIfExists('"+self.model_name.lower()+"');\n")
        self.txt.append("\n\t}\n") #Close


        if close: self.__closeFile()
        file.writelines(self.txt)
        pass
    pass

class Migrations_Generator(object):
    def __init__(self,app:object,project_name,out_path):
        
        for m in app["tables"]:
            print("Cooking "+m["name"]+" model ...")
            migration_generator(m["name"],m['fields']).create(path= out_path+project_name+"/database/migrations",default_fields=True,close = (m == app["tables"][-1]))
            #model_.set_fields(m["fields"])
        

if __name__ == "__main__":
    
    from json import load
    try:
        app= load(open('../../json_examples/trucks_admin.json'))
        a = Migrations_Generator(app,'project','../../out/')
    except Exception as e:
        print(e)
    
    
