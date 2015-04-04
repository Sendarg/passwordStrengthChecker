#coding:utf8
import sys,os
__author__="Sendarg Lee"
#
sNumerics = '0123456789'
sAlphas = 'abcdefghijklmnopqrstuvwxyz'
sKeyboard = ['`1234567890-= ',' qwertyuiop[]\\',' asdfghjkl;\'  ',' zxcvbnm,./   ']
##------- all check role
def checkSeq_line(pwd,sSeq,least):
	nSeqline = 0
	for s in range(0,len(sSeq)-least+1):
		sFwd = sSeq[s:s+least]
		if sFwd in pwd :
			nSeqline += 1
	return nSeqline

def checkSeq_Matrix(pwd,matrix,least):
	nSeqMtx = 0	
	for l in range(0,len(matrix)):
		for c in range(0,len(matrix[l])-least+1):			
			tmpFwd = matrix[l][c:c+least]
			sFwd=''
			for x in range(0,len(tmpFwd)):
				sFwd += tmpFwd[x]
			if sFwd in pwd:
				nSeqMtx += 1
	return nSeqMtx

def checkIncludeStr(pwd,str):
	cInclude=0
	for s in str:
		if s.lower() in pwd.lower():
			cInclude+=1
	return cInclude

def checkRepeatChar(pwd,least):
	cRepChar=0
	for p in range(0,len(pwd)-least+1):
		# 3pos repeat
		# offset 1 compare
		if pwd[p:p+least-1] == pwd[p+1:p+least]:
			cRepChar+=1
	return cRepChar			

def checkBirthNum(pwd):
	"this is for birthday num  check  in pass at 2015/04/02"
	str_num=filter(str.isdigit,pwd)
	return isBirth(str_num)


def checkBasicComplex(pwd,leastLen):
	countAlpL=0
	countAlpU=0
	countNum=0
	countSymbol=0
	for c in pwd:
		if c in sAlphas:
			countAlpL+=1
		elif c in sAlphas.upper():
			countAlpU+=1
		elif c in sNumerics:
			countNum+=1
		else:
			countSymbol+=1
	countZero=0
	for single in countAlpL,countAlpU,countNum,countSymbol:
		if single == 0:countZero+=1
	# great Logic!
	if countZero>1 or len(pwd)<leastLen:
		return countZero
	else:
		return 0
	
### not very profect,how about 3steps? how about it is not start as 0 index
def checkStep2Seq(pwd,sleast):
	sStp1=''
	sStp2=''
	cStp1=0
	cStp2=0
	# get 2 part step of pwd
	for c in range(0,len(pwd),2):
		sStp1 += pwd[c:c+1]
		sStp2 += pwd[c+1:c+2]
	# seq
	for a in sNumerics,sAlphas,sAlphas.upper():
		if len(sStp1) >=sleast  and sStp1[0:sleast] in a:
			cStp1+=1
		if len(sStp2) >=sleast  and sStp2[0:sleast] in a:
			cStp2+=1
	# keyword & dict word 
	for a in sKeyword,sDict:
		for word in a:
			if len(sStp1) >=sleast  and sStp1[0:sleast] in word:
				cStp1+=1
			if len(sStp2) >=sleast  and sStp2[0:sleast] in word:
				cStp2+=1
	if cStp1+cStp2 >= 2:
		return cStp1+cStp2
	else:
		return 0

##------- common method
def matrix_transpose(matrix):
	col=len(matrix[0])
	matrix2=[[r[c]for r in matrix] for c in xrange(col)]
	return matrix2

# simple
def lower_rev(pwd):
	pwd_low= pwd.lower()
	pwd_rev = pwd_low[::-1]
	return pwd_low,pwd_rev

# keyboard spec SHIFT
def lower_shift_rev(pwd):
	pwd_shoff = shiftoff(pwd.lower())
	pwd_rev = pwd_shoff[::-1]
	return pwd_shoff,pwd_rev

# clear SHIFT
def shiftoff(pwd):
	pwd_shoff=''
	sKeyo='`1234567890-=[]\;\',./'
	sKeyo_Shift='~!@#$%^&*()_+{}|:"<>?'
	for s in pwd:
		for o in sKeyo_Shift:
			if s==o:		
				pos=sKeyo_Shift.index(o)
				s=sKeyo[pos:pos+1]
		pwd_shoff += s
	return pwd_shoff

def isBirth(num):
	birnum=0
	###  yyyy
	num=str(num)
	for x in range(0,len(num)-3):
		year=num[x:x+4]
		# print year
		if int(year) in range(1950,2010):
			birnum += 1
			# break
	### yymmdd
	for x in range(0, len(num) - 5):
		str1 = num[x:x + 6]
		yy=str1[0:2]
		mm=str1[2:4]
		dd=str1[4:6]
		# print yy+mm+dd
		if int(yy) in range(50, 100) and int(mm) in range(1,13) and int(dd) in range(1,32):
			birnum += 1
			break # mmdd repeat
	return  birnum


##------- do check 
def check_all_role(pwd):
	rstLst=['',0,0,0,0,0,0,0,0,0]
	rstLst[0]=pwd
	# number & alphas ageinst keyboard 
	for p in lower_rev(pwd):
		rstLst[2] += checkSeq_line(p,sNumerics,nleast)
		rstLst[3] += checkSeq_line(p,sAlphas,aleast)
	#spec shift keyboard
	for p in lower_shift_rev(pwd):
		rstLst[4] += checkSeq_Matrix(p,sKeyboard,kleast)+checkSeq_Matrix(p,matrix_transpose(sKeyboard),kleast)
	# simple str
	rstLst[5] = checkIncludeStr(pwd,sKeyword)
	# repeat str
	rstLst[6] = checkRepeatChar(pwd,rleast)
	rstLst[7] = checkBasicComplex(pwd,minlen_pwd)
	rstLst[8] = checkStep2Seq(pwd,sleast)
	rstLst[9] = checkBirthNum(pwd)
	# count scope
	for c in range(2,len(rstLst)):
		rstLst[1] += rstLst[c]
	return rstLst

def out_print_format(rstLst,isSym):
	outstyle=''
	if	isSym:
		# sheet format
		for c in rstLst:
			outstyle += str(c)+'\t'
	else:
		# human print
		for c in range(1,len(rstLst)):
			if rstLst[c]>0:
				rstLst[c]='×'.decode("utf-8")
			else:
				rstLst[c] ='√'.decode("utf-8")
		# sheet format
		for c in rstLst:
			outstyle += c+'\t'

	return outstyle
	
def check_pwdfile(file,isNum=False,out=None):
	allout=[]
	# print titles
	tits=''
	for a in title:
		tits+=a+'\t'

	allout.append(tits)
	# proce file
	for l in open(file,'r'):
		l = l.rstrip()
		if len(l)>0:
			allout.append(out_print_format(check_all_role(l),isNum))
	# proce output
	if out:
		outfile=open(out,"w+")
		for l in allout:
			outfile.write(l+"\n")
		outfile.close()
	else:
		for l in allout:
			print l


def optionsProcess():
	## add options
	from optparse import OptionParser
	usage=u"Usage: %prog [ -w wordlist_file ] [ -l least ] [ -n ] [ -o outputfile ] clear_password_file\nExample: %prog -w wordlist.txt -l 2 -n -o out.txt all.txt "
	parser = OptionParser(
		description="This program was written by Sendarg Lee, use it carefuly! It only work on 64bit Windows!\n",
		prog="passwordrolechecker.py",
		version="1.0",
		usage=usage)
	parser.add_option("-w",dest="word",help="Specify a keyword,direcoty file,When not specify,use default keywords :%s,%s"%(sKeyword,sDict))
	parser.add_option("-l",action="store",dest="least",type=int,default=3,
					  help="least length in check role,default least is 3")
	parser.add_option("-n",action="store_true",default=False,
					  help="output as numbers?,when -n output as numbers")
	parser.add_option("-o",action="store",dest="out",
					  help="output filename,when not specify,print to terminal")
	(options, args) = parser.parse_args()
	## process options
	OUT=options.out
	if OUT :
		if os.path.isfile(OUT):
			print "File %s exites,Please select another output filename"%(options.out)
			print parser.print_help()
			sys.exit()
		else:
			pass
	else:
		print "Print at stdout!"
		pass
	NUM=options.n
	LEAST=options.least
	print "Check all role at least %d"%LEAST
	WORD=options.word
	# process args
	if len(args)==1:
		# get all files to process
		if os.path.isfile(args[0]):
			FILE=args[0]
			return FILE,WORD,LEAST,NUM,OUT
		else:
			print "Please select a volid file of clear password"
			sys.exit()
	else:
		print "Please select a file of clear password"
		print parser.print_help()
		sys.exit()

def check_user_lic():
	return  True




if __name__ == '__main__':
	## settings of keyword,least of word,length,etc
	global sKeyword,sDict,nleast,aleast,kleast,rleast,sleast,minlen_pwd,title,checkCover
	sKeyword='jack.bower','petter','LA'
	sDict='admin','test'
	minlen_pwd = 8
	# minlen_aL=1
	# minlen_aU=1
	# minlen_num=1
	# minlen_smbl=1
	title='password','result','seqnumbers','seqal','seqkeybord','keyword','repeadchar','basicrole','seqstep',"birthday"
	# for display in usage
	checkCover=""
	for t in title:
		checkCover+="\n"+t
	# begin check
	FILE,WORD,LEAST,NUM,OUT=optionsProcess()##must out a define,can't directory use.because default vaule
	# get all least
	nleast = LEAST
	aleast = LEAST
	kleast = LEAST
	rleast = LEAST
	sleast = LEAST
	#get keywords
	if WORD  is  not None and os.path.isfile(WORD):
		sKeyword=[]
		sDict=[]
		for w in open(WORD).readlines():
			sKeyword.append(w.lstrip().rstrip().lower())
		print "Use keyword in file %s to check"%WORD
	# go
	if check_user_lic():
		check_pwdfile(FILE,NUM,OUT)
	else:
		sys.exit()
