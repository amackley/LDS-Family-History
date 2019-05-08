#!/usr/bin/env python3
# Copyright 2009-2017 Aaron Mackley#
import datetime

def writeALine(theLine):
  #Open write to and close output file
    outputfile = open("Super Powers OutputTest.txt", "a")
    outputfile.write(theLine)
    outputfile.write('\n')
    outputfile.close()


def createConcept(concept):
  l = ('create_concept  ' + '$conceptId' + str(concept[0])+ '\t' + concept[2])
  # print(l)
  writeALine(l)
  

def updateConcept(concept):
  conceptID = concept[0]
  conceptValue = concept[1]
  
  l = ('update_concept' + '\t' + '$conceptId' + str(conceptID) + '\t' + 'attrs=1:' + str(conceptValue))
  # print(l)
  writeALine(l)

theTermDict = dict()
termDictCount = 100
  
def addTermToTermDict(theTerm):
  global theTermDict
  global termDictCount
  
  theTermDict[theTerm] = termDictCount
  termDictCount +=1
  
  # for k, v in theTermDict.items(): print(f'{k}: {v}')
  


def createTerm(term):
  
  conceptID = term[0]
  oTerm = term[3]
  oTerm = str(oTerm)
  aTerm = term[4]
  aTerm = str(aTerm)
  aTerm = aTerm.replace('\n', ' ').replace('\r', '')
  
# Work with the Official Term 
  # ol = ('create_term' + '\t' + oTerm + '\t' + 'en' + '\t' + '$' + str(conceptID) )
  # ol = ('create_term' + '\t' + oTerm + '\t' + 'en' + '\t' + '$1' )
  ol = ('create_term' + '\t' + oTerm + '\t' + 'en' + '\t' + 'OFFICIAL' + '\t' + '$conceptId' +str(conceptID) )
  addTermToTermDict(oTerm)
  # print(ol)
  writeALine(ol)

# Work with the Alternate Term if it is not empty.
  if aTerm != ' ':
    # al = ('create_term' + '\t' + aTerm + '\t' + 'en' + '\t' + '$' + str(conceptID) )
    # al = ('create_term' + '\t' + aTerm + '\t' + 'en' + '\t' + '$3' )
    al = ('create_term' + '\t' + aTerm + '\t' + 'en' + '\t' + 'ALTERNATE' + '\t' + '$conceptId' +str(conceptID) )
    # print(al)
    writeALine(al)
  

def updateList(theList):
  writeALine('update_list\t126890\tlock=false')
  writeALine('update_list\t126890\tterms=' + theList )
  writeALine('update_list\t126890\tlock=true')
 

def main():  
   
  #Get Name of list from Name of the File. Use the OS file commands to do this.
  #Strip the extension off the name of the file. 
  
  # Open the file for reading 
  inputfile = open("Super Powers Descriptor List.csv", "r")
  outputfile = open("Super Powers OutputTest.txt", "w+")
  outputfile.close()

  
  #Open the new output file for writing.
  #outputfile = open("Super Powers Descriptor LoadSequence.txt", "w+")
  

  
  # Open the file and read the contents
  if inputfile.mode == 'r':
    fl = inputfile.readlines()
    currentLine = ''
    for x in fl:
      attribs = x.split(",")
      i = int(fl.index(x)) +1 #To get the index to match the spreadsheet line numbers. Probably not necessary, but...
      attribs.insert(0,i)
      if attribs[0] == 1: #Ignore the First line which includes the titles
        continue
      # for attrib in attribs:
      createConcept(attribs)
      updateConcept(attribs)
      createTerm(attribs)
      # #  # currentLine = currentLine + str(attrib) + '\t'
      # #  # print(attrib)
      # # #writeALine(currentLine)
    
    global theTermDict
    theTermListToSend = ''
    for k, v in theTermDict.items():
      # print(f'{k}: {v}')
      theTermListToSend = theTermListToSend + '$termId' + str(v) + ','
    theTermListToSend = theTermListToSend[:-1]
    updateList(theTermListToSend)
    

    now = datetime.datetime.now()
    print("File Updated on " + str(now))

  
  
  #Close the files
  inputfile.close()

  



   
if __name__ == "__main__":
  main()