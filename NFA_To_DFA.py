import re

def NFA_To_DFA(inString):

	def getEmptyValue():
		value = []
		for input in nfaInputs:
			value.append('')
		return value
		
	inList = inString.split(',')
	nfaStates = inList[0].split()
	nfaInputs = inList[1].split()
	transistions = inList[2].split()
	startingState = inList[3]
	nfaFinalState = inList[4]
	
	# create datastructure for nfa data
	# states stored in a list, each state is a key in a dictionary
	# for a list value containing transistions, the index of the transistion 
	# corresponds to the index of the input in the list of inputs.
	nfaStateTransitionPairs = {} # empty dictionary
	lengthInputs = len(nfaInputs)
	for i in range(len(nfaStates)):
		state = nfaStates[i]
		value = []
		n = 0
		while(n < lengthInputs):
			value.append(transistions[n + i * lengthInputs])
			n = n + 1
		nfaStateTransitionPairs[state] = value
	print('nfaState:')
	print (nfaStates)
	print('nfa state transition pairs:')
	print (nfaStateTransitionPairs)
	print('')
	
	# --- begin conversion ---
	dfaStates = []
	dfaStateTransisionPairs = {}
	
	# add the death state
	dfaStates.append('D')
	deathValue = []
	for input in nfaInputs:
		deathValue.append('D')
	dfaStateTransisionPairs['D'] = deathValue
	print('after adding death state to dfa')
	print(dfaStates)
	print(dfaStateTransisionPairs)
	print('')
	
	# handle starting state to start the chain reaction
	dfaStates.append(startingState)
	startTransStates = nfaStateTransitionPairs[startingState]
	startValue = []
	for state in startTransStates:
		if state != '-':
			startValue.append(state)
		else:
			startValue.append('D')
	dfaStateTransisionPairs[startingState] = startValue
	print('after adding starting state to dfa')
	print(dfaStates)
	print(dfaStateTransisionPairs)
	print('')
	
	
	
	unProcessedStates = []
	for state in startValue:
		if state not in dfaStates:
			unProcessedStates.append(state)
	print('unProcessedStates after adding starting')
	print(unProcessedStates)
	print('')
		
		
		
	while(len(unProcessedStates) != 0):
		curState = unProcessedStates.pop(0)
		print('\nprocessing: ' + curState)
		dfaStates.append(curState)
		
		
		
		# union if applicable
		value = getEmptyValue()
		for i in range(len(curState)):
			letter = curState[i]
			print('letter = ' + letter)
			
			letterStates = nfaStateTransitionPairs[letter]
			print('transitions:')
			print(letterStates)
			
			for j in range(len(letterStates)):
				print('curIndex = ' + str(j))
				state = letterStates[j]
				print('value at index' + str(j) + ' ' + value[j])
				if state != '-':
					#if state not in value[j]:
					stateToList = list(state)
					for let in stateToList:
						if re.search(let, value[j]) == None:
							value[j] = value[j] + let
							value[j] = ''.join(sorted(value[j]))
							print('value at index' + str(j) + ' ' + value[j])
			# check for and add death states
			for j in range(len(value)):
				if value[j] == '':
					value[j] = 'D'
			print(value)
			print('')
			
		dfaStateTransisionPairs[curState] = value
		
		# add states to unProcessedStates
		for state in value:
			if state not in dfaStates and state not in unProcessedStates:
				unProcessedStates.append(state)
		print('updated unProcessedStates')
		print(unProcessedStates)
		
	# compute dfa final states
	dfaFinalStates = ''
	for state in dfaStates:
		stateToList = list(state)
		for let in stateToList:
			if re.search(let, nfaFinalState) != None:
				dfaFinalStates = dfaFinalStates + ' ' + state
				break
		
		
		
	print('')
	print('dfa states:')
	print(dfaStates)
	print('dfa state transistion pairs:')
	print(dfaStateTransisionPairs)
	print('starting state: ' + startingState)
	print('final states: ' + dfaFinalStates)
	return 


	
# Input formatted: 
# states, inputs, transistions, startState, finalState	

NFA_To_DFA("A B C,a b,AB C A B - AB,A,C")

# --- above input returns ---

# dfa states:
# ['D', 'A', 'AB', 'C', 'BC']
# dfa state transistion pairs:
# {'D': ['D', 'D'], 'A': ['AB', 'C'], 'AB': ['AB', 'BC'], 'C': ['D', 'AB'], 'BC': ['A', 'AB']}
# starting state: A
# final states:  C BC


NFA_To_DFA("A B,0 1,B - B B,A,B")

# https://www.tutorialspoint.com/automata_theory/ndfa_to_dfa_conversion.htm
NFA_To_DFA("A B C d E,0 1,ABCdE dE C E - B E - - -,A,E")

