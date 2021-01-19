def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]

def swich (d, text, lvl=3, rvs = False, log=False, err = 50):

	spam = ["?", "!", "."]
	s = d
	for i in range(len(spam)):
	 	s = s.replace(spam[i], "")
	d = s
	
	if lvl==3:
		for x in text:
			cmp=text[x]
			for y in range(len(cmp)):
				t=cmp[y]
				if rvs:
					d,t=t,d
				if d in t:
					if log:
						print("[log] Comand swich: " + str(x))
					return (x)
					
	if lvl==2:
		for x in range(len(text)):
			t=text[x]
			if rvs:
				d,t=t,d
			if d in t:
				return True
				
	if lvl==1:
		if rvs:
			d,text=text,d
		if d in text:
			return True
			
	if log:
		print("[log] Swich false")
	return False

	#S.rstrip([chars])	Удаление пробельных символов в конце строки
	#S.replace(шаблон, замена)	Замена шаблона