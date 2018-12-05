
#To run this application z3 package must be installed and its path has to be added to the environmental variables
#This application is a basic version of timetable generator using z3 constraint solver
#It has many limitations which can be seen in docs folder
#when the term "class"/"classes" is used it refers to the course


from z3 import *

#Stores the list of class lab_details for each lab
global labs
labs = []

#Solver for solving the all the constraints
global s
s=Solver()

#It is a list of class course_z3
global all_classes
all_classes = []

#It contain all the basic constraints for classes
#For what includes basic constraints visit Docs folder
global all_classes_rules
all_classes_rules = []

#List of class professor_details for each professor
global professors
professors = []

#Temp variable for temp use
global temp
temp = []

#List all rules for professors other than basic rules
global rules_professors
rules_professors = []

#List all rules for labs other than basic rules
global rules_labs
rules_labs = []

#variable for garbage use
global waste
waste = Int('waste') 

#variable that contains all the constraints that link professors and labs to actual courses
global matching
matching = []

#returns appropriate time string for given slot 
def slot_time(A):
	if(A==1 or A==6 or A== 11 or A==16 or A==21 or A==26):
		return "8:30 to 9:25"
	if(A==2 or A==7 or A== 12 or A==17 or A==22 or A==27):
		return "9:30 to 10:25"
	if(A==3 or A==8 or A== 13 or A==18 or A==23 or A==28):
		return "10:30 to 11:25"
	if(A==4 or A==9 or A== 14 or A==19 or A==24 or A==29):
		return "11:30 to 12:25"
	if(A==5 or A==10 or A== 15 or A==20 or A==25 or A==30):
		return "12:30 to 13:25"
	if(A>30 and A<37):
		return "9:00 to 12:00"
	if(A>36 and A<43):
		return "14:00 to 17:00"


#returns appropriate day for given slot 
def slot_day(A):
	if(A>0 and A<6):
		return "Monday"
	if(A>5 and A<11):
		return "Tuesday"
	if(A>10 and A<16):
		return "Wednesday"
	if(A>15 and A<21):
		return "Thursday"
	if(A>20 and A<26):
		return "Friday"
	if(A>25 and A<31):
		return "Saturday"

	if(A==31 or A==37):
		return "Monday"
	if(A==32 or A==38):
		return "Tuesday"
	if(A==33 or A==39):
		return "Wednesday"
	if(A==34 or A==40):
		return "Thursday"
	if(A==35 or A==41):
		return "Friday"
	if(A==36 or A==42):
		return "Saturday"


#contains details for each course that are exclusively meant for professors
class detail_course_for_professors:
	def __init__(self,val,name,professor,lec,tut,lab,ii,jj):
		self.ii = ii
		self.jj = jj
		self.val = val
		self.name = name
		self.professor = professor
		self.lec = lec
		self.tut = tut
		self.lab = lab
		self.lec_arr = []
		self.tut_arr = []
		self.lab_arr = []
		self.input_course_details()
	def input_course_details(self):
		for i in range(self.lec):
			temp = course_details(self.name,i,self.professor,self.val,"lec",all_classes[self.ii][self.jj].lec_arr[i].ans)
			self.lec_arr.append(temp)
		for i in range(self.tut):
			temp = course_details(self.name,i,self.professor,self.val,"tut",all_classes[self.ii][self.jj].tut_arr[i].ans)
			self.tut_arr.append(temp)
		for i in range(self.lab):
			temp = course_details(self.name,i,self.professor,self.val,"lab",all_classes[self.ii][self.jj].lab_arr[i].ans)
			self.lab_arr.append(temp)




#contains details for each course that are exclusively meant for labs
class detail_course_for_labs:
	def __init__(self,val,name,lab_name,lab,ii,jj):
		self.ii = ii
		self.jj = jj
		self.val = val
		self.name = name
		self.lab_name = lab
		self.lab = lab
		self.lab_arr = []
		self.create_lab_arr()

	def create_lab_arr(self):
		for i in range(self.lab):
			temp = course_details_for_lab(self.val,self.name,self.lab_name,i,all_classes[self.ii][self.jj].lab_arr[i].ans)
			self.lab_arr.append(temp)

		

			
#contains details for each session that are exclusively meant for labs
class course_details_for_lab:
	def __init__ (self,val,name,lab_name,times,A):
		self.A = A
		self.val = val
		self.name = name
		self.lab_name = lab_name
		self.times = times
		self.ans = Int("%s_%s_%s_%s_%s" %(val,lab_name,name,"lab",times))
		self.connect()
	def connect(self):
		temp = (self.ans==self.A)
		matching.append(temp)



#contains details for each session that are exclusively meant for professors
class course_details:
	def __init__(self,name,times,professor,val,type,A):
		self.A = A
		self.type = type
		self.val = val
		self.name = name
		self.times = times
		self.professor = professor
		self.ans =Int("%s_%s_%s_%s_%s" %(val,professor,name,type,times))
		self.connect()
	def connect(self):
		temp = (self.ans==self.A)
		matching.append(temp)


#contains all the details for a professor
class professor_details:
	def __init__(self,name):
		self.name = name
		self.courses=[]
		self.detail_courses = []
		def professor_courses(A):
			for i in range(len(A)):
				self.courses.append(A[i])

	#Adds all the details of courses taken by a professor 

	def professor_detail_courses(self,A):
		for i in range(len(A)):
			for j in range(len(A[i])):
				temp_list = []
				temp =0
				index =0
				for k in range(len(self.courses)):
					if A[i][j].name == self.courses[k]:
						index = k
						temp =1
						break
				if temp == 1:
					temp = detail_course(A[i][j].val,A[i][j].name,self.name,A[i][j].lec,A[i][j].tut,A[i][j].lab)
					self.detail_courses.append(temp)






#temporary class for storing professor variables
class temp_professor_details:
	def __init__(self,course,name):
		self.course = course
		self.name = name

#Class that contains all the details of a lab
class lab_details:
	def __init__(self,name,quant):
		self.name = name
		self.quant = quant
		self.courses = []
		self.detail_courses = []
		self.special_lab_arr = []
	
	def lab_courses(A):
		for i in range(len(A)):
			self.courses.append(A[i])

	def create_detail_courses(self,A):
		for i in range(len(A)):
			for j in range(len(A[i])):
				temp = 0
				index =0
				for k in range(len(self.courses)):
					if A[i][j].name == self.courses[k]:
						temp =1
						index = k
						break
				if temp == 1:
					temp = detail_course_for_labs(A[i][j].val,A[i][j].name,self.name,A[i][j].lab,i,j)
					self.detail_courses.append(temp)
	
	def create_special_lab_arr(self,A):
		for i in range(len(A)):
			for j in range(len(A[i])):
				temp = 0
				index = 0
				for k in range(len(self.courses)):
					if A[i][j].name == self.courses[k]:
						temp = 1
						index = k
				if temp == 1:
					temp = special_lab_arr(A[i][j].val,A[i][j].name,self.name)
					self.special_lab_arr.append(temp)
							


#creates a special list of z3 variables for labs but this has no implementation as of now
class special_lab_arr:
	def __init__ (self,val,name,lab_name):
		self.name = name
		self.lab_name = lab_name
		self.val = val
		self.ans_arr = []
		self.create_arr()
	def create_arr(self):
		temp_arr = []
		for i in range(12):
			temp = Int('%s_%s_%s_%s_%s'%(self.val,"special",self.name,self.lab_name,i))
			temp_arr.append(temp)
		self.ans_arr = temp_arr



#temp class for storing lab details
class temp_lab_details:
	def __init__(self,course,lab):
		self.course = course
		self.lab = lab


#Stores details of a course in general
class course_z3:
	def __init__(self,val,name,lec,tut,lab):
		self.val = val
		self.name = name
		self.lec = lec
		self.tut = tut
		self.lab = lab
		self.lec_arr = []
		self.tut_arr = []
		self.lab_arr = []

		for i in range(lec):
			self.lec_arr.append(z3_class(val,name,"lec",i))

		for i in range(tut):
			self.tut_arr.append(z3_class(val,name,"tut",i))

		for i in range(lab):
			self.lab_arr.append(z3_class(val,name,"lab",i))


#Stores details of a session in general
class z3_class :
	def __init__(self,val,name,type,num):
		self.val = val
		self.name = name
		self.type = type
		self.num = num
		self.ans = Int("%s_%s_%s_%s" %(val,name,type,num))



#A temporary class for storing details of a course
class course:
	def __init__(self,n,l,t,lbs):
		self.name = n
		self.lec = l
		self.lec = int(self.lec)
		self.tut = t
		self.tut = int(self.tut)
		self.lab = lbs
		self.lab = int(self.lab)
		self.create()

	def create(self):
		self.lec_arr=[None for x in range(self.lec)]
		self.tut_arr=[None for x in range(self.tut)]
		self.lab_arr=[None for x in range(self.lab)]




#For removing the "\n" if present at the end of the string
def clean(a):
	if a.endswith("\n"):

		a=a.replace("\n","")

	return a


#Creates a list of class course_z3 for a given branch which contains details of all the courses they have
def create_instance(val,file_name):
	f = open(file_name)
	all=[]
	all_z3 = []
	while 2>1 :
		a = f.readline()
		a = clean(a)
		if a=="START" :
			while 2>1 :
				a = f.readline()
				a = clean(a)
				if a=="//" :
					a = f.readline()
					a = clean(a)
					if a != "END" :
						n = a
						a = f.readline()
						a = clean(a)
						l,t,lbs = a.split()
						all.append(course(n,l,t,lbs))

					if a == "END":
						break
				if a == "END" :
					break
			if a == "END" :
					break


	for i in range(len(all)):
		all_z3.append(course_z3(val,all[i].name,all[i].lec,all[i].tut,all[i].lab))

	return all_z3




#Stores the quantity of labs that are available 
#It reads the data given in a perticular format from the file with name "lab_quantity.txt"
def lab_quantity():
	global labs
	file = open("lab_quantity.txt")
	while 2>1:
		line = file.readline()
		if line == "" :
			break
		else:
			line = clean(line)
			temp1 = line
			line = file.readline()
			line = clean(line)
			temp2 = line
			temp = lab_details(temp1,temp2)
			labs.append(temp)


#Reads and stores details and list of all the courses that are taken in a perticular lab
def course_lab():
	temp_course_lab = []
	file = open("lab_details.txt")
	while 2>1 :
		line = file.readline()
		line = clean(line)
		
		if line == "START":
			while 2>1 :
				line = clean(file.readline())
				if line == "//":
					line = file.readline()
					line = clean(line)
					if line != "END" :
						temp1 = line
						line = file.readline()
						line = clean(line)
						temp2 = line
						temp = temp_lab_details(temp1,temp2)
						temp_course_lab.append(temp)
					else:
						return temp_course_lab
						break
		if line == "END":
			break



#Adds all the course details to the actual corresponding lab_details class
def update_lab_details(A):
	for i in range(len(A)):
		for j in range(len(labs)):
			if A[i].lab == labs[j].name :
				labs[j].courses.append(A[i].course)
				break;


#Reads the stores the list of all the professors from "professor_quantity.txt" with details given in perticular format
def professor_quantity():
	global professors
	file = open("professor_quantity.txt")
	global professors
	while 2>1 :
		line = file.readline()
		line = clean(line)
		if line == "" :
			break
		else:
			temp = professor_details(line)
			professors.append(temp)



#Reads and stores details and list of all the courses that are taken in a perticular professor
def course_professor():
	file = open("professor_details.txt")
	ans = []
	while 2>1 :
		line = file.readline()
		line = clean(line)
		
		if line == "START":
			while 2>1 :
				line = clean(file.readline())
				if line == "//":
					line = file.readline()
					line = clean(line)
					if line != "END" :
						temp1 = line
						line = file.readline()
						line = clean(line)
						temp2 = line
						temp = temp_professor_details(temp1,temp2)
						ans.append(temp)
					else:
						return ans
						break
		if line == "END":
			break



#Adds all the course to the actual corresponding professor_details class
def update_professor_details(A):
	for i in range(len(A)):
		for j in range(len(professors)):
			if A[i].name == professors[j].name :
				professors[j].courses.append(A[i].course)
				break;



#Adds all the details for each course for a given professor
def update_professors_course_details(prof,A):
	for i in range(len(A)):
					for j in range(len(A[i])):
						temp_list = []
						temp =0
						index =0
						for k in range(len(prof.courses)):
							if A[i][j].name == prof.courses[k]:
								index = k
								temp =1
								break
						if temp == 1:
							temp = detail_course_for_professors(A[i][j].val,A[i][j].name,prof.name,A[i][j].lec,A[i][j].tut,A[i][j].lab,i,j)
							prof.detail_courses.append(temp)



#Creates and stores all the constraints for professors and stores them in corresponding global variable
def create_professor_rules():
	global rules_professors
	for i in range(len(professors)):
		temp = []
		for j in range(len(professors[i].detail_courses)):
			for k in range(len(professors[i].detail_courses[j].lec_arr)):
				temp.append(professors[i].detail_courses[j].lec_arr[k].ans)
			for k in range(len(professors[i].detail_courses[j].tut_arr)):
				temp.append(professors[i].detail_courses[j].tut_arr[k].ans)
			for k in range(len(professors[i].detail_courses[j].lab_arr)):
				temp.append(professors[i].detail_courses[j].lab_arr[k].ans)
		if temp != [] :
			rule = Distinct(temp)
			rules_professors.append(rule)


#Creates and stores all the constraints for labs and stores them in corresponding global variable
def create_lab_rules():
	global rules_labs
	for i in range(len(labs)):
		temp = []
		for j in range(len(labs[i].detail_courses)):
			for k in range(len(labs[i].detail_courses[j].lab_arr)):
				temp.append(labs[i].detail_courses[j].lab_arr[k].ans)
		if temp != [] :
			rule = Distinct(temp)
			rules_labs.append(rule)
				
	



"""
Both "create_lab_rules_1" and "create_lab_rules_2" creates a set of special rules for labs but which are not implemented completely
"""
def create_lab_rules_1():
	global rules_labs
	global waste
	for i in range(len(labs)):
		for j in range(len(labs[i].detail_courses)):
			index = 0
			for k in range(len(labs[i].special_lab_arr)):
				if labs[i].special_lab_arr[k].name == labs[i].detail_courses[j].name and labs[i].special_lab_arr[k].val == labs[i].detail_courses[j].val :
					index = k
			for k in range(len(labs[i].detail_courses[j].lab_arr)):
				temp = [If(labs[i].detail_courses[j].lab_arr[k].ans==l,labs[i].special_lab_arr[index].ans_arr[l-31]==1,waste == 10) for l in range(31,43)]
				rules_labs = rules_labs + temp



def create_lab_rules_2():
	global rules_labs
	global waste
	for i in range(len(labs)):
		for k in range(12):
			temp_arr = [labs[i].special_lab_arr[j].ans_arr[k] for j in range(len(labs[i].special_lab_arr))]
			temp = Sum(temp_arr)<(int(labs[i].quant)+1)
			rules_labs.append(temp)



		



file_names = []
input = open("input.txt")

while 2>1 :
	line = input.readline()
	if line == "":
		break
	else:
		line = clean(line)
		file_names.append(line)


for i in range(len(file_names)):
	all_classes.append(create_instance(i,file_names[i]))



professor_quantity()
temp_prof_course_details = []
temp_pro_course_details = course_professor()
update_professor_details(temp_pro_course_details)
for i in range(len(professors)):
	update_professors_course_details(professors[i],all_classes)




lab_quantity()
temp_course_details = []
temp_course_details = course_lab()
update_lab_details(temp_course_details)
for i in range(len(labs)):
	labs[i].create_detail_courses(all_classes)

for i in range(len(labs)):
	labs[i].create_special_lab_arr(all_classes)


create_professor_rules()
create_lab_rules()
#create_lab_rules_1()
#create_lab_rules_2()
######################################################################################################################################


######################################################################################################################################
#START of Putting all the basic constraints
"""
This function puts all the basic constrains to a given branch
To know what all are the  basic constrants refer docs folder
"""
def all_basic_constraints(A):

	all_z3=A

	global waste
	waste = Int('waste')
	global unique
	unique = []
	global var_range
	var_range = []
	global lab_cond
	lab_cond = []
	global no_same_class
	no_same_class = []


	def make_unique(A,ii,jj,name):
		global unique
		for i in range(len(all_z3)):
			for j in range(len(all_z3[i].lec_arr)):
				if  ii != i or jj != j or name != "lec":
					temp = Distinct(A,all_z3[i].lec_arr[j].ans)
					unique.append(temp)

			for j in range(len(all_z3[i].tut_arr)):
				if  ii != i or jj != j or name != "tut":
					temp = Distinct(A,all_z3[i].tut_arr[j].ans)
					unique.append(temp)

			for j in range(len(all_z3[i].lab_arr)):
				if  ii != i or jj != j or name != "lab":
					temp = Distinct(A,all_z3[i].lab_arr[j].ans)
					unique.append(temp)


	def set_range(A,type):
		global var_range
		if type == "lab":
			temp = And(A>30,A<43)
			var_range.append(temp)

		else:
			temp = And(A>0,A<31)
			var_range.append(temp)



	def lab_condition_helper(A):
		global lab_cond
		global waste
		for i in range(len(all_z3)):
			for j in range(len(all_z3[i].lab_arr)):
				temp = If(all_z3[i].lab_arr[j].ans == 31,And(A != 1,A != 2,A != 3,A != 4,A != 5),waste == 0)
				lab_cond.append(temp)
				temp = If(all_z3[i].lab_arr[j].ans == 32,And(A != 7,A != 8,A != 9,A != 10,A != 6),waste == 0)
				lab_cond.append(temp)
				temp = If(all_z3[i].lab_arr[j].ans == 33,And(A != 13,A != 14,A != 15,A != 12,A != 11),waste == 0)
				lab_cond.append(temp)
				temp = If(all_z3[i].lab_arr[j].ans == 34,And(A != 16,A != 17,A != 18,A != 19,A != 20),waste == 0)
				lab_cond.append(temp)
				temp = If(all_z3[i].lab_arr[j].ans == 35,And(A != 21,A != 22,A != 23,A != 24,A != 25),waste == 0)
				lab_cond.append(temp)
				temp = If(all_z3[i].lab_arr[j].ans == 36,And(A != 26,A != 27,A != 28,A != 29,A != 30),waste == 0)
				lab_cond.append(temp)



	def lab_condition() :
	
		for i in range(len(all_z3)):
			for j in range(len(all_z3[i].lec_arr)):
				lab_condition_helper(all_z3[i].lec_arr[j].ans)

			for j in range(len(all_z3[i].tut_arr)):
				lab_condition_helper(all_z3[i].tut_arr[j].ans)



	def no_same_helper(B,A):
		global waste
		global no_same_class
		temp = [If(B==i,And(A != 5*(j-1)+1,A != 5*(j-1)+2,A != 5*(j-1)+3,A != 5*(j-1)+4,A != 5*(j-1)+5),waste == 0)  for j in range(1,7) for i in range(5*(j-1)+1,5*(j-1)+6)] 
		no_same_class = no_same_class+temp

	def no_same_helper_lab(A,B):
		global waste
		global no_same_class
		temp = If(A==31,B!=37,waste==0)
		no_same_class.append(temp)
		temp = If(A==32,B!=38,waste==0)
		no_same_class.append(temp)
		temp = If(A==33,B!=39,waste==0)
		no_same_class.append(temp)
		temp = If(A==34,B!=40,waste==0)
		no_same_class.append(temp)
		temp = If(A==35,B!=41,waste==0)
		no_same_class.append(temp)
		temp = If(A==36,B!=42,waste==0)
		no_same_class.append(temp)


	def no_same():
		for i in range(len(all_z3)):
			for j in range(len(all_z3[i].lec_arr)):
				for k in range(len(all_z3[i].lec_arr)):
					if(j != k):
						no_same_helper(all_z3[i].lec_arr[j].ans,all_z3[i].lec_arr[k].ans)

				for k in range(len(all_z3[i].tut_arr)):
					no_same_helper(all_z3[i].lec_arr[j].ans,all_z3[i].tut_arr[k].ans)


			for j in range(len(all_z3[i].tut_arr)):
				for k in range(len(all_z3[i].lec_arr)):
					no_same_helper(all_z3[i].tut_arr[j].ans,all_z3[i].lec_arr[k].ans)

				for k in range(len(all_z3[i].tut_arr)):
					if(j != k):
						no_same_helper(all_z3[i].tut_arr[j].ans,all_z3[i].tut_arr[k].ans)

			for j in range(len(all_z3[i].lab_arr)):
				for k in range(len(all_z3[i].lab_arr)):
					if(j!=k):
						no_same_helper_lab(all_z3[i].lab_arr[j].ans,all_z3[i].lab_arr[k].ans)




	for i in range(len(all_z3)):
		for j in range(len(all_z3[i].lec_arr)):
			make_unique(all_z3[i].lec_arr[j].ans,i,j,"lec")
			set_range(all_z3[i].lec_arr[j].ans,"lec")

		for j in range(len(all_z3[i].tut_arr)):
			make_unique(all_z3[i].tut_arr[j].ans,i,j,"tut")
			set_range(all_z3[i].tut_arr[j].ans,"tut")

		for j in range(len(all_z3[i].lab_arr)):
			make_unique(all_z3[i].lab_arr[j].ans,i,j,"lab")
			set_range(all_z3[i].lab_arr[j].ans,"lab")

	lab_condition()
	no_same()
	rule_final = unique + var_range + lab_cond+no_same_class
	return rule_final

#END of putting all the basic constraints
######################################################################################################################################

for i in range(len(all_classes)):
	temp = []
	temp = all_basic_constraints(all_classes[i])
	all_classes_rules.append(temp)

temp_all_rules = []
for i in range(len(all_classes_rules)):
	temp_all_rules = temp_all_rules + all_classes_rules[i]

all_classes_rules = temp_all_rules

rules_final = []
rules_final = rules_professors+all_classes_rules + matching + rules_labs
#rules_final = rules_final + rules_labs
s.add(rules_final)
print(s.check())
#print(s.model())



print("done")
ans = s.model()


#printing output timetable daywise
###########################################################################################################################################


#This function prints the output files in daywise format
def print_timetable_daywise(file_name,model,all):
	global all_z3
	all_z3 = all
	global out
	out = open(file_name,"w")
	global ans
	ans = model
	out.write("Timetable day wise"+"\n\n\n")
	out.write("On Monday")
	out.write("\n")
	for i in range(len(all_z3)):
		for j in range(len(all_z3[i].lec_arr)):
			if slot_day(int(str(ans[all_z3[i].lec_arr[j].ans]))) == "Monday" :
				out.write(str(all_z3[i].lec_arr[j].name) + " Lecture ( " + str(slot_time(int(str(ans[all_z3[i].lec_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].tut_arr)):
			if slot_day(int(str(ans[all_z3[i].tut_arr[j].ans]))) == "Monday" :
				out.write(str(all_z3[i].tut_arr[j].name) + " Tutorial ( " + str(slot_time(int(str(ans[all_z3[i].tut_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].lab_arr)):
			if slot_day(int(str(ans[all_z3[i].lab_arr[j].ans]))) == "Monday" :
				out.write(str(all_z3[i].lab_arr[j].name) + " Lab ( " + str(slot_time(int(str(ans[all_z3[i].lab_arr[j].ans])))) +" ) \n")
	out.write("\n\n")


	out.write("On Tuesday")
	out.write("\n")
	for i in range(len(all_z3)):
		for j in range(len(all_z3[i].lec_arr)):
			if slot_day(int(str(ans[all_z3[i].lec_arr[j].ans]))) == "Tuesday" :
				out.write(str(all_z3[i].lec_arr[j].name) + " Lecture ( " + str(slot_time(int(str(ans[all_z3[i].lec_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].tut_arr)):
			if slot_day(int(str(ans[all_z3[i].tut_arr[j].ans]))) == "Tuesday" :
				out.write(str(all_z3[i].tut_arr[j].name) + " Tutorial ( " + str(slot_time(int(str(ans[all_z3[i].tut_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].lab_arr)):
			if slot_day(int(str(ans[all_z3[i].lab_arr[j].ans]))) == "Tuesday" :
				out.write(str(all_z3[i].lab_arr[j].name) + " Lab ( " + str(slot_time(int(str(ans[all_z3[i].lab_arr[j].ans])))) +" ) \n")
	out.write("\n\n")


	out.write("On Wednesday")
	out.write("\n")
	for i in range(len(all_z3)):
		for j in range(len(all_z3[i].lec_arr)):
			if slot_day(int(str(ans[all_z3[i].lec_arr[j].ans]))) == "Wednesday" :
				out.write(str(all_z3[i].lec_arr[j].name) + " Lecture ( " + str(slot_time(int(str(ans[all_z3[i].lec_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].tut_arr)):
			if slot_day(int(str(ans[all_z3[i].tut_arr[j].ans]))) == "Wednesday" :
				out.write(str(all_z3[i].tut_arr[j].name) + " Tutorial ( " + str(slot_time(int(str(ans[all_z3[i].tut_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].lab_arr)):
			if slot_day(int(str(ans[all_z3[i].lab_arr[j].ans]))) == "Wednesday" :
				out.write(str(all_z3[i].lab_arr[j].name) + " Lab ( " + str(slot_time(int(str(ans[all_z3[i].lab_arr[j].ans])))) +" ) \n")
	out.write("\n\n")


	out.write("On Thursday")
	out.write("\n")
	for i in range(len(all_z3)):
		for j in range(len(all_z3[i].lec_arr)):
			if slot_day(int(str(ans[all_z3[i].lec_arr[j].ans]))) == "Thursday" :
				out.write(str(all_z3[i].lec_arr[j].name) + " Lecture ( " + str(slot_time(int(str(ans[all_z3[i].lec_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].tut_arr)):
			if slot_day(int(str(ans[all_z3[i].tut_arr[j].ans]))) == "Thursday" :
				out.write(str(all_z3[i].tut_arr[j].name) + " Tutorial ( " + str(slot_time(int(str(ans[all_z3[i].tut_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].lab_arr)):
			if slot_day(int(str(ans[all_z3[i].lab_arr[j].ans]))) == "Thursday" :
				out.write(str(all_z3[i].lab_arr[j].name) + " Lab ( " + str(slot_time(int(str(ans[all_z3[i].lab_arr[j].ans])))) +" ) \n")
	out.write("\n\n")

	out.write("On Friday")
	out.write("\n")
	for i in range(len(all_z3)):
		for j in range(len(all_z3[i].lec_arr)):
			if slot_day(int(str(ans[all_z3[i].lec_arr[j].ans]))) == "Friday" :
				out.write(str(all_z3[i].lec_arr[j].name) + " Lecture ( " + str(slot_time(int(str(ans[all_z3[i].lec_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].tut_arr)):
			if slot_day(int(str(ans[all_z3[i].tut_arr[j].ans]))) == "Friday" :
				out.write(str(all_z3[i].tut_arr[j].name) + " Tutorial ( " + str(slot_time(int(str(ans[all_z3[i].tut_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].lab_arr)):
			if slot_day(int(str(ans[all_z3[i].lab_arr[j].ans]))) == "Friday" :
				out.write(str(all_z3[i].lab_arr[j].name) + " Lab ( " + str(slot_time(int(str(ans[all_z3[i].lab_arr[j].ans])))) +" ) \n")
	out.write("\n\n")


	out.write("On Saturday")
	out.write("\n")
	for i in range(len(all_z3)):
		for j in range(len(all_z3[i].lec_arr)):
			if slot_day(int(str(ans[all_z3[i].lec_arr[j].ans]))) == "Saturday" :
				out.write(str(all_z3[i].lec_arr[j].name) + " Lecture ( " + str(slot_time(int(str(ans[all_z3[i].lec_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].tut_arr)):
			if slot_day(int(str(ans[all_z3[i].tut_arr[j].ans]))) == "Saturday" :
				out.write(str(all_z3[i].tut_arr[j].name) + " Tutorial ( " + str(slot_time(int(str(ans[all_z3[i].tut_arr[j].ans])))) +" ) \n")

		for j in range(len(all_z3[i].lab_arr)):
			if slot_day(int(str(ans[all_z3[i].lab_arr[j].ans]))) == "Saturday" :
				out.write(str(all_z3[i].lab_arr[j].name) + " Lab ( " + str(slot_time(int(str(ans[all_z3[i].lab_arr[j].ans])))) +" ) \n")
	out.write("\n\n")

###########################################################################################################################################


#This function prints the output files in slotwise format
def printing_slots(file_name,all):
		all_z3 = all
		f = open(file_name,"w")
		for i in range(len(all_z3)):
			f.write(all_z3[i].name)
			f.write("\n")
			for j in range(len(all_z3[i].lec_arr)):
				f.write(str(all_z3[i].lec_arr[j].ans) + "    " + str(ans[all_z3[i].lec_arr[j].ans]))
				f.write("\n")
			for j in range(len(all_z3[i].tut_arr)):
				f.write(str(all_z3[i].tut_arr[j].ans) + "    " + str(ans[all_z3[i].tut_arr[j].ans]))
				f.write("\n")
			for j in range(len(all_z3[i].lab_arr)):
				f.write(str(all_z3[i].lab_arr[j].ans) + "    " + str(ans[all_z3[i].lab_arr[j].ans]))
				f.write("\n")







if s.check() == sat:
	for i in range(len(all_classes)):
		print_timetable_daywise(file_names[i]+"time_table.txt",ans,all_classes[i])
		printing_slots(file_names[i]+"slots.txt",all_classes[i])

else :
	print("sorry!")

print("done")
