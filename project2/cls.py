#!/usr/bin/python

#  Title: IPP Project 2, CLS (C++ Classes)
#  Author: Ondrej Svoreň 
#  Login: xsvore01

#used libraries
import sys, getopt, argparse

#global variables
details = False
details_all = False
conflicts = False
args = False
private = False
public = False
protected = False
stdout = True
k = 2

privacy_next = 'private'
mystr = 'none'
outputfile = ''
classname = ''

class_list = []
meth_list = []
attr_list = []

#Classes definitions
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
      self.is_parent = False
      self.virtual = False
      self.constOrDest = False

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


#function proceeds output in required formate in case of input argument "--details=classname" and takes "classname" as one of the function parameters
def details_output(classname, methorattr, mthattr, privacy, n, k_string, stdout, outputfile):
   global private
   global public
   global protected
   global meth_list
   global attr_list
   global args

   mylist = []
   for i in range(len(methorattr)):
      if (mthattr == 'methods'):
         if (methorattr[i].privacy == privacy) and ((methorattr[i].constOrDest != True) or (methorattr[i].name == classname) or (methorattr[i].name == '~' + classname)):
            mylist.append(methorattr[i])
      else:
         if (methorattr[i].privacy == privacy):
            mylist.append(methorattr[i])

   if (mthattr == 'methods'):
      if mylist:
         if (privacy == 'private'):
            mylist = list(set(mylist) - set(meth_list))
            if mylist:
               private = True
         elif (privacy == 'protected'):
            mylist = list(set(mylist) - set(meth_list))
            if mylist:
               protected = True
         elif (privacy == 'public'):
            mylist = list(set(mylist) - set(meth_list))
            if mylist:
               public = True
         if mylist:   
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
                  if (method.virtual == True):
                     print(k_string*n + '<virtual pure="' + method.pure + '"/>')
                  

               elif (stdout == False):
                  outputfile.write(k_string*n + '<method name="' + method.name + '" type="' + method.mtype + '" scope="' + method.scope + '">\n')
                  n += 1
                  if (method.parentcls.name != classname):
                     n += 1
                     outputfile.write(k_string*n + '<from name="' + method.parentcls.name + '"/>\n')
                     # n -= 1
                  if (method.virtual == True):
                     outputfile.write(k_string*n + '<virtual pure="' + method.pure + '"/>\n')
                  
               
               if method.arguments:
                  args = True
                  if(stdout == True):
                     
                     print (k_string*n + '<arguments>')   
                  else:
                     
                     outputfile.write(k_string*n + '<arguments>\n')
                  n += 1
                  for arg in method.arguments:
                     
                     if (stdout == True):
                        print(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype +'"/>')
                     else:
                        outputfile.write(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype +'"/>\n')
                  n -= 1
                  
               
               if (args == True):
                  args = False
                  if(stdout == True):
                     print (k_string*n + '</arguments>')
                  else:
                     outputfile.write(k_string*n + '</arguments>\n')
               else:
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
            mylist = list(set(mylist) - set(attr_list))

            if mylist:
               private = True 
               if (stdout == True):
                  print(k_string*n + '<' + privacy + '>')
               else:
                  outputfile.write(k_string*n + '<' + privacy + '>\n')
         elif (privacy == 'protected') and (protected == False):
            mylist = list(set(mylist) - set(attr_list))
            if mylist:
               protected = True
               if (stdout == True):
                  print(k_string*n + '<' + privacy + '>')
               else:
                  outputfile.write(k_string*n + '<' + privacy + '>\n')

         elif (privacy == 'public') and (public == False):
            mylist = list(set(mylist) - set(attr_list))
            if mylist:
               public = True
               if (stdout == True):
                  print(k_string*n + '<' + privacy + '>')
               else:
                  outputfile.write(k_string*n + '<' + privacy + '>\n')

         if (mylist):

            n += 1   
            if(stdout == True):
               print(k_string*n + '<attributes>')
            else:
               outputfile.write(k_string*n + '<attributes>\n')
            n += 1
            for attr in mylist:
               if (stdout == True) and (attr.privacy == privacy) and (attr.parentcls.name != classname):
                  print (k_string*n + '<attribute name="' + attr.name + '" type="' + attr.attype + '" scope="' + attr.scope + '">')
                  n += 1
                  print (k_string*n + '<from name="' + attr.parentcls.name + '"/>')
                  n -= 1
               elif (stdout == True) and (attr.privacy == privacy):
                   print (k_string*n + '<attribute name="' + attr.name + '" type="' + attr.attype + '" scope="' + attr.scope + '"/>')
               
               elif (stdout == False) and (attr.privacy == privacy) and (attr.parentcls.name != classname):
                  outputfile.write(k_string*n + '<attribute name="' + attr.name + '" type="' + attr.attype + '" scope="' + attr.scope + '">\n')
                  n += 1
                  outputfile.write(k_string*n + '<from name="' + attr.parentcls.name + '"/>\n')
                  n -= 1
               elif (stdout == False) and (attr.privacy == privacy):
                  outputfile.write(k_string*n + '<attribute name="' + attr.name + '" type="' + attr.attype + '" scope="' + attr.scope + '"/>\n')
            
               
               if(stdout == True):
                  if (attr.parentcls.name != classname):
                     print(k_string*n + '</attribute>')
               else:
                  if (attr.parentcls.name != classname):
                     outputfile.write(k_string*n + '</attribute>\n')
            n -= 1
            if (stdout == True):
               print(k_string*n + '</attributes>')
            else:
               outputfile.write(k_string*n + '</attributes>\n')

#recursive function used in case without argument "--details", the output is inheritance tree
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

#function proceeds output in form of xml elements and calls another output functions depending on the input command line arguments
def output(stdout, outputfilename, k, class_list, classname = ''):

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
         try:
            outputfile = open(outputfilename, 'w')
         except IOError:
            sys.stderr.write('Error opening output file!\n')
            sys.exit(3)
         else: 
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
         try:
            outputfile = open(outputfilename, 'w')
         except IOError:
            sys.stderr.write('Error opening output file!\n')
            sys.exit(3)
         else: 
            outputfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            outputfile.write('<model>')
      
      for clss in class_list:
         if (stdout == True):
            print(k_string*n + '<class name="' + clss.name + '" kind="' + clss.kind + '">')
         else:
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
            private = False
            outputfile.write(k_string*n + '</private>\n')
   

         details_output(clss.name, clss.methods, 'methods', 'protected', n, k_string, stdout, outputfile) 

         details_output(clss.name, clss.attributes, 'attributes', 'protected', n, k_string, stdout, outputfile)  
         

         if (stdout == True) and (protected == True):
            protected = False
            print (k_string*n + '</protected>')
         elif (stdout == False) and (protected == True):
            protected = False
            outputfile.write(k_string*n + '</protected>\n')


         details_output(clss.name, clss.methods, 'methods', 'public', n, k_string, stdout, outputfile) 

         details_output(clss.name, clss.attributes, 'attributes', 'public', n, k_string, stdout, outputfile)  
         

         if (stdout == True) and (public == True):
            public = False
            print (k_string*n + '</public>')
         elif (stdout == False) and (public == True):
            public = False
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
            try:
               outputfile = open(outputfilename, 'w')
            except IOError:
               sys.stderr.write('Error opening output file!\n')
               sys.exit(3)
            else: 
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
            try:
               outputfile = open(outputfilename, 'w')
            except IOError:
               sys.stderr.write('Error opening output file!\n')
               sys.exit(3)
            else: 
               outputfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
               outputfile.close()

#function proceeds testing, if the input argument of the function (string) has approved data type
#function proceeds also constructor and destruktor test
def test_type(string):
   global class_list
   is_def = False
   types = ['A','B','C','D',
            'A *','B *','C *','D *',
            'A &amp;','B &amp;','C &amp;','D &amp;',
            'int', 'int *', 'int &amp;',
           'float', 'float *', 'float &amp;', 
           'double', 'double *', 'double &amp;',
           'long double', 'long double *', 'long double &amp;', 'void', 'void *', 'void &amp;',
           'bool', 'bool *', 'bool &amp;',
           'char', 'char *', 'char &amp;',
           'char16_t', 'char16_t *', 'char16_t &amp;', 'char32_t', 'char32_t *', 'char32_t &amp;',
           'wchar_t', 'wchar_t *', 'wchar_t &amp;','signed char', 'signed char *', 'signed char &amp;',
           'short int', 'short int *', 'short int &amp;', 'long int', 'long int *', 'long int &amp;', 'long long int',
           'long long int *', 'long long int &amp;', 'unsigned char', 'unsigned char *', 'unsigned char &amp;',
           'unsigned short int', 'unsigned short int *', 'unsigned short int &amp;', 'unsigned int', 'unsigned int *',
           'unsigned int &amp;', 'unsigned long int', 'unsigned long int *', 'unsigned long int &amp;',
           'unsigned long long int', 'unsigned long long int *', 'unsigned long long int &amp;','short','short *','short &amp;','long','long *','long &amp;','unsigned short','unsigned short *','unsigned short &amp;','unsigned','unsigned *','unsigned &amp;','unsigned long','unsigned long *','unsigned long &amp;','unsigned long long','unsigned long long *','unsigned long long &amp;']

   classes = ['A','B','C','D',
            'A *','B *','C *','D *',
            'A &amp;','B &amp;','C &amp;','D &amp;']


   for classname in classes:
      if (string == classname):
         for clss in class_list:
            if (clss.name in string):
               is_def = True
               break
         if (is_def == False):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)    


   for t in types:
      if (string == t):
         return t

   return False

#function detects conflicts in inheritance and in case of conflict proceeds required output
def is_conflict(class1):

   global conflicts
   global outputfile
   global k
   global classname

   conflict_all = False

   k_string = k * ' '
   n = 2

   if (class1.attributes) and (class1.methods):
      for attr in class1.attributes:
         for meth in class1.methods:
            if (attr.name == meth.name):
               sys.stderr.write('Conflict in inheritance!\n')
               sys.exit(21)

   if (class1.attributes) and (len(class1.attributes) != 1):
      for i in range(len(class1.attributes)-1):
         for j in range(i+1, len(class1.attributes)):
            if (class1.attributes[i].name == class1.attributes[j].name) and (class1.attributes[i].parentcls != class1 and class1.attributes[j].parentcls != class1):
               if (conflicts != True):
                  if (classname == class1.name) or (classname == ''):
                     sys.stderr.write('Conflict in inheritance!\n')
                     sys.exit(21)
                  else:
                     return

               else:
                  for attr in class1.attributes[i].parentcls.attributes:
                     if (attr.name == class1.attributes[i].name):
                        privacy = attr.privacy

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
                     print(k_string*n + '<' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '<' + privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<attribute name="' + class1.attributes[i].name + '" type="' + class1.attributes[i].attype + '" scope="' + class1.attributes[i].scope + '"/>')
                  else:
                     outputfile.write(k_string*n + '<attribute name="' + class1.attributes[i].name + '" type="' + class1.attributes[i].attype + '" scope="' + class1.attributes[i].scope + '"/>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + privacy + '>\n')

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

                  for attr in class1.attributes[j].parentcls.attributes:
                     if (attr.name == class1.attributes[j].name):
                        privacy = attr.privacy
                  if (stdout == True):
                     print(k_string*n + '<class name="' + class1.attributes[j].parentcls.name + '">')
                  else:
                     outputfile.write(k_string*n + '<class name="' + class1.attributes[j].parentcls.name + '">\n')

                  n += 1

                  if (stdout == True):
                     print(k_string*n + '<' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '<' + privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<attribute name="' + class1.attributes[j].name + '" type="' + class1.attributes[j].attype + '" scope="' + class1.attributes[i].scope + '"/>')
                  else:
                     outputfile.write(k_string*n + '<attribute name="' + class1.attributes[j].name + '" type="' + class1.attributes[j].attype + '" scope="' + class1.attributes[i].scope + '"/>\n')

                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + privacy + '>\n')

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

   if (class1.methods) and (len(class1.methods) != 1):
      for i in range(len(class1.methods)):
         if (class1.methods[i].constOrDest == True):
            continue
         for j in range(i+1, len(class1.methods)):
            if (class1.methods[j].constOrDest == True):
               continue
            if (class1.methods[i].name == class1.methods[j].name) and (class1.methods[i].parentcls != class1) and (class1.methods[j].parentcls != class1) and (len(class1.methods[i].arguments) == len(class1.methods[j].arguments)):
               if (conflicts != True):
                  if (classname == class1.name) or (classname == ''):
                     sys.stderr.write('Conflict in inheritance!\n')
                     sys.exit(21)
                  else:
                     return
               else:
                  for m in class1.methods[i].parentcls.methods:
                     if (m.name == class1.methods[i].name):
                        privacy = m.privacy
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
                     print(k_string*n + '<' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '<' + privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<method name="' + class1.methods[i].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '">')
                  else:
                     outputfile.write(k_string*n + '<method name="' + class1.methods[i].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '">\n')

                  if class1.methods[i].arguments:
                     n += 1
                     if (stdout == True):
                        print(k_string*n + '<arguments>')
                     else:
                        outputfile.write(k_string*n + '<arguments>\n')
                     for arg in class1.methods[i].arguments:
                        n += 1
                        if (stdout == True):
                           print(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype + '"/>' )
                        else:
                           outputfile.write(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype + '"/>\n')
                        n -= 1

                     if (stdout == True):
                        print(k_string*n + '</arguments>')
                     else:
                        outputfile.write(k_string*n + '</arguments>\n')


                  else:
                     n += 1
                     if (stdout == True):
                        print(k_string*n + '<arguments/>')
                     else:
                        outputfile.write(k_string*n + '<arguments/>\n')
                     n -=1


                  n -= 1
                  if (stdout == True):
                     print(k_string*n + '</method>')
                  else:
                     outputfile.write(k_string*n + '</method>\n')


                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + privacy + '>\n')

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

                  for m in class1.methods[j].parentcls.methods:
                     if (m.name == class1.methods[j].name):
                        privacy = m.privacy
                  if (stdout == True):
                     print(k_string*n + '<class name="' + class1.methods[j].parentcls.name + '">')
                  else:
                     outputfile.write(k_string*n + '<class name="' + class1.methods[j].parentcls.name + '">\n')

                  n += 1

                  if (stdout == True):
                     print(k_string*n + '<' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '<' + privacy + '>\n')

                  n += 1 
                  
                  if (stdout == True):
                     print(k_string*n + '<method name="' + class1.methods[j].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '">')
                  else:
                     outputfile.write(k_string*n + '<method name="' + class1.methods[j].name + '" type="' + class1.methods[i].mtype + '" scope="' + class1.methods[i].scope + '">\n')

                  if class1.methods[j].arguments:
                     n += 1
                     if (stdout == True):
                        print(k_string*n + '<arguments>')
                     else:
                        outputfile.write(k_string*n + '<arguments>\n')
                     for arg in class1.methods[j].arguments:
                        n += 1
                        if (stdout == True):
                           print(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype + '"/>' )
                        else:
                           outputfile.write(k_string*n + '<argument name="' + arg.name + '" type="' + arg.argtype + '"/>\n')
                        n -= 1

                     if (stdout == True):
                        print(k_string*n + '</arguments>')
                     else:
                        outputfile.write(k_string*n + '</arguments>\n')


                  else:
                     n += 1
                     if (stdout == True):
                        print(k_string*n + '<arguments/>')
                     else:
                        outputfile.write(k_string*n + '<arguments/>\n')
                     n -=1


                  n -= 1
                  if (stdout == True):
                     print(k_string*n + '</method>')
                  else:
                     outputfile.write(k_string*n + '</method>\n')


                  n -= 1

                  if (stdout == True):
                     print(k_string*n + '</' + privacy + '>')
                  else:
                     outputfile.write(k_string*n + '</' + privacy + '>\n')

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

                  if not class1.methods:
                     return

#function proceeds inheritance of attributes and methods depending on the privacy
def derivate(input_list, class1, privacy, index):
   global class_list
   global conflicts
   global passed
   global meth_list
   global attr_list
   base_class = ''

   for clss in class_list:
      if (clss.name == input_list[index]) and (clss.name != class1.name):
         base_class = clss
         break

   if (base_class == ''):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)

   base_class.privacy = privacy

   for parent in class1.parents:
      if (parent == base_class):
         sys.stderr.write('Wrong input file format!\n')
         sys.exit(4)
   class1.add_parent_class(base_class)
   
   if (base_class.kind != 'concrete'):
      class1.kind = base_class.kind

   for m in base_class.methods:      
      if (privacy == 'public'):

         method1 = Method(m.name, m.mtype, m.parentcls, m.scope, m.privacy, m.pure)
         method1.privacy = m.privacy
         method1.virtual = m.virtual
         method1.arguments = m.arguments
         method1.constOrDest = m.constOrDest
         class1.add_method(method1)
         if (m.privacy == 'private'):
            meth_list.append(method1)

      elif (privacy == 'protected'):
         
         method1 = Method(m.name, m.mtype, m.parentcls, m.scope, m.privacy, m.pure)
         method1.privacy = privacy
         method1.virtual = m.virtual
         method1.arguments = m.arguments
         method1.constOrDest = m.constOrDest
         class1.add_method(method1)
         if (m.privacy == 'private'):
            meth_list.append(method1)

      elif (privacy == 'private'):
        
         method1 = Method(m.name, m.mtype, m.parentcls, m.scope, m.privacy, m.pure)
         method1.privacy = privacy
         method1.virtual = m.virtual
         method1.arguments = m.arguments
         method1.constOrDest = m.constOrDest
         class1.add_method(method1)
         if (m.privacy == 'private'):
            meth_list.append(method1)


   for attr in base_class.attributes:
      if (privacy == 'public'):
        
         attr1 = Attribute(attr.name, attr.attype, attr.parentcls, attr.scope, attr.privacy)
         attr1.privacy = attr.privacy
         class1.add_attribute(attr1)
         if (attr.privacy == 'private'):
            attr_list.append(attr1)

      elif (privacy == 'protected'):
        
         attr1 = Attribute(attr.name, attr.attype, attr.parentcls, attr.scope, attr.privacy)
         attr1.privacy = privacy
         class1.add_attribute(attr1)
         if (attr.privacy == 'private'):
            attr_list.append(attr1)

      elif (privacy == 'private'):
         attr1 = Attribute(attr.name, attr.attype, attr.parentcls, attr.scope, attr.privacy)
         attr1.privacy = privacy
         class1.add_attribute(attr1)
         if (attr.privacy == 'private'):
            attr_list.append(attr1)  

#function determinates privacy in case of inheritance and uses it as one of the arguments of function "derivate"
def inheritance_privacy(input_list, class1, index):
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
      return index+1

#function proceeds declaration of methods and arguments, attributes, constructors and destructors in concrete class
def declaration(class1, input_list, scope, privacy, virtual, index):
   pureness = 'no'
   if (test_type(input_list[index]) != False):
      if (input_list[index+1] == '('): 
         constructor = Method(input_list[index], 'void', class1, scope, privacy)
         constructor.constOrDest = True
         i = index + 2 
         while (input_list[i] != ')'):
            if (input_list[i] == 'void'):
               i += 1
               continue
            if (test_type(input_list[i]) != False):
               arg1 = Argument(input_list[i+1], input_list[i])
               constructor.add_argument(arg1)
               if (input_list[i+2] == ','):
                  i = i + 3
               elif (input_list[i+2] == ')'):
                  i = i + 2
                  break 
               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

         if (input_list[i+1] == '{'):
            if (input_list[i+2] != '}'):
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
            class1.add_method(constructor)
            if (input_list[i+3] == ';'):
               return i+4
            else:
               return i+3
         elif (input_list[i+1] == ';'):
            class1.add_method(constructor)
            return i+2
         else:
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)         
      
      if (input_list[index+2] == ';'):
         attr1 = Attribute(input_list[index+1], input_list[index], class1, scope, privacy)
         x = 0
         length = len(class1.attributes)
         if (length != 0):
            while (x < length):
               if (class1.attributes[x].name == attr1.name) and (class1.attributes[x].attype == attr1.attype) and (class1.attributes[x].parentcls == class1):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
               elif (class1.attributes[x].name == attr1.name) and (class1.attributes[x].parentcls == class1):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
               elif (class1.attributes[x].name == attr1.name) and (class1.attributes[x].attype == attr1.attype) and (class1.attributes[x].parentcls != class1):
                  del class1.attributes[x]
                  length -= 1
               else:
                  x += 1

         if class1.methods:
            for m in class1.methods:
               if (m.name == attr1.name):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

         class1.add_attribute(attr1)
         return index+3

      elif (input_list[index+2] == '='):
         if (input_list[index+4] == ';'):
            attr1 = Attribute(input_list[index+1], input_list[index], class1, scope, privacy)
            x = 0
            length = len(class1.attributes)
            while (x < length):
               if (class1.attributes[x].name == attr1.name) and (class1.attributes[x].attype == attr1.attype) and (class1.attributes[x].parentcls == class1):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)
               elif (class1.attributes[x].name == attr1.name) and (class1.attributes[x].attype == attr1.attype) and (class1.attributes[x].parentcls != class1):
                  del class1.attributes[x]
                  length -= 1
               else:
                  x += 1

            for m in class1.methods:
               if (m.name == attr1.name):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

            class1.add_attribute(attr1)
            return index+5

      elif (input_list[index+2] == '('):
         method1 = Method(input_list[index+1], input_list[index], class1, scope, privacy)
         if (virtual == 'yes'):
            method1.virtual = True
         i = index+3

         while (input_list[i] != ')'):
            if (input_list[i] == 'void'):
               i += 1
               continue

            if (test_type(input_list[i]) != False):
               arg1 = Argument(input_list[i+1], input_list[i])
               method1.add_argument(arg1)
               if (input_list[i+2] == ','):
                  i = i + 3
               elif (input_list[i+2] == ')'):
                  i = i + 2
                  break
            
            else:
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)

         if (input_list[i+1] == '='):
            if (input_list[i+2] == '0'):
               if (input_list[i+3] == ';'):
                  if (virtual == 'yes'):   
                     method1.pure = 'yes'
                     method1.virtual = True
                     class1.kind = 'abstract'

                     for attr in class1.attributes:
                        if (attr.name == method1.name):
                           sys.stderr.write('Wrong input file formating!\n')
                           sys.exit(4)
                  else:
                     sys.stderr.write('Wrong input file formating!\n')
                     sys.exit(4)
                  class1.add_method(method1)
                  return i+4

               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

         elif (input_list[i+1] == ';'):
            class1.add_method(method1)
            return i+2

         elif (input_list[i+1] != '{'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)

         if (input_list[i+2] != '}'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)

         x = 0
         length = len(class1.methods)
         while (x < length):
            if (class1.methods[x].name == method1.name) and (class1.methods[x].mtype == method1.mtype) and (class1.methods[x].parentcls != class1):
               class1.methods.remove(class1.methods[x])
               length -= 1
            elif (class1.methods[x].name == method1.name) and (class1.methods[x].mtype == method1.mtype) and (class1.methods[x].parentcls == class1):
               if (class1.methods[x].arguments) and (method1.arguments):
                  for arg in class1.methods[x].arguments:
                     for arg2 in method1.arguments:
                        if (arg.name == arg2.name) and (arg.argtype == arg2.argtype) and (len(method1.arguments) == len(class1.methods[x].arguments)):  
                           sys.stderr.write('Wrong input file formating!\n')
                           sys.exit(4)
               x += 1
            else:
               x += 1

         for attr in class1.attributes:
            if (attr.name == method1.name):
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
         
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

   elif (input_list[index] == '~'):
      if (input_list[index+1] != class1.name):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)
      if (input_list[index+2] != '('):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)
      if (input_list[index+3] != ')'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)   

      destructor = Method(input_list[index] + input_list[index+1], 'void', class1, scope, privacy)
      destructor.constOrDest = True
      if (input_list[index+4] == '{'):
         if (input_list[index+5] != '}'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
         for m in class1.methods:
            if (m.name == destructor.name):
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
         class1.add_method(destructor)
         if (input_list[index+6] == ';'):
            return index+7
         else:
            return index+6
      elif (input_list[index+4] == ';'):
         for m in class1.methods:
            if (m.name == destructor.name):
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)
         class1.add_method(destructor)
         return index+5
      else:
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)

   elif (input_list[index] != '}'):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)
   
   return index

#function proceeds choosing of function or attribute that is inbred from the base class and has to be used in the derived class
def using(class1, input_list, index, privacy = 'private'):
   global class_list

   defined = False
   for clss in class_list:
      if (input_list[index] == clss.name):
         defined = True
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

   if (clss.attributes):
      for attr in clss.attributes:
         if (attr.parentcls.name == clss.name) and (input_list[index+3] == attr.name):
            break
         elif (input_list[index+3] == attr.name):
            clss = attr.parentcls
            break

      x = 0
      length = len(class1.attributes)
      while (x < length):
         if (input_list[index+3] == class1.attributes[x].name) and (class1.attributes[x].parentcls != clss):
            class1.attributes.remove(class1.attributes[x])
            length -= 1
            continue
         elif (input_list[index+3] == class1.attributes[x].name) and (class1.attributes[x].parentcls == clss):
            class1.attributes[x].privacy = privacy
         x += 1

   if (clss.methods):
      for m in clss.methods:

         if (m.parentcls.name == clss.name) and (input_list[index+3] == m.name):
            break
         elif (input_list[index+3] == m.name):
            clss = m.parentcls
            break

      x = 0
      length = len(class1.methods)
      while (x < length):
         if (input_list[index+3] == class1.methods[x].name) and (class1.methods[x].parentcls != clss):
            class1.methods.remove(class1.methods[x])
            length -= 1
            continue
         elif (input_list[index+3] == class1.methods[x].name) and (class1.methods[x].parentcls == clss):
            class1.methods[x].privacy = privacy
         x += 1

   if (input_list[index+4] != ';'):
      sys.stderr.write('Wrong input file formating!\n')
      sys.exit(4)

   return index+5

#function parses definition of the class, determinates privacy and scope of attributes and methods and virtualness of methods in the class and calls function "declaration"
def body_of_class(class1, input_list, index):

   global class_list
   global privacy_next

   scope = 'instance'
   virtual = 'no'
   privacy = 'private'
   defined = False

   if (input_list[index] == '\t'):
      index += 1

   if (input_list[index] == 'static'):
      scope = 'static'
      if (privacy == 'private'):
         privacy = privacy_next
      index = declaration(class1, input_list, scope, privacy, virtual, index+1)
      return index

   elif (input_list[index] == 'private'):
      if (input_list[index+1] != ':'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4) 
      if (input_list[index+2] == '\t'):
         index += 1

      if(input_list[index+2] == '}'):
         return index+2

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

      if (input_list[index+2] == '\t'):
         index += 1

      if(input_list[index+2] == '}'):
         return index+2

      privacy = 'public'
      privacy_next = 'public'
      
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
      if (input_list[index+1] != ':'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4) 

      privacy = 'protected'
      privacy_next = 'protected'

      if (input_list[index+2] == 'private'):
         if (input_list[index+3] ==  ':'):
            privacy = 'private'
            index = index+2

      if (input_list[index+2] == '\t'):
         index += 1

      if(input_list[index+2] == '}'):
         return index+2

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
      if (privacy == 'private'):
         privacy = privacy_next
      index = declaration(class1, input_list, scope, privacy, virtual, index+1)
      return index

   elif (input_list[index] == 'using'):
      index =  using(class1, input_list, index+1)
      return index

   else:
      if (privacy == 'private'):
         privacy = privacy_next
      index = declaration(class1, input_list, scope, privacy, virtual, index)
      return index

#function controls syntax, defines classes and controls defining of functions and attibutes
def analysis(input_list):
   global class_list
   global conflicts
   global privacy_next

   i = 0
   while (i < len(input_list)):
      if (input_list[i] != 'class'):
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)

      else:
         class1 = Class(input_list[i+1])
         class_list.append(class1)

         if (input_list[i+2] == ':'):
            index = inheritance_privacy(input_list, class1, i+3)
            while (input_list[index] != '{'):
               if (input_list[index] == ','):
                  index = inheritance_privacy(input_list, class1, index+1)

               else:
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

            i = index - 2

         elif (input_list[i+2] != '{'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)

         privacy_next = 'private'
         index = body_of_class(class1, input_list, i+3)
         while (input_list[index] != '}'):
            index = body_of_class(class1, input_list, index)

         if (input_list[index+1] != ';'):
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
         i = index + 2

         if (conflicts == False):
            is_conflict(class1)

   return class_list

#function binds strings from parser and creates data type, that matches one of the supported data type and returns it as one string
def word_control(word):

   global mystr
   
   if (word == 'signed'):
      if (mystr == 'none'):
         mystr = word
         return 'next'   
      else:
         sys.stderr.write('Incompatible type!\n')
         sys.exit(4)
   elif (word == 'char'):
      if (mystr == 'signed') or (mystr == 'unsigned'):
         mystr += ' ' + word
         return mystr
      elif (mystr == 'none'):
         return word
      else:
         sys.stderr.write('Incompatible type!\n')
         sys.exit(4)

   elif (word == 'short'):
      if (mystr == 'unsigned'):
         mystr += ' ' + word
         return 'next'
      elif (mystr == 'none'):
         mystr = word
         return 'next'
      else:
         sys.stderr.write('Incompatible type!\n')
         sys.exit(4)
   elif (word == 'int'):
         if (mystr == 'short') or (mystr == 'long') or (mystr == 'long long') or (mystr == 'unsigned short') or (mystr == 'unsigned long') or (mystr == 'unsigned long long') or (mystr == 'unsigned'): 
            mystr += ' ' + word
            return mystr
         elif (mystr == 'none'):
            return word
         else:
            sys.stderr.write('Incompatible type!\n')
            sys.exit(4)
   elif (word == 'long'):
      if (mystr == 'long') or (mystr == 'unsigned') or (mystr == 'unsigned long'):
         mystr += ' ' + word
         return 'next'
      elif (mystr == 'none'):
         mystr = word
         return 'next'
      else:
         sys.stderr.write('Incompatible type!\n')
         sys.exit(4)
   elif (word == 'unsigned'):
      if (mystr == 'none'):
         mystr = word
         return 'next'
      else:
         sys.stderr.write('Incompatible type!\n')
         sys.exit(4)
   elif (word == 'float'):
      if (mystr == 'none'):
         return word
      else:
         sys.stderr.write('Incompatible type!\n')
         sys.exit(4)
   elif (word == 'double'):
      if (mystr == 'long'):
         mystr += ' ' + word
         return mystr
      elif (mystr == 'none'):
         return word
      else:
         sys.stderr.write('Incompatible type!\n')
         sys.exit(4)
   else:
      if (mystr == 'short') or (mystr == 'long') or (mystr == 'long long') or (mystr == 'unsigned short') or (mystr == 'unsigned') or (mystr == 'unsigned long') or (mystr == 'unsigned long long'):
         word = mystr
      mystr = 'none'
      return word

#function parses input file or string from standard input to sequence of tokens represented by list 
def input_parser(input_content):
   word = ''
   input_list = []
   types = ['int', 'int *', 'int &amp;',
           'float', 'float *', 'float &amp;', 
           'double', 'double *', 'double &amp;',
           'long double', 'long double *', 'long double &amp;',
           'bool', 'bool *', 'bool &amp;',
           'char', 'char *', 'char &amp;',
           'char16_t', 'char16_t *', 'char16_t &amp;', 'char32_t', 'char32_t *', 'char32_t &amp;',
           'wchar_t', 'wchar_t *', 'wchar_t &amp;','signed char', 'signed char *', 'signed char &amp;',
           'short int', 'short int *', 'short int &amp;', 'long int', 'long int *', 'long int &amp;', 'long long int',
           'long long int *', 'long long int &amp;', 'unsigned char', 'unsigned char *', 'unsigned char &amp;',
           'unsigned short int', 'unsigned short int *', 'unsigned short int &amp;', 'unsigned int', 'unsigned int *',
           'unsigned int &amp;', 'unsigned long int', 'unsigned long int *', 'unsigned long int &amp;',
           'unsigned long long int', 'unsigned long long int *', 'unsigned long long int &amp;','short','short *','short &amp;','long','long *','long &amp;','unsigned short','unsigned short *','unsigned short &amp;','unsigned','unsigned *','unsigned &amp;','unsigned long','unsigned long *','unsigned long &amp;','unsigned long long','unsigned long long *','unsigned long long &amp;']

   for char in input_content:
      if ((char == '\n') or (char == ' ')) and (word != ''):
         word = word_control(word)
         if (word != 'next'):
            input_list.append(word)
         word = ''
         continue
      elif ((char == '(') or (char == ')')) and (word != ''):
         word = word_control(word)
         if (word != 'next'):
            input_list.append(word)
         
         word = ''
         input_list.append(char)

      elif (char == '{') or (char == '}') or (char == ';') or (char == '=') or (char.isdigit()) or (char == '\t') or (char == '~'):
         if (word == 'char') or (word == 'char3') or (word == 'char1') or (char.isdigit()):
            word += char
            continue
         elif (word != ''):
            word = word_control(word)
            if (word != 'next'):
               input_list.append(word)
            word = ''
         input_list.append(char)
      elif (char != '\n') and (char != ' '):
         if ((char == ',') or (char == ':')) and (word != ''):
            word = word_control(word)
            if (word != 'next'):
               input_list.append(word)
            
            input_list.append(char)
            word = ''
         else:   
            if((char == ':') or (char == '*') or (char == '&')) and (word == ''):
               if (char == '*'):
                  word = word_control(char)
                  if (word != '*'):
                     input_list.append(word)
               word = ''
               input_list.append(char)

               continue
            word += char

   for t in types:
      x = 0
      length = len(input_list)
      while(x < length): 
         if (t == input_list[x]) or (input_list[x] == 'A') or (input_list[x] == 'B') or (input_list[x] == 'C') or (input_list[x] == 'D') or (input_list[x] == 'void'):
            if (input_list[x+1] == '*'):
               word = input_list[x] + ' *'
               input_list.insert(x, word)
               del input_list[x+2]
               del input_list[x+1]
               length -= 1

            elif (input_list[x+1] == '&'):
               word = input_list[x] + ' &amp;'
               input_list.insert(x, word)
               del input_list[x+2]
               del input_list[x+1]
               length -= 1
         x += 1

   for t in types:
      x = 0
      length = len(input_list)
      while(x < length): 
         if (t == input_list[x]):
            if (input_list[x+1] == ')') or (input_list[x+1] == ','):
               input_list.insert(x+1, '')
               length += 1
         x += 1

   class_list = analysis(input_list)
   return class_list

#function parses command line arguments
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

   try:
      parsed = parser.parse_args()
   except SystemExit:
      sys.exit(1)

   if (parsed.k == []):
      k = 4
   elif (parsed.k != None):
      k = int(parsed.k[0])
   
   if (parsed.details == []):
      details_all = True
      if (parsed.conflicts == True):
         conflicts = True

   elif (parsed.details != None):
      classname = parsed.details[0]
      if (parsed.conflicts == True):
         conflicts = True
   
   elif (parsed.details == None):
      if (parsed.conflicts == True):
         sys.stderr.write('Wrong parameters formating!\n')
         sys.exit(1)

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
      try:
         inputfile = open(inputfilename, 'r')
      except IOError:
         sys.stderr.write('Error opening input file!\n')
         sys.exit(2)
      else:
         inputfile = open(inputfilename, 'r')
         input_content = inputfile.read()
   else:
      input_content = sys.stdin.read()

   output(stdout, outputfilename, k, input_parser(input_content), classname)

   if (stdin == False):
      inputfile.close()

if __name__ == "__main__":
    main()