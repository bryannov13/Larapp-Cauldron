from Generator.controllers import Controllers_Generator
from Generator.js import Js_Generator
from Generator.migrations import Migrations_Generator
from Generator.models import Models_Generator
from Generator.request import Requests_Generator
from Generator.routes import Routes_Generator
from Generator.views import Views_Generator

from json import load

class projectGenerator():
    def __init__(self, input_path:str, out_path:str='../out/'):
        #self.app = App
        self.app= load(open(input_path))
        self.out_path = out_path
        pass

    def createControllers(self):
        try: Controllers_Generator(self.app,'project',self.out_path)
        except Exception as e: print("Fallo al crear controladores\n"+e)
        
    def createJs(self):
        try: Js_Generator(self.app,'project',self.out_path)
        except Exception as e: print("Fallo al crear JS\n"+e)
    
    def createMigrations(self):
        try: Migrations_Generator(self.app,'project',self.out_path)
        except Exception as e: print("Fallo al crear Migraciones\n"+e)
        
    def createModels(self):
        try: Models_Generator(self.app,'project',self.out_path)
        except Exception as e: print("Fallo al crear Modelos\n"+e)
    
    def createRequest(self):
        try: Requests_Generator(self.app,'project',self.out_path)
        except Exception as e: print("Fallo al crear Request\n"+e)
        
    def createRoutes(self):
        try: Routes_Generator(self.app,'project',self.out_path)
        except Exception as e: print("Fallo al crear Rutas\n"+e)
    
    def start(self):
        self.createControllers()
        self.createJs()
        self.createMigrations()
        self.createModels()
        self.createRequest()
        self.createRoutes()

        pass

if __name__ == "__main__":
    projectGenerator('D:/Documents/htdocs/bryan/apps_builder/Larapp-Cauldron/json_examples/trucks_admin.json').start()
    pass
