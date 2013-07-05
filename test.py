'''
Created on Jul 4, 2013

@author: kinow
'''
from markmail import MarkMail

if __name__ == '__main__':
    markmail = MarkMail()
    
    messages = markmail.search('list%3Aorg.apache.announce+order%3Adate-backward')
    
    print messages