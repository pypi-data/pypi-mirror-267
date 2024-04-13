from os import system, get_terminal_size
import time
import random as rn

def commence():
	ground = "–"
	dino = " "*10 + "(⁠☞⁠ ⁠ಠ⁠_⁠ಠ⁠)⁠☞"
	dino_space = "                   "
	obst_up = "  "*20
	road = "\n" + ground*(get_terminal_size()[0])
	move_obst = False
	jump = False
	switch = False
	mid = ""
	add_mid = False
	failed = False
	
	# RERENDERING ALL THE TIME
	tacle = "–"
	while True:
		if rn.random() > 0 and not "∆" in obst_up:
			obst_up = "  "*30
			obst_down = "  "*20
			obst_up += "∆"
			obst_down += "∆"
			move_obst = True
			
		if move_obst == True:
			obst_up = obst_up[1:]
			obst_down = obst_down[1:]
		
		if obst_up == "":
			move_obst = False
		
		if add_mid:
			mid += " "
			
		road = road.replace("–", "", 1)
		road += ground
		
		
		#if obst_down == "∆":
#			outer = road + f"\n{dino}\n{obst_up}\n{dino_space}{obst_down}\n" + road
#			print(outer)
			#break
		#if not kb.is_pressed("a") and len(obst_down) < 4:
#			failed = True
		if obst_down == "∆":
			if failed:
				print(outer)
				break
			
			mid = ""
			jump = True
			if not switch:
				obst_down = dino_space + "∆"
				switch = True
			else:
				obst_down = "∆"
				switch = False
				
			## BREAK ALL HERE
#			outer = road + f"\n{dino}\n{obst_up}\n{obst_down}\n" + road
#			print(outer)
		else:
			if jump:
				outer = road + f"\n{dino}\n{obst_up}\n{obst_down}\n\n" + road
				if len(obst_down.split("∆")[0]) < len(" "*10):
					jump = None
					
					#obst_down = obst_down.replace("  "*10, "")
			elif jump == False:
				outer = road + f"\n\n\n{obst_up}\n{dino}{obst_down}\n" + road
			elif jump == None:
				#if not "(⁠" in obst_down:
#					obst_down += "(⁠☞⁠ ⁠ಠ⁠_⁠ಠ⁠)⁠☞"
				add_mid = True
				#mid += " "
				#mid = ""
				
				if len(mid) > 10:
					mid = ""
				outer = road + f"\n\n\n{obst_up}\n{obst_down}{mid}(⁠☞⁠ ⁠ಠ⁠_⁠ಠ⁠)⁠☞\n" + road
			
			if not " " in obst_down.split("(")[0]:
				jump = False
				
		#else:
#			if jump:
#				outer = road + f"\n{dino}\n{obst_up}\n{obst_down}\n\n" + road
#				if len(obst_down.split("∆")[0]) < len(" "*10):
#					#jump = False
#					jump = None
#					
#					#obst_down = obst_down.replace("  "*10, "")
#			elif jump == False:
#				outer = road + f"{len(obst_down)}\n\n\n{obst_up}\n{dino}{obst_down}\n" + road
#			elif jump == None:
		
		
				
			print(outer)
			time.sleep(.04)
			system('clear')
	

#commence()

