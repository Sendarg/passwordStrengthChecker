# passwordrolechecker
Usage: passwordrolechecker.py [ -w wordlist_file ] [ -l least ] [ -n ] [ -o outputfile ] clear_password_file
Example: passwordrolechecker.py -w wordlist.txt -l 2 -n -o out.txt all.txt 

This program was written by Sendarg Lee, use it carefuly! It only work on
64bit Windows!

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -w WORD     Specify a keyword,direcoty file,When not specify,use default
              keywords :('jack.bower', 'petter', 'LA'),('admin', 'test')
  -l LEAST    least length in check role,default least is 3
  -n          output as numbers?,when -n output as numbers
  -o OUT      output filename,when not specify,print to terminal
None
