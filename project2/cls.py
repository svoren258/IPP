#!/usr/bin/python

import sys, getopt

details = False

private = False
public = False
protected = False

#defined_class = []

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
   def __init__(self, name, mtype, scope = 'instance', privacy = 'private', pure = 'no'):
      super(Method, self).__init__()
      self.name = name
      self.mtype = mtype
      self.scope = scope
      self.privacy = privacy
      self.pure = pure
      self.arguments = []

   def add_arguments(self, argument):
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
            if (stdout == True):
               print(k_string*n + '<method name="' + method.name + '" type="' + method.mtype + '" scope="' + method.scope + '">')
               n += 1
               print(k_string*n + '<virtual pure="' + method.pure + '"/>')
            else:
               outputfile.write(k_string*n + '<method name="' + method.name + '" type="' + method.mtype + '" scope="' + method.scope + '">\n')
               n += 1
               outputfile.write(k_string*n + '<virtual pure="' + method.pure + '"/>\n')
            n += 1

            if method.arguments:
               if(stdout == True):
                  print (k_string*n + '<arguments>')   
               else:
                  outputfile.write(k_string*n + '<arguments>\n')

               for arg in method.arguments:
                  n += 1
                  if (stdout == True):
                     print(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype +'">')
                  else:
                     outputfile.write(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype +'">\n')
               
            n -= 1
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
            if (stdout == True):
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
         

def output(stdout, outputfilename, k, class_list, classname = ''):

   #global defined_class
   isdef = False
   mylist = []
   k_string = int(k) * ' '
   n = 1
   outputfile = ''
   global details
   global private
   global public
   global protected

   if (details == False):
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
                        classname = class_list[j].name
                        n += 1
                        break

            while (n > 1):
               n -= 1
               if (stdout == True):
                  print(k_string*n + '</class>')
               else:
                  outputfile.write(k_string*n + '</class>\n')
      if (stdout == True):
         print ('</model>')
      else:
         outputfile.write('</model>\n')
         outputfile.close()

   else:
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

   if (string == 'void'):
      return string

   for t in types:
      if (string == t):
         return t

   return False


def definition(class_list, input_list, class1, index):
   print('som v definition')
   print(input_list[index+3])

   if (input_list[index+3] == 'virtual'):
      class1.change_kind('abstract')
      if (test_type(input_list[index+4]) != False):
         if (input_list[index+6] != '('):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
         print('som pred vytvorenim metody')
         method1 = Method(input_list[index+5], input_list[index+4])
         class1.add_method(method1)

         if (input_list[index+7] == ')'):
            for x in range(index+8, len(input_list)):
               if (input_list[x] == ';' ):
                  return x


         if (test_type(input_list[index+7]) != False):
            if (test_type(input_list[index+7]) == 'void'):
               print('mam vod')
               if (input_list[index+9] == '='):
                  if (input_list[index+10] == '0'):
                     print('nastavjem pe')
                     method1.pure = 'yes' 
                     if (input_list[index+11] == ';'):
                        return index+11
               else:
                  for x in range(index+8, len(input_list)):
                     if (input_list[x] == ';'):
                        return x
            else:  
               arg1 = Argument(input_list[index+8], input_list[index+7])
               method1.add_arguments(arg1)
               if (input_list[index+9] == ")"):
                  for x in range(index+10, len(input_list)):
                     if (input_list[x] == ';'):
                        return x
               elif (input_list[index+9] == ','):
                  print('method has more than one argument')

               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
         else:
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)

                    
      else:
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)


   elif (input_list[index+3] == 'public'):
      print('som v public')
      if (input_list[index+4] != ':'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)
      if (test_type(input_list[index+5]) == False):
         if (input_list[index+5] == 'virtual'):
            if (test_type(input_list[index+6]) == False):
               sys.stderr.write('Wrong input file formating!\n')
            else:
               if (input_list[index+8] == '('):
                  for x in range(len(class1.methods)):
                     if (class1.methods[x].name == input_list[index+7]):
                        class1.methods.remove(class1.methods[x])
                  method1 = Method(input_list[index+7], input_list[index+6])
                  method1.privacy = 'public'
                  class1.add_method(method1)
               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
               if (test_type(input_list[index+9]) != False):
                  if (input_list[index+9] == 'void'):
                     if (input_list[index+10] != ')'):
                        sys.stderr.write('Wrong input file formating!\n')
                        sys.exit(4)
                     if (input_list[index+11] == '{'):
                        if (input_list[index+12] != '}'):
                           sys.stderr.write('Wrong input file formating!\n')
                           sys.exit(4)
                        return index+13
                     elif (input_list[index+11] == '='):
                        if (input_list[index+12] == '0'):
                           method1.pure = 'yes'
                           return index+13

                  else:
                     arg1 = Argument(input_list[index+10], input_list[index+9])
                     method1.add_arguments(arg1)
                     if (input_list[index+11] == ')'):
                        if (input_list[index+12] != '{'):
                           sys.stderr.write('Wrong input file formating!\n')
                           sys.exit(4)
                        if (input_list[index+13] == '}'):
                           return index+14

         else:
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
      
      if (input_list[index+7] == ';'):
         print('pridavam attr')
         attr1 = Attribute(input_list[index+6], input_list[index+5], class1)
         class1.add_attribute(attr1)
         return index+7

      elif (input_list[index+7] == '('):
         print('pridavam meth')
         method1 = Method(input_list[index+6], input_list[index+5])
         class1.add_method(method1)

      else:
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)

      if (input_list[index+8] == ')'):
         for x in range(index+9, len(input_list)):
            if (input_list[x] == ';'):
              return x

      if (test_type(input_list[index+8]) != False):
         if (test_type(input_list[index+8]) == 'void'):
            if (input_list[index+9] != ')'):
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
            if (input_list[index+10] == '{'):
               if (input_list[index+11] == '}'):
                  for x in range(index+12, len(input_list)):
                     if (input_list[x] == ';'):
                        return x
            for x in range(index+9, len(input_list)):
               if (input_list[x] == ';'):
                  return x
         else:  
            arg1 = Argument(input_list[index+9], input_list[index+8])
            method1.add_arguments(arg1)
            if (input_list[index+10] == ")"):
               for x in range(index+11, len(input_list)):
                  if (input_list[x] == ';'):
                     return x
            elif (input_list[index+10] == ','):
               print('method has more than one argument')

            else:
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
      else:
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)
            
   elif (input_list[index+3] == 'private'):
      print('som v private')
      print(input_list[index+4])
      if (input_list[index+4] != ':'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)

      print('presiel som')
      if (test_type(input_list[index+5]) != False):
         print('mam typ')
         if (input_list[index+7] == ';'):
            attr1 = Attribute(input_list[index+6], input_list[index+5], class1)
            class1.add_attribute(attr1)
            return index+7

         elif (input_list[index+7] == '('):
            method1 = Method(input_list[index+6], input_list[index+5])
            class1.add_method(method1)
            if (test_type(input_list[index+8]) != False):
               if (input_list[index+8] != 'void'):
                  arg1 = Argument(input_list[index+9], input_list[index+8])
                  method1.add_arguments(arg1)
               elif (input_list[index+9] == ')'):
                  if (input_list[index+10] == '{'):
                     if (input_list[index + 11] != '}'):
                        sys.stderr.write('Wrong input file formating!\n')
                        sys.exit(4)
                        return index+12

                  
            elif (input_list[index+8] == ')'):
               if (input_list[index+9] == '{'):
                  if (input_list[index + 10] != '}'):
                     sys.stderr.write('Wrong input file formating!\n')
                     sys.exit(4)
                  return index+11

            else: 
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)

      elif (input_list[index+5] == 'virtual'):
         print('elseifvirutal')
         print(input_list[index+6])
         if (test_type(input_list[index+6]) != False):

            if (input_list[index+8] == '('):
               print('typ', input_list[index+6])
               method1 = Method(input_list[index+7], input_list[index+6])
               print(method1.mtype)
               class1.add_method(method1)
               if (test_type(input_list[index+9]) != False):
                  if (input_list[index+9] != 'void'):
                     arg1 = Argument(input_list[index+10], input_list[index+9])
                     method1.add_arguments(arg1)
                     
                  elif (input_list[index+10] == ')'):
                     if (input_list[index+11] == '{'):
                        if (input_list[index + 12] != '}'):
                           sys.stderr.write('Wrong input file formating!\n')
                           sys.exit(4)
                           return index+13
                     elif (input_list[index+11] == '='):
                        if (input_list[index+12] == '0'):
                           method1.pure = 'yes'
                           print('som pred returnom')
                           return index+13

                     
               elif (input_list[index+9] == ')'):
                  if (input_list[index+10] == '{'):
                     if (input_list[index + 11] != '}'):
                        sys.stderr.write('Wrong input file formating!\n')
                        sys.exit(4)
                     return index+12

            else: 
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)

            
   elif (input_list[index+3] == 'protected'):
      print('protected')

   elif (input_list[index+3] == 'using'):
      print('mam using')
      if class_list:
         print('mam class list')
         for clss in class_list:
            if (clss.name == input_list[index+4]):
               print('nasiel som clss')

               if (input_list[index+5] != ':'):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
               if (input_list[index+6] != ':'):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
               for attr in clss.attributes:
                  if (attr.name == input_list[index+7]):
                     for attr2 in class1.attributes:
                        if (attr.name == attr2.name) and (attr.attype == attr2.attype):
                           continue
                        elif (attr.name == attr2.name):
                           class1.attributes.remove(attr2)
                     return index+8
                  else:
                     sys.stderr.write('Wrong input file formating!\n')
                     sys.exit(4)
                  
                  
 
   # elif (input_list[index+3] == '}'):
   #    print('som v ife v def')
   #    if (input_list[index+4] != ';'):
   #       sys.stderr.write('Wrong input file formating!\n')
   #       sys.exit(4)
   #    return index+2

   else:
      print('som v definition v else')
      print(input_list[index+3])
      if (test_type(input_list[index+3]) == False):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)

      if (input_list[index+5] == ";"):
         attribute1 = Attribute(input_list[index+4], input_list[index+3], class1)
         class1.add_attribute(attribute1)
         return index+4

      elif(input_list[index+5] == "("):
         print('pridavam metodu v definition')
         method1 = Method(input_list[index+4], input_list[index+3])
         class1.add_method(method1)   
         if (input_list[index+6] == ')'):
            if (input_list[index+7] == '{'):
               for x in range(index+8, len(input_list)):
                  if (input_list[x] == ';'):
                     return x

         else:
            if (test_type(input_list[index+6]) == False):
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
            if (test_type(input_list[index+6]) == 'void'):
               for x in range(index+7, len(input_list)):
                  if (input_list[x] == ';'):
                     return x
            else:  
               arg1 = Argument(input_list[index+7], input_list[index+6])
               method1.add_arguments(arg1)
               if (input_list[index+8] == ")"):
                  for x in range(index+9, len(input_list)):
                     if (input_list[x] == ';'):
                        return x
               elif (input_list[index+8] == ','):
                  print('method has more than one argument')

               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
      else:
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)




def analysis(input_list):
   print ('som v analysis')
   #global defined_class
   class_list = []
   #for item in input_list:
   for i in range(len(input_list)):
      if (input_list[i] == 'class'):
         print ('som v ife')
         class1 = Class(input_list[i+1])
         #defined_class.append(class1.name)
         if (input_list[i+2] == '{'):
            if (input_list[i+3] == '}'):
               if (input_list[i+4] == ';'):
                  print('pridavam triedu')
                  class_list.append(class1)
                  continue
            else:
               print('som v else')
               index = definition(class_list, input_list, class1, i)
               while (input_list[index+1] != '}'):
                  index = definition(class_list, input_list, class1, index+1)


         elif (input_list[i+2] == ":"):
            print('som v else s :')
            if (input_list[i+3] == 'protected'):
               print('som v protected')
               for clss in class_list:
                  if (input_list[i+4] == clss.name):
                     clss.privacy = 'protected'    
                     clss.is_parent()   
                     class1.add_parent_class(clss)
                     if (clss.kind != 'concrete'):
                        class1.kind = clss.kind
                     for m in clss.methods:
                        if (m.pure != 'yes'):
                           m.privacy = 'protected'
                           class1.add_method(m)
                     for a in clss.attributes:
                        a.privacy = 'protected'
                        print(a.name)
                        print('pridavam attribute')
                        class1.add_attribute(a)
               if (input_list[i+5] == ','):
                  for clss in class_list:
                     if (input_list[i+6] == clss.name):  
                        clss.is_parent()     
                        class1.add_parent_class(clss)
                        if (clss.kind != 'concrete'):
                           class1.kind = clss.kind
                        print('pridavam parenta')
                        for m in clss.methods:
                           if (m.pure != 'yes'):
                              class1.add_method(m)
                        for a in clss.attributes:
                           print('som vo fore pridavam atr')
                           class1.add_attribute(a)
                        print('som pridal parenta a mam:', input_list[i+7])
                        if (input_list[i+7] == '{'): 
                           if (input_list[i+8] == '}'):
                              if (input_list[i+9] != ';'):
                                 sys.stderr.write('Wrong input file formating!\n')
                                 sys.exit(4)
                           else:
                              print('som v posratom else')
                              index = definition(class_list, input_list, class1, i+5)
                              while (input_list[index+1] != '}'):
                                 index = definition(class_list, input_list, class1, index+1)
                        else:
                           sys.stderr.write('Wrong input file formating!\n')
                           sys.exit(4)

               elif (input_list[i+5] == '{'):
                  if (input_list[i+6] == '}'):
                     if (input_list[i+7] != ';'):
                        sys.stderr.write('Wrong input file formating!\n')
                        sys.exit(4)

                  else:
                     index = definition(class_list, input_list, class1, i+3)
                     while (input_list[index+1] != '}'):
                        index = definition(class_list, input_list, class1, index+1) 
               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

            elif(input_list[i+3] == 'public'):
               print('som v public s :')
               for clss in class_list:
                  if (input_list[i+4] == clss.name):
                     clss.privacy = 'public'    
                     clss.is_parent()   
                     class1.add_parent_class(clss)
                     if (clss.kind != 'concrete'):
                        class1.kind = clss.kind

                     for m in clss.methods:
                        class1.add_method(m)

                     for a in clss.attributes:
                        a.privacy = 'public'
                        print(a.name)
                        print('pridavam attribute')
                        class1.add_attribute(a)
               if (input_list[i+5] == ','):
                  if (input_list[i+6] == 'public'):
                      for clss in class_list:
                        if (input_list[i+7] == clss.name):  
                           clss.privacy = 'public'
                           clss.is_parent()     
                           class1.add_parent_class(clss)
                           if (clss.kind != 'concrete'):
                              class1.kind = clss.kind
                           print('pridavam parenta')
                           for m in clss.methods:
                              class1.add_method(m)
                           for a in clss.attributes:
                              print('som vo fore pridavam atr')
                              class1.add_attribute(a)
                           print('som pridal parenta a mam:', input_list[i+8])
                           if (input_list[i+8] == '{'): 
                              if (input_list[i+9] == '}'):
                                 if (input_list[i+10] != ';'):
                                    sys.stderr.write('Wrong input file formating!\n')
                                    sys.exit(4)
                              else:
                                 print('som v posratom else')
                                 index = definition(class_list,input_list, class1, i+6)
                                 while (input_list[index+1] != '}'):
                                    index = definition(class_list, input_list, class1, index+1)
                           else:
                              sys.stderr.write('Wrong input file formating!\n')
                              sys.exit(4)
                  else:
                     for clss in class_list:
                        if (input_list[i+6] == clss.name):  
                           clss.is_parent()     
                           class1.add_parent_class(clss)
                           if (clss.kind != 'concrete'):
                              class1.kind = clss.kind
                           print('pridavam parenta')
                           for m in clss.methods:
                              class1.add_method(m)
                           for a in clss.attributes:
                              print('som vo fore pridavam atr')
                              class1.add_attribute(a)
                           print('som pridal parenta a mam:', input_list[i+7])
                           if (input_list[i+7] == '{'): 
                              if (input_list[i+8] == '}'):
                                 if (input_list[i+9] != ';'):
                                    sys.stderr.write('Wrong input file formating!\n')
                                    sys.exit(4)
                              else:
                                 print('som v posratom else')
                                 index = definition(class_list, input_list, class1, i+5)
                                 while (input_list[index+1] != '}'):
                                    index = definition(class_list, input_list, class1, index+1)
                           else:
                              sys.stderr.write('Wrong input file formating!\n')
                              sys.exit(4)

               elif (input_list[i+5] == '{'):
                  if (input_list[i+6] == '}'):
                     if (input_list[i+7] != ';'):
                        sys.stderr.write('Wrong input file formating!\n')
                        sys.exit(4)

                  else:
                     index = definition(class_list, input_list, class1, i+3)
                     while (input_list[index+1] != '}'):
                        index = definition(class_list, input_list, class1, index+1) 
               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

            else:
               print('som v else :')
               for clss in class_list:
                  print(clss.name)
                  print(input_list[i+3])
                  if (input_list[i+3] == clss.name): 
                     print('som v ife')
                     clss.is_parent()   
                     class1.add_parent_class(clss)
                     if (clss.kind != 'concrete'):
                        class1.kind = clss.kind
                     for m in clss.methods:
                           class1.add_method(m)
                     
                     for a in clss.attributes:
                        class1.add_attribute(a)
               if (input_list[i+4] == ','):
                  for clss in class_list:
                     if (input_list[i+5] == clss.name):   
                        clss.is_parent()    
                        class1.add_parent_class(clss)
                        if (clss.kind != 'concrete'):
                           class1.kind = clss.kind

                        for m in clss.methods:
                           if (m.pure != 'yes'):
                              class1.add_method(m)
                        for a in clss.attributes:
                           class1.add_attribute(a)
                  if (input_list[i+6] == '{'):
                     if (input_list[i+7] == '}'):
                        if (input_list[i+8] != ';'):
                           sys.stderr.write('Wrong input file formating!\n')
                           sys.exit(4)

                     else:
                        index = definition(class_list, input_list, class1, i+4)
                        while (input_list[index+1] != '}'):
                           index = definition(class_list, input_list, class1, index+1)
                  else:
                     sys.stderr.write('Wrong input file formating!\n')
                     sys.exit(4)

                  # if (input_list[i+7] == "}"):
                  #    if (input_list[i+8] == ";"):
                  #       class_list.append(class1)
                  #       continue

               elif (input_list[i+4] == '{'):
                  if (input_list[i+5] == '}'):
                     if (input_list[i+6] != ';'):
                        sys.stderr.write('Wrong input file formating!\n')
                        sys.exit(4)

                  # if (input_list[i+5] == '}'):
                  #    if (input_list[i+6] == ';'):
                  #       class_list.append(class1)
                  #       continue

                  else:
                     print('som pred def')
                     index = definition(class_list, input_list, class1, i+2)
                     print(input_list[index])
                     while (input_list[index+1] != '}'):
                        index = definition(class_list, input_list, class1, index-2)
               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

         else:
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
         print('pridavam triedu')
         # print(class1.name)
         # if class1.methods:
         #    print(class1.methods[0].name)
         class_list.append(class1)
   for i in range(len(class_list)):
      print (class_list[i].name)
   # for i in range(len(defined_class)):
   #    print(defined_class[i])
   return class_list


def parser(input_content):
   word = ''
   input_list = []
   
   for char in input_content:
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
         if (char == ';') and (word != ''):
            input_list.append(word)
            word = ''
         input_list.append(char)
      elif (char != '\n') and (char != ' ') and (char != '\t'):
         if ((char == ',') or (char == ':')) and (word != ''):
            input_list.append(word)
            input_list.append(char)
            word = ''
         else:   
            if(char == ':') and (word == ''):
               input_list.append(char)
               continue
            word += char
         continue
   print (input_list)
   class_list = analysis(input_list)
   return class_list

def main(argv):
   inputfilename = ''
   outputfilename = ''
   classname = ''
   global details
   k = 4
   stdin = True
   stdout = True
   try:
      opts, args = getopt.getopt(argv,"i:o:",["help", "input=", "output=", "pretty-xml=", "details="])
   except getopt.GetoptError:
      sys.stderr.write('Wrong parameters formating!\n')
      sys.exit(1)
   for opt, arg in opts:
      if opt == '--help':
         print ('usage: $ python3.6 cls.py --input=file --output=file --pretty-xml=k --details=class')
         sys.exit()
      elif opt in ("--input="):
         inputfilename = arg
         stdin = False
      elif opt in ("--output="):
         outputfilename = arg
         stdout = False
      elif opt in ("--pretty-xml"):
         if (arg != '') and (arg.isdigit()):
            k = arg
         else:
            sys.stderr.write('Wrong parameters formating!\n')
            sys.exit(1)

      elif opt in ("--details"):
         classname = arg
         details = True

   if (stdin == False):
      print ('Input file name:', inputfilename) 
      inputfile = open(inputfilename, 'r')
      input_content = inputfile.read()

   else:
      input_content = input()
      input_content += '\n'

   # class_list = parser(input_content)

   output(stdout, outputfilename, k, parser(input_content), classname)

   #closing files
   if (stdin == False):
      inputfile.close()
   
if __name__ == "__main__":
   main(sys.argv[1:])