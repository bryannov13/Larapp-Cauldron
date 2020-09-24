from os import path as p
from os import makedirs
from .tools import get_file
from .tools import set_directory


class index_generator():
    
    def __init__(self, model_name:str,fields:list,app_name:str="App"):
        self.txt = []
        self.fields=fields
        self.app_name = app_name
        self.model_name = model_name
        
    
    def __set_default_dependencies(self):
        #Dependencies
        self.txt.append("<!--"+str(self.model_name)+"_model -->\n")
        self.txt.append("@extends('layouts.app')\n")
        self.txt.append("@section('top-title', '"+self.model_name+"')\n")
        self.txt.append("@section('content')\n\n")

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
        
    #def __set_default_fields(self)->list: return ["\t\t\t$table->boolean('status');\n","\n\t\t\t$table->timestamps();\n"]
        
    def set_file(self,path):
        if not p.exists(path): model_file = open(path,"x")
            
        else: model_file = open(path,"w")
        

        self.__set_default_dependencies()
        
        return model_file
        
    def create(self, path, default_fields=False):
        
        set_directory(path)
        path= path+"/index.blade.php"
        file = self.set_file(path)
        
        
        self.txt.append("@include('alerts.message')\n")
        self.txt.append("@include('alerts.request')\n")
        self.txt.append("@include('"+self.model_name+".form-modal')\n\n")
        
        #Card

        self.txt.append('\t<div class="card">\n')
        self.txt.append('\t\t<div class="card-body">\n')
        self.txt.append('\t\t\t<div class="container-fluid">\n')
        self.txt.append('\t\t\t\t<div class="row">\n')
        self.txt.append('\t\t\t\t\t<div class="col-12">\n')
        self.txt.append('\t\t\t\t\t\t@if(auth()->user()->hasPermission("Agregar-'+self.model_name+'"))\n')
        self.txt.append('\t\t\t\t\t\t\t<button class="btn btn-default pull-right btn-wd" onclick="create()">\n')
        self.txt.append('\t\t\t\t\t\t\t\t<i class="fa fa-plus-circle"></i> <span>Agregar</span>\n')
        self.txt.append('\t\t\t\t\t\t\t</button>\n')
        self.txt.append('\t\t\t\t\t\t@endif\n')
        self.txt.append('\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t<div class="col-12">\n')
        self.txt.append('\t\t\t\t\t\t<div class="card">\n')
        self.txt.append('\t\t\t\t\t\t\t<div class="card-body">\n')
        self.txt.append('\t\t\t\t\t\t\t\t<form method="POST" id="search-form" class="form-inline" role="form">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t<div class="form-check">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t<label class="form-check-label">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t\t<input class="form-check-input" type="checkbox" id="showInactive" name="showInactive" value="1">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t\t<span class="form-check-sign"></span>Inactivos\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t</label>\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t\t\t\t</form>\n')
        self.txt.append('\t\t\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t\t<table class="table table-bordered table-grid table-general" id="'+self.model_name+'-table" style="width:100%"></table>\n')
        self.txt.append('\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t</div>\n')
        self.txt.append('\t\t\t</div>\n')
        self.txt.append('\t\t</div>\n')
        self.txt.append('\t</div>\n')
        self.txt.append('@endsection\n\n')
        self.txt.append('@section("js")\n')
        self.txt.append('\t{!!Html::script("assets/js/'+self.model_name+'.js")!!}\n')
        self.txt.append('@endsection\n')
        
        
        file.writelines(self.txt)
        pass
    pass

class form_generator():
    
    def __init__(self, model_name:str,fields:list,app_name:str="App"):
        self.txt = []
        self.fields=fields
        self.app_name = app_name
        self.model_name = model_name
        
    
    def __set_default_dependencies(self):
        #Dependencies
        self.txt.append("<!--"+str(self.model_name)+"_model -->\n")
        self.txt.append("@extends('layouts.app')\n")
        self.txt.append("@section('top-title', '"+self.model_name+"')\n")
        self.txt.append("@section('content')\n\n")


    def _set_fields(self,default_fields:bool=True)->list:
        arra_txt = []
        
        for i,field in enumerate(self.fields):
            #if i: arra_txt.append(',\n')

            if field['type'] == 'Integer' or field['type'] == 'Floating':
                arra_txt.append('\t\t\t\t\t\t\t\t\t<div class="row">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t<div class="col-12">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<label>'+field['name']+': <span style="color:red">*</span></label>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<input type="text" name="'+field['name']+'" id="'+field['name']+'" class="form-control change_salary" value="{{old("'+field['name']+'", isset($register) ? $register->"'+field['name']+'" : '')}}" data-parsley-required data-parsley-type="number" min="0" max="9999" maxlength="12">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t</div>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t</div>\n')

            elif field['type'] == 'String':
                arra_txt.append('\t\t\t\t\t\t\t\t\t<div class="row">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t<div class="col-12">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<label>'+field['name']+': <span style="color:red">*</span></label>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<input type="text" name="'+field['name']+'" data-parsley-maxlength="100" data-parsley-required value="{{old("'+field['name']+'", isset($record) ? $record->'+field['name']+' : "")}}" class="form-control">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t</div>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t</div>\n')

            elif field['type'] == 'DateTime': 
                arra_txt.append('\t\t\t\t\t\t\t\t\t<div class="row">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t<div class="col-12">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<label>'+field['name']+': <span style="color:red">*</span></label>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<input type="text" name="'+field['name']+'" id="'+field['name']+'" class="form-control datetimepicker" value="{{old("'+field['name']+'", isset($register) ? $register->'+field['name']+' : '')}}" data-parsley-required>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t</div>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t</div>\n')
            else: 
                arra_txt.append('\t\t\t\t\t\t\t\t\t<div class="row">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t<div class="form-group col-md-12">\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<label>@lang("'+field['name']+'"):</label>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t<select type="text" class="form-control" name="'+field['name']+'" id="'+field['name']+'" >\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t\t<option value="">- Seleccione -</option>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t\t@foreach($items as $item)\n')#Pendiente hacer clase superior que incluya foreign keys, fields, model_name entre otros
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t\t\t<option @if(isset($register) && $register->'+field['name']+' == $item->id) selected @endif value="{{$item->id}}">{{ $item->id }}</option>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t\t@endforeach\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t\t</select>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t\t</div>\n')
                arra_txt.append('\t\t\t\t\t\t\t\t\t</div>\n')
                
        #if default_fields: arra_txt.extend(self.__set_default_fields())
            
        return arra_txt
        
    #def __set_default_fields(self)->list: return ["\t\t\t$table->boolean('status');\n","\n\t\t\t$table->timestamps();\n"]
        
    def set_file(self,path):
        if not p.exists(path): model_file = open(path,"x")
            
        else: model_file = open(path,"w")
        
        #self.__set_default_dependencies()
        
        return model_file
        
    def create(self, path, default_fields=False):
        
        set_directory(path)
        path= path+"/form.blade.php"
        file = self.set_file(path)
        
        
        self.txt.append("@include('alerts.message')\n")
        self.txt.append("@include('alerts.request')\n")
        #self.txt.append("@include('"+self.model_name+".form-modal')\n\n")
        
        #Card

        self.txt.append('\t<div class="card">\n')
        self.txt.append('\t\t<div class="card-body">\n')
        self.txt.append('\t\t\t<div class="container-fluid">\n')
        self.txt.append('\t\t\t\t<div class="row">\n')
        self.txt.append('\t\t\t\t\t<div class="col-12-lg container">\n')
        self.txt.append('\t\t\t\t\t\t<div class="catalog-modal">\n')
        self.txt.append('\t\t\t\t\t\t\t<div class="card card-body">\n')
        self.txt.append('\t\t\t\t\t\t\t\t<form action="{{$url}}"  method="POST" class="form-view">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t{{ csrf_field() }}>\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t@if($action == "edit")\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t<input name="_method" type="hidden" value="PUT">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t<input name="id" type="hidden" value="{{$record->id}}">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t@endif\n')

        self.txt.extend(self._set_fields())

        self.txt.append('\t\t\t\t\t\t\t\t\t<div class="form-group m-t-1">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t<div class="pull-right">\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t\t<a class="btn btn-default btn-wd" href="{{url("/'+self.model_name+'")}}">Cancelar</a>\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t\t@if($action != "show")\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t\t\t<button type="submit" class="btn btn-primary-ws btn-wd">Guardar</button>\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t\t@endif\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t\t\t\t</form>\n')
        self.txt.append('\t\t\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t\t</div>\n')
        self.txt.append('\t\t\t\t</div>\n')
        self.txt.append('\t\t\t</div>\n')
        self.txt.append('\t\t</div>\n')
        self.txt.append('\t@endsection\n')
        self.txt.append('@section("js")\n')
        self.txt.append('\t{!!Html::script("assets/js/'+self.model_name+'.js")!!}\n')
        self.txt.append('@endsection\n')
        
        file.writelines(self.txt)
        pass
    pass


class Views_Generator(object):
    def __init__(self,app:object,project_name,out_path):
        
        try:
            for m in app["tables"]:
                print("Controlling "+m["name"]+" model ...")
                index_generator(m["name"],m['fields'],app["name"]).create(path= out_path+project_name+"/resources/views/"+app["name"]+"/"+m["name"],default_fields=True)
                form_generator(m["name"],m['fields'],app["name"]).create(path= out_path+project_name+"/resources/views/"+app["name"]+"/"+m["name"],default_fields=True)
                
                #model_.set_fields(m["fields"]) resources\views\area\index.blade.php
                pass
        except Exception as e:
            print("Controller:\n")
            print(e)
            pass
                
        
    pass

if __name__ == "__main__":
    
    from json import load
    try:
        app= load(open('../../json_examples/trucks_admin.json'))
        a = Views_Generator(app,'project','../../out/')
    except Exception as e:
        print(e)
    
    
