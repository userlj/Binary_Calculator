#!/usr/bin/python
import cgi
import cgitb
cgitb.enable()


form = cgi.FieldStorage()
o = form.getvalue("output")
op = form.getvalue("op")
h = form.getvalue("hidden_mem")
state = form.getvalue("state")
temp = h
errorMsg = ""


# check the length of input
def chk_len(str):
	if len(str)>7:
		global errorMsg
		errorMsg = "Error: Operand Overflow!"
		return False
	else:
		return True


# convert string to integer
def s2i(str):
	int_str = int(str,2)
	return int_str


# addition
def add(dec_a,dec_b):
	global errorMsg
	result = bin(dec_a + dec_b)[2:]
	result_len = len(result)
	if result_len>8:
		result = result[result_len-8:]
		errorMsg = "Error: Result Overflow!"
	return result


# substraction
def sub(dec_a,dec_b):
        global errorMsg
        result = dec_a - dec_b
        if result < 0:
		errorMsg = "Negative Result!"
		return bin((eval("0b"+str(int(bin(result)[3:].zfill(8).replace("0","2").replace("1","0").replace("2","1"))))+eval("0b1")))[2:].zfill(8)
	else:
		return bin(result)[2:].zfill(8) 


# bitwise AND operation
def AND(dec_a,dec_b):
	result = bin(dec_a & dec_b)[2:].zfill(8)
	return result


# bitwise OR operation
def OR(dec_a,dec_b):
        result = bin(dec_a | dec_b)[2:].zfill(8)
        return result


# bitwise XOR operation
def XOR(dec_a,dec_b):
        result = bin(dec_a ^ dec_b)[2:].zfill(8)
        return result


# get the value of buttons
if op == "C":		#clear the accumulator
	out = "0"
	global errorMsg
	errorMsg = ""
elif op == "1":		#enter a 1 into the low order position of the accumulator
	if chk_len(o):
		if s2i(o)==0:
			out = "1"
		else:
			out = o + str(op)
	else:
		out = "0"
elif op == "0":		#enter a 0 into the low order position of the accumulator
	if chk_len(o):
		if s2i(o)==0:
			out = "0"
		else:
			out = o + str(op)
	else:
		out = "0"
elif op == "MC":	#clear the internal memory
	temp = 0
	out = o
elif op == "MR":	#move the contents of memory to the accumulator display
	out = temp
elif op == "MS":	#store the contents of the accumulator in memory
	temp = o
	out = "0"
elif op == "+":		#save the accumulator in temp, clear it, set state to add
	temp = o
	out = "0"
	state = "add"
elif op == "-":		#save the accumulator in temp, clear it, set state to minus
	temp = o
	out = "0"
	state = "minus"
elif op == "AND":	#save the accumulator in temp, clear it, set state to AND
	temp = o
	out = "0"
	state = "AND"
elif op == "OR":	#save the accumulator in temp, clear it, set state to OR
	temp = o
	out = "0"
	state = "OR"
elif op == "XOR":	#save the accumulator in temp, clear it, set state to XOR
	temp = o
	out = "0"
	state = "XOR"
elif op == "=":
	if state == "add":
	        out = add(s2i(temp),s2i(o))
        	state = "normal"
	elif state == "minus":
		out = sub(s2i(temp),s2i(o))
		state = "normal"
	elif state == "AND":
		out = AND(s2i(temp),s2i(o))
		state = "normal"
        elif state == "OR":
                out = OR(s2i(temp),s2i(o))
                state = "normal"
        elif state == "XOR":
                out = XOR(s2i(temp),s2i(o))
                state = "normal"
	elif state == "normal":
		out = o

print "Content-type: text/html"
print

print "<head>"
print "<title>"
print "cs422 Project1-Lingjie"
print "</title>"
print "</head>"
print "<center>"
print "<br>"
print "<fieldset style=width:180px><br>"
print "<fieldset style=width:180px><br><legend><b>Binary Calculator</b></legend>"
print "<form action=http://harvey.binghamton.edu/~lmeng4/cgi-bin/calc.py method=post>"
print "<br>"
print '<input style="text-align:right;width:175px;height:40px" name=output type=text value='+out+' readonly=readonly>'
print "<table>"
print "<tr>"
print '<td><input type=submit name=op value=0 style="width:55px; height:40px">'
print '<td><input type=submit name=op value=1 style="width:55px; height:40px">'
print '<td><input type=submit name=op value=C style="width:55px; height:40px">'
print "<tr>"
print '<td><input type=submit name=op value=AND style="width:55px; height:40px">'
print '<td><input type=submit name=op value=OR style="width:55px; height:40px">'
print '<td><input type=submit name=op value=XOR style="width:55px; height:40px">'
print "<tr>"
print '<td><input type=submit name=op value=+ style="width:55px; height:40px">'
print '<td><input type=submit name=op value=- style="width:55px; height:40px">'
print '<td><input type=submit name=op value== style="width:55px; height:40px">'
print "<tr>"
print '<td><input type=submit name=op value=MC style="width:55px; height:40px">'
print '<td><input type=submit name=op value=MR style="width:55px; height:40px">'
print '<td><input type=submit name=op value=MS style="width:55px; height:40px">'
print "<tr>"
print "</fieldset>"
print "<input type=hidden name=hidden_mem value="+str(temp)+">"
print "<input type=hidden name=state value="+str(state)+">"
print "</table>"
print "</form>"
print "TEMP: <b>"+str(temp)+"</b><br>"
print "STATE: <b>"+str(state)+"</b><br>"
print "<font color=red><b>"+errorMsg+"</b></font>"

