#!/usr/bin/python

import sys, getopt

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
   def __init__(self, name, attype, scope = 'instance', privacy = 'private'):
      super(Attribute, self).__init__()
      self.name = name
      self.attype = attype
      self.scope = scope
      self.privacy = privacy
        
class Argument(object):
   def __init__(self, name, artype):
      super(Argument, self).__init__()
      self.name = name
      self.artype = artype

def details_output(methorattr, privacy):
   methorattr_list = []
   for i in range(len(methorattr)):
      if (methorattr[i].privacy == privacy):
         methorattr_list.append(methorattr[i])
         
   return methorattr_list


def output(stdout, outputfilename, k, class_list, classname = ''):

   #global defined_class
   isdef = False
   mylist = []
   k_string = int(k) * ' '
   n = 1

   if (classname == ''):
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
                  for parent_name in class_list[j].parents:
                     if (parent_name == classname):
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
            outputfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            outputfile = open(outputfilename, 'w')
            outputfile.write('<class name="' + classname + '" kind="' + class_list[i].kind + '">\n')

         mylist = details_output(class_list[i].methods, 'private')
         if mylist:
            if (stdout == True):
               print(k_string*n + '<private>')
               n += 1
               print(k_string*n + '<methods>')
            else:
               outputfile.write(k_string*n + '<private>\n')
               n += 1
               outputfile.write(k_string*n + '<methods>\n')
            n += 1
            for method in mylist:
               if (stdout == True):
                  print(k_string*n + '<method name="' + method.name + '" type="' + method.mtype + '" scope="' + method.scope + '">')
                  n += 1
                  print(k_string*n + '<virtual pure="' + method.pure + '"/>')
               else:
                  outputfile.write(k_string*n + '<method name="' + method.name + '" type="' + method.mtype + '" scope="' + method.scope + '">')
                  n += 1
                  outputfile.write(k_string*n + '<virtual pure="' + method.pure + '"/>')
               n += 1
         
         mylist = details_output(class_list[i].attributes, 'private')
         if mylist:
            print('class has private attributes')
         else:
            n -= 1
            if (stdout == True):
               print(k_string*n + '<arguments/>')
            else:
               outputfile.write(k_string*n + '<arguments/>\n')

         n -= 1
         print (k_string*n + '</method>')
         n -= 1
         print (k_string*n + '</methods>')
         n -= 1
         print (k_string*n + '</private>')
         n -= 1
         print (k_string*n + '</class>')


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


def definition(input_list, class1, index):
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

   bool_type = False
   if (input_list[index+3] == 'virtual'):
      class1.change_kind('abstract')
      # if (test_type(index+4) != False):
         #print(test_type(index+4))
      for dtype in types:
         if (input_list[index+4] == dtype):
            bool_type = True
            mtype = dtype
            break
      if (bool_type == True):
         bool_type = False
         if (input_list[index+6] == '('):
            method1 = Method(input_list[index+5], dtype)
            method1.change_pure('yes')
            class1.add_method(method1)
            for x in range(index+7, len(input_list)):
               if (input_list[x] == ';'):
                  return x
            # if (test_type(index+7) != False):
            #    print(test_type[index+7])
            for dtype in types:
               if (input_list[index+7] == dtype):
                  bool_type = True
                  argtype = dtype
                  break
            if (bool_type == True):
               bool_type = False
               arg1 = Argument(input_list[index+8, dtype])
               method1.add_arguments(arg1)
            else:
               sys.stderr.write('Wrong input file formating!\n')
               sys.exit(4)

         else:
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)
      else:
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)


   #elif (input_list[index+3] == 'public'):

   #elif (input_list[index+3] == 'private'):

   #elif (input_list[index+3] == 'protected'):


   else:
      for dtype in types:
         if (input_list[index+3] == dtype):
            attype = dtype
            bool_type = True
            break
      if (bool_type == True):
         if (input_list[index+5] == ";"):
            attribute1 = Attribute(input_list[index+4], attype)
            class1.add_attribute(attribute1)

         elif(input_list[index+5] == "("):
            method1 = Method(input_list[index+4], attype)
            class1.add_method(method1)

      else:   
         sys.stderr.write('Wrong input file formating!\n')
         sys.exit(4)

def analysis(input_list):
   #global defined_class
   class_list = []
   #for item in input_list:
   for i in range(len(input_list)):
      if (input_list[i] == 'class'):
         class1 = Class(input_list[i+1])
         #defined_class.append(class1.name)
         if (input_list[i+2] == '{'):
            if (input_list[i+3] == '}'):
               if (input_list[i+4] == ';'):
                  class_list.append(class1)
                  continue
            else:
               index = definition(input_list, class1, i)
               while (input_list[index+1] != '}'):
                  index = definition(input_list, class1, index+1)


         elif (input_list[i+2] == ":"):
            if (input_list[i+3] == 'protected'):
               class1.add_parent_class(input_list[i+4])
            else:
               class1.add_parent_class(input_list[i+3])
               if (input_list[i+4] == ','):
                  class1.add_parent_class(input_list[i+5])
                  if (input_list[i+6] != '{'):
                     sys.stderr.write('Wrong input file formating!\n')
                     sys.exit(4)

               elif (input_list[i+4] != '{'):
                  sys.stderr.write('Wrong input file formating!\n')
                  sys.exit(4)

         else:
            sys.stderr.write('Wrong input file formating!\n')
            sys.exit(4)

         class_list.append(class1)
   # for i in range(len(class_list)):
      # print (class_list[i].name)
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
         input_list.append(char)
      elif (char != '\n') and (char != ' '):
         if (char == ','):
            input_list.append(word)
            input_list.append(char)
            word = ''
         else:   
            word += char
         continue
   print (input_list)
   class_list =  analysis(input_list)
   return class_list

def main(argv):
   inputfilename = ''
   outputfilename = ''
   classname = ''
   details = False
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