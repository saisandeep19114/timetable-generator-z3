from z3 import *
import sys
import os


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
global out 
out = open("timetable.txt","w")
global s
s=Solver()

all_z3=[]


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
	global no_same_class
	temp = [If(B==i,And(A != 5*(j-1)+1,A != 5*(j-1)+2,A != 5*(j-1)+3,A != 5*(j-1)+4,A != 5*(j-1)+5),waste == 0)  for j in range(1,7) for i in range(5*(j-1)+1,5*(j-1)+6)] 
	no_same_class = no_same_class+temp
	
	


def no_same_helper_lab(A,B):
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




def clean(a):
	if a.endswith("\n"):

		a=a.replace("\n","")

	return a

class course_z3:
	def __init__(self,name,lec,tut,lab):
		self.name = name
		self.lec = lec
		self.tut = tut
		self.lab = lab
		self.lec_arr = []
		self.tut_arr = []
		self.lab_arr = []

		for i in range(lec):
			self.lec_arr.append(z3_class(name,"lec",i))

		for i in range(tut):
			self.tut_arr.append(z3_class(name,"tut",i))

		for i in range(lab):
			self.lab_arr.append(z3_class(name,"lab",i))
	



class z3_class :
	def __init__(self,name,type,num):
		self.name = name
		self.type = type
		self.num = num
		self.ans = Int("%s_%s_%s" %(name,type,num))


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



f = open("Details.txt")
all=[]
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
	all_z3.append(course_z3(all[i].name,all[i].lec,all[i].tut,all[i].lab))





#rule_unique = [Distinct([all_z3[i].lec_arr[j].ans for j in range(len(all_z3[i].lec_arr))],
#						[all_z3[i].tut_arr[k].ans for k in range(len(all_z3[i].tut_arr))],
#						[all_z3[i].lab_arr[l].ans for l in range(len(all_z3[i].lab_arr))])
#			   for i in range(len(all_z3))]

#rule_unique_lec = [ Distinct([all_z3[i].lec_arr[j].ans for i in range(len(all_z3))  for j in range(len(all_z3[i].lec_arr)) ] ) ]
#i=0;
#j=0;
#rule_unique_tut = [ Distinct([all_z3[i].tut_arr[j].ans for i in range(len(all_z3))  for j in range(len(all_z3[i].tut_arr)) ] ) ] 
#i=0;
#j=0;
#rule_unique_lab = [ Distinct([all_z3[i].lab_arr[j].ans for i in range(len(all_z3))  for j in range(len(all_z3[i].lab_arr)) ] ) ] 



#rule_unique = rule_unique_lec+rule_unique_tut+rule_unique_lab

#rule_unique = [ Distinct([all_z3[i].lec_arr[j].ans all_z3[i].tut_arr[k].ans all_z3[i].lab_arr[l].ans for i in range(len(all_z3))  for j in range(len(all_z3[i].lec_arr)) for k in range(len(all_z3[i].tut_arr))  for l in range(len(all_z3[i].lab_arr)) ] ) ]



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



s.add(rule_final)

print(s.check())
global ans
if s.check() == sat :
	ans = s.model()
	print(s.model())
	f = open("slots.txt","w")
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

else:
	print("Timetable not possible")

def print_timetable_daywise():
	global out
	global ans
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


if s.check() == sat:
	print_timetable_daywise()



print("done")










