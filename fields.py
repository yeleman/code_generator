"""
Django field that autogenerate code for django.

/!\ Not tested with unit tests yet in this module
However, I tested it with unitests in a live django project and it did fine.
But don't take my word for it and use with care.

"""

from django.db import models

from code_generator import generate_code, get_code_from_model


class CodeField(models.CharField):
    """
        Store an ordinary text code to increment with the following 
    """

    
    def generate_code(self, **kwargs):
        return generate_code(get_code_from_model, model=self.model, 
                             field=self.attname, **kwargs)
    
    
    #TODO: find a cleaner way to do this and allow any argument to pass
    def __init__(self, *args, **kwargs):
    
        gen_kwargs = {}
        gen_kwargs['prefix'] = kwargs.pop('prefix', '')
        gen_kwargs['suffix'] = kwargs.pop('suffix', '')
        gen_kwargs['min_length'] = kwargs.pop('min_length', 3)
        gen_kwargs['inc'] = kwargs.pop('inc', 1)
        gen_kwargs['pad_with'] = kwargs.pop('pad_with', '0')
        gen_kwargs['default'] = kwargs.pop('default', '0')
        
        kwargs.setdefault('blank', True)
        kwargs.setdefault('unique', True)
    
        models.CharField.__init__(self, *args, **kwargs)
        
        self.gen_kwargs = gen_kwargs
    
    
    def pre_save(self, model_instance, add):
    
        
        code = getattr(model_instance, self.attname, None)
        
        if not code:
        
            # check if the code match the prefix / suffix
            #get_code_from_model
            
            code = generate_code(get_code_from_model, 
                                 model=model_instance.__class__, 
                                 field=self.attname, **self.gen_kwargs)
                                     
                                     
        
        setattr(model_instance, self.attname, code)
        return code
        

    def value_to_string(self, obj):
        return repr(obj)
