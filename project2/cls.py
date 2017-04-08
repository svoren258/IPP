#!/usr/bin/python

import sys, getopt, argparse

details = False
details_all = False
conflicts = False
classname = ''

private = False
public = False
protected = False

k = 2
stdout = True
outputfile = ''

class_list = []

class Class(object):
   def __init__(self, name, kind = 'concrete', privacy = 'private'):
      super(Class, self).__init__()
      self.name = name
      self.kind = kind
      self.privacy = privacy
      self.parents = []
      self.methods = []
      self.attributes = []
      self.root = False
        
   def add_parent_class(self, cls):
      self.parents.append(cls)

   def add_method(self, method):
      self.methods.append(method)

   def add_attribute(self, attribute):
      self.attributes.append(attribute)

   def change_kind(self, kind):
      self.kind = kind

   def change_privacy(self, privacy):
      self.privacy = privacy

   def is_parent(self):
      if (self.privacy != 'private'):
         if (self.root == True):
            sys.stderr.write('Conflict in inheritance!\n')
            sys.exit(21)
      self.root = True

class Method(object):
   def __init__(self, name, mtype, parentcls, scope = 'instance', privacy = 'private', pure = 'no'):
      super(Method, self).__init__()
      self.name = name
      self.mtype = mtype
      self.scope = scope
      self.privacy = privacy
      self.pure = pure
      self.arguments = []
      self.parentcls = parentcls

   def add_argument(self, argument):
      self.arguments.append(argument) 

   def change_scope(self, scope):
      self.scope = scope

   def change_privacy(self, privacy):
      self.privacy = privacy

   def change_pure(self, pure):
      self.pure = pure

class Attribute(object):
   def __init__(self, name, attype, parentcls, scope = 'instance', privacy = 'private'):
      super(Attribute, self).__init__()
      self.name = name
      self.attype = attype
      self.scope = scope
      self.privacy = privacy
      self.parentcls = parentcls
        
class Argument(object):
   def __init__(self, name, argtype):
      super(Argument, self).__init__()
      self.name = name
      self.argtype = argtype


def details_output(classname, methorattr, mthattr, privacy, n, k_string, stdout, outputfile):
   global private
   global public
   global protected
   mylist = []
   for i in range(len(methorattr)):
      if (methorattr[i].privacy == privacy):
         mylist.append(methorattr[i])

   if (mthattr == 'methods'):
      if mylist:
         if (privacy == 'private'):
            private = True
         elif (privacy == 'protected'):
            protected = True
         elif (privacy == 'public'):
            public = True   
         if (stdout == True):
            print(k_string*n + '<' + privacy +'>')
            n += 1
            print(k_string*n + '<methods>')
         else:
            outputfile.write(k_string*n + '<' + privacy + '>\n')
            n += 1
            outputfile.write(k_string*n + '<methods>\n')
         n += 1
         for method in mylist:
            if (stdout == True) and (method.privacy == privacy):
               print(k_string*n + '<method name="' + method.name + '" type="' + method.mtype + '" scope="' + method.scope + '">')
               if (method.parentcls.name != classname):
                  n += 1
                  print (k_string*n + '<from name="' + method.parentcls.name + '"/>')
                  n -= 1
               n += 1
               print(k_string*n + '<virtual pure="' + method.pure + '"/>')
               

            else:
               outputfile.write(k_string*n + '<method name="' + method.name + '" type="' + method.mtype + '" scope="' + method.scope + '">\n')
               n += 1
               if (method.parentcls.name != classname):
                  n += 1
                  outputfile.write(k_string*n + '<from name="' + method.parentcls.name + '"/>\n')
                  # n -= 1
               outputfile.write(k_string*n + '<virtual pure="' + method.pure + '"/>\n')
               
            
            if(stdout == True):
               print (k_string*n + '<arguments>')   
            else:
               outputfile.write(k_string*n + '<arguments>\n')

            if method.arguments:
               n += 1
               for arg in method.arguments:
                  n += 1
                  if (stdout == True):
                     print(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype +'">')
                  else:
                     outputfile.write(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype +'">\n')
               
            
            if(stdout == True):
               print (k_string*n + '<arguments/>')
            else:
               outputfile.write(k_string*n + '<arguments/>\n')

            n -= 1
            if(stdout == True):
               print (k_string*n + '</method>')
            else:
               outputfile.write(k_string*n + '</method>\n')

         n -= 1
         if(stdout == True):
            print (k_string*n + '</methods>')
         else:
            outputfile.write(k_string*n + '</methods>\n')

   elif(mthattr == 'attributes'):
      if mylist:
         if (privacy == 'private') and (private == False):
            private = True 
            if (stdout == True):
               print(k_string*n + '<' + privacy + '>')
            else:
               outputfile.write(k_string*n + '<' + privacy + '>\n')
         elif (privacy == 'protected') and (protected == False):
            protected = True
            if (stdout == True):
               print(k_string*n + '<' + privacy + '>')
            else:
               outputfile.write(k_string*n + '<' + privacy + '>\n')

         elif (privacy == 'public') and (public == False):
            public = True
            if (stdout == True):
               print(k_string*n + '<' + privacy + '>')
            else:
               outputfile.write(k_string*n + '<' + privacy + '>\n')

         n += 1   
         if(stdout == True):
            print(k_string*n + '<attributes>')
         else:
            outputfile.write(k_string*n + '<attributes>\n')
         n += 1
         for attr in mylist:
            if (stdout == True) and (attr.privacy == privacy):
               print (k_string*n + '<attribute name="' + attr.name + '" type="' + attr.attype + '" scope="' + attr.scope + '">')
               
               if (attr.parentcls.name != classname):
                  n += 1
                  print (k_string*n + '<from name="' + attr.parentcls.name + '"/>')
                  n -= 1
            else:
               outputfile.write(k_string*n + '<attribute name="' + attr.name + '" type="' + attr.attype + '" scope="' + attr.scope + '">\n')
               if (attr.parentcls.name != classname):
                  n += 1
                  outputfile.write(k_string*n + '<from name="' + attr.parentcls.name + '"/>\n')
                  n -= 1
         
            
            if(stdout == True):
               print(k_string*n + '</attribute>')
            else:
               outputfile.write(k_string*n + '</attribute>\n')
         n -= 1
         if (stdout == True):
            print(k_string*n + '</attributes>')
         else:
            outputfile.write(k_string*n + '</attributes>\n')
         
def next(classname, k_string, n, class_list, stdout, outputfile):
   for j in range(len(class_list)): 
      if not class_list[j].parents:
         continue
      else:
         for parent in class_list[j].parents:
            if (parent.name == classname):

               if (stdout == True):
                  print (k_string*n + '<class name="' + class_list[j].name + '" kind="' + class_list[j].kind + '">')
               else:
                  outputfile.write(k_string*n + '<class name="' + class_list[j].name + '" kind="' + class_list[j].kind + '">\n')
               next(class_list[j].name, k_string, n+1, class_list, stdout, outputfile)
               
               if (stdout == True):
                  print(k_string*n + '</class>')
               else:
                  outputfile.write(k_string*n + '</class>\n')
               break



def output(stdout, outputfilename, k, class_list, classname = ''):

   print('som v output a mam classname', classname)
   #global defined_class
   isdef = False
   mylist = []
   k_string = int(k) * ' '
   n = 1
   global outputfile
   global details
   global details_all
   global private
   global public
   global protected
   global conflicts

   if (classname == '') and (details_all == False):
      if (stdout == True):
         print ('<?xml version="1.0" encoding="UTF-8"?>')
         print ('<model>')
      else:
         outputfile = open(outputfilename, 'w')
         outputfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
         outputfile.write('<model>\n')

      for i in range(len(class_list)):
         if not class_list[i].parents:
            if (stdout == True):
               print (k_string*n + '<class name="' + class_list[i].name + '" kind="' + class_list[i].kind + '">')
            else:
               outputfile.write(k_string*n + '<class name="' + class_list[i].name + '" kind="' + class_list[i].kind + '">\n')  
            classname = class_list[i].name
            n += 1     

            next(classname, k_string, n, class_list, stdout, outputfile)

            while (n > 1):
               n -= 1
               if (stdout == True):
                  print(k_string*n + '</class>')
               else:
                  outputfile.write(k_string*n + '</class>\n')

         elif not class_list[i].parents and not class_list[i].is_parent():
            if (stdout == True):
               print (k_string*n + '<class name="' + class_list[i].name + '" kind="' + class_list[i].kind + '"></class>')
            else:
               outputfile.write(k_string*n + '<class name="' + class_list[i].name + '" kind="' + class_list[i].kind + '"></class>\n')  
            classname = class_list[i].name
      if (stdout == True):
         print ('</model>')
      else:
         outputfile.write('</model>\n')
         outputfile.close()

   elif(details_all == True):
      if (stdout == True):
         print ('<?xml version="1.0" encoding="UTF-8"?>')
         print ('<model>')
      else:
         outputfile = open(outputfilename, 'w')
         outputfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
         outputfile.write('<model>')
      
      for clss in class_list:
         if (stdout == True):
            print(k_string*n + '<class name="' + clss.name + '" kind="' + clss.kind + '">')
         else:
            outputfile = open(outputfilename, 'w')
            outputfile.write(k_string*n + '<class name="' + clss.name + '" kind="' + clss.kind + '">\n')

         n += 1
         if (clss.parents):
            if (stdout == True):
               print(k_string*n + '<inheritance>')
            else:
               outputfile.write(k_string*n + '<inheritance>\n')

            n += 1
            for parent in clss.parents:
               if (stdout == True):
                  print(k_string*n + '<from name="' + parent.name + '" privacy="' + parent.privacy + '"/>')
               else:
                  outputfile.write(k_string*n + '<from name="' + parent.name + '" privacy="' + parent.privacy + '"/>\n')
        
            n -= 1
            if (stdout == True):
               print(k_string*n + '</inheritance>')
            else:
               outputfile.write(k_string*n + '</inheritance>\n')

            if (conflicts == True):
               if(stdout == True):
                  print (k_string*n + '<conflicts>')   
               else:
                  outputfile.write(k_string*n + '<conflicts>\n')
                     
               is_conflict(clss)

               if (stdout == True):
                  print (k_string*n + '</conflicts>')
               else:
                  outputfile.write(k_string*n + '</conflicts>\n')

         details_output(clss.name, clss.methods, 'methods', 'private', n, k_string, stdout, outputfile)

         details_output(clss.name, clss.attributes, 'attributes', 'private', n, k_string, stdout, outputfile) 
         
         if (stdout == True) and (private == True):
            private = False
            print (k_string*n + '</private>')
         elif (stdout == False) and (private == True):
            outputfile.write(k_string*n + '</private>\n')
   

         details_output(clss.name, clss.methods, 'methods', 'protected', n, k_string, stdout, outputfile) 

         details_output(clss.name, clss.attributes, 'attributes', 'protected', n, k_string, stdout, outputfile)  
         

         if (stdout == True) and (protected == True):
            protected = False
            print (k_string*n + '</protected>')
         elif (stdout == False) and (protected == True):
            outputfile.write(k_string*n + '</protected>\n')


         details_output(clss.name, clss.methods, 'methods', 'public', n, k_string, stdout, outputfile) 

         details_output(clss.name, clss.attributes, 'attributes', 'public', n, k_string, stdout, outputfile)  
         

         if (stdout == True) and (public == True):
            public = False
            print (k_string*n + '</public>')
         elif (stdout == False) and (public == True):
            outputfile.write(k_string*n + '</public>\n')

         n = 1
         if (stdout == True):
            print (k_string*n + '</class>')
         else:
            outputfile.write(k_string*n + '</class>\n')


      if (stdout == True):
         print ('</model>')
      else:
         outputfile.write('</model>')


   elif (classname != ''):
      for i in range(len(class_list)):
         if (classname == class_list[i].name):
            isdef = True
            break

      if (isdef == True):
         if (stdout == True):
            print ('<?xml version="1.0" encoding="UTF-8"?>')
            print('<class name="' + classname + '" kind="' + class_list[i].kind + '">')
         else:
            outputfile = open(outputfilename, 'w')
            outputfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            outputfile.write('<class name="' + classname + '" kind="' + class_list[i].kind + '">\n')

         if (class_list[i].parents):
            if (stdout == True):
               print(k_string*n + '<inheritance>')
            else:
               outputfile.write(k_string*n + '<inheritance>\n')
            
            n += 1
            for parent in class_list[i].parents:
               if (stdout == True):
                  print(k_string*n + '<from name="' + parent.name + '" privacy="' + parent.privacy + '"/>')
               else:
                  outputfile.write(k_string*n + '<from name="' + parent.name + '" privacy="' + parent.privacy + '"/>\n')
            
            n -= 1
            if (stdout == True):
               print(k_string*n + '</inheritance>')
            else:
               outputfile.write(k_string*n + '</inheritance>\n')

            if (conflicts == True):
               if(stdout == True):
                  print (k_string*n + '<conflicts>')   
               else:
                  outputfile.write(k_string*n + '<conflicts>\n')
                     
               is_conflict(class_list[i])

               if (stdout == True):
                  print (k_string*n + '</conflicts>')
               else:
                  outputfile.write(k_string*n + '</conflicts>\n')

         details_output(classname, class_list[i].methods, 'methods', 'private', n, k_string, stdout, outputfile)

         details_output(classname, class_list[i].attributes, 'attributes', 'private', n, k_string, stdout, outputfile) 
         
         if (stdout == True) and (private == True):
            print (k_string*n + '</private>')
         elif (stdout == False) and (private == True):
            outputfile.write(k_string*n + '</private>\n')
   

         details_output(classname, class_list[i].methods, 'methods', 'protected', n, k_string, stdout, outputfile) 

         details_output(classname, class_list[i].attributes, 'attributes', 'protected', n, k_string, stdout, outputfile)  
         

         if (stdout == True) and (protected == True):
            print (k_string*n + '</protected>')
         elif (stdout == False) and (protected == True):
            outputfile.write(k_string*n + '</protected>\n')


         details_output(classname, class_list[i].methods, 'methods', 'public', n, k_string, stdout, outputfile) 

         details_output(classname, class_list[i].attributes, 'attributes', 'public', n, k_string, stdout, outputfile)  
         

         if (stdout == True) and (public == True):
            print (k_string*n + '</public>')
         elif (stdout == False) and (public == True):
            outputfile.write(k_string*n + '</public>\n')

         n = 0
         if (stdout == True):
            print (k_string*n + '</class>')
         else:
            outputfile.write(k_string*n + '</class>\n')

      else:
         if (stdout == True):
            print ('<?xml version="1.0" encoding="UTF-8"?>')
         else:
            outputfile = open(outputfilename, 'w')
            outputfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            outputfile.close()


def test_type(string):
   types = ['int', 'int *', 'int&',
           'float', 'float *', 'float&', 
           'double', 'double *', 'double&',
           'long double', 'long double *', 'long double&', 'void', 'void *', 'void&',
           'bool', 'bool *', 'bool&',
           'char', 'char *', 'char&',
           'char16_t', 'char16_t *', 'char16_t&', 'char32_t', 'char32_t *', 'char32_t&',
           'wchar_t', 'wchar_t *', 'wchar_t&','signed char', 'signed char *', 'signed char&',
           'short int', 'short int *', 'short int&', 'long int', 'long int *', 'long int&', 'long long int',
           'long long int *', 'long long int&', 'unsigned char', 'unsigned char *', 'unsigned char&',
           'unsigned short int', 'unsigned short int *', 'unsigned short int&', 'unsigned int', 'unsigned int *',
           'unsigned int&', 'unsigned long int', 'unsigned long int *', 'unsigned long int&',
           'unsigned long long int', 'unsigned long long int *', 'unsigned long long int&']

   for t in types:
      if (string == t):
         return t

   return False

def is_conflict(class1):
   global conflicts
   global outputfile
   global k
   global classname

   conflict_all = False

   k_string = k * ' '
   n = 2

   if (class1.attributes) and (len(class1.attributes) != 1):
      for i in range(len(class1.attributes)-1):
         for j in range(i+1, len(class1.attributes)):
            if (class1.attributes[i].name == class1.attributes[j].name) and (class1.attributes[i].parentcls != class1 and class1.attributes[j].parentcls != class1):
               if (conflicts != True):
                  if (classname == class1.name):
                     print('attributes conflict')
                     sys.stderr.write('Conflict in inheritance!\n')
                     sys.exit(21)
                  else:
                     return

               else:
                  if (stdout == True):
                     print(k_string*n + '<member name="' + class1.attributes[i].name + '">')
                  else:
                     outputfile.write(k_string*n + '<member name="' + class1.attributes[i].name + '">\n')

                  n += 1 

                  if (stdout == True):
                     print(k_string*n + '<class name="' + class1.attributes[i].parentcls.name + '">')
                  else:
                     outputfile.write(k_string*n + '<class name="' + class1.attributes[i].parentcls.name + '">\n')

                  n += 1

                  if (stdout == True):
                     print(k_string*n + '<' + class1.attributes[i].privacy + '>')
                  else:
                     outputfile.write(k_string*n + '<' + class1.attributes[i].privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<attribute name="' + class1.attributes[i].name + '" type="' + class1.attributes[i].attype + '" scope="' + class1.attributes[i].scope + '"/>')
                  else:
                     outputfile.write(k_string*n + '<attribute name="' + class1.attributes[i].name + '" type="' + class1.attributes[i].attype + '" scope="' + class1.attributes[i].scope + '"/>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + class1.attributes[i].privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + class1.attributes[i].privacy + '>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</class>')
                  else:
                     outputfile.write(k_string*n + '</class>\n')


                  if (class1.attributes[i].parentcls.name == class1.attributes[j].parentcls.name):
                     class1.attributes.remove(class1.attributes[i])
                     n -= 1
                     if (stdout == True):
                        print(k_string*n + '</member>')
                     else:
                        outputfile.write(k_string*n + '</member>\n')
                     return
                  else:
                     conflict_all = True

                  if (stdout == True):
                     print(k_string*n + '<class name="' + class1.attributes[j].parentcls.name + '">')
                  else:
                     outputfile.write(k_string*n + '<class name="' + class1.attributes[j].parentcls.name + '">\n')

                  n += 1

                  if (stdout == True):
                     print(k_string*n + '<' + class1.attributes[j].privacy + '>')
                  else:
                     outputfile.write(k_string*n + '<' + class1.attributes[j].privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<attribute name="' + class1.attributes[j].name + '" type="' + class1.attributes[j].attype + '" scope="' + class1.attributes[i].scope + '"/>')
                  else:
                     outputfile.write(k_string*n + '<attribute name="' + class1.attributes[j].name + '" type="' + class1.attributes[j].attype + '" scope="' + class1.attributes[i].scope + '"/>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + class1.attributes[j].privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + class1.attributes[j].privacy + '>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</class>')
                  else:
                     outputfile.write(k_string*n + '</class>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</member>')
                  else:
                     outputfile.write(k_string*n + '</member>\n')

                  if (conflict_all == True):
                     class1.attributes.remove(class1.attributes[j])
                     class1.attributes.remove(class1.attributes[i])
                     conflict_all = False

   print(len(class1.methods))
   if (class1.methods) and (len(class1.methods) != 1):
      for i in range(len(class1.methods)):
         for j in range(i+1, len(class1.methods)):
            if (class1.methods[i].name == class1.methods[j].name) and (class1.methods[i].parentcls != class1 and class1.methods[j].parentcls != class1):
               if (conflicts != True):
                  if (classname == class1.name):
                     print('methods conflict')
                     sys.stderr.write('Conflict in inheritance!\n')
                     sys.exit(21)
                  else:
                     return
               else:
                  if (stdout == True):
                     print(k_string*n + '<member name="' + class1.methods[i].name + '">')
                  else:
                     outputfile.write(k_string*n + '<member name="' + class1.methods[i].name + '">\n')

                  n += 1 

                  if (stdout == True):
                     print(k_string*n + '<class name="' + class1.methods[i].parentcls .name+ '">')
                  else:
                     outputfile.write(k_string*n + '<class name="' + class1.methods[i].parentcls.name + '">\n')

                  n += 1

                  if (stdout == True):
                     print(k_string*n + '<' + class1.methods[i].privacy + '>')
                  else:
                     print(k_string*n + '<' + class1.methods[i].privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<method name="' + class1.methods[i].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '"/>')
                  else:
                     outputfile.write(k_string*n + '<method name="' + class1.methods[i].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '"/>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + class1.methods[i].privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + class1.methods[i].privacy + '>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</class>')
                  else:
                     outputfile.write(k_string*n + '</class>\n')

                  if (class1.methods[i].parentcls.name == class1.methods[j].parentcls.name):
                     class1.methods.remove(class1.methods[i])
                     n -= 1
                     if (stdout == True):
                        print(k_string*n + '</member>')
                     else:
                        outputfile.write(k_string*n + '</member>\n')
                     return
                  else:
                     conflict_all = True

                  if (stdout == True):
                     print(k_string*n + '<class name="' + class1.methods[j].parentcls.name + '">')
                  else:
                     outputfile.write(k_string*n + '<class name="' + class1.methods[j].parentcls.name + '">\n')

                  n += 1

                  if (stdout == True):
                     print(k_string*n + '<' + class1.methods[j].privacy + '>')
                  else:
                     print(k_string*n + '<' + class1.methods[j].privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<method name="' + class1.methods[j].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '"/>')
                  else:
                     outputfile.write(k_string*n + '<method name="' + class1.methods[j].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '"/>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + class1.methods[j].privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + class1.methods[j].privacy + '>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</class>')
                  else:
                     outputfile.write(k_string*n + '</class>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</member>')
                  else:
                     outputfile.write(k_string*n + '</member>\n')

                  if (conflict_all == True):
                     class1.methods.remove(class1.methods[j])
                     class1.methods.remove(class1.methods[i])
                     conflict_all = False


def derivate(input_list, class1, privacy, index):
   print('derivate')
   global class_list
   global conflicts

   for clss in class_list:
      if (clss.name == input_list[index]):
         base_class = clss
         break

   base_class.privacy = privacy

   class1.add_parent_class(base_class)
   if (base_class.kind != 'concrete'):
      class1.kind = base_class.kind

   for m in base_class.methods:      

      if (privacy == 'public'):
         if (m.privacy == 'private'):
            continue
         method1 = Method(m.name, m.mtype, m.parentcls, m.scope, m.privacy, m.pure)
         method1.privacy = privacy
         class1.add_method(method1)

      elif (privacy == 'protected'):
         method1 = Method(m.name, m.mtype, m.parentcls, m.scope, m.privacy, m.pure)
         method1.privacy = privacy
         # method1 = Method(m.name, m.mtype, m.parentcls, m.scope, privacy, m.pure)
         class1.add_method(method1)


      elif (privacy == 'private'):
         if (m.privacy == 'private'):
            print('continue')
            continue
         method1 = Method(m.name, m.mtype, m.parentcls, m.scope, m.privacy, m.pure)
         method1.privacy = privacy
         # method1 = Method(m.name, m.mtype, m.parentcls, m.scope, privacy, m.pure)
         class1.add_method(method1)


   for attr in base_class.attributes:
      if (privacy == 'public'):
         print('som v public')
         #base_class.privacy = privacy
         if (attr.privacy == 'private'):
            continue
         attr1 = Attribute(attr.name, attr.attype, attr.parentcls, attr.scope, attr.privacy)
         attr1.privacy = privacy
         class1.add_attribute(attr1)

      elif (privacy == 'protected'):
         #base_class.privacy = privacy
         attr1 = Attribute(attr.name, attr.attype, attr.parentcls, attr.scope, attr.privacy)
         attr1.privacy = privacy
         class1.add_attribute(attr1)

      elif (privacy == 'private'):
         # if (attr.privacy == 'private'):
         #    continue
         attr1 = Attribute(attr.name, attr.attype, attr.parentcls, attr.scope, attr.privacy)
         attr1.privacy = attr.privacy
         class1.add_attribute(attr1)

   print(len(class1.methods))
   for m in class1.methods:
      print(m.name)
      print(m.privacy)
      print(m.mtype)

   for attr in class1.attributes:
      print(attr.name)
      print(attr.privacy)
      print(attr.attype)

def inheritance_privacy(input_list, class1, index):
   print('inheritance privacy')

   privacy = 'private'
   if (input_list[index] == 'public'):
      privacy = 'public'
      derivate(input_list, class1, privacy, index+1)
      return index+2
   elif (input_list[index] == 'private'):
      privacy = 'private'
      derivate(input_list, class1, privacy, index+1)
      return index+2
   elif (input_list[index] == 'protected'):
      privacy = 'protected'
      derivate(input_list, class1, privacy, index+1)
      return index+2
   else:
      derivate(input_list, class1, privacy, index)
      print (input_list[index+1])
      return index+1

def declaration(class1, input_list, scope, privacy, virtual, index):
   print('declaration')
   print(input_list[index])
   print(privacy)
   pureness = 'no'

   if (test_type(input_list[index]) != False):
      if (input_list[index+2] == ';'):
         attr1 = Attribute(input_list[index+1], input_list[index], class1, scope, privacy)
         class1.add_attribute(attr1)
         return index+3

      elif (input_list[index+2] == '('):
         print('vytvaram metodu')
         method1 = Method(input_list[index+1], input_list[index], class1, scope, privacy)
         print(method1.privacy)
         i = index+3
         while (input_list[i] != ')'):
            if (input_list[i] == 'void'):
               i += 1
               continue

            if (test_type(input_list[i]) != False):
               arg1 = Argument(input_list[i+1], input_list[i])
               method1.add_argument(arg1)
               i += 2
            
            else:
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
               
         print(input_list[i+1])
         print(virtual)
         if (input_list[i+1] == '='):
            if (input_list[i+2] == '0'):
               if (input_list[i+3] == ';'):
                  if (virtual == 'yes'):   
                     method1.pure = 'yes'
                     class1.kind = 'abstract'
                     print('pridavam virtual pure metodu')
                  class1.add_method(method1)
                  return i+4

               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

         elif (input_list[i+1] != '{'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)

         if (input_list[i+2] != '}'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)

         x = 0
         length = len(class1.methods)
         print(len(class1.methods))
         while (x < length):
            if (class1.methods[x].name == method1.name) and (class1.methods[x].mtype == method1.mtype):
               class1.methods.remove(class1.methods[x])
               length -= 1
               print(x)
            else:
               x += 1

         class1.add_method(method1)

         for m in class1.methods:
            if (m.pure == 'yes'):
               pureness = 'yes'
               break
            
         if (pureness != 'yes'):
            class1.kind = 'concrete'
            
         if (input_list[i+3] != ';'):
            return i+3
         else:
            while (input_list[i+3] == ';'):
               i += 1
            return i+3

      elif (input_list[index+2] == '='):
         if (input_list[index+4] != ';'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
         return index+5

   elif (input_list[index] != '}'):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)
   
   return index

def using(class1, input_list, index, privacy = 'private'):
   print('using')
   global class_list
   defined = False

   for clss in class_list:
      if (input_list[index] == clss.name):
         defined = True
         break

   for attr in clss.attributes:
      if (attr.parentcls.name == clss.name) and (input_list[index+3] == attr.name):
         break
      elif (input_list[index+3] == attr.name):
         clss = attr.parentcls
         break

      
   if (defined != True):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)
   if (input_list[index+1] != ':'):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)
   if (input_list[index+2] != ':'):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)

   x = 0
   length = len(class1.attributes)
   print(len(class1.attributes))
   while (x < length):
      print(input_list[index+3])
      print(class1.attributes[x].parentcls.name)
      if (input_list[index+3] == class1.attributes[x].name) and (class1.attributes[x].parentcls != clss):
         class1.attributes.remove(class1.attributes[x])
         length -= 1
      elif (input_list[index+3] == class1.attributes[x].name) and (class1.attributes[x].parentcls == clss):
         class1.attributes[x].privacy = privacy
         x += 1

   if (input_list[index+4] != ';'):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)
   return index+5

def body_of_class(class1, input_list, index):
   print('body of class')

   global class_list

   scope = 'instance'
   virtual = 'no'
   privacy = 'private'
   defined = False

   if (input_list[index] == 'static'):
      scope = 'static'
      index = declaration(class1, input_list, scope, privacy, virtual, index+1)
      return index

   elif (input_list[index] == 'private'):
      if (input_list[index+1] != ':'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4) 

      privacy = 'private'
      if (input_list[index+2] == 'virtual'):
         virtual = 'yes'
         index = declaration(class1, input_list, scope, privacy, virtual, index+3)
      elif (input_list[index+2] == 'static'):
         scope = 'static'
         index = declaration(class1, input_list, scope, privacy, virtual, index+3)
      elif (input_list[index+2] == 'using'):
         index = using(class1, input_list, index+3, privacy)
      else:
         index = declaration(class1, input_list, scope, privacy, virtual, index+2)
      return index

   elif (input_list[index] == 'public'):
      if (input_list[index+1] != ':'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4) 

      privacy = 'public'
      if (input_list[index+2] == 'virtual'):
         virtual = 'yes'
         index = declaration(class1, input_list, scope, privacy, virtual, index+3)
      elif (input_list[index+2] == 'static'):
         scope = 'static'
         index = declaration(class1, input_list, scope, privacy, virtual, index+3)
      elif (input_list[index+2] == 'using'):
         index = using(class1, input_list, index+3, privacy)
      else:
         index = declaration(class1, input_list, scope, privacy, virtual, index+2)
      return index

   elif (input_list[index] == 'protected'):
      print('som v protected v body_of_class')
      if (input_list[index+1] != ':'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4) 

      privacy = 'protected'
      if (input_list[index+2] == 'virtual'):
         virtual = 'yes'
         index = declaration(class1, input_list, scope, privacy, virtual, index+3)
      elif (input_list[index+2] == 'static'):
         scope = 'static'
         index = declaration(class1, input_list, scope, privacy, virtual, index+3)
      elif (input_list[index+2] == 'using'):
         index = using(class1, input_list, index+3, privacy)
      else:
         index = declaration(class1, input_list, scope, privacy, virtual, index+2)
      return index

   elif (input_list[index] == 'virtual'):
      virtual = 'yes'
      index = declaration(class1, input_list, scope, privacy, virtual, index+1)
      return index

   elif (input_list[index] == 'using'):
      index =  using(class1, input_list, index+1)
      return index

   else:
      index = declaration(class1, input_list, scope, privacy, virtual, index)
      return index

   

def analysis(input_list):
   print('som v analysis')
   global class_list
   global conflicts

   i = 0
   while (i < len(input_list)):
      print('while')
      print(input_list[i])
      if (input_list[i] != 'class'):
         sys.stderr.write('Syntax error!\n')
         sys.exit(4)

      else:
         class1 = Class(input_list[i+1])
         class_list.append(class1)
         print('creating class', input_list[i+1])

         if (input_list[i+2] == ':'):
            index = inheritance_privacy(input_list, class1, i+3)
            print(input_list[index])
            while (input_list[index] != '{'):
               if (input_list[index] == ','):
                  index = inheritance_privacy(input_list, class1, index+1)

               else:
                  sys.stderr.write('Syntax error!\n')
                  sys.exit(4)

            i = index - 2

         elif (input_list[i+2] != '{'):
            sys.stderr.write('Syntax error!\n')
            sys.exit(4)
         print('do body_of_class ide', input_list[i+3])
         index = body_of_class(class1, input_list, i+3)
         print(input_list[index])
         while (input_list[index] != '}'):
            index = body_of_class(class1, input_list, index)

         if (input_list[index+1] != ';'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
         i = index + 2

         if (conflicts == False):
            is_conflict(class1)

   return class_list

def parsering(input_content):
   word = ''
   input_list = []
   types = ['int', 'bool', 'char', 'float', 'double', 'void', 'char16_t', 'char32_t', 'wchar_t']
   
   for char in input_content:
      print(char)
      if ((char == '\n') or (char == ' ')) and (word != ''):
         input_list.append(word)
         word = ''
         continue
      elif ((char == "(") or (char == ")")) and (word != ''):
         input_list.append(word)
         word = ''
         word += char
         input_list.append(word)
         word = ''
      elif (char == '{') or (char == '}') or (char == ';') or (char == '=') or (char.isdigit()):
         if (word != ''):
            input_list.append(word)
            word = ''
         input_list.append(char)
      elif (char != '\n') and (char != ' ') and (char != '\t'):
         if ((char == ',') or (char == ':')) and (word != ''):
            input_list.append(word)
            input_list.append(char)
            word = ''
         else:   
            if((char == ':') or (char == '*') or (char == '&'))  and (word == ''):
               input_list.append(char)
               continue
            word += char

   print (input_list)
   
   for t in types:
      for c in input_list:
         if (t == c):
            index = input_list.index(c)
            if (input_list[index+1] == '*'):
               word = input_list[index] + ' ' + input_list[index+1]
               input_list.insert(index, word)
               input_list.remove(c)
               input_list.remove('*')
               break
            elif (input_list[index+1] == '&'):
               word = input_list[index] + input_list[index+1]

   class_list = analysis(input_list)

   # for clss in class_list:
   #    print(clss.name)
   #    for m in clss.methods:
   #       print(m.name)
   #       print(m.privacy)
   #    for attr in clss.attributes:
   #       print(attr.name)
   #       print(attr.privacy)
   return class_list

def main():
   global details_all
   global details
   global conflicts
   global stdout
   global k
   global classname

   inputfilename = ''
   outputfilename = ''
   
   stdin = True

   parser = argparse.ArgumentParser()

   parser.add_argument('-i', '--input=', dest='input')
   parser.add_argument('-o', '--output=', dest='output')
   parser.add_argument('--details', action='store', nargs='*', dest='details')
   parser.add_argument('--pretty-xml', dest='k', nargs='*', action='store')
   parser.add_argument('--conflicts', dest='conflicts', action='store_true')

   parsed = parser.parse_args()

   print(parsed)

   if (parsed.k == []):
      k = 4
   elif (parsed.k != None):
      k = parsed.k[0]
   
   if (parsed.details == []):
      details_all = True
      if (parsed.conflicts == True):
         conflicts = True

   elif (parsed.details != None):
      classname = parsed.details[0]
      if (parsed.conflicts == True):
         conflicts = True

   if (parsed.input):
      inputfilename = parsed.input
      stdin = False
   else:
      stdin = True

   if (parsed.output):
      outputfilename = parsed.output
      stdout = False
   else:
      stdout = True

   if (stdin == False):
      # print ('Input file name:', inputfilename) 
      inputfile = open(inputfilename, 'r')
      input_content = inputfile.read()

   else:
      # input_content = input()
      # input_content += '\n'
      input_content = sys.stdin.read()
   #class_list = parsering(input_content)
   # for clss in class_list:
   #    print(clss.name)
   # for clss in class_list:
   #    print(clss.name)
   #    for m in clss.methods:
   #       print(m.name)
   #       print(m.privacy)
   #    for attr in clss.attributes:
   #       print(attr.name)
   #       print(attr.privacy)

   output(stdout, outputfilename, k, parsering(input_content), classname)

   #closing files
   if (stdin == False):
      inputfile.close()

if __name__ == "__main__":
    main()