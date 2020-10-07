from Generator.controllers import Controllers_Generator
from Generator.js import Js_Generator
from Generator.migrations import Migrations_Generator
from Generator.models import Models_Generator
from Generator.request import Requests_Generator
from Generator.routes import Routes_Generator
from Generator.views import Views_Generator

from json import load
from shutil import rmtree

class projectGenerator():
    def __init__(self, input_path:str, out_path:str='../out/', project_name:str = 'project'):
        #self.app = App
        self.app= load(open(input_path))
        self.out_path = out_path
        self.project_name = project_name
        pass

    def createControllers(self): Controllers_Generator(self.app,self.project_name,self.out_path)
        
    def createJs(self): Js_Generator(self.app,self.project_name,self.out_path)
        
    def createMigrations(self): Migrations_Generator(self.app,self.project_name,self.out_path)
        
    def createModels(self): Models_Generator(self.app,self.project_name,self.out_path)
        
    def createRequest(self): Requests_Generator(self.app,self.project_name,self.out_path)
        
    def createRoutes(self): Routes_Generator(self.app,self.project_name,self.out_path)
        
    def createViews(self): Views_Generator(self.app,self.project_name,self.out_path)
        
    def start(self):
        if self.verify_foreigns():
            try:
                self.createControllers()
                self.createJs()
                self.createMigrations()
                self.createModels()
                self.createRequest()
                self.createRoutes()
                self.createViews()
            except Exception as e:
                print(e)
                rmtree(self.out_path+"/"+self.project_name)

    def verify_foreigns(self)->bool:
        tables = []
        foreigns = []
        status = True
        
        #Recolectar nombres de tablas
        for t in self.app['tables']: tables.append(t['name'])

        #Recolectar tipos de foreigns
        for t in self.app['tables']:
            for f in t['fields']:
                if not (f['type'] == 'String' or 
                        f['type'] == 'Integer' or 
                        f['type'] == 'Floating' or 
                        f['type'] == 'DateTime' or 
                        f['type'] == 'Boolean'):
                    foreigns.append(f['type'])
        
        for f in foreigns:
            if not (f in tables):
                print(f + " No es una tabla")
                status = False
                
        return status
        pass

        pass

if __name__ == "__main__":
    projectGenerator('D:/Documents/htdocs/bryan/apps_builder/Larapp-Cauldron/json_examples/trucks_admin.json').start()
    pass
