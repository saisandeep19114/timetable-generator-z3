

def clean(a):
	if a.endswith("\n"):
		a=a.replace("\n","")

	return a

class course:
	def __init__(self,n,l,t,lbs):
		self.name = n
		self.lec = l
		self.lec = int(self.lec)
		self.tut = t
		self.tut = int(self.lec)
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


#for i in range(len(all)) :
#	print (all[i].name + "  " + str(all[i].lec)+str(all[i].tut)+str(all[i].lab))

o = open("modify.txt","w")
for i in range(len(all)):
	o.write(all[i].name + " = course("+all[i].name+","+str(all[i].lec)+","+str(all[i].tut)+","+str(all[i].lab)+")")
	o.write("\n")

#Giving not equal to condition
o.write("\n")
o.write("\n")
o.write("\n")
for i in range(len(all)):
	for j in range(len(all)):
		for k in range(len(all[i].lec_arr)):
			for l in range(len(all[j].lec_arr)):
				o.write(all[i].arr













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








def range_set(A,type):
	global range
	if type == "lab":
		temp = [And(A>36,A<43)]
		range.append(temp)

	else:
		temp = [And(A>0,A<37)]
		range.append(temp)











def no_same_helper(B,A):
	temp = If(B==1,And(A != 1,A != 2,A != 3,A != 4,A != 5),waste == 0)
	no_same_class.append(temp)
	temp = If(B==2,And(A != 7,A != 8,A != 9,A != 10,A != 6),waste == 0)
	no_same_class.append(temp)
	temp = If(B==3,And(A != 13,A != 14,A != 15,A != 12,A != 11),waste == 0)
	no_same_class.append(temp)
	temp = If(B==4,And(A != 16,A != 17,A != 18,A != 19,A != 20),waste == 0)
	no_same_class.append(temp)
	temp = If(B==5,And(A != 21,A != 22,A != 23,A != 24,A != 25),waste == 0)
	no_same_class.append(temp)
	temp = If(B==6,And(A != 26,A != 27,A != 28,A != 29,A != 30),waste == 0)
	no_same_class.append(temp)


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



















	if s.check() == sat :
	print(s.model())
	f = open("slots.txt","w")
	for i in range(len(all_z3)):
		f.write(all_z3[i].name)
		for j in range(len(all_z3[i].lec_arr)):
			f.write(str(all_z3[i].lec_arr[j].ans) + "    " + str(ans(all_z3[i].lec_arr[j].ans)))

		for j in range(len(all_z3[i].tut_arr)):
			f.write(str(all_z3[i].tut_arr[j].ans) + "    " + str(ans(all_z3[i].tut_arr[j].ans)))

		for j in range(len(all_z3[i].lab_arr)):
			f.write(str(all_z3[i].lab_arr[j].ans) + "    " + str(ans(all_z3[i].lab_arr[j].ans)))