import eons
import re
import logging
import sys
import copy
import inspect
import jsonpickle # NOTE: both pickle & dill fail to save and restore the Parser; however jsonpickle appears to work.
from pathlib import Path
from collections import OrderedDict
from collections import defaultdict
from collections import Counter
import os
import types
from copy import deepcopy
from typing import Any

######## START CONTENT ########

class Structure (eons.Functor):

	def __init__(this, name="Structure"):
		super().__init__(name)

		# Used when parsing. Terrible name per Sly.
		this.optionalKWArgs['p'] = None

		this.optionalKWArgs['exclusions'] = []
		this.optionalKWArgs['inclusions'] = []
		this.optionalKWArgs['overrides'] = []

		this.fetch.use = [
			'args',
			'this',
		]
		this.fetch.attr.use = []

	def Function(this):
		pass

	def GetProduct(this, index):
		# No mangling necessary.. yet..
		return this.p[index]

	def Engulf(this, substrate, escape=False):
		if (
			substrate is None
			or isinstance(substrate, bool)
			or isinstance(substrate, int)
			or isinstance(substrate, float)
			or isinstance(substrate, list)
			or isinstance(substrate, dict)
		):
			return substrate
		
		ret = str(substrate)
		
		if (not len(ret)):
			return ret

		if (ret[0] == ret[-1] 
			and (
				ret[0] == '"'
				or ret[0] == "'"
			)
		):
			ret = ret[1:-1]

		if (escape):
			ret = re.sub(r"\\", r"\\\\", ret)
			ret = re.sub(r"'", r"\'", ret)
		return ret


class SyntaxError(Exception, metaclass=eons.ActualType): pass

@eons.kind(Structure)
def Block(
	openings = [],
	closings = [],
	content = "",
):
	# Return only the content, not the open nor close.
	# We must also filter for EOL tokens.
	possibleContent = None
	i = 0
	failedMatches = []
	reject = [r'^\s*$'] + openings + closings
	while (True):
		try:
			possibleContent = this.GetProduct(i)
			logging.debug(f"{this.name} Block has possibleContent '{possibleContent}' ({i}).")

			if (isinstance(possibleContent, str)):
				if (not len(possibleContent)):
					i += 1
					continue

				shouldReject = False
				for r in reject:
					if (re.search(r, possibleContent)):
						failedMatches.append(possibleContent)
						shouldReject = True
						break
				if (shouldReject):
					i += 1
					continue

				# String not skipped or rejected. This should be it.
				break

			elif (isinstance(possibleContent, list)):
				# Sets and friends will return lists, so this is probably what we're looking for.
				break

			else:
				i += 1

		except Exception as e:
			logging.error(f"{this.name} Block failed to find content due to {type(e)}: {e}")
			# Empty blocks are acceptable.
			if (not len(failedMatches)):
				logging.debug(f"Block {this.name} is empty.")
				return ""

			raise SyntaxError(f"Could not find content for {this.name} block in {failedMatches}.")

	return this.Engulf(possibleContent)

# SymmetricBlocks use the same symbols for both openings and closings.
@eons.kind(Block)
def SymmetricBlock(
	openings = [],
	content = "",
):
	# SymmetricBlocks should always have 1 opening and 1 closing.
	return this.GetProduct(1)

# OpenEndedBlocks only specify openings.
# They are closed by the beginning of another block.
# To make this possible, we just reinterpret closings as a list of blocks, not regexes.
# NOTE: All OpenEndedBlocks are terminated by the end of the line (r'$')
# NOTE: OpenEndedBlocks are not allowed to be nested: they are also automatically closed by all listed openings.
@eons.kind(Block)
def OpenEndedBlock(
	closings = [
		# Example only
		# 'BlockComment',
		# 'LineComment'
	],
	doesSpaceClose = False,
):
	return this.parent.Function(this)

@eons.kind(Block)
def MetaBlock(
	compose = [],
):
	return this.parent.Function(this)

# There should only ever be one CatchAllBlock. We call it 'Name'.
# This Block matches anything that is not explicitly matched by another Block.
# specialStarts allows characters which normally cannot be inside a CatchAllBlock to start a CatchAllBlock.
# For example, '/=' is valid, while '=/' is not.
@eons.kind(Block)
def CatchAllBlock(
	specialStarts = [
		# Example only
		# '/',
	],
):
	return this.GetProduct(0)

# Expressions build the contents of all other Blocks beside the CatchAllBlock.
@eons.kind(OpenEndedBlock)
def Expression(
	openings = [r';', r','],
	nest = [], # List of blocks that can be nested inside this block.
	exclusions = [
		'EOL',
	]
):
	return this.Engulf(this.GetProduct(0))

# ExpressionSet is constructed from a series of Expressions.
# Each nest in a Expression is realized through a ExpressionSet.
@eons.kind(Block)
def ExpressionSet():

	if (isinstance(this.GetProduct(0), str)):
		if (not len(this.GetProduct(0))):
			return []
		return [this.Engulf(this.GetProduct(0))]
	elif (isinstance(this.GetProduct(0), int) or isinstance(this.GetProduct(0), float)):
		return [this.GetProduct(0)]

	ret = this.GetProduct(0)

	if (isinstance(this.GetProduct(0), list)):
		try:
			if (isinstance(this.GetProduct(1), list)):
				ret = this.GetProduct(0) + this.GetProduct(1)
			elif (isinstance(this.GetProduct(1), str)):
				if (not len(this.GetProduct(1))):
					ret = this.GetProduct(0)
				else:
					ret = this.GetProduct(0) + [this.Engulf(this.GetProduct(1))]
			else:
				ret.append(this.Engulf(this.GetProduct(1)))
		except Exception as e:
			pass
	
	return ret

@eons.kind(SymmetricBlock)
def UnformattedString(
	openings = [r"\'"],
	representation = "\\'UNFORMATTED_STRING\\'", #NOT a raw string
	content = None,
	overrides = [
		'prioritize',
	],
	inclusions = [
		'newline',
	],
):
	# UnformattedStrings are lexed wholesale.
	string = this.Engulf(this.GetProduct(0), escape=True)

	# Escape any newline characters.
	string = string.replace('\n', '\\n')

	return f"String('{string}')"

@eons.kind(SymmetricBlock)
def FormattedString(
	lexer = None,
	parser = None,
	openings = [r'"', r'`'],
	representation = '\"FORMATTED_STRING\"', #NOT a raw string
	content = None,
	nest = [
		'Execution',
	],
	overrides = [
		'prioritize',
	],
	inclusions = [
		'newline',
	],
):
	if (lexer is None):
		lexer = this.executor.Fetch('lexer')
	if (parser is None):
		parser = this.executor.Fetch('parser')

	rawString = f"'{this.GetProduct(0)[1:-1]}'" # Standardize quotations

	# This is what we want to do, but python does not support the P<-...> module (only P<...>)
	# executionBlocks = re.findall(r'{(?:[^{}]|(?P<open>{)|(?P<-open>}))*(?(open)(?!))}', rawString)

	executionBlocks = []

	openCount = 0
	openPos = 0
	for i,char in enumerate(rawString):
		if (char == '{'):
			openCount += 1
			openPos = i+1
		elif (char == '}'):
			openCount -= 1
		if (openCount == 0 and openPos > 0):
			# logging.critical(f"Execution block: {rawString[openPos:i]}")
			executionBlocks.append(rawString[openPos:i])
			openPos = 0

	if (openCount > 0):
		raise SyntaxError(f"Unbalanced curly braces in formatted string: {rawString}")

	# logging.critical(f"Execution blocks: {executionBlocks}")

	stringComponents = [rawString]
	for i, block in enumerate(executionBlocks):
		stringComponents[0] = stringComponents[0].replace(f"{{{block}}}", r"%s", 1)
		stringComponents.append(parser.parse(lexer.tokenize(block)))
	
	# Escape any newline characters only AFTER the rawString has been processed.
	stringComponents[0] = stringComponents[0].replace('\n', '\\\\n')

	# logging.critical(f"String components: {stringComponents}")

	# Wipe result data, since our return value here can apparently be clobbered by the parser calls.
	import eons #huh?
	this.result.data = eons.util.DotDict()

	return f"String({', '.join([str(c) for c in stringComponents])})"

@eons.kind(MetaBlock)
def String(
	compose = [
		'UnformattedString',
		'FormattedString',
	],
	representation = r'`STRING`',
	content = None,
	exclusions = ['lexer'],
	overrides = [
		'prioritize',
	],
):
	return this.GetProduct(0) # already parsed.

@eons.kind(Block)
def BlockComment(
	openings = [r'/\*'],
	closings = [r'\*/'],
	representation = r'/\*BLOCK_COMMENT\*/',
	content = None,
	exclusions = [
		'tokens',
		'parser',
	],
	inclusions = [
		'newline',
		'space.padding',
	],
):
	return ''

@eons.kind(OpenEndedBlock)
def LineComment(
	openings = [r'#', r'//'],
	closings = [],
	representation = r'//LINE_COMMENT',
	content = None,
	exclusions = [
		'tokens',
		'parser',
	],
	inclusions = [
		'space.padding',
	],
):
	return ''

@eons.kind(OpenEndedBlock)
def Kind(
	openings = [r':'],
	closings = [],
	representation = r':KIND',
	content = "LimitedExpression",
):
	if (len(this.p) <= 1):
		return "Kind()"

	if (this.GetProduct(0) in openings and this.GetProduct(1) in openings):
		return "Kind()"
	if (this.GetProduct(0).startswith('Kind')):
		return this.GetProduct(0)
	kind = this.Engulf(this.GetProduct(1), escape=True)
	if (len(kind)):
		kind = f"'{kind}'"
	return f"Kind({kind})"

@eons.kind(Block)
def Parameter(
	openings = [r'\('],
	closings = [r'\)'],
	representation = r'\(PARAMETER\)',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
):
	return this.parent.Function(this)

@eons.kind(Block)
def Execution(
	openings = [r'{'],
	closings = [r'}'],
	representation = r'{{EXECUTION}}',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
):
	return this.parent.Function(this)

@eons.kind(Block)
def Container(
	openings = [r'\['],
	closings = [r'\]'],
	representation = r'\[CONTAINER\]',
	content = "FullExpressionSet",
	inclusions = [
		'space.padding',
	],
):
	return this.parent.Function(this)


@eons.kind(Structure)
def Syntax():
	pass

@eons.kind(Syntax)
def ExactSyntax(
	match = r'',
	# literalMatch = False,
	recurseOn = None,
	readDirection = ">"
):
	pass

@eons.kind(ExactSyntax)
def FlexibleTokenSyntax(
	match = [],
	exclusions = [
		'lexer',
		'all.catch.block'
	],
):
	pass

@eons.kind(Syntax)
def BlockSyntax(
	blocks = [],
):
	pass

@eons.kind(BlockSyntax)
def Invokation():
	pass

@eons.kind(FlexibleTokenSyntax)
def OperatorOverload():
	args = {
		'name': this.GetProduct(0),
		'kind': this.Engulf(this.GetProduct(1)),
		'parameter': None,
		'execution': None,
	}
	if (len(this.p) == 3):
		args['execution'] = this.Engulf(this.GetProduct(2))
	elif (len(this.p) == 4):
		args['parameter'] = this.Engulf(this.GetProduct(2))
		args['execution'] = this.Engulf(this.GetProduct(3))

	argString = ','.join([f'{k}={v}' for k, v in args.items()])

	return f"Type({argString})"


@eons.kind(BlockSyntax)
def SimpleType(
	blocks = [
		'Name',
		'Kind',
	],
):
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))})"

@eons.kind(BlockSyntax)
def ContainerAccess(
	blocks = [
		'Name',
		'Container',
	]
):
	return f"Within(name={this.GetProduct(0)},container={this.Engulf(this.GetProduct(1))})"

@eons.kind(Invokation)
def StandardInvokation(
	blocks = [
		'Name',
		'Parameter',
	]
):
	return f"Invoke(name={this.GetProduct(0)},parameter={this.Engulf(this.GetProduct(1))})"

@eons.kind(Invokation)
def AccessInvokation(
	blocks = [
		'ExplicitAccess',
		'Parameter',
	]
):
	return f"Invoke(source='{this.Engulf(this.GetProduct(0), escape=True)}',parameter={this.Engulf(this.GetProduct(1))})"

@eons.kind(AccessInvokation)
def ComplexAccessInvokation(
	blocks = [
		'ComplexExplicitAccess',
		'Parameter',
	]
):
	return this.parent.Function(this)

@eons.kind(Invokation)
def InvokationWithExecution(
	blocks = [
		'Name',
		'Execution',
	]
):
	return f"Invoke(name={this.GetProduct(0)},execution={this.Engulf(this.GetProduct(1))})"

@eons.kind(BlockSyntax)
def StructType(
	blocks = [
		'Name',
		'Kind',
		'Parameter',
	],
):
	if (this.GetProduct(0).startswith('Type')):
		return f"{this.GetProduct(0)[:-1]},parameter={this.Engulf(this.GetProduct(1))})"
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))},parameter={this.Engulf(this.GetProduct(2))})"

# Executive type is terminal. No other types build on it.
@eons.kind(BlockSyntax)
def ExecutiveType(
	blocks = [
		'Name',
		'Kind',
		'Execution',
	],
):
	if (this.GetProduct(0).startswith('Type')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"

@eons.kind(Invokation)
def InvokationWithParametersAndExecution(
	blocks = [
		'Name',
		'Parameter',
		'Execution',
	]
):
	if (this.GetProduct(0).startswith('Invoke')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Invoke(name={this.GetProduct(0)},parameter={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"

@eons.kind(Invokation)
def ContainerInvokation(
	blocks = [
		'Name',
		'Container',
		'Execution',
	],
):
	if (this.GetProduct(0).startswith('Within')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Within(name={this.GetProduct(0)},container={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"

@eons.kind(Invokation)
def ContainerInvokationWithParameters(
	blocks = [
		'Name',
		'Parameter',
		'Container',
		'Execution',
	],
):
	if (this.GetProduct(0).startswith('Invoke')):
		return f"{this.GetProduct(0)[:-1]},container={this.Engulf(this.GetProduct(1))},execution={this.Engulf(this.GetProduct(2))})"
	return f"Invoke(name={this.GetProduct(0)},parameter={this.Engulf(this.GetProduct(1))},container={this.Engulf(this.GetProduct(2))},execution={this.Engulf(this.GetProduct(3))})"

@eons.kind(BlockSyntax)
def FunctorType(
	blocks = [
		'Name',
		'Kind',
		'Parameter',
		'Execution',
	],
):
	if (this.GetProduct(0).startswith('Type')):
		return f"{this.GetProduct(0)[:-1]},execution={this.Engulf(this.GetProduct(1))})"
	return f"Type(name={this.GetProduct(0)},kind={this.Engulf(this.GetProduct(1))},parameter={this.Engulf(this.GetProduct(2))},execution={this.Engulf(this.GetProduct(3))})"

@eons.kind(ExactSyntax)
def EOL(
	match = r'[\\n\\r\\s]+',
	exclusions = [
		'parser',
	],
):
	return ''

@eons.kind(FlexibleTokenSyntax)
def AutofillAccessOrInvokation(
	match = [
		{
			'first': [
				r'name',
				r'sequence',
				r'complexsequence',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
				# Explicitly NOT simpletype
			],
			'second': [
				r'name',
				r'sequence',
				r'complexsequence',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		},
		{
			'first': [
				r'number',
				r'string',
			],
			'second': [
				r'name'
			]
		},
		{
			'first': [
				r'simpletype',
			],
			'second': [
				r'name'
			]
		}
	],
	recurseOn = "name",
	overrides = [
		'deprioritize'
	]
):
	return f"Autofill('{this.Engulf(this.GetProduct(0), escape=True)}','{this.Engulf(this.GetProduct(1), escape=True)}')"

@eons.kind(FlexibleTokenSyntax)
def AutofillInvokation(
	match = [
		{
			'first': [
				r'name',
				r'containeraccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'sequence',
				r'complexsequence',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
				r'autofillaccessorinvokation',
			],
			'second': [
				r'number',
				r'string',
			],
		},
		{
			'first': [
				r'shorttype',
			],
			'second': [
				r'number',
				r'string',
				r'sequence',
				r'container',
				r'containeraccess',
				r'standardinvokation',
				r'accessinvokation',
				r'complexaccessinvokation',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
				r'autofillaccessorinvokation',
				r'simpletype',
				r'structtype',
				r'executivetype',
				r'functortype',
			],
		}
	],
	overrides = [
		'deprioritize'
	]
):
	return f"Call('{this.Engulf(this.GetProduct(0), escape=True)}',{this.Engulf(str(this.GetProduct(1)))})"

@eons.kind(ExactSyntax)
def Sequence(
	match = r'NAME/NAME',
	# recurseOn = "name" # Now handled by ComplexSequence
):
	return f"Sequence({this.GetProduct(0)},{this.GetProduct(2)})"

@eons.kind(FlexibleTokenSyntax)
def ComplexSequence(
	match = [
		{
			'first': [
				r'sequence',
				r'standardinvokation',
				r'containeraccess',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
			'second': [
				r'SEQUENCE',
			],
			'third': [
				r'name',
				r'standardinvokation',
				r'containeraccess',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		},
		{
			'first': [
				r'name',
			],
			'second': [
				r'SEQUENCE',
			],
			'third': [
				r'standardinvokation',
				r'containeraccess',
				r'explicitaccess',
				r'complexexplicitaccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		}
	]
):
	return f"Sequence('{this.Engulf(this.GetProduct(0), escape=True)}','{this.Engulf(this.GetProduct(2), escape=True)}')"

@eons.kind(OperatorOverload)
def DivisionOverload(
	match = [
		r'SEQUENCE kind',
		r'SEQUENCE kind execution',
		r'SEQUENCE kind parameter execution',
	]
):
	return this.parent.Function(this)


# We have to specify the /= operator to prevent it from getting caught in a SEQUENCE match.
# TODO: Is there a fancier way to do a negative look ahead of an already matched name, so that we can include this logic in the SEQUENCE match?
@eons.kind(ExactSyntax)
def DivisionAssignment(
	match = r'NAME/=NAME',
):
	return f"{this.Engulf(this.GetProduct(0))} /= {this.Engulf(this.GetProduct(2))}"

# NOTE: Sequences and division CANNOT be combined.
@eons.kind(FlexibleTokenSyntax)
def ComplexDivisionAssignment(
	match = [
		{
			'first': [
				r'explicitaccess',
				r'complexexplicitaccess',
				r'standardinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
			'second': [
				r'DIVISIONASSIGNMENT',
			],
			'third': [
				r'name',
				r'autofillaccessorinvokation',
				r'standardinvokation',
				r'explicitaccess',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		},
		{
			'first': [
				r'name',
			],
			'second': [
				r'DIVISIONASSIGNMENT',
			],
			'third': [
				r'autofillaccessorinvokation',
				r'standardinvokation',
				r'explicitaccess',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
		}
	]
):
	return f"{this.Engulf(str(this.GetProduct(0)))} /= {this.Engulf(str(this.GetProduct(2)))}"

@eons.kind(OperatorOverload)
def DivisionAssignmentOverload(
	match = [
		r'DIVISIONASSIGNMENT kind',
		r'DIVISIONASSIGNMENT kind execution',
		r'DIVISIONASSIGNMENT kind parameter execution',
	]
):
	return this.parent.Function(this)

@eons.kind(ExactSyntax)
def ExplicitAccess(
	match = r'NAME\.NAME',
	# recurseOn = "name" # Now handled by ComplexExplicitAccess
):
	return f"Get({this.GetProduct(0)},{this.GetProduct(2)})"

@eons.kind(FlexibleTokenSyntax)
def ComplexExplicitAccess(
	match = [
		{
			'first': [
				r'explicitaccess',
				r'standardinvokation',
				r'containeraccess',
				r'this',
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef',
				r'globalscope',
				r'caller',
			],
			'second': [
				r'EXPLICITACCESS',
			],
			'third': [
				r'name',
				r'standardinvokation',
				r'containeraccess',
			],
		},
		{
			'first': [
				r'name'
			],
			'second': [
				r'EXPLICITACCESS',
			],
			'third': [
				r'standardinvokation',
				r'containeraccess',
			],
		},
	]
):
	return f"Get('{this.Engulf(this.GetProduct(0), escape=True)}','{this.Engulf(this.GetProduct(2), escape=True)}')"

@eons.kind(ExactSyntax)
def ShortType(
	match = r'NAME\s+:=\s+'
):
	return f"Get(Type(name={this.GetProduct(0)}),'=')"

@eons.kind(FlexibleTokenSyntax)
def SimpleTypeWithShortTypeAssignment(
	match = [r'name OPEN_KIND limitedexpression SHORTTYPE']
):
	return f"Get(Type(name={this.Engulf(this.GetProduct(0))}, kind={this.Engulf(this.GetProduct(2))}))"

@eons.kind(ExactSyntax)
def This(
	match = r'\./NAME'
):
	toAccess = this.Engulf(this.GetProduct(1)[1:-1])
	if (toAccess.startswith('this')):
		return toAccess
	return f"this.{toAccess}"

@eons.kind(ExactSyntax)
def EpidefOption1(
	match = r'\.\.NAME'
):
	return f"this.epidef.{this.Engulf(this.GetProduct(1)[1:-1])}"

@eons.kind(ExactSyntax)
def EpidefOption2(
	match = r'\.\./NAME'
):
	return f"this.epidef.{this.Engulf(this.GetProduct(1)[1:-1])}"

@eons.kind(FlexibleTokenSyntax)
def ComplexEpidef(
	match = [
		{
			'first': [
				r'EPIDEFOPTION2'
			],
			'second': [
				r'epidefoption1',
				r'epidefoption2',
				r'complexepidef'
			]
		}
	]
):
	return f"this.epidef.{this.Engulf(this.GetProduct(1)[5:])}"

@eons.kind(ExactSyntax)
def GlobalScope(
	match = r'~/NAME'
):
	return f"HOME.Instance().{this.Engulf(this.GetProduct(1)[1:-1])}"

@eons.kind(ExactSyntax)
def Caller(
	match = r'@NAME',
):
	# Enable @@... to become this.caller.caller...
	toAccess = this.Engulf(this.GetProduct(1)[1:-1])
	if (toAccess.startswith('this.caller')):
		return f"this.caller.{toAccess[5:]}"
	return f"this.caller.{toAccess}"


# These don't actually do anything, they just help in ordering the files appropriately.

@eons.kind(CatchAllBlock)
def Name(
	representation = r'NAME',
):
	return f"'{this.GetProduct(0)}'"

@eons.kind(Expression)
def ProtoExpression(
	representation = r'PROTOEXPRESSION',
	nest = [
		'Name',
		'Number',
		'String',

		# ExactSyntaxes
		'AutofillAccessOrInvokation',
		'AutofillInvokation',
		'Sequence',
		'DivisionAssignment',
		'This',
		'ExplicitAccess',
		'EpidefOption1',
		'EpidefOption2',
		'ComplexEpidef',
		'GlobalScope',
	],
	before = "Sequence",
):
	return this.parent.Function(this)

@eons.kind(ExpressionSet)
def ProtoExpressionSet(
	representation = r'PROTOEXPRESSIONSET',
	content = "ProtoExpression",
	before = "ProtoExpression",
):
	return this.parent.Function(this)


@eons.kind(Expression)
def LimitedExpression(
	representation = r'LIMITEDEXPRESSION',
	nest = [
		'ProtoExpression',
		'ProtoExpressionSet',
		# 'Execution',
		# 'Container',

		# BlockSyntaxes
		'InvokationWithExecution',
		'ContainerAccess',
		'ContainerInvokation',
	],
	before = "ProtoExpressionSet"
):
	return this.parent.Function(this)

@eons.kind(ExpressionSet)
def LimitedExpressionSet(
	representation = r'LIMITEDEXPRESSIONSET',
	content = "LimitedExpression",
	before = "LimitedExpression"
):
	return this.parent.Function(this)


@eons.kind(Expression)
def FullExpression(
	representation = r'FULLEXPRESSION',
	nest = [
		# 'close_expression',

		'LimitedExpression',
		'LimitedExpressionSet',
		'Kind',
		# 'Parameter',

		# BlockSyntaxes
		'FunctorType',
		'StructType',
		'ExecutiveType',
		'SimpleType',
		'StandardInvokation',
		'AccessInvokation',
		'ComplexAccessInvokation',
		'InvokationWithParametersAndExecution',
		'ContainerInvokationWithParameters',

		# ExactSyntaxes
		'SimpleTypeWithShortTypeAssignment',
		'ComplexSequence',
		'DivisionOverload',
		'ComplexDivisionAssignment',
		'DivisionAssignmentOverload',
		'ComplexExplicitAccess',
	],
	before = "FunctorType",
):
	return this.parent.Function(this)

@eons.kind(ExpressionSet)
def FullExpressionSet(
	representation = r'FULLEXPRESSIONSET',
	content = "FullExpression",
	before = "FullExpression",
):
	return this.parent.Function(this)


################################################################################
#                                 ORDER MATTERS
# The order provided is the priority each section is given when parsing.
################################################################################

# The Summary contains a list of all the blocks and syntaxes that are defined in the Elder language.
# This is used by the parser to determine what to parse.
# Unfortunately, this is not automated (yet), so if you add a new block or syntax, you must add it to the Summary below.

summary = eons.util.DotDict()

summary.builtins = [
	"NUMBER",
]

summary.token = eons.util.DotDict()
summary.token.priority = [
	"UNFORMATTEDSTRING",
	"FORMATTEDSTRING",
	"DIVISIONASSIGNMENT",
	"NUMBER",
	"SHORTTYPE",
	"OPEN_KIND",
	"OPEN_EXECUTION",
	"OPEN_PARAMETER",
	"OPEN_CONTAINER",
	"CLOSE_EXECUTION",
	"CLOSE_PARAMETER",
	"CLOSE_CONTAINER",
	"CLOSE_EXPRESSION",
	"THIS",
	"EPIDEFOPTION2",
	"EPIDEFOPTION1",
	"GLOBALSCOPE",
	"EXPLICITACCESS",
	"SEQUENCE",
	"CALLER",
	"EOL",
	"NAME",
]

summary.blocks = [
	"FullExpressionSet",
	"FullExpression",
	"Execution",
	"Parameter",
	"Container",
	"Kind",
	"LimitedExpressionSet",
	"LimitedExpression",
	"ProtoExpressionSet",
	"ProtoExpression",
	"BlockComment",
	"LineComment",
	"UnformattedString",
	"FormattedString",
	"String",
	"Name",
]

summary.catchAllBlock = "Name"
summary.startingBlock = "FullExpressionSet"
summary.expression = "Expression" # The DefaultBlock
summary.eol = "EOL"

summary.syntax = eons.util.DotDict()

summary.syntax.block = [
	"SimpleType",
	"ContainerAccess",
	"StandardInvokation",
	"AccessInvokation",
	"ComplexAccessInvokation",
	"InvokationWithExecution",
	"StructType",
	"ExecutiveType",
	"InvokationWithParametersAndExecution",
	"ContainerInvokation",
	"ContainerInvokationWithParameters",
	"FunctorType",
]

summary.syntax.exact = [
	"DivisionAssignment",
	"ComplexDivisionAssignment",
	"This",
	"EpidefOption2",
	"EpidefOption1",
	"ComplexEpidef",
	"GlobalScope",
	"DivisionOverload",
	"DivisionAssignmentOverload",
	"ExplicitAccess",
	"ComplexExplicitAccess",
	"Sequence",
	"ComplexSequence",
	"AutofillAccessOrInvokation",
	"AutofillInvokation",
	"EOL",
	"ShortType",
	"SimpleTypeWithShortTypeAssignment",
	"Caller",
]
# sly/ast.py

class AST(object):
	
	@classmethod
	def __init_subclass__(cls, **kwargs):
		mod = sys.modules[cls.__module__]
		if not hasattr(cls, '__annotations__'):
			return

		hints = list(cls.__annotations__.items())

		def __init__(self, *args, **kwargs):
			if len(hints) != len(args):
				raise TypeError(f'Expected {len(hints)} arguments')
			for arg, (name, val) in zip(args, hints):
				if isinstance(val, str):
					val = getattr(mod, val)
				if not isinstance(arg, val):
					raise TypeError(f'{name} argument must be {val}')
				setattr(self, name, arg)

		cls.__init__ = __init__


# -----------------------------------------------------------------------------
# sly: lex.py
#
# Copyright (C) 2016 - 2018
# David M. Beazley (Dabeaz LLC)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
#	this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#	this list of conditions and the following disclaimer in the documentation
#	and/or other materials provided with the distribution.
# * Neither the name of the David Beazley or Dabeaz LLC may be used to
#	endorse or promote products derived from this software without
#  specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------

# __all__ = ['Lexer', 'LexerStateChange']


class LexError(Exception):
	'''
	Exception raised if an invalid character is encountered and no default
	error handler function is defined.  The .text attribute of the exception
	contains all remaining untokenized text. The .error_index is the index
	location of the error.
	'''
	def __init__(self, message, text, error_index):
		self.args = (message,)
		self.text = text
		self.error_index = error_index

class PatternError(Exception):
	'''
	Exception raised if there's some kind of problem with the specified
	regex patterns in the lexer.
	'''
	pass

class LexerBuildError(Exception):
	'''
	Exception raised if there's some sort of problem building the lexer.
	'''
	pass

class LexerStateChange(Exception):
	'''
	Exception raised to force a lexing state change
	'''
	def __init__(self, newstate, tok=None):
		self.newstate = newstate
		self.tok = tok

class Token(object):
	'''
	Representation of a single token.
	'''
	__slots__ = ('type', 'value', 'lineno', 'index', 'end')
	def __repr__(self):
		return f'Token(type={self.type!r}, value={self.value!r}, lineno={self.lineno}, index={self.index}, end={self.end})'

class TokenStr(str):
	@staticmethod
	def __new__(cls, value, key=None, remap=None):
		self = super().__new__(cls, value)
		self.key = key
		self.remap = remap
		return self

	# Implementation of TOKEN[value] = NEWTOKEN
	def __setitem__(self, key, value):
		if self.remap is not None:
			self.remap[self.key, key] = value

	# Implementation of del TOKEN[value]
	def __delitem__(self, key):
		if self.remap is not None:
			self.remap[self.key, key] = self.key

class _Before:
	def __init__(self, tok, pattern):
		self.tok = tok
		self.pattern = pattern

class LexerMetaDict(dict):
	'''
	Special dictionary that prohibits duplicate definitions in lexer specifications.
	'''
	def __init__(self):
		self.before = { }
		self.delete = [ ]
		self.remap = { }

	def __setitem__(self, key, value):
		if isinstance(value, str):
			value = TokenStr(value, key, self.remap)
			
		if isinstance(value, _Before):
			self.before[key] = value.tok
			value = TokenStr(value.pattern, key, self.remap)
			
		if key in self and not isinstance(value, property):
			prior = self[key]
			if isinstance(prior, str):
				if callable(value):
					value.pattern = prior
				else:
					raise AttributeError(f'Name {key} redefined')

		super().__setitem__(key, value)

	def __delitem__(self, key):
		self.delete.append(key)
		if key not in self and key.isupper():
			pass
		else:
			return super().__delitem__(key)

	def __getitem__(self, key):
		if key not in self and key.split('ignore_')[-1].isupper() and key[:1] != '_':
			return TokenStr(key, key, self.remap)
		else:
			return super().__getitem__(key)

class LexerMeta(type):
	'''
	Metaclass for collecting lexing rules
	'''
	@classmethod
	def __prepare__(meta, name, bases):
		d = LexerMetaDict()

		def _(pattern, *extra):
			patterns = [pattern, *extra]
			def decorate(func):
				pattern = '|'.join(f'({pat})' for pat in patterns )
				if hasattr(func, 'pattern'):
					func.pattern = pattern + '|' + func.pattern
				else:
					func.pattern = pattern
				return func
			return decorate

		d['_'] = _
		d['before'] = _Before
		return d

	def __new__(meta, clsname, bases, attributes):
		del attributes['_']
		del attributes['before']

		# Create attributes for use in the actual class body
		cls_attributes = { str(key): str(val) if isinstance(val, TokenStr) else val
							for key, val in attributes.items() }
		cls = super().__new__(meta, clsname, bases, cls_attributes)

		# Attach various metadata to the class
		cls._attributes = dict(attributes)
		cls._remap = attributes.remap
		cls._before = attributes.before
		cls._delete = attributes.delete
		cls._build()
		return cls

class Lexer(metaclass=LexerMeta):
	# These attributes may be defined in subclasses
	tokens = set()
	literals = set()
	ignore = ''
	reflags = 0
	regex_module = re

	_token_names = set()
	_token_funcs = {}
	_ignored_tokens = set()
	_remapping = {}
	_delete = {}
	_remap = {}

	# Internal attributes
	__state_stack = None
	__set_state = None

	@classmethod
	def _collect_rules(cls):
		# Collect all of the rules from class definitions that look like token
		# information.	There are a few things that govern this:
		#
		# 1.  Any definition of the form NAME = str is a token if NAME is
		#	 is defined in the tokens set.
		#
		# 2.  Any definition of the form ignore_NAME = str is a rule for an ignored
		#	 token.
		#
		# 3.  Any function defined with a 'pattern' attribute is treated as a rule.
		#	 Such functions can be created with the @_ decorator or by defining
		#	 function with the same name as a previously defined string.
		#
		# This function is responsible for keeping rules in order. 

		# Collect all previous rules from base classes
		rules = []

		for base in cls.__bases__:
			if isinstance(base, LexerMeta):
				rules.extend(base._rules)
				
		# Dictionary of previous rules
		existing = dict(rules)

		for key, value in cls._attributes.items():
			if (key in cls._token_names) or key.startswith('ignore_') or hasattr(value, 'pattern'):
				if callable(value) and not hasattr(value, 'pattern'):
					raise LexerBuildError(f"function {value} doesn't have a regex pattern")
				
				if key in existing:
					# The definition matches something that already existed in the base class.
					# We replace it, but keep the original ordering
					n = rules.index((key, existing[key]))
					rules[n] = (key, value)
					existing[key] = value

				elif isinstance(value, TokenStr) and key in cls._before:
					before = cls._before[key]
					if before in existing:
						# Position the token before another specified token
						n = rules.index((before, existing[before]))
						rules.insert(n, (key, value))
					else:
						# Put at the end of the rule list
						rules.append((key, value))
					existing[key] = value
				else:
					rules.append((key, value))
					existing[key] = value

			elif isinstance(value, str) and not key.startswith('_') and key not in {'ignore', 'literals'}:
				raise LexerBuildError(f'{key} does not match a name in tokens')

		# Apply deletion rules
		rules = [ (key, value) for key, value in rules if key not in cls._delete ]
		cls._rules = rules

	@classmethod
	def _build(cls):
		'''
		Build the lexer object from the collected tokens and regular expressions.
		Validate the rules to make sure they look sane.
		'''
		if 'tokens' not in vars(cls):
			raise LexerBuildError(f'{cls.__qualname__} class does not define a tokens attribute')

		# Pull definitions created for any parent classes
		cls._token_names = cls._token_names | set(cls.tokens)
		cls._ignored_tokens = set(cls._ignored_tokens)
		cls._token_funcs = dict(cls._token_funcs)
		cls._remapping = dict(cls._remapping)

		for (key, val), newtok in cls._remap.items():
			if key not in cls._remapping:
				cls._remapping[key] = newtok #{}
			# cls._remapping[key][val] = newtok

		# remapped_toks = set()
		# for d in cls._remapping.values():
		# 	remapped_toks.update(d.values())

		# undefined = remapped_toks - set(cls._token_names)
		# if undefined:
		# 	missing = ', '.join(undefined)
		# 	raise LexerBuildError(f'{missing} not included in token(s)')

		cls._collect_rules()

		parts = []
		for tokname, value in cls._rules:
			if tokname.startswith('ignore_'):
				tokname = tokname[7:]
				cls._ignored_tokens.add(tokname)

			if isinstance(value, str):
				pattern = value

			elif callable(value):
				cls._token_funcs[tokname] = value
				pattern = getattr(value, 'pattern')

			# Form the regular expression component
			part = f'(?P<{tokname}>{pattern})'

			# Make sure the individual regex compiles properly
			try:
				cpat = cls.regex_module.compile(part, cls.reflags)
			except Exception as e:
				raise PatternError(f'Invalid regex for token {tokname}') from e

			# Verify that the pattern doesn't match the empty string
			if cpat.match(''):
				raise PatternError(f'Regex for token {tokname} matches empty input')

			parts.append(part)

		if not parts:
			return

		# Form the master regular expression
		#previous = ('|' + cls._master_re.pattern) if cls._master_re else ''
		# cls._master_re = cls.regex_module.compile('|'.join(parts) + previous, cls.reflags)
		cls._master_re = cls.regex_module.compile('|'.join(parts), cls.reflags)

		# Verify that that ignore and literals specifiers match the input type
		if not isinstance(cls.ignore, str):
			raise LexerBuildError('ignore specifier must be a string')

		if not all(isinstance(lit, str) for lit in cls.literals):
			raise LexerBuildError('literals must be specified as strings')

	def begin(self, cls):
		'''
		Begin a new lexer state
		'''
		assert isinstance(cls, LexerMeta), "state must be a subclass of Lexer"
		if self.__set_state:
			self.__set_state(cls)
		self.__class__ = cls

	def push_state(self, cls):
		'''
		Push a new lexer state onto the stack
		'''
		if self.__state_stack is None:
			self.__state_stack = []
		self.__state_stack.append(type(self))
		self.begin(cls)

	def pop_state(self):
		'''
		Pop a lexer state from the stack
		'''
		self.begin(self.__state_stack.pop())

	def tokenize(self, text, lineno=1, index=0):
		_ignored_tokens = _master_re = _ignore = _token_funcs = _literals = _remapping = None

		# --- Support for state changes
		def _set_state(cls):
			nonlocal _ignored_tokens, _master_re, _ignore, _token_funcs, _literals, _remapping
			_ignored_tokens = cls._ignored_tokens
			_master_re = cls._master_re
			_ignore = cls.ignore
			_token_funcs = cls._token_funcs
			_literals = cls.literals
			_remapping = cls._remapping

		self.__set_state = _set_state
		_set_state(type(self))

		# --- Support for backtracking
		_mark_stack = []
		def _mark():
			_mark_stack.append((type(self), index, lineno))
		self.mark = _mark

		def _accept():
			_mark_stack.pop()
		self.accept = _accept

		def _reject():
			nonlocal index, lineno
			cls, index, lineno = _mark_stack[-1]
			_set_state(cls)
		self.reject = _reject


		# --- Main tokenization function
		text += ';'
		self.text = text
		try:
			while True:
				try:
					if text[index] in _ignore:
						index += 1
						continue
				except IndexError:
					return

				tok = Token()
				tok.lineno = lineno
				tok.index = index
				m = _master_re.match(text, index)
				if m:
					tok.end = index = m.end()
					tok.value = m.group()
					tok.type = m.lastgroup

					if tok.type in _remapping:
						tok.type = _remapping[tok.type]

					# This isn't the safest, but this file is not for general consumption, so removing the guardrails is okay for Elderlang.
					if isinstance(tok.type, list):
						tokList = tok.type
						for tok.type in tokList:
							yield tok

					else:
						if tok.type in _token_funcs:
							self.index = index
							self.lineno = lineno
							tok = _token_funcs[tok.type](self, tok)
							index = self.index
							lineno = self.lineno
							if not tok:
								continue

						if tok.type in _ignored_tokens:
							continue

						yield tok

				else:
					# No match, see if the character is in literals
					if text[index] in _literals:
						tok.value = text[index]
						tok.end = index + 1
						tok.type = tok.value
						index += 1
						yield tok
					else:
						# A lexing error
						self.index = index
						self.lineno = lineno
						tok.type = 'ERROR'
						tok.value = text[index:]
						tok = self.error(tok)
						if tok is not None:
							tok.end = self.index
							yield tok

						index = self.index
						lineno = self.lineno

		# Set the final state of the lexer before exiting (even if exception)
		finally:
			self.text = text
			self.index = index
			self.lineno = lineno

	# Default implementations of the error handler. May be changed in subclasses
	def error(self, t):
		raise LexError(f'Illegal character {t.value[0]!r} at index {self.index}', t.value, self.index)

# -----------------------------------------------------------------------------
# sly: yacc.py
#
# Copyright (C) 2016-2018
# David M. Beazley (Dabeaz LLC)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the David Beazley or Dabeaz LLC may be used to
#   endorse or promote products derived from this software without
#  specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------


# __all__		= [ 'Parser' ]

class YaccError(Exception):
	'''
	Exception raised for yacc-related build errors.
	'''
	pass

#-----------------------------------------------------------------------------
#					 === User configurable parameters ===
#
# Change these to modify the default behavior of yacc (if you wish).  
# Move these parameters to the Yacc class itself.
#-----------------------------------------------------------------------------

ERROR_COUNT = 3				# Number of symbols that must be shifted to leave recovery mode
MAXINT = sys.maxsize

# ----------------------------------------------------------------------
# This class is used to hold non-terminal grammar symbols during parsing.
# It normally has the following attributes set:
#		.type	   = Grammar symbol type
#		.value	  = Symbol value
#		.lineno	 = Starting line number
#		.index	  = Starting lex position
# ----------------------------------------------------------------------

class YaccSymbol:
	def __str__(self):
		return self.type

	def __repr__(self):
		return str(self)

# ----------------------------------------------------------------------
# This class is a wrapper around the objects actually passed to each
# grammar rule.   Index lookup and assignment actually assign the
# .value attribute of the underlying YaccSymbol object.
# The lineno() method returns the line number of a given
# item (or 0 if not defined).   
# ----------------------------------------------------------------------

class YaccProduction:
	__slots__ = ('_slice', '_namemap', '_stack')
	def __init__(self, s, stack=None):
		self._slice = s
		self._namemap = { }
		self._stack = stack

	def __getitem__(self, n):
		ret = None
		if n >= 0:
			try: 
				ret = self._slice[n].value
				# if (hasattr(ret, 'type') and ret.type == '$end'):
				# 	ret = self.__getitem__(n+1)
				# else:
				# 	ret = ret.value
			except Exception as e:
				logging.debug(f'Could not get {self._slice}[{n}].value: {e}')
				return None
		else:
			try:
				ret = self._stack[n].value
			except Exception as e:
				logging.debug(f'Could not get {self._stack}[{n}].value: {e}')
				return None
		
		return ret

	def __setitem__(self, n, v):
		if n >= 0:
			self._slice[n].value = v
		else:
			self._stack[n].value = v

	def __len__(self):
		return len(self._slice)

	@property
	def lineno(self):
		for tok in self._slice:
			lineno = getattr(tok, 'lineno', None)
			if lineno:
				return lineno
		raise AttributeError('No line number found')

	@property
	def index(self):
		for tok in self._slice:
			index = getattr(tok, 'index', None)
			if index is not None:
				return index
		raise AttributeError('No index attribute found')

	@property
	def end(self):
		result = None
		for tok in self._slice:
			r = getattr(tok, 'end', None)
			if r:
				result = r
		return result
	
	def __getattr__(self, name):
		if name in self._namemap:
			return self._namemap[name](self._slice)
		else:
			nameset = '{' + ', '.join(self._namemap) + '}'
			raise AttributeError(f'No symbol {name}. Must be one of {nameset}.')

	def __setattr__(self, name, value):
		if name[:1] == '_':
			super().__setattr__(name, value)
		else:
			raise AttributeError(f"Can't reassign the value of attribute {name!r}")

# -----------------------------------------------------------------------------
#						  === Grammar Representation ===
#
# The following functions, classes, and variables are used to represent and
# manipulate the rules that make up a grammar.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# class Production:
#
# This class stores the raw information about a single production or grammar rule.
# A grammar rule refers to a specification such as this:
#
#	   expr : expr PLUS term
#
# Here are the basic attributes defined on all productions
#
#	   name	 - Name of the production.  For example 'expr'
#	   prod	 - A list of symbols on the right side ['expr','PLUS','term']
#	   prec	 - Production precedence level
#	   number   - Production number.
#	   func	 - Function that executes on reduce
#	   file	 - File where production function is defined
#	   lineno   - Line number where production function is defined
#
# The following attributes are defined or optional.
#
#	   len	   - Length of the production (number of symbols on right hand side)
#	   usyms	 - Set of unique symbols found in the production
# -----------------------------------------------------------------------------

class AccessFunctor1 (eons.Functor):
	def __init__(this, name="AccessFunctor1", index=0):
		super().__init__(name)

		this.arg.kw.optional['s'] = 0
		this.arg.kw.optional['i'] = index

		this.arg.mapping = ['s', 'i']

		this.feature.track = False
		this.feature.autoReturn = False
		this.feature.rollback = False

	def Function(this):
		return this.s[this.i].value


class AccessFunctor2 (AccessFunctor1):
	def __init__(this, name="AccessFunctor2", index=0, n=0):
		super().__init__(name, index)

		this.arg.kw.optional['n'] = n

		this.arg.mapping.append('n')

	def Function(this):
		return ([x[this.n] for x in this.s[this.i].value]) if isinstance(this.s[this.i].value, list) else this.s[this.i].value[this.n]

class Production(object):
	reduced = 0
	def __init__(self, number, name, prod, precedence=('right', 0), func=None, file='', line=0):
		self.name	 = name
		self.prod	 = tuple(prod)
		self.number   = number
		self.func	 = func
		self.file	 = file
		self.line	 = line
		self.prec	 = precedence
		
		# Internal settings used during table construction
		self.len  = len(self.prod)   # Length of the production

		# Create a list of unique production symbols used in the production
		self.usyms = []
		symmap = defaultdict(list)
		for n, s in enumerate(self.prod):
			symmap[s].append(n)
			if s not in self.usyms:
				self.usyms.append(s)

		# Create a name mapping
		# First determine (in advance) if there are duplicate names
		namecount = defaultdict(int)
		for key in self.prod:
			namecount[key] += 1
			if key in _name_aliases:
				for key in _name_aliases[key]:
					namecount[key] += 1

		# Now, walk through the names and generate accessor functions
		nameuse = defaultdict(int)
		namemap = { }
		for index, key in enumerate(self.prod):
			if namecount[key] > 1:
				k = f'{key}{nameuse[key]}'
				nameuse[key] += 1
			else:
				k = key
			namemap[k] = AccessFunctor1(str(k), index)
			if key in _name_aliases:
				for n, alias in enumerate(_name_aliases[key]):
					if namecount[alias] > 1:
						k = f'{alias}{nameuse[alias]}'
						nameuse[alias] += 1
					else:
						k = alias
					# The value is either a list (for repetition) or a tuple for optional 
					namemap[k] = AccessFunctor2(str(k), index, n)

		self.namemap = namemap
				
		# List of all LR items for the production
		self.lr_items = []
		self.lr_next = None

	def __str__(self):
		if self.prod:
			s = '%s -> %s' % (self.name, ' '.join(self.prod))
		else:
			s = f'{self.name} -> <empty>'

		if self.prec[1]:
			s += '  [precedence=%s, level=%d]' % self.prec

		return s

	def __repr__(self):
		return f'Production({self})'

	def __len__(self):
		return len(self.prod)

	def __nonzero__(self):
		raise RuntimeError('Used')
		return 1

	def __getitem__(self, index):
		return self.prod[index]

	# Return the nth lr_item from the production (or None if at the end)
	def lr_item(self, n):
		if n > len(self.prod):
			return None
		p = LRItem(self, n)
		# Precompute the list of productions immediately following.
		try:
			p.lr_after = Prodnames[p.prod[n+1]]
		except (IndexError, KeyError):
			p.lr_after = []
		try:
			p.lr_before = p.prod[n-1]
		except IndexError:
			p.lr_before = None
		return p

# -----------------------------------------------------------------------------
# class LRItem
#
# This class represents a specific stage of parsing a production rule.  For
# example:
#
#	   expr : expr . PLUS term
#
# In the above, the "." represents the current location of the parse.  Here
# basic attributes:
#
#	   name	   - Name of the production.  For example 'expr'
#	   prod	   - A list of symbols on the right side ['expr','.', 'PLUS','term']
#	   number	 - Production number.
#
#	   lr_next	  Next LR item. Example, if we are ' expr -> expr . PLUS term'
#					then lr_next refers to 'expr -> expr PLUS . term'
#	   lr_index   - LR item index (location of the ".") in the prod list.
#	   lookaheads - LALR lookahead symbols for this item
#	   len		- Length of the production (number of symbols on right hand side)
#	   lr_after	- List of all productions that immediately follow
#	   lr_before   - Grammar symbol immediately before
# -----------------------------------------------------------------------------

class LRItem(object):
	def __init__(self, p, n):
		self.name	   = p.name
		self.prod	   = list(p.prod)
		self.number	 = p.number
		self.lr_index   = n
		self.lookaheads = {}
		self.prod.insert(n, '.')
		self.prod	   = tuple(self.prod)
		self.len		= len(self.prod)
		self.usyms	  = p.usyms

	def __str__(self):
		if self.prod:
			s = '%s -> %s' % (self.name, ' '.join(self.prod))
		else:
			s = f'{self.name} -> <empty>'
		return s

	def __repr__(self):
		return f'LRItem({self})'

# -----------------------------------------------------------------------------
# rightmost_terminal()
#
# Return the rightmost terminal from a list of symbols.  Used in add_production()
# -----------------------------------------------------------------------------
def rightmost_terminal(symbols, terminals):
	i = len(symbols) - 1
	while i >= 0:
		if symbols[i] in terminals:
			return symbols[i]
		i -= 1
	return None

# -----------------------------------------------------------------------------
#						   === GRAMMAR CLASS ===
#
# The following class represents the contents of the specified grammar along
# with various computed properties such as first sets, follow sets, LR items, etc.
# This data is used for critical parts of the table generation process later.
# -----------------------------------------------------------------------------

class GrammarError(YaccError):
	pass

class Grammar(object):
	def __init__(self, terminals):
		self.Productions  = [None]  # A list of all of the productions.  The first
									# entry is always reserved for the purpose of
									# building an augmented grammar

		self.Prodnames	= {}	  # A dictionary mapping the names of nonterminals to a list of all
									# productions of that nonterminal.

		self.Prodmap	  = {}	  # A dictionary that is only used to detect duplicate
									# productions.

		self.Terminals	= {}	  # A dictionary mapping the names of terminal symbols to a
									# list of the rules where they are used.

		for term in terminals:
			self.Terminals[term] = []

		self.Terminals['error'] = []

		self.Nonterminals = {}	  # A dictionary mapping names of nonterminals to a list
									# of rule numbers where they are used.

		self.First		= {}	  # A dictionary of precomputed FIRST(x) symbols

		self.Follow	   = {}	  # A dictionary of precomputed FOLLOW(x) symbols

		self.Precedence   = {}	  # Precedence rules for each terminal. Contains tuples of the
									# form ('right',level) or ('nonassoc', level) or ('left',level)

		self.UsedPrecedence = set() # Precedence rules that were actually used by the grammer.
									# This is only used to provide error checking and to generate
									# a warning about unused precedence rules.

		self.Start = None		   # Starting symbol for the grammar


	def __len__(self):
		return len(self.Productions)

	def __getitem__(self, index):
		return self.Productions[index]

	# -----------------------------------------------------------------------------
	# set_precedence()
	#
	# Sets the precedence for a given terminal. assoc is the associativity such as
	# 'left','right', or 'nonassoc'.  level is a numeric level.
	#
	# -----------------------------------------------------------------------------

	def set_precedence(self, term, assoc, level):
		assert self.Productions == [None], 'Must call set_precedence() before add_production()'
		if term in self.Precedence:
			raise GrammarError(f'Precedence already specified for terminal {term!r}')
		if assoc not in ['left', 'right', 'nonassoc']:
			raise GrammarError(f"Associativity of {term!r} must be one of 'left','right', or 'nonassoc'")
		self.Precedence[term] = (assoc, level)

	# -----------------------------------------------------------------------------
	# add_production()
	#
	# Given an action function, this function assembles a production rule and
	# computes its precedence level.
	#
	# The production rule is supplied as a list of symbols.   For example,
	# a rule such as 'expr : expr PLUS term' has a production name of 'expr' and
	# symbols ['expr','PLUS','term'].
	#
	# Precedence is determined by the precedence of the right-most non-terminal
	# or the precedence of a terminal specified by %prec.
	#
	# A variety of error checks are performed to make sure production symbols
	# are valid and that %prec is used correctly.
	# -----------------------------------------------------------------------------

	def add_production(self, prodname, syms, func=None, file='', line=0):

		if prodname in self.Terminals:
			raise GrammarError(f'{file}:{line}: Illegal rule name {prodname!r}. Already defined as a token')
		if prodname == 'error':
			raise GrammarError(f'{file}:{line}: Illegal rule name {prodname!r}. error is a reserved word')

		# Look for literal tokens
		for n, s in enumerate(syms):
			if s[0] in "'\"" and s[0] == s[-1]:
				c = s[1:-1]
				if (len(c) != 1):
					raise GrammarError(f'{file}:{line}: Literal token {s} in rule {prodname!r} may only be a single character')
				if c not in self.Terminals:
					self.Terminals[c] = []
				syms[n] = c
				continue

		# Determine the precedence level
		if '%prec' in syms:
			if syms[-1] == '%prec':
				raise GrammarError(f'{file}:{line}: Syntax error. Nothing follows %%prec')
			if syms[-2] != '%prec':
				raise GrammarError(f'{file}:{line}: Syntax error. %prec can only appear at the end of a grammar rule')
			precname = syms[-1]
			prodprec = self.Precedence.get(precname)
			if not prodprec:
				raise GrammarError(f'{file}:{line}: Nothing known about the precedence of {precname!r}')
			else:
				self.UsedPrecedence.add(precname)
			del syms[-2:]	 # Drop %prec from the rule
		else:
			# If no %prec, precedence is determined by the rightmost terminal symbol
			precname = rightmost_terminal(syms, self.Terminals)
			prodprec = self.Precedence.get(precname, ('right', 0))

		# See if the rule is already in the rulemap
		map = '%s -> %s' % (prodname, syms)
		if map in self.Prodmap:
			m = self.Prodmap[map]
			raise GrammarError(f'{file}:{line}: Duplicate rule {m}. ' +
							   f'Previous definition at {m.file}:{m.line}')

		# From this point on, everything is valid.  Create a new Production instance
		pnumber  = len(self.Productions)
		if prodname not in self.Nonterminals:
			self.Nonterminals[prodname] = []

		# Add the production number to Terminals and Nonterminals
		for t in syms:
			if t in self.Terminals:
				self.Terminals[t].append(pnumber)
			else:
				if t not in self.Nonterminals:
					self.Nonterminals[t] = []
				self.Nonterminals[t].append(pnumber)

		# Create a production and add it to the list of productions
		p = Production(pnumber, prodname, syms, prodprec, func, file, line)
		self.Productions.append(p)
		self.Prodmap[map] = p

		# Add to the global productions list
		try:
			self.Prodnames[prodname].append(p)
		except KeyError:
			self.Prodnames[prodname] = [p]

	# -----------------------------------------------------------------------------
	# set_start()
	#
	# Sets the starting symbol and creates the augmented grammar.  Production
	# rule 0 is S' -> start where start is the start symbol.
	# -----------------------------------------------------------------------------

	def set_start(self, start=None):
		if callable(start):
			start = start.__name__

		if not start:
			start = self.Productions[1].name

		if start not in self.Nonterminals:
			raise GrammarError(f'start symbol {start} undefined')
		self.Productions[0] = Production(0, "S'", [start])
		self.Nonterminals[start].append(0)
		self.Start = start

	# -----------------------------------------------------------------------------
	# find_unreachable()
	#
	# Find all of the nonterminal symbols that can't be reached from the starting
	# symbol.  Returns a list of nonterminals that can't be reached.
	# -----------------------------------------------------------------------------

	def find_unreachable(self):

		# Mark all symbols that are reachable from a symbol s
		def mark_reachable_from(s):
			if s in reachable:
				return
			reachable.add(s)
			for p in self.Prodnames.get(s, []):
				for r in p.prod:
					mark_reachable_from(r)

		reachable = set()
		mark_reachable_from(self.Productions[0].prod[0])
		return [s for s in self.Nonterminals if s not in reachable]

	# -----------------------------------------------------------------------------
	# infinite_cycles()
	#
	# This function looks at the various parsing rules and tries to detect
	# infinite recursion cycles (grammar rules where there is no possible way
	# to derive a string of only terminals).
	# -----------------------------------------------------------------------------

	def infinite_cycles(self):
		terminates = {}

		# Terminals:
		for t in self.Terminals:
			terminates[t] = True

		terminates['$end'] = True

		# Nonterminals:

		# Initialize to false:
		for n in self.Nonterminals:
			terminates[n] = False

		# Then propagate termination until no change:
		while True:
			some_change = False
			for (n, pl) in self.Prodnames.items():
				# Nonterminal n terminates iff any of its productions terminates.
				for p in pl:
					# Production p terminates iff all of its rhs symbols terminate.
					for s in p.prod:
						if not terminates[s]:
							# The symbol s does not terminate,
							# so production p does not terminate.
							p_terminates = False
							break
					else:
						# didn't break from the loop,
						# so every symbol s terminates
						# so production p terminates.
						p_terminates = True

					if p_terminates:
						# symbol n terminates!
						if not terminates[n]:
							terminates[n] = True
							some_change = True
						# Don't need to consider any more productions for this n.
						break

			if not some_change:
				break

		infinite = []
		for (s, term) in terminates.items():
			if not term:
				if s not in self.Prodnames and s not in self.Terminals and s != 'error':
					# s is used-but-not-defined, and we've already warned of that,
					# so it would be overkill to say that it's also non-terminating.
					pass
				else:
					infinite.append(s)

		return infinite

	# -----------------------------------------------------------------------------
	# undefined_symbols()
	#
	# Find all symbols that were used the grammar, but not defined as tokens or
	# grammar rules.  Returns a list of tuples (sym, prod) where sym in the symbol
	# and prod is the production where the symbol was used.
	# -----------------------------------------------------------------------------
	def undefined_symbols(self):
		result = []
		for p in self.Productions:
			if not p:
				continue

			for s in p.prod:
				if s not in self.Prodnames and s not in self.Terminals and s != 'error':
					result.append((s, p))
		return result

	# -----------------------------------------------------------------------------
	# unused_terminals()
	#
	# Find all terminals that were defined, but not used by the grammar.  Returns
	# a list of all symbols.
	# -----------------------------------------------------------------------------
	def unused_terminals(self):
		unused_tok = []
		for s, v in self.Terminals.items():
			if s != 'error' and not v:
				unused_tok.append(s)

		return unused_tok

	# ------------------------------------------------------------------------------
	# unused_rules()
	#
	# Find all grammar rules that were defined,  but not used (maybe not reachable)
	# Returns a list of productions.
	# ------------------------------------------------------------------------------

	def unused_rules(self):
		unused_prod = []
		for s, v in self.Nonterminals.items():
			if not v:
				p = self.Prodnames[s][0]
				unused_prod.append(p)
		return unused_prod

	# -----------------------------------------------------------------------------
	# unused_precedence()
	#
	# Returns a list of tuples (term,precedence) corresponding to precedence
	# rules that were never used by the grammar.  term is the name of the terminal
	# on which precedence was applied and precedence is a string such as 'left' or
	# 'right' corresponding to the type of precedence.
	# -----------------------------------------------------------------------------

	def unused_precedence(self):
		unused = []
		for termname in self.Precedence:
			if not (termname in self.Terminals or termname in self.UsedPrecedence):
				unused.append((termname, self.Precedence[termname][0]))

		return unused

	# -------------------------------------------------------------------------
	# _first()
	#
	# Compute the value of FIRST1(beta) where beta is a tuple of symbols.
	#
	# During execution of compute_first1, the result may be incomplete.
	# Afterward (e.g., when called from compute_follow()), it will be complete.
	# -------------------------------------------------------------------------
	def _first(self, beta):

		# We are computing First(x1,x2,x3,...,xn)
		result = []
		for x in beta:
			x_produces_empty = False

			# Add all the non-<empty> symbols of First[x] to the result.
			for f in self.First[x]:
				if f == '<empty>':
					x_produces_empty = True
				else:
					if f not in result:
						result.append(f)

			if x_produces_empty:
				# We have to consider the next x in beta,
				# i.e. stay in the loop.
				pass
			else:
				# We don't have to consider any further symbols in beta.
				break
		else:
			# There was no 'break' from the loop,
			# so x_produces_empty was true for all x in beta,
			# so beta produces empty as well.
			result.append('<empty>')

		return result

	# -------------------------------------------------------------------------
	# compute_first()
	#
	# Compute the value of FIRST1(X) for all symbols
	# -------------------------------------------------------------------------
	def compute_first(self):
		if self.First:
			return self.First

		# Terminals:
		for t in self.Terminals:
			self.First[t] = [t]

		self.First['$end'] = ['$end']

		# Nonterminals:

		# Initialize to the empty set:
		for n in self.Nonterminals:
			self.First[n] = []

		# Then propagate symbols until no change:
		while True:
			some_change = False
			for n in self.Nonterminals:
				for p in self.Prodnames[n]:
					for f in self._first(p.prod):
						if f not in self.First[n]:
							self.First[n].append(f)
							some_change = True
			if not some_change:
				break

		return self.First

	# ---------------------------------------------------------------------
	# compute_follow()
	#
	# Computes all of the follow sets for every non-terminal symbol.  The
	# follow set is the set of all symbols that might follow a given
	# non-terminal.  See the Dragon book, 2nd Ed. p. 189.
	# ---------------------------------------------------------------------
	def compute_follow(self, start=None):
		# If already computed, return the result
		if self.Follow:
			return self.Follow

		# If first sets not computed yet, do that first.
		if not self.First:
			self.compute_first()

		# Add '$end' to the follow list of the start symbol
		for k in self.Nonterminals:
			self.Follow[k] = []

		if not start:
			start = self.Productions[1].name

		self.Follow[start] = ['$end']

		while True:
			didadd = False
			for p in self.Productions[1:]:
				# Here is the production set
				for i, B in enumerate(p.prod):
					if B in self.Nonterminals:
						# Okay. We got a non-terminal in a production
						fst = self._first(p.prod[i+1:])
						hasempty = False
						for f in fst:
							if f != '<empty>' and f not in self.Follow[B]:
								self.Follow[B].append(f)
								didadd = True
							if f == '<empty>':
								hasempty = True
						if hasempty or i == (len(p.prod)-1):
							# Add elements of follow(a) to follow(b)
							for f in self.Follow[p.name]:
								if f not in self.Follow[B]:
									self.Follow[B].append(f)
									didadd = True
			if not didadd:
				break
		return self.Follow


	# -----------------------------------------------------------------------------
	# build_lritems()
	#
	# This function walks the list of productions and builds a complete set of the
	# LR items.  The LR items are stored in two ways:  First, they are uniquely
	# numbered and placed in the list _lritems.  Second, a linked list of LR items
	# is built for each production.  For example:
	#
	#   E -> E PLUS E
	#
	# Creates the list
	#
	#  [E -> . E PLUS E, E -> E . PLUS E, E -> E PLUS . E, E -> E PLUS E . ]
	# -----------------------------------------------------------------------------

	def build_lritems(self):
		for p in self.Productions:
			lastlri = p
			i = 0
			lr_items = []
			while True:
				if i > len(p):
					lri = None
				else:
					lri = LRItem(p, i)
					# Precompute the list of productions immediately following
					try:
						lri.lr_after = self.Prodnames[lri.prod[i+1]]
					except (IndexError, KeyError):
						lri.lr_after = []
					try:
						lri.lr_before = lri.prod[i-1]
					except IndexError:
						lri.lr_before = None

				lastlri.lr_next = lri
				if not lri:
					break
				lr_items.append(lri)
				lastlri = lri
				i += 1
			p.lr_items = lr_items


	# ----------------------------------------------------------------------
	# Debugging output.  Printing the grammar will produce a detailed
	# description along with some diagnostics.
	# ----------------------------------------------------------------------
	def __str__(self):
		out = []
		out.append('Grammar:\n')
		for n, p in enumerate(self.Productions):
			out.append(f'Rule {n:<5d} {p}')
		
		unused_terminals = self.unused_terminals()
		if unused_terminals:
			out.append('\nUnused terminals:\n')
			for term in unused_terminals:
				out.append(f'	{term}')

		out.append('\nTerminals, with rules where they appear:\n')
		for term in sorted(self.Terminals):
			out.append('%-20s : %s' % (term, ' '.join(str(s) for s in self.Terminals[term])))

		out.append('\nNonterminals, with rules where they appear:\n')
		for nonterm in sorted(self.Nonterminals):
			out.append('%-20s : %s' % (nonterm, ' '.join(str(s) for s in self.Nonterminals[nonterm])))

		out.append('')
		return '\n'.join(out)

# -----------------------------------------------------------------------------
#						   === LR Generator ===
#
# The following classes and functions are used to generate LR parsing tables on
# a grammar.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# digraph()
# traverse()
#
# The following two functions are used to compute set valued functions
# of the form:
#
#	 F(x) = F'(x) U U{F(y) | x R y}
#
# This is used to compute the values of Read() sets as well as FOLLOW sets
# in LALR(1) generation.
#
# Inputs:  X	- An input set
#		  R	- A relation
#		  FP   - Set-valued function
# ------------------------------------------------------------------------------

def digraph(X, R, FP):
	N = {}
	for x in X:
		N[x] = 0
	stack = []
	F = {}
	for x in X:
		if N[x] == 0:
			traverse(x, N, stack, F, X, R, FP)
	return F

def traverse(x, N, stack, F, X, R, FP):
	stack.append(x)
	d = len(stack)
	N[x] = d
	F[x] = FP(x)			 # F(X) <- F'(x)

	rel = R(x)			   # Get y's related to x
	for y in rel:
		if N[y] == 0:
			traverse(y, N, stack, F, X, R, FP)
		N[x] = min(N[x], N[y])
		for a in F.get(y, []):
			if a not in F[x]:
				F[x].append(a)
	if N[x] == d:
		N[stack[-1]] = MAXINT
		F[stack[-1]] = F[x]
		element = stack.pop()
		while element != x:
			N[stack[-1]] = MAXINT
			F[stack[-1]] = F[x]
			element = stack.pop()

class LALRError(YaccError):
	pass

# -----------------------------------------------------------------------------
#							 == LRGeneratedTable ==
#
# This class implements the LR table generation algorithm.  There are no
# public methods except for write()
# -----------------------------------------------------------------------------

class LRTable(object):
	def __init__(self, grammar):
		self.grammar = grammar

		# Internal attributes
		self.lr_action	 = {}		# Action table
		self.lr_goto	   = {}		# Goto table
		self.lr_productions  = grammar.Productions	# Copy of grammar Production array
		self.lr_goto_cache = {}		# Cache of computed gotos
		self.lr0_cidhash   = {}		# Cache of closures
		self._add_count	= 0		 # Internal counter used to detect cycles

		# Diagonistic information filled in by the table generator
		self.state_descriptions = OrderedDict()
		self.sr_conflict   = 0
		self.rr_conflict   = 0
		self.conflicts	 = []		# List of conflicts

		self.sr_conflicts  = []
		self.rr_conflicts  = []

		# Build the tables
		self.grammar.build_lritems()
		self.grammar.compute_first()
		self.grammar.compute_follow()
		self.lr_parse_table()

		# Build default states
		# This identifies parser states where there is only one possible reduction action.
		# For such states, the parser can make a choose to make a rule reduction without consuming
		# the next look-ahead token.  This delayed invocation of the tokenizer can be useful in
		# certain kinds of advanced parsing situations where the lexer and parser interact with
		# each other or change states (i.e., manipulation of scope, lexer states, etc.).
		#
		# See:  http://www.gnu.org/software/bison/manual/html_node/Default-Reductions.html#Default-Reductions
		self.defaulted_states = {}
		for state, actions in self.lr_action.items():
			rules = list(actions.values())
			if len(rules) == 1 and rules[0] < 0:
				self.defaulted_states[state] = rules[0]

	# Compute the LR(0) closure operation on I, where I is a set of LR(0) items.
	def lr0_closure(self, I):
		self._add_count += 1

		# Add everything in I to J
		J = I[:]
		didadd = True
		while didadd:
			didadd = False
			for j in J:
				for x in j.lr_after:
					if getattr(x, 'lr0_added', 0) == self._add_count:
						continue
					# Add B --> .G to J
					J.append(x.lr_next)
					x.lr0_added = self._add_count
					didadd = True

		return J

	# Compute the LR(0) goto function goto(I,X) where I is a set
	# of LR(0) items and X is a grammar symbol.   This function is written
	# in a way that guarantees uniqueness of the generated goto sets
	# (i.e. the same goto set will never be returned as two different Python
	# objects).  With uniqueness, we can later do fast set comparisons using
	# id(obj) instead of element-wise comparison.

	def lr0_goto(self, I, x):
		# First we look for a previously cached entry
		g = self.lr_goto_cache.get((id(I), x))
		if g:
			return g

		# Now we generate the goto set in a way that guarantees uniqueness
		# of the result

		s = self.lr_goto_cache.get(x)
		if not s:
			s = {}
			self.lr_goto_cache[x] = s

		gs = []
		for p in I:
			n = p.lr_next
			if n and n.lr_before == x:
				s1 = s.get(id(n))
				if not s1:
					s1 = {}
					s[id(n)] = s1
				gs.append(n)
				s = s1
		g = s.get('$end')
		if not g:
			if gs:
				g = self.lr0_closure(gs)
				s['$end'] = g
			else:
				s['$end'] = gs
		self.lr_goto_cache[(id(I), x)] = g
		return g

	# Compute the LR(0) sets of item function
	def lr0_items(self):
		C = [self.lr0_closure([self.grammar.Productions[0].lr_next])]
		i = 0
		for I in C:
			self.lr0_cidhash[id(I)] = i
			i += 1

		# Loop over the items in C and each grammar symbols
		i = 0
		while i < len(C):
			I = C[i]
			i += 1

			# Collect all of the symbols that could possibly be in the goto(I,X) sets
			asyms = {}
			for ii in I:
				for s in ii.usyms:
					asyms[s] = None

			for x in asyms:
				g = self.lr0_goto(I, x)
				if not g or id(g) in self.lr0_cidhash:
					continue
				self.lr0_cidhash[id(g)] = len(C)
				C.append(g)

		return C

	# -----------------------------------------------------------------------------
	#					   ==== LALR(1) Parsing ====
	#
	# LALR(1) parsing is almost exactly the same as SLR except that instead of
	# relying upon Follow() sets when performing reductions, a more selective
	# lookahead set that incorporates the state of the LR(0) machine is utilized.
	# Thus, we mainly just have to focus on calculating the lookahead sets.
	#
	# The method used here is due to DeRemer and Pennelo (1982).
	#
	# DeRemer, F. L., and T. J. Pennelo: "Efficient Computation of LALR(1)
	#	 Lookahead Sets", ACM Transactions on Programming Languages and Systems,
	#	 Vol. 4, No. 4, Oct. 1982, pp. 615-649
	#
	# Further details can also be found in:
	#
	#  J. Tremblay and P. Sorenson, "The Theory and Practice of Compiler Writing",
	#	  McGraw-Hill Book Company, (1985).
	#
	# -----------------------------------------------------------------------------

	# -----------------------------------------------------------------------------
	# compute_nullable_nonterminals()
	#
	# Creates a dictionary containing all of the non-terminals that might produce
	# an empty production.
	# -----------------------------------------------------------------------------

	def compute_nullable_nonterminals(self):
		nullable = set()
		num_nullable = 0
		while True:
			for p in self.grammar.Productions[1:]:
				if p.len == 0:
					nullable.add(p.name)
					continue
				for t in p.prod:
					if t not in nullable:
						break
				else:
					nullable.add(p.name)
			if len(nullable) == num_nullable:
				break
			num_nullable = len(nullable)
		return nullable

	# -----------------------------------------------------------------------------
	# find_nonterminal_trans(C)
	#
	# Given a set of LR(0) items, this functions finds all of the non-terminal
	# transitions.	These are transitions in which a dot appears immediately before
	# a non-terminal.   Returns a list of tuples of the form (state,N) where state
	# is the state number and N is the nonterminal symbol.
	#
	# The input C is the set of LR(0) items.
	# -----------------------------------------------------------------------------

	def find_nonterminal_transitions(self, C):
		trans = []
		for stateno, state in enumerate(C):
			for p in state:
				if p.lr_index < p.len - 1:
					t = (stateno, p.prod[p.lr_index+1])
					if t[1] in self.grammar.Nonterminals:
						if t not in trans:
							trans.append(t)
		return trans

	# -----------------------------------------------------------------------------
	# dr_relation()
	#
	# Computes the DR(p,A) relationships for non-terminal transitions.  The input
	# is a tuple (state,N) where state is a number and N is a nonterminal symbol.
	#
	# Returns a list of terminals.
	# -----------------------------------------------------------------------------

	def dr_relation(self, C, trans, nullable):
		dr_set = {}
		state, N = trans
		terms = []

		g = self.lr0_goto(C[state], N)
		for p in g:
			if p.lr_index < p.len - 1:
				a = p.prod[p.lr_index+1]
				if a in self.grammar.Terminals:
					if a not in terms:
						terms.append(a)

		# This extra bit is to handle the start state
		if state == 0 and N == self.grammar.Productions[0].prod[0]:
			terms.append('$end')

		return terms

	# -----------------------------------------------------------------------------
	# reads_relation()
	#
	# Computes the READS() relation (p,A) READS (t,C).
	# -----------------------------------------------------------------------------

	def reads_relation(self, C, trans, empty):
		# Look for empty transitions
		rel = []
		state, N = trans

		g = self.lr0_goto(C[state], N)
		j = self.lr0_cidhash.get(id(g), -1)
		for p in g:
			if p.lr_index < p.len - 1:
				a = p.prod[p.lr_index + 1]
				if a in empty:
					rel.append((j, a))

		return rel

	# -----------------------------------------------------------------------------
	# compute_lookback_includes()
	#
	# Determines the lookback and includes relations
	#
	# LOOKBACK:
	#
	# This relation is determined by running the LR(0) state machine forward.
	# For example, starting with a production "N : . A B C", we run it forward
	# to obtain "N : A B C ."   We then build a relationship between this final
	# state and the starting state.   These relationships are stored in a dictionary
	# lookdict.
	#
	# INCLUDES:
	#
	# Computes the INCLUDE() relation (p,A) INCLUDES (p',B).
	#
	# This relation is used to determine non-terminal transitions that occur
	# inside of other non-terminal transition states.   (p,A) INCLUDES (p', B)
	# if the following holds:
	#
	#	   B -> LAT, where T -> epsilon and p' -L-> p
	#
	# L is essentially a prefix (which may be empty), T is a suffix that must be
	# able to derive an empty string.  State p' must lead to state p with the string L.
	#
	# -----------------------------------------------------------------------------

	def compute_lookback_includes(self, C, trans, nullable):
		lookdict = {}		  # Dictionary of lookback relations
		includedict = {}	   # Dictionary of include relations

		# Make a dictionary of non-terminal transitions
		dtrans = {}
		for t in trans:
			dtrans[t] = 1

		# Loop over all transitions and compute lookbacks and includes
		for state, N in trans:
			lookb = []
			includes = []
			for p in C[state]:
				if p.name != N:
					continue

				# Okay, we have a name match.  We now follow the production all the way
				# through the state machine until we get the . on the right hand side

				lr_index = p.lr_index
				j = state
				while lr_index < p.len - 1:
					lr_index = lr_index + 1
					t = p.prod[lr_index]

					# Check to see if this symbol and state are a non-terminal transition
					if (j, t) in dtrans:
						# Yes.  Okay, there is some chance that this is an includes relation
						# the only way to know for certain is whether the rest of the
						# production derives empty

						li = lr_index + 1
						while li < p.len:
							if p.prod[li] in self.grammar.Terminals:
								break	  # No forget it
							if p.prod[li] not in nullable:
								break
							li = li + 1
						else:
							# Appears to be a relation between (j,t) and (state,N)
							includes.append((j, t))

					g = self.lr0_goto(C[j], t)			   # Go to next set
					j = self.lr0_cidhash.get(id(g), -1)	  # Go to next state

				# When we get here, j is the final state, now we have to locate the production
				for r in C[j]:
					if r.name != p.name:
						continue
					if r.len != p.len:
						continue
					i = 0
					# This look is comparing a production ". A B C" with "A B C ."
					while i < r.lr_index:
						if r.prod[i] != p.prod[i+1]:
							break
						i = i + 1
					else:
						lookb.append((j, r))
			for i in includes:
				if i not in includedict:
					includedict[i] = []
				includedict[i].append((state, N))
			lookdict[(state, N)] = lookb

		return lookdict, includedict

	# -----------------------------------------------------------------------------
	# compute_read_sets()
	#
	# Given a set of LR(0) items, this function computes the read sets.
	#
	# Inputs:  C		=  Set of LR(0) items
	#		  ntrans   = Set of nonterminal transitions
	#		  nullable = Set of empty transitions
	#
	# Returns a set containing the read sets
	# -----------------------------------------------------------------------------

	def compute_read_sets(self, C, ntrans, nullable):
		FP = lambda x: self.dr_relation(C, x, nullable)
		R =  lambda x: self.reads_relation(C, x, nullable)
		F = digraph(ntrans, R, FP)
		return F

	# -----------------------------------------------------------------------------
	# compute_follow_sets()
	#
	# Given a set of LR(0) items, a set of non-terminal transitions, a readset,
	# and an include set, this function computes the follow sets
	#
	# Follow(p,A) = Read(p,A) U U {Follow(p',B) | (p,A) INCLUDES (p',B)}
	#
	# Inputs:
	#			ntrans	 = Set of nonterminal transitions
	#			readsets   = Readset (previously computed)
	#			inclsets   = Include sets (previously computed)
	#
	# Returns a set containing the follow sets
	# -----------------------------------------------------------------------------

	def compute_follow_sets(self, ntrans, readsets, inclsets):
		FP = lambda x: readsets[x]
		R  = lambda x: inclsets.get(x, [])
		F = digraph(ntrans, R, FP)
		return F

	# -----------------------------------------------------------------------------
	# add_lookaheads()
	#
	# Attaches the lookahead symbols to grammar rules.
	#
	# Inputs:	lookbacks		 -  Set of lookback relations
	#			followset		 -  Computed follow set
	#
	# This function directly attaches the lookaheads to productions contained
	# in the lookbacks set
	# -----------------------------------------------------------------------------

	def add_lookaheads(self, lookbacks, followset):
		for trans, lb in lookbacks.items():
			# Loop over productions in lookback
			for state, p in lb:
				if state not in p.lookaheads:
					p.lookaheads[state] = []
				f = followset.get(trans, [])
				for a in f:
					if a not in p.lookaheads[state]:
						p.lookaheads[state].append(a)

	# -----------------------------------------------------------------------------
	# add_lalr_lookaheads()
	#
	# This function does all of the work of adding lookahead information for use
	# with LALR parsing
	# -----------------------------------------------------------------------------

	def add_lalr_lookaheads(self, C):
		# Determine all of the nullable nonterminals
		nullable = self.compute_nullable_nonterminals()

		# Find all non-terminal transitions
		trans = self.find_nonterminal_transitions(C)

		# Compute read sets
		readsets = self.compute_read_sets(C, trans, nullable)

		# Compute lookback/includes relations
		lookd, included = self.compute_lookback_includes(C, trans, nullable)

		# Compute LALR FOLLOW sets
		followsets = self.compute_follow_sets(trans, readsets, included)

		# Add all of the lookaheads
		self.add_lookaheads(lookd, followsets)

	# -----------------------------------------------------------------------------
	# lr_parse_table()
	#
	# This function constructs the final LALR parse table.  Touch this code and die.
	# -----------------------------------------------------------------------------
	def lr_parse_table(self):
		Productions = self.grammar.Productions
		Precedence  = self.grammar.Precedence
		goto   = self.lr_goto		 # Goto array
		action = self.lr_action	   # Action array

		actionp = {}				  # Action production array (temporary)

		# Step 1: Construct C = { I0, I1, ... IN}, collection of LR(0) items
		# This determines the number of states

		C = self.lr0_items()
		self.add_lalr_lookaheads(C)

		# Build the parser table, state by state
		for st, I in enumerate(C):
			descrip = []
			# Loop over each production in I
			actlist = []			  # List of actions
			st_action  = {}
			st_actionp = {}
			st_goto	= {}

			descrip.append(f'\nstate {st}\n')
			for p in I:
				descrip.append(f'	({p.number}) {p}')

			for p in I:
					if p.len == p.lr_index + 1:
						if p.name == "S'":
							# Start symbol. Accept!
							st_action['$end'] = 0
							st_actionp['$end'] = p
						else:
							# We are at the end of a production.  Reduce!
							laheads = p.lookaheads[st]
							for a in laheads:
								actlist.append((a, p, f'reduce using rule {p.number} ({p})'))
								r = st_action.get(a)
								if r is not None:
									# Have a shift/reduce or reduce/reduce conflict
									if r > 0:
										# Need to decide on shift or reduce here
										# By default we favor shifting. Need to add
										# some precedence rules here.

										# Shift precedence comes from the token
										sprec, slevel = Precedence.get(a, ('right', 0))

										# Reduce precedence comes from rule being reduced (p)
										rprec, rlevel = Productions[p.number].prec

										if (slevel < rlevel) or ((slevel == rlevel) and (rprec == 'left')):
											# We really need to reduce here.
											st_action[a] = -p.number
											st_actionp[a] = p
											if not slevel and not rlevel:
												descrip.append(f'  ! shift/reduce conflict for {a} resolved as reduce')
												self.sr_conflicts.append((st, a, 'reduce'))
											Productions[p.number].reduced += 1
										elif (slevel == rlevel) and (rprec == 'nonassoc'):
											st_action[a] = None
										else:
											# Hmmm. Guess we'll keep the shift
											if not rlevel:
												descrip.append(f'  ! shift/reduce conflict for {a} resolved as shift')
												self.sr_conflicts.append((st, a, 'shift'))
									elif r <= 0:
										# Reduce/reduce conflict.   In this case, we favor the rule
										# that was defined first in the grammar file
										oldp = Productions[-r]
										pp = Productions[p.number]
										if oldp.line > pp.line:
											st_action[a] = -p.number
											st_actionp[a] = p
											chosenp, rejectp = pp, oldp
											Productions[p.number].reduced += 1
											Productions[oldp.number].reduced -= 1
										else:
											chosenp, rejectp = oldp, pp
										self.rr_conflicts.append((st, chosenp, rejectp))
										descrip.append('  ! reduce/reduce conflict for %s resolved using rule %d (%s)' % 
													   (a, st_actionp[a].number, st_actionp[a]))
									else:
										raise LALRError(f'Unknown conflict in state {st}')
								else:
									st_action[a] = -p.number
									st_actionp[a] = p
									Productions[p.number].reduced += 1
					else:
						i = p.lr_index
						a = p.prod[i+1]	   # Get symbol right after the "."
						if a in self.grammar.Terminals:
							g = self.lr0_goto(I, a)
							j = self.lr0_cidhash.get(id(g), -1)
							if j >= 0:
								# We are in a shift state
								actlist.append((a, p, f'shift and go to state {j}'))
								r = st_action.get(a)
								if r is not None:
									# Whoa have a shift/reduce or shift/shift conflict
									if r > 0:
										if r != j:
											raise LALRError(f'Shift/shift conflict in state {st}')
									elif r <= 0:
										# Do a precedence check.
										#   -  if precedence of reduce rule is higher, we reduce.
										#   -  if precedence of reduce is same and left assoc, we reduce.
										#   -  otherwise we shift
										rprec, rlevel = Productions[st_actionp[a].number].prec
										sprec, slevel = Precedence.get(a, ('right', 0))
										if (slevel > rlevel) or ((slevel == rlevel) and (rprec == 'right')):
											# We decide to shift here... highest precedence to shift
											Productions[st_actionp[a].number].reduced -= 1
											st_action[a] = j
											st_actionp[a] = p
											if not rlevel:
												descrip.append(f'  ! shift/reduce conflict for {a} resolved as shift')
												self.sr_conflicts.append((st, a, 'shift'))
										elif (slevel == rlevel) and (rprec == 'nonassoc'):
											st_action[a] = None
										else:
											# Hmmm. Guess we'll keep the reduce
											if not slevel and not rlevel:
												descrip.append(f'  ! shift/reduce conflict for {a} resolved as reduce')
												self.sr_conflicts.append((st, a, 'reduce'))

									else:
										raise LALRError(f'Unknown conflict in state {st}')
								else:
									st_action[a] = j
									st_actionp[a] = p

			# Print the actions associated with each terminal
			_actprint = {}
			for a, p, m in actlist:
				if a in st_action:
					if p is st_actionp[a]:
						descrip.append(f'	{a:<15s} {m}')
						_actprint[(a, m)] = 1
			descrip.append('')

			# Construct the goto table for this state
			nkeys = {}
			for ii in I:
				for s in ii.usyms:
					if s in self.grammar.Nonterminals:
						nkeys[s] = None
			for n in nkeys:
				g = self.lr0_goto(I, n)
				j = self.lr0_cidhash.get(id(g), -1)
				if j >= 0:
					st_goto[n] = j
					descrip.append(f'	{n:<30s} shift and go to state {j}')

			action[st] = st_action
			actionp[st] = st_actionp
			goto[st] = st_goto
			self.state_descriptions[st] = '\n'.join(descrip)

	# ----------------------------------------------------------------------
	# Debugging output.   Printing the LRTable object will produce a listing
	# of all of the states, conflicts, and other details.
	# ----------------------------------------------------------------------
	def __str__(self):
		out = []
		for descrip in self.state_descriptions.values():
			out.append(descrip)
			
		if self.sr_conflicts or self.rr_conflicts:
			out.append('\nConflicts:\n')

			for state, tok, resolution in self.sr_conflicts:
				out.append(f'shift/reduce conflict for {tok} in state {state} resolved as {resolution}')

			already_reported = set()
			for state, rule, rejected in self.rr_conflicts:
				if (state, id(rule), id(rejected)) in already_reported:
					continue
				out.append(f'reduce/reduce conflict in state {state} resolved using rule {rule}')
				out.append(f'rejected rule ({rejected}) in state {state}')
				already_reported.add((state, id(rule), id(rejected)))

			warned_never = set()
			for state, rule, rejected in self.rr_conflicts:
				if not rejected.reduced and (rejected not in warned_never):
					out.append(f'Rule ({rejected}) is never reduced')
					warned_never.add(rejected)

		return '\n'.join(out)

# Collect grammar rules from a function
def _collect_grammar_rules(func):
	grammar = []
	while func:
		prodname = func.__name__
		unwrapped = inspect.unwrap(func)
		filename = unwrapped.__code__.co_filename
		lineno = unwrapped.__code__.co_firstlineno
		for rule, lineno in zip(func.rules, range(lineno+len(func.rules)-1, 0, -1)):
			syms = rule.split()
			ebnf_prod = []
			while ('{' in syms) or ('[' in syms):
				for s in syms:
					if s == '[':
						syms, prod = _replace_ebnf_optional(syms)
						ebnf_prod.extend(prod)
						break
					elif s == '{':
						syms, prod = _replace_ebnf_repeat(syms)
						ebnf_prod.extend(prod)
						break
					elif '|' in s:
						syms, prod = _replace_ebnf_choice(syms)
						ebnf_prod.extend(prod)
						break

			if syms[1:2] == [':'] or syms[1:2] == ['::=']:
				grammar.append((func, filename, lineno, syms[0], syms[2:]))
			else:
				grammar.append((func, filename, lineno, prodname, syms))
			grammar.extend(ebnf_prod)
			
		func = getattr(func, 'next_func', None)

	return grammar

# Replace EBNF repetition
def _replace_ebnf_repeat(syms):
	syms = list(syms)
	first = syms.index('{')
	end = syms.index('}', first)

	# Look for choices inside
	repeated_syms = syms[first+1:end]
	if any('|' in sym for sym in repeated_syms):
		repeated_syms, prods = _replace_ebnf_choice(repeated_syms)
	else:
		prods = []

	symname, moreprods = _generate_repeat_rules(repeated_syms)
	syms[first:end+1] = [symname]
	return syms, prods + moreprods

def _replace_ebnf_optional(syms):
	syms = list(syms)
	first = syms.index('[')
	end = syms.index(']', first)
	symname, prods = _generate_optional_rules(syms[first+1:end])
	syms[first:end+1] = [symname]
	return syms, prods

def _replace_ebnf_choice(syms):
	syms = list(syms)
	newprods = [ ]
	n = 0
	while n < len(syms):
		if '|' in syms[n]:
			symname, prods = _generate_choice_rules(syms[n].split('|'))
			syms[n] = symname
			newprods.extend(prods)
		n += 1
	return syms, newprods
	
# Generate grammar rules for repeated items
_gencount = 0

# Dictionary mapping name aliases generated by EBNF rules.

_name_aliases = { }

def _sanitize_symbols(symbols):
	for sym in symbols:
		if sym.startswith("'"):
			yield str(hex(ord(sym[1])))
		elif sym.isidentifier():
			yield sym
		else:
			yield sym.encode('utf-8').hex()
			
def _generate_repeat_rules(symbols):
	'''
	Symbols is a list of grammar symbols [ symbols ]. This
	generates code corresponding to these grammar construction:
  
	   @('repeat : many')
	   def repeat(self, p):
		   return p.many

	   @('repeat :')
	   def repeat(self, p):
		   return []

	   @('many : many symbols')
	   def many(self, p):
		   p.many.append(symbols)
		   return p.many

	   @('many : symbols')
	   def many(self, p):
		   return [ p.symbols ]
	'''
	global _gencount
	_gencount += 1
	basename = f'_{_gencount}_' + '_'.join(_sanitize_symbols(symbols))
	name = f'{basename}_repeat'
	oname = f'{basename}_items'
	iname = f'{basename}_item'
	symtext = ' '.join(symbols)

	_name_aliases[name] = symbols

	productions = [ ]
	_ = _decorator

	@_(f'{name} : {oname}')
	def repeat(self, p):
		return getattr(p, oname)

	@_(f'{name} : ')
	def repeat2(self, p):
		return []
	productions.extend(_collect_grammar_rules(repeat))
	productions.extend(_collect_grammar_rules(repeat2))

	@_(f'{oname} : {oname} {iname}')
	def many(self, p):
		items = getattr(p, oname)
		items.append(getattr(p, iname))
		return items

	@_(f'{oname} : {iname}')
	def many2(self, p):
		return [ getattr(p, iname) ]

	productions.extend(_collect_grammar_rules(many))
	productions.extend(_collect_grammar_rules(many2))

	@_(f'{iname} : {symtext}')
	def item(self, p):
		return tuple(p)

	productions.extend(_collect_grammar_rules(item))
	return name, productions

def _generate_optional_rules(symbols):
	'''
	Symbols is a list of grammar symbols [ symbols ]. This
	generates code corresponding to these grammar construction:
  
	   @('optional : symbols')
	   def optional(self, p):
		   return p.symbols

	   @('optional :')
	   def optional(self, p):
		   return None
	'''
	global _gencount
	_gencount += 1
	basename = f'_{_gencount}_' + '_'.join(_sanitize_symbols(symbols))
	name = f'{basename}_optional'
	symtext = ' '.join(symbols)
	
	_name_aliases[name] = symbols

	productions = [ ]
	_ = _decorator

	no_values = (None,) * len(symbols)

	@_(f'{name} : {symtext}')
	def optional(self, p):
		return tuple(p)

	@_(f'{name} : ')
	def optional2(self, p):
		return no_values

	productions.extend(_collect_grammar_rules(optional))
	productions.extend(_collect_grammar_rules(optional2))
	return name, productions

def _generate_choice_rules(symbols):
	'''
	Symbols is a list of grammar symbols such as [ 'PLUS', 'MINUS' ].
	This generates code corresponding to the following construction:
	
	@('PLUS', 'MINUS')
	def choice(self, p):
		return p[0]
	'''
	global _gencount
	_gencount += 1
	basename = f'_{_gencount}_' + '_'.join(_sanitize_symbols(symbols))
	name = f'{basename}_choice'

	_ = _decorator
	productions = [ ]


	def choice(self, p):
		return p[0]
	choice.__name__ = name
	choice = _(*symbols)(choice)
	productions.extend(_collect_grammar_rules(choice))
	return name, productions
	
class ParserMetaDict(dict):
	'''
	Dictionary that allows decorated grammar rule functions to be overloaded
	'''
	def __setitem__(self, key, value):
		if key in self and callable(value) and hasattr(value, 'rules'):
			value.next_func = self[key]
			if not hasattr(value.next_func, 'rules'):
				raise GrammarError(f'Redefinition of {key}. Perhaps an earlier {key} is missing @_')
		super().__setitem__(key, value)
	
	def __getitem__(self, key):
		if key not in self and key.isupper() and key[:1] != '_':
			return key.upper()
		else:
			return super().__getitem__(key)

def _decorator(rule, *extra):
	rules = [rule, *extra]
	def decorate(func):
		func.rules = [ *getattr(func, 'rules', []), *rules[::-1] ]
		return func
	return decorate

class ParserMeta(type):
	@classmethod
	def __prepare__(meta, *args, **kwargs):
		d = ParserMetaDict()
		d['_'] = _decorator
		return d

	def __new__(meta, clsname, bases, attributes):
		del attributes['_']
		cls = super().__new__(meta, clsname, bases, attributes)
		cls._build(list(attributes.items()))
		return cls

class Parser(metaclass=ParserMeta):
	# Automatic tracking of position information
	track_positions = True

	# Debugging filename where parsetab.out data can be written
	debugfile = None

	@classmethod
	def __validate_tokens(cls):
		if not hasattr(cls, 'tokens'):
			logging.error('No token list is defined')
			return False

		if not cls.tokens:
			logging.error('tokens is empty')
			return False

		if 'error' in cls.tokens:
			logging.error("Illegal token name 'error'. Is a reserved word")
			return False

		return True

	@classmethod
	def __validate_precedence(cls):
		if not hasattr(cls, 'precedence'):
			cls.__preclist = []
			return True

		preclist = []
		if not isinstance(cls.precedence, (list, tuple)):
			logging.error('precedence must be a list or tuple')
			return False

		for level, p in enumerate(cls.precedence, start=1):
			if not isinstance(p, (list, tuple)):
				logging.error(f'Bad precedence table entry {p!r}. Must be a list or tuple')
				return False

			if len(p) < 2:
				logging.error(f'Malformed precedence entry {p!r}. Must be (assoc, term, ..., term)')
				return False

			if not all(isinstance(term, str) for term in p):
				logging.error('precedence items must be strings')
				return False
			
			assoc = p[0]
			preclist.extend((term, assoc, level) for term in p[1:])

		cls.__preclist = preclist
		return True

	@classmethod
	def __validate_specification(cls):
		'''
		Validate various parts of the grammar specification
		'''
		if not cls.__validate_tokens():
			return False
		if not cls.__validate_precedence():
			return False
		return True

	@classmethod
	def __build_grammar(cls, rules):
		'''
		Build the grammar from the grammar rules
		'''
		grammar_rules = []
		errors = ''
		# Check for non-empty symbols
		if not rules:
			raise YaccError('No grammar rules are defined')

		grammar = Grammar(cls.tokens)

		# Set the precedence level for terminals
		for term, assoc, level in cls.__preclist:
			try:
				grammar.set_precedence(term, assoc, level)
			except GrammarError as e:
				errors += f'{e}\n'

		for name, func in rules:
			try:
				parsed_rule = _collect_grammar_rules(func)
				for pfunc, rulefile, ruleline, prodname, syms in parsed_rule:
					try:
						grammar.add_production(prodname, syms, pfunc, rulefile, ruleline)
					except GrammarError as e:
						errors += f'{e}\n'
			except SyntaxError as e:
				errors += f'{e}\n'
		try:
			grammar.set_start(getattr(cls, 'start', None))
		except GrammarError as e:
			errors += f'{e}\n'

		undefined_symbols = grammar.undefined_symbols()
		for sym, prod in undefined_symbols:
			errors += '%s:%d: Symbol %r used, but not defined as a token or a rule\n' % (prod.file, prod.line, sym)

		unused_terminals = grammar.unused_terminals()
		if unused_terminals:
			unused_str = '{' + ','.join(unused_terminals) + '}'
			logging.warning(f'Token{"(s)" if len(unused_terminals) >1 else ""} {unused_str} defined, but not used')

		unused_rules = grammar.unused_rules()
		for prod in unused_rules:
			logging.warning('%s:%d: Rule %r defined, but not used', prod.file, prod.line, prod.name)

		if len(unused_terminals) == 1:
			logging.warning('There is 1 unused token')
		if len(unused_terminals) > 1:
			logging.warning('There are %d unused tokens', len(unused_terminals))

		if len(unused_rules) == 1:
			logging.warning('There is 1 unused rule')
		if len(unused_rules) > 1:
			logging.warning('There are %d unused rules', len(unused_rules))

		unreachable = grammar.find_unreachable()
		for u in unreachable:
			logging.warning('Symbol %r is unreachable', u)

		if len(undefined_symbols) == 0:
			infinite = grammar.infinite_cycles()
			for inf in infinite:
				errors += 'Infinite recursion detected for symbol %r\n' % inf

		unused_prec = grammar.unused_precedence()
		for term, assoc in unused_prec:
			errors += 'Precedence rule %r defined for unknown symbol %r\n' % (assoc, term)

		cls._grammar = grammar
		if errors:
			raise YaccError('Unable to build grammar.\n'+errors)

	@classmethod
	def __build_lrtables(cls):
		'''
		Build the LR Parsing tables from the grammar
		'''
		lrtable = LRTable(cls._grammar)
		num_sr = len(lrtable.sr_conflicts)

		# Report shift/reduce and reduce/reduce conflicts
		if num_sr != getattr(cls, 'expected_shift_reduce', None):
			if num_sr == 1:
				logging.warning('1 shift/reduce conflict')
			elif num_sr > 1:
				logging.warning('%d shift/reduce conflicts', num_sr)

		num_rr = len(lrtable.rr_conflicts)
		if num_rr != getattr(cls, 'expected_reduce_reduce', None):
			if num_rr == 1:
				logging.warning('1 reduce/reduce conflict')
			elif num_rr > 1:
				logging.warning('%d reduce/reduce conflicts', num_rr)

		cls._lrtable = lrtable
		return True

	@classmethod
	def __collect_rules(cls, definitions):
		'''
		Collect all of the tagged grammar rules
		'''
		rules = [ (name, value) for name, value in definitions
				  if callable(value) and hasattr(value, 'rules') ]
		return rules

	# ----------------------------------------------------------------------
	# Build the LALR(1) tables. definitions is a list of (name, item) tuples
	# of all definitions provided in the class, listed in the order in which
	# they were defined.  This method is triggered by a metaclass.
	# ----------------------------------------------------------------------
	@classmethod
	def _build(cls, definitions):
		if vars(cls).get('_build', False):
			return

		# Collect all of the grammar rules from the class definition
		rules = cls.__collect_rules(definitions)

		# Validate other parts of the grammar specification
		if not cls.__validate_specification():
			raise YaccError('Invalid parser specification')

		# Build the underlying grammar object
		# Always build the grammar fresh.
		cls.__build_grammar(rules)

		# Build the LR tables
		lrtableFile = Path(__file__).resolve().parent.joinpath(f"{cls.__qualname__.lower()}.lrtable")
		try:
			with open(lrtableFile, 'r') as f:
					cls._lrtable = jsonpickle.decode(f.read(), keys=True)
		except:
			if not cls.__build_lrtables():
				raise YaccError('Can\'t build parsing tables')
			with open(lrtableFile, 'w+') as f:
					f.write(jsonpickle.encode(cls._lrtable, keys=True))

		if cls.debugfile:
			with open(cls.debugfile, 'w') as f:
				f.write(str(cls._grammar))
				f.write('\n')
				f.write(str(cls._lrtable))
			logging.info('Parser debugging for %s written to %s', cls.__qualname__, cls.debugfile)


	# ----------------------------------------------------------------------
	# Parsing Support.  This is the parsing runtime that users use to
	# ----------------------------------------------------------------------
	def error(self, token):
		'''
		Default error handling function.  This may be subclassed.
		'''
		if token:
			lineno = getattr(token, 'lineno', 0)
			if lineno:
				logging.critical(f'sly: Syntax error at line {lineno}, token={token.type}\n')
			else:
				logging.critical(f'sly: Syntax error, token={token.type}')
		else:
			logging.critical('sly: Parse error in input. EOF\n')
 
	def errok(self):
		'''
		Clear the error status
		'''
		self.errorok = True

	def restart(self):
		'''
		Force the parser to restart from a fresh state. Clears the statestack
		'''
		del self.statestack[:]
		del self.symstack[:]
		sym = YaccSymbol()
		sym.type = '$end'
		self.symstack.append(sym)
		self.statestack.append(0)
		self.state = 0

	def does_current_production_match_symbols(self, symstack):
		if (not self.production.len):
			return True

		# Some tokens are deliberately injected into the symbol stack to help with parsing.
		# TODO: Make this dynamic.
		if (self.production.name == "close_expression"):
			return True

		if (self.production.len > len(symstack)):
			return False
		
		alignment = dict(zip([sym.type for sym in symstack[-self.production.len:]], list(self.production.namemap.keys())))
		logging.debug(f"Checking alignment of {alignment}")
		for sym, name in alignment.items():
			if (not name.startswith(sym)):
				return False
		
		return True

	def parse(self, tokens):
		'''
		Parse the given input tokens.
		'''
		lookahead = None								  # Current lookahead symbol
		lookaheadstack = []							   # Stack of lookahead symbols
		actions = self._lrtable.lr_action				 # Local reference to action table (to avoid lookup on self.)
		goto	= self._lrtable.lr_goto				   # Local reference to goto table (to avoid lookup on self.)
		prod	= self._grammar.Productions			   # Local reference to production list (to avoid lookup on self.)
		defaulted_states = self._lrtable.defaulted_states # Local reference to defaulted states
		pslice  = YaccProduction(None)					# Production object passed to grammar rules
		errorcount = 0									# Used during error recovery

		# Set up the state and symbol stacks
		self.tokens = tokens
		self.statestack = statestack = []				 # Stack of parsing states
		self.symstack = symstack = []					 # Stack of grammar symbols
		pslice._stack = symstack						  # Associate the stack with the production
		self.restart()

		# Set up position tracking
		track_positions = self.track_positions
		if not hasattr(self, '_line_positions'):
			self._line_positions = { }		   # id: -> lineno
			self._index_positions = { }		  # id: -> (start, end)

		errtoken   = None								 # Err token
		while True:
			# Get the next symbol on the input.  If a lookahead symbol
			# is already set, we just use that. Otherwise, we'll pull
			# the next token off of the lookaheadstack or from the lexer
			if self.state not in defaulted_states:
				if not lookahead:
					if not lookaheadstack:
						lookahead = next(tokens, None)  # Get the next token
					else:
						lookahead = lookaheadstack.pop()
					if not lookahead:
						lookahead = YaccSymbol()
						lookahead.type = '$end'
					
				# Check the action table
				ltype = lookahead.type
				t = actions[self.state].get(ltype)
			else:
				t = defaulted_states[self.state]

			logging.debug(f"state {self.state}, token {lookahead.type}, action {t}")
			logging.debug(f"Stack: {symstack}")

			if t is not None:
				if t > 0:
					# shift a symbol on the stack
					statestack.append(t)
					self.state = t

					symstack.append(lookahead)
					lookahead = None

					# Decrease error count on successful shift
					if errorcount:
						errorcount -= 1
					continue

				if t < 0:
					# reduce a symbol on the stack, emit a production
					self.production = prod[-t]
					pname = self.production.name
					plen  = self.production.len

					# The following match logic has been added to account for situations where one production might match multiple different sets of symbols, each of a possibly different size.
					# Usually, we don't need to worry about the symbol stacking matching exactly which production to use, since the functions are all the same.
					# However, if the match is incorrect and uses, say a size larger than the symbol stack or some other erroneous value, we'll crash.
					# So, for added safety, we take the time to make sure we select exactly the right production.
					# TODO: If we ever start adding data to the parsing table, we should add the match length so we can skip this calculation.

					matched = self.does_current_production_match_symbols(symstack)
					if (not matched):
						logging.debug(f"Attempting to correct improper product selection for {pname} in {symstack}")

						offset = 0
						while (not matched):
							offset += 1
							try:
								possibleCorrectMatch = prod[-t-offset]
								if (possibleCorrectMatch.name != pname):
									break

								logging.debug(f"Possible correct match: {possibleCorrectMatch.name} ({possibleCorrectMatch.namemap})")
								self.production = possibleCorrectMatch

								if (self.does_current_production_match_symbols(symstack)):
									logging.debug(f"Correct match found: {possibleCorrectMatch.name} ({possibleCorrectMatch.namemap})")
									plen = possibleCorrectMatch.len
									matched = True
									break

							except:
								break

						if (not matched):
							raise RuntimeError(f"Parse error: {pname} ({p.namemap}) cannot be reduced from {symstack}")

					p = self.production

					pslice._namemap = p.namemap
					pslice._slice = symstack[-plen:] if plen else []

					sym = YaccSymbol()
					sym.type = pname
					value = p.func(self, pslice)
					if value is pslice:
						value = (pname, *(s.value for s in pslice._slice))

					sym.value = value
						
					# Record positions
					if track_positions:
						if plen:
							sym.lineno = symstack[-plen].lineno
							sym.index = symstack[-plen].index
							sym.end = symstack[-1].end
						else:
							# A zero-length production  (what to put here?)
							sym.lineno = None
							sym.index = None
							sym.end = None
						self._line_positions[id(value)] = sym.lineno
						self._index_positions[id(value)] = (sym.index, sym.end)
							
					if plen:
						del symstack[-plen:]
						del statestack[-plen:]

					symstack.append(sym)
					self.state = goto[statestack[-1]][pname]
					statestack.append(self.state)
					continue

				if t == 0:
					n = symstack[-1]
					result = getattr(n, 'value', None)
					return result

			if t is None:
				# We have some kind of parsing error here.  To handle
				# this, we are going to push the current token onto
				# the tokenstack and replace it with an 'error' token.
				# If there are any synchronization rules, they may
				# catch it.
				#
				# In addition to pushing the error token, we call call
				# the user defined error() function if this is the
				# first syntax error.  This function is only called if
				# errorcount == 0.
				if errorcount == 0 or self.errorok:
					errorcount = ERROR_COUNT
					self.errorok = False
					if lookahead.type == '$end':
						errtoken = None			   # End of file!
					else:
						errtoken = lookahead

					tok = self.error(errtoken)
					if tok:
						# User must have done some kind of panic
						# mode recovery on their own.  The
						# returned token is the next lookahead
						lookahead = tok
						self.errorok = True
						continue
					else:
						# If at EOF. We just return. Basically dead.
						if not errtoken:
							return
				else:
					# Reset the error count.  Unsuccessful token shifted
					errorcount = ERROR_COUNT

				# case 1:  the statestack only has 1 entry on it.  If we're in this state, the
				# entire parse has been rolled back and we're completely hosed.   The token is
				# discarded and we just keep going.

				if len(statestack) <= 1 and lookahead.type != '$end':
					lookahead = None
					self.state = 0
					# Nuke the lookahead stack
					del lookaheadstack[:]
					continue

				# case 2: the statestack has a couple of entries on it, but we're
				# at the end of the file. nuke the top entry and generate an error token

				# Start nuking entries on the stack
				if lookahead.type == '$end':
					# Whoa. We're really hosed here. Bail out
					return

				if lookahead.type != 'error':
					sym = symstack[-1]
					if sym.type == 'error':
						# Hmmm. Error is on top of stack, we'll just nuke input
						# symbol and continue
						lookahead = None
						continue

					# Create the error symbol for the first time and make it the new lookahead symbol
					t = YaccSymbol()
					t.type = 'error'

					if hasattr(lookahead, 'lineno'):
						t.lineno = lookahead.lineno
					if hasattr(lookahead, 'index'):
						t.index = lookahead.index
					if hasattr(lookahead, 'end'):
						t.end = lookahead.end
					t.value = lookahead
					lookaheadstack.append(lookahead)
					lookahead = t
				else:
					sym = symstack.pop()
					statestack.pop()
					self.state = statestack[-1]
				continue

			# Call an error function here
			raise RuntimeError('sly: internal parser error!!!\n')

	# Return position tracking information
	def line_position(self, value):
		return self._line_positions[id(value)]

	def index_position(self, value):
		return self._index_positions[id(value)]
	

class ElderLexer(Lexer):
	def error(this, t):
		logging.critical(f"Illegal character {t.value[0]!r} at index {this.index}")
		this.index += 1

	tokens = { UNFORMATTEDSTRING, FORMATTEDSTRING, OPEN_EXECUTION, OPEN_PARAMETER, OPEN_CONTAINER, OPEN_KIND, CLOSE_EXECUTION, CLOSE_PARAMETER, CLOSE_CONTAINER, CLOSE_EXPRESSION, DIVISIONASSIGNMENT, THIS, EPIDEFOPTION2, EPIDEFOPTION1, GLOBALSCOPE, EXPLICITACCESS, SEQUENCE, EOL, SHORTTYPE, CALLER, NAME, NUMBER }

	ignore = ' \t'

	ignore_blockcomment = r'(/\*)[\s\S]*?(\*/)\s*'
	ignore_linecomment = r'(#|//)(?:(?!:\n).)+\s*'

	UNFORMATTEDSTRING = r'((\')[\s\S]*?([^\\]\'))'
	FORMATTEDSTRING = r'((")[\s\S]*?([^\\]")|(`)[\s\S]*?([^\\]`))'
	DIVISIONASSIGNMENT = r'(/=)'
	NUMBER = r'\d+'
	SHORTTYPE = r'(:=)'
	OPEN_KIND = r'(:)'
	OPEN_EXECUTION = r'\s*({)\s*'
	OPEN_PARAMETER = r'\s*(\()\s*'
	OPEN_CONTAINER = r'\s*(\[)\s*'
	CLOSE_EXECUTION = r'\s*(})'
	CLOSE_PARAMETER = r'\s*(\))'
	CLOSE_CONTAINER = r'\s*(\])'
	CLOSE_EXPRESSION = r'(;|,)'
	THIS = r'(\./)'
	EPIDEFOPTION2 = r'(\.\./)'
	EPIDEFOPTION1 = r'(\.\.)'
	GLOBALSCOPE = r'(~/)'
	EXPLICITACCESS = r'(\.)'
	SEQUENCE = r'(/)'
	CALLER = r'(@)'
	EOL = r'([\n\r\s]+)'
	NAME = r'(?:(?!\\|{|}|\(|\)|\[|\]|:|/\*|\*/|#|//|\'|"|`|;|,|/=|\./|\.\./|\.\.|~/|\.|/|[\n\r\s]+|:=|@)\S)+'

	CLOSE_EXECUTION[''] = ['CLOSE_EXPRESSION', 'CLOSE_EXECUTION']
	CLOSE_PARAMETER[''] = ['CLOSE_EXPRESSION', 'CLOSE_PARAMETER']
	CLOSE_CONTAINER[''] = ['CLOSE_EXPRESSION', 'CLOSE_CONTAINER']


class ElderParser(Parser):
	tokens = { UNFORMATTEDSTRING, FORMATTEDSTRING, OPEN_EXECUTION, OPEN_PARAMETER, OPEN_CONTAINER, OPEN_KIND, CLOSE_EXECUTION, CLOSE_PARAMETER, CLOSE_CONTAINER, CLOSE_EXPRESSION, DIVISIONASSIGNMENT, THIS, EPIDEFOPTION2, EPIDEFOPTION1, GLOBALSCOPE, EXPLICITACCESS, SEQUENCE, EOL, SHORTTYPE, CALLER, NAME, NUMBER }
	start = 'fullexpressionset'

	precedence = (
		('right', 'AUTOFILLACCESSORINVOKATION_SYNTAX'),
		('right', 'AUTOFILLINVOKATION_SYNTAX'),
		('right', OPEN_EXECUTION, OPEN_PARAMETER, OPEN_CONTAINER, OPEN_KIND, CLOSE_EXECUTION, CLOSE_PARAMETER, CLOSE_CONTAINER),
		('right', 'CALLER_SYNTAX'),
		('right', 'SIMPLETYPEWITHSHORTTYPEASSIGNMENT_SYNTAX'),
		('right', 'SHORTTYPE_SYNTAX'),
		('right', 'COMPLEXSEQUENCE_SYNTAX'),
		('right', 'SEQUENCE_SYNTAX'),
		('right', 'COMPLEXEXPLICITACCESS_SYNTAX'),
		('right', 'EXPLICITACCESS_SYNTAX'),
		('right', 'DIVISIONASSIGNMENTOVERLOAD_SYNTAX'),
		('right', 'DIVISIONOVERLOAD_SYNTAX'),
		('right', 'GLOBALSCOPE_SYNTAX'),
		('right', 'COMPLEXEPIDEF_SYNTAX'),
		('right', 'EPIDEFOPTION1_SYNTAX'),
		('right', 'EPIDEFOPTION2_SYNTAX'),
		('right', 'THIS_SYNTAX'),
		('right', 'COMPLEXDIVISIONASSIGNMENT_SYNTAX'),
		('right', 'DIVISIONASSIGNMENT_SYNTAX'),
		('right', 'CLOSE_EXPRESSION'),
		('right', 'FULLEXPRESSIONSET'),
		('right', 'FULLEXPRESSION'),
		('right', 'EXECUTION'),
		('right', 'PARAMETER'),
		('right', 'CONTAINER'),
		('right', 'KIND'),
		('right', 'LIMITEDEXPRESSIONSET'),
		('right', 'LIMITEDEXPRESSION'),
		('right', 'PROTOEXPRESSIONSET'),
		('right', 'PROTOEXPRESSION'),
		('right', 'SIMPLETYPE'),
		('right', 'CONTAINERACCESS'),
		('right', 'STANDARDINVOKATION'),
		('right', 'ACCESSINVOKATION'),
		('right', 'COMPLEXACCESSINVOKATION'),
		('right', 'INVOKATIONWITHEXECUTION'),
		('right', 'STRUCTTYPE'),
		('right', 'EXECUTIVETYPE'),
		('right', 'INVOKATIONWITHPARAMETERSANDEXECUTION'),
		('right', 'CONTAINERINVOKATION'),
		('right', 'CONTAINERINVOKATIONWITHPARAMETERS'),
		('right', 'FUNCTORTYPE'),
		('right', DIVISIONASSIGNMENT, THIS, EPIDEFOPTION2, EPIDEFOPTION1, GLOBALSCOPE, EXPLICITACCESS, SEQUENCE, SHORTTYPE, CALLER),
		('right', NAME),
		('right', NUMBER),
		('right', 'UNFORMATTEDSTRING'),
		('right', 'FORMATTEDSTRING'),
		('right', 'STRING')
	)

	def __init__(this):
		this.executor = eons.Executor(name="Parser")
		this.executor.parser = this
		this.executor.lexer = ElderLexer()
		this.executor()

	@_(
		'name kind  %prec SIMPLETYPE',
	)
	def simpletype(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("SimpleType", p=p).returned
		logging.info(f"...SimpleType produced {ret}")
		return ret

	@_(
		'name container  %prec CONTAINERACCESS',
	)
	def containeraccess(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ContainerAccess", p=p).returned
		logging.info(f"...ContainerAccess produced {ret}")
		return ret

	@_(
		'name parameter  %prec STANDARDINVOKATION',
	)
	def standardinvokation(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("StandardInvokation", p=p).returned
		logging.info(f"...StandardInvokation produced {ret}")
		return ret

	@_(
		'explicitaccess parameter  %prec ACCESSINVOKATION',
	)
	def accessinvokation(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("AccessInvokation", p=p).returned
		logging.info(f"...AccessInvokation produced {ret}")
		return ret

	@_(
		'complexexplicitaccess parameter  %prec COMPLEXACCESSINVOKATION',
	)
	def complexaccessinvokation(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ComplexAccessInvokation", p=p).returned
		logging.info(f"...ComplexAccessInvokation produced {ret}")
		return ret

	@_(
		'name execution  %prec INVOKATIONWITHEXECUTION',
	)
	def invokationwithexecution(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("InvokationWithExecution", p=p).returned
		logging.info(f"...InvokationWithExecution produced {ret}")
		return ret

	@_(
		'simpletype parameter  %prec STRUCTTYPE',
		'name kind parameter  %prec STRUCTTYPE',
	)
	def structtype(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("StructType", p=p).returned
		logging.info(f"...StructType produced {ret}")
		return ret

	@_(
		'simpletype execution  %prec EXECUTIVETYPE',
		'name kind execution  %prec EXECUTIVETYPE',
	)
	def executivetype(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ExecutiveType", p=p).returned
		logging.info(f"...ExecutiveType produced {ret}")
		return ret

	@_(
		'name parameter execution  %prec INVOKATIONWITHPARAMETERSANDEXECUTION',
		'standardinvokation execution  %prec INVOKATIONWITHPARAMETERSANDEXECUTION',
	)
	def invokationwithparametersandexecution(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("InvokationWithParametersAndExecution", p=p).returned
		logging.info(f"...InvokationWithParametersAndExecution produced {ret}")
		return ret

	@_(
		'containeraccess execution  %prec CONTAINERINVOKATION',
		'name container execution  %prec CONTAINERINVOKATION',
	)
	def containerinvokation(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ContainerInvokation", p=p).returned
		logging.info(f"...ContainerInvokation produced {ret}")
		return ret

	@_(
		'standardinvokation container execution  %prec CONTAINERINVOKATIONWITHPARAMETERS',
		'name parameter container execution  %prec CONTAINERINVOKATIONWITHPARAMETERS',
	)
	def containerinvokationwithparameters(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ContainerInvokationWithParameters", p=p).returned
		logging.info(f"...ContainerInvokationWithParameters produced {ret}")
		return ret

	@_(
		'completefullexpression %prec FULLEXPRESSIONSET',
		'fullexpressionset completefullexpression %prec FULLEXPRESSIONSET',
	)
	def fullexpressionset(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("FullExpressionSet", p=p).returned
		logging.info(f"...FullExpressionSet produced {ret}")
		return ret

	@_(
		'limitedexpression %prec FULLEXPRESSION',
		'limitedexpressionset %prec FULLEXPRESSION',
		'kind %prec FULLEXPRESSION',
		'functortype %prec FULLEXPRESSION',
		'structtype %prec FULLEXPRESSION',
		'executivetype %prec FULLEXPRESSION',
		'simpletype %prec FULLEXPRESSION',
		'standardinvokation %prec FULLEXPRESSION',
		'accessinvokation %prec FULLEXPRESSION',
		'complexaccessinvokation %prec FULLEXPRESSION',
		'invokationwithparametersandexecution %prec FULLEXPRESSION',
		'containerinvokationwithparameters %prec FULLEXPRESSION',
		'simpletypewithshorttypeassignment %prec FULLEXPRESSION',
		'complexsequence %prec FULLEXPRESSION',
		'divisionoverload %prec FULLEXPRESSION',
		'complexdivisionassignment %prec FULLEXPRESSION',
		'divisionassignmentoverload %prec FULLEXPRESSION',
		'complexexplicitaccess %prec FULLEXPRESSION',
	)
	def fullexpression(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("FullExpression", p=p).returned
		logging.info(f"...FullExpression produced {ret}")
		return ret

	@_(
		'name kind parameter execution  %prec FUNCTORTYPE',
		'structtype execution  %prec FUNCTORTYPE',
	)
	def functortype(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("FunctorType", p=p).returned
		logging.info(f"...FunctorType produced {ret}")
		return ret

	@_(
		'open_execution fullexpressionset close_execution %prec EXECUTION',
		'open_execution close_execution %prec EXECUTION',
		'open_execution fullexpression close_execution %prec EXECUTION',
	)
	def execution(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("Execution", p=p).returned
		logging.info(f"...Execution produced {ret}")
		return ret

	@_(
		'OPEN_EXECUTION %prec OPEN_EXECUTION',
	)
	def open_execution(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...OPEN_EXECUTION produced {ret}")
		return ret

	@_(
		'CLOSE_EXECUTION %prec CLOSE_EXECUTION',
	)
	def close_execution(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...CLOSE_EXECUTION produced {ret}")
		return ret

	@_(
		'open_parameter fullexpressionset close_parameter %prec PARAMETER',
		'open_parameter close_parameter %prec PARAMETER',
		'open_parameter fullexpression close_parameter %prec PARAMETER',
	)
	def parameter(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("Parameter", p=p).returned
		logging.info(f"...Parameter produced {ret}")
		return ret

	@_(
		'OPEN_PARAMETER %prec OPEN_PARAMETER',
	)
	def open_parameter(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...OPEN_PARAMETER produced {ret}")
		return ret

	@_(
		'CLOSE_PARAMETER %prec CLOSE_PARAMETER',
	)
	def close_parameter(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...CLOSE_PARAMETER produced {ret}")
		return ret

	@_(
		'open_container fullexpressionset close_container %prec CONTAINER',
		'open_container close_container %prec CONTAINER',
		'open_container fullexpression close_container %prec CONTAINER',
	)
	def container(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("Container", p=p).returned
		logging.info(f"...Container produced {ret}")
		return ret

	@_(
		'OPEN_CONTAINER %prec OPEN_CONTAINER',
	)
	def open_container(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...OPEN_CONTAINER produced {ret}")
		return ret

	@_(
		'CLOSE_CONTAINER %prec CLOSE_CONTAINER',
	)
	def close_container(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...CLOSE_CONTAINER produced {ret}")
		return ret

	@_(
		'open_kind limitedexpression %prec KIND',
		'open_kind limitedexpression close_expression %prec KIND',
		'open_kind limitedexpression open_kind %prec KIND',
		'open_kind open_kind %prec KIND',
		'open_kind %prec KIND',
		'kind open_kind %prec KIND',
		'OPEN_KIND limitedexpression %prec KIND',
		'OPEN_KIND limitedexpression close_expression %prec KIND',
		'OPEN_KIND limitedexpression OPEN_KIND %prec KIND',
		'OPEN_KIND OPEN_KIND %prec KIND',
	)
	def kind(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("Kind", p=p).returned
		logging.info(f"...Kind produced {ret}")
		return ret

	@_(
		'OPEN_KIND %prec OPEN_KIND',
	)
	def open_kind(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...OPEN_KIND produced {ret}")
		return ret

	@_(
		'UNFORMATTEDSTRING %prec UNFORMATTEDSTRING',
	)
	def unformattedstring(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("UnformattedString", p=p).returned
		logging.info(f"...UnformattedString produced {ret}")
		return ret

	@_(
		'FORMATTEDSTRING %prec FORMATTEDSTRING',
	)
	def formattedstring(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("FormattedString", p=p).returned
		logging.info(f"...FormattedString produced {ret}")
		return ret

	@_(
		'unformattedstring %prec STRING',
		'formattedstring %prec STRING',
	)
	def string(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("String", p=p).returned
		logging.info(f"...String produced {ret}")
		return ret

	@_(
		'name DIVISIONASSIGNMENT name %prec DIVISIONASSIGNMENT_SYNTAX',
	)
	def divisionassignment(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("DivisionAssignment", p=p).returned
		logging.info(f"...DivisionAssignment produced {ret}")
		return ret

	@_(
		'explicitaccess DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'explicitaccess DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexexplicitaccess DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'standardinvokation DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'containeraccess DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'this DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption1 DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'epidefoption2 DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'complexepidef DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'globalscope DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT name %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'caller DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT autofillaccessorinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT standardinvokation %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT explicitaccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT containeraccess %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT this %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT epidefoption1 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT epidefoption2 %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT complexepidef %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT globalscope %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
		'name DIVISIONASSIGNMENT caller %prec COMPLEXDIVISIONASSIGNMENT_SYNTAX',
	)
	def complexdivisionassignment(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ComplexDivisionAssignment", p=p).returned
		logging.info(f"...ComplexDivisionAssignment produced {ret}")
		return ret

	@_(
		'THIS name %prec THIS_SYNTAX',
	)
	def this(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("This", p=p).returned
		logging.info(f"...This produced {ret}")
		return ret

	@_(
		'EPIDEFOPTION2 name %prec EPIDEFOPTION2_SYNTAX',
	)
	def epidefoption2(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("EpidefOption2", p=p).returned
		logging.info(f"...EpidefOption2 produced {ret}")
		return ret

	@_(
		'EPIDEFOPTION1 name %prec EPIDEFOPTION1_SYNTAX',
	)
	def epidefoption1(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("EpidefOption1", p=p).returned
		logging.info(f"...EpidefOption1 produced {ret}")
		return ret

	@_(
		'EPIDEFOPTION2 epidefoption1 %prec COMPLEXEPIDEF_SYNTAX',
		'EPIDEFOPTION2 epidefoption2 %prec COMPLEXEPIDEF_SYNTAX',
		'EPIDEFOPTION2 complexepidef %prec COMPLEXEPIDEF_SYNTAX',
	)
	def complexepidef(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ComplexEpidef", p=p).returned
		logging.info(f"...ComplexEpidef produced {ret}")
		return ret

	@_(
		'GLOBALSCOPE name %prec GLOBALSCOPE_SYNTAX',
	)
	def globalscope(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("GlobalScope", p=p).returned
		logging.info(f"...GlobalScope produced {ret}")
		return ret

	@_(
		'SEQUENCE kind %prec DIVISIONOVERLOAD_SYNTAX',
		'SEQUENCE kind execution %prec DIVISIONOVERLOAD_SYNTAX',
		'SEQUENCE kind parameter execution %prec DIVISIONOVERLOAD_SYNTAX',
	)
	def divisionoverload(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("DivisionOverload", p=p).returned
		logging.info(f"...DivisionOverload produced {ret}")
		return ret

	@_(
		'DIVISIONASSIGNMENT kind %prec DIVISIONASSIGNMENTOVERLOAD_SYNTAX',
		'DIVISIONASSIGNMENT kind execution %prec DIVISIONASSIGNMENTOVERLOAD_SYNTAX',
		'DIVISIONASSIGNMENT kind parameter execution %prec DIVISIONASSIGNMENTOVERLOAD_SYNTAX',
	)
	def divisionassignmentoverload(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("DivisionAssignmentOverload", p=p).returned
		logging.info(f"...DivisionAssignmentOverload produced {ret}")
		return ret

	@_(
		'name EXPLICITACCESS name %prec EXPLICITACCESS_SYNTAX',
	)
	def explicitaccess(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ExplicitAccess", p=p).returned
		logging.info(f"...ExplicitAccess produced {ret}")
		return ret

	@_(
		'explicitaccess EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'explicitaccess EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'explicitaccess EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'standardinvokation EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'standardinvokation EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'standardinvokation EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'containeraccess EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'containeraccess EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'containeraccess EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'this EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'this EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'this EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'epidefoption1 EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'epidefoption1 EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'epidefoption1 EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'epidefoption2 EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'epidefoption2 EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'epidefoption2 EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'complexepidef EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'complexepidef EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'complexepidef EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'globalscope EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'globalscope EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'globalscope EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'caller EXPLICITACCESS name %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'caller EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'caller EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'name EXPLICITACCESS standardinvokation %prec COMPLEXEXPLICITACCESS_SYNTAX',
		'name EXPLICITACCESS containeraccess %prec COMPLEXEXPLICITACCESS_SYNTAX',
	)
	def complexexplicitaccess(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ComplexExplicitAccess", p=p).returned
		logging.info(f"...ComplexExplicitAccess produced {ret}")
		return ret

	@_(
		'completelimitedexpression %prec LIMITEDEXPRESSIONSET',
		'limitedexpressionset completelimitedexpression %prec LIMITEDEXPRESSIONSET',
	)
	def limitedexpressionset(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("LimitedExpressionSet", p=p).returned
		logging.info(f"...LimitedExpressionSet produced {ret}")
		return ret

	@_(
		'protoexpression %prec LIMITEDEXPRESSION',
		'protoexpressionset %prec LIMITEDEXPRESSION',
		'invokationwithexecution %prec LIMITEDEXPRESSION',
		'containeraccess %prec LIMITEDEXPRESSION',
		'containerinvokation %prec LIMITEDEXPRESSION',
	)
	def limitedexpression(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("LimitedExpression", p=p).returned
		logging.info(f"...LimitedExpression produced {ret}")
		return ret

	@_(
		'completeprotoexpression %prec PROTOEXPRESSIONSET',
		'protoexpressionset completeprotoexpression %prec PROTOEXPRESSIONSET',
	)
	def protoexpressionset(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ProtoExpressionSet", p=p).returned
		logging.info(f"...ProtoExpressionSet produced {ret}")
		return ret

	@_(
		'name %prec PROTOEXPRESSION',
		'number %prec PROTOEXPRESSION',
		'string %prec PROTOEXPRESSION',
		'autofillaccessorinvokation %prec PROTOEXPRESSION',
		'autofillinvokation %prec PROTOEXPRESSION',
		'sequence %prec PROTOEXPRESSION',
		'divisionassignment %prec PROTOEXPRESSION',
		'this %prec PROTOEXPRESSION',
		'explicitaccess %prec PROTOEXPRESSION',
		'epidefoption1 %prec PROTOEXPRESSION',
		'epidefoption2 %prec PROTOEXPRESSION',
		'complexepidef %prec PROTOEXPRESSION',
		'globalscope %prec PROTOEXPRESSION',
	)
	def protoexpression(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ProtoExpression", p=p).returned
		logging.info(f"...ProtoExpression produced {ret}")
		return ret

	@_(
		'name SEQUENCE name %prec SEQUENCE_SYNTAX',
	)
	def sequence(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("Sequence", p=p).returned
		logging.info(f"...Sequence produced {ret}")
		return ret

	@_(
		'sequence SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'sequence SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'standardinvokation SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'containeraccess SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'explicitaccess SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'complexexplicitaccess SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'this SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption1 SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'epidefoption2 SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'complexepidef SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'globalscope SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE name %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'caller SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE standardinvokation %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE containeraccess %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE explicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE complexexplicitaccess %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE this %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE epidefoption1 %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE epidefoption2 %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE complexepidef %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE globalscope %prec COMPLEXSEQUENCE_SYNTAX',
		'name SEQUENCE caller %prec COMPLEXSEQUENCE_SYNTAX',
	)
	def complexsequence(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ComplexSequence", p=p).returned
		logging.info(f"...ComplexSequence produced {ret}")
		return ret

	@_(
		'name name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'name caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'number name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'string name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'simpletype name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation name %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation sequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation complexsequence %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation explicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation complexexplicitaccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation standardinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation accessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation complexaccessinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation containeraccess %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation this %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation epidefoption1 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation epidefoption2 %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation complexepidef %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation globalscope %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'autofillaccessorinvokation caller %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'sequence autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexsequence autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'explicitaccess autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexexplicitaccess autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'standardinvokation autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'accessinvokation autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexaccessinvokation autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'containeraccess autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'this autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption1 autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'epidefoption2 autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'complexepidef autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'globalscope autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'caller autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'number autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'string autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
		'simpletype autofillaccessorinvokation %prec AUTOFILLACCESSORINVOKATION_SYNTAX',
	)
	def autofillaccessorinvokation(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("AutofillAccessOrInvokation", p=p).returned
		logging.info(f"...AutofillAccessOrInvokation produced {ret}")
		return ret

	@_(
		'name number %prec AUTOFILLINVOKATION_SYNTAX',
		'name string %prec AUTOFILLINVOKATION_SYNTAX',
		'containeraccess number %prec AUTOFILLINVOKATION_SYNTAX',
		'containeraccess string %prec AUTOFILLINVOKATION_SYNTAX',
		'standardinvokation number %prec AUTOFILLINVOKATION_SYNTAX',
		'standardinvokation string %prec AUTOFILLINVOKATION_SYNTAX',
		'accessinvokation number %prec AUTOFILLINVOKATION_SYNTAX',
		'accessinvokation string %prec AUTOFILLINVOKATION_SYNTAX',
		'complexaccessinvokation number %prec AUTOFILLINVOKATION_SYNTAX',
		'complexaccessinvokation string %prec AUTOFILLINVOKATION_SYNTAX',
		'explicitaccess number %prec AUTOFILLINVOKATION_SYNTAX',
		'explicitaccess string %prec AUTOFILLINVOKATION_SYNTAX',
		'complexexplicitaccess number %prec AUTOFILLINVOKATION_SYNTAX',
		'complexexplicitaccess string %prec AUTOFILLINVOKATION_SYNTAX',
		'sequence number %prec AUTOFILLINVOKATION_SYNTAX',
		'sequence string %prec AUTOFILLINVOKATION_SYNTAX',
		'complexsequence number %prec AUTOFILLINVOKATION_SYNTAX',
		'complexsequence string %prec AUTOFILLINVOKATION_SYNTAX',
		'this number %prec AUTOFILLINVOKATION_SYNTAX',
		'this string %prec AUTOFILLINVOKATION_SYNTAX',
		'epidefoption1 number %prec AUTOFILLINVOKATION_SYNTAX',
		'epidefoption1 string %prec AUTOFILLINVOKATION_SYNTAX',
		'epidefoption2 number %prec AUTOFILLINVOKATION_SYNTAX',
		'epidefoption2 string %prec AUTOFILLINVOKATION_SYNTAX',
		'complexepidef number %prec AUTOFILLINVOKATION_SYNTAX',
		'complexepidef string %prec AUTOFILLINVOKATION_SYNTAX',
		'globalscope number %prec AUTOFILLINVOKATION_SYNTAX',
		'globalscope string %prec AUTOFILLINVOKATION_SYNTAX',
		'caller number %prec AUTOFILLINVOKATION_SYNTAX',
		'caller string %prec AUTOFILLINVOKATION_SYNTAX',
		'autofillaccessorinvokation number %prec AUTOFILLINVOKATION_SYNTAX',
		'autofillaccessorinvokation string %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype number %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype string %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype sequence %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype container %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype containeraccess %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype standardinvokation %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype accessinvokation %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype complexaccessinvokation %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype explicitaccess %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype complexexplicitaccess %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype this %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype epidefoption1 %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype epidefoption2 %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype complexepidef %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype globalscope %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype caller %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype autofillaccessorinvokation %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype simpletype %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype structtype %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype executivetype %prec AUTOFILLINVOKATION_SYNTAX',
		'shorttype functortype %prec AUTOFILLINVOKATION_SYNTAX',
	)
	def autofillinvokation(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("AutofillInvokation", p=p).returned
		logging.info(f"...AutofillInvokation produced {ret}")
		return ret

	@_(
		'name SHORTTYPE %prec SHORTTYPE_SYNTAX',
	)
	def shorttype(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("ShortType", p=p).returned
		logging.info(f"...ShortType produced {ret}")
		return ret

	@_(
		'name OPEN_KIND limitedexpression SHORTTYPE %prec SIMPLETYPEWITHSHORTTYPEASSIGNMENT_SYNTAX',
	)
	def simpletypewithshorttypeassignment(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("SimpleTypeWithShortTypeAssignment", p=p).returned
		logging.info(f"...SimpleTypeWithShortTypeAssignment produced {ret}")
		return ret

	@_(
		'CALLER name %prec CALLER_SYNTAX',
	)
	def caller(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = this.executor.Execute("Caller", p=p).returned
		logging.info(f"...Caller produced {ret}")
		return ret

	@_(
		'fullexpression close_expression %prec FULLEXPRESSION',
		'close_expression %prec FULLEXPRESSION',
	)
	def completefullexpression(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = p[0]
		logging.info(f"...completefullexpression produced {ret}")
		return ret

	@_(
		'limitedexpression close_expression %prec LIMITEDEXPRESSION',
	)
	def completelimitedexpression(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = p[0]
		logging.info(f"...completelimitedexpression produced {ret}")
		return ret

	@_(
		'protoexpression close_expression %prec PROTOEXPRESSION',
	)
	def completeprotoexpression(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = p[0]
		logging.info(f"...completeprotoexpression produced {ret}")
		return ret

	@_(
		'EOL %prec CLOSE_EXPRESSION',
		'CLOSE_EXPRESSION %prec CLOSE_EXPRESSION',
		'close_expression CLOSE_EXPRESSION %prec CLOSE_EXPRESSION',
		'close_expression EOL %prec CLOSE_EXPRESSION',
	)
	def close_expression(this, p):
		pstr = ''.join([str(p[i]) for i in range(len(p))])
		logging.info(f"Given {pstr}...")
		ret = ''
		logging.info(f"...close_expression produced {ret}")
		return ret

	@_('NAME %prec NAME')
	def name(this, p):
		ret = this.executor.Execute("Name", p=p).returned
		logging.debug(f"Name produced {ret}")
		return ret
	
	@_(
		'NUMBER %prec NUMBER',
		'NUMBER EXPLICITACCESS NUMBER %prec NUMBER',
		'number EXPLICITACCESS NUMBER %prec NUMBER',
	)
	def number(this, p):
		isFloat = False
		try:
			if (p[1] == '.'):
				isFloat = True
		except:
			pass
		if (isFloat):
			return float(f"{p[0]}.{p[2]}")
		return int(p[0])


class Sanitize (eons.Functor):

	keywords = [
		'break',
		'continue',
		'case',
		'default',
		'else',
		'for',
		'if',
		'not',
		'return',
		'switch',
		'while',
		'try',
		'catch',
	]

	keywordInvokations = [
		'break',
		'continue',
	]

	types = [
		'bool',
		'float',
		'int',
		'string',
		'functor',
		'container',
		'pointer',
	]

	symbols = {
		'!': 'not',
		'=': 'eq',
		'&': 'and',
		'|': 'or',
		'>': 'gt',
		'<': 'lt',
		'+': 'plus',
		'-': 'minus',
		'*': 'times',
		'/': 'divide',
		'^': 'pow',
		'%': 'mod',
	}

	allBuiltins = [
		'BREAK',
		'CONTINUE',
		'CASE',
		'DEFAULT',
		'ELSE',
		'FOR',
		'IF',
		'NOT',
		'RETURN',
		'SWITCH',
		'WHILE',
		'TRY',
		'CATCH',
		'BOOL',
		'FLOAT',
		'INT',
		'STRING',
		'FUNCTOR',
		'NOT',
		'EQ',
		'EQEQ',
		'AND',
		'ANDAND',
		'OR',
		'OROR',
		'GT',
		'GTEQ',
		'LT',
		'LTEQ',
		'PLUS',
		'PLUSEQ',
		'MINUS',
		'MINUSEQ',
		'TIMES',
		'TIMESEQ',
		'DIVIDE',
		'DIVIDEEQ',
		'POW',
		'POWEQ'
		'MOD',
		'MODEQ',
	]

	operatorMap = {
		'PLUS': '__add__',
		'MINUS': '__sub__',
		'TIMES': '__mul__',
		'DIVIDE': '__truediv__',
		'MOD': '__mod__',
		'PLUSEQ': '__iadd__',
		'MINUSEQ': '__isub__',
		'TIMESEQ': '__imul__',
		'DIVIDEEQ': '__idiv__',
		'MODEQ': '__imod__',
		'POW': '__pow__',
		'AND': '__and__',
		'OR': '__or__',
		'ANDAND': '__and__',
		'OROR': '__or__',
		'GT': '__gt__',
		'GTEQ': '__ge__',
		'LT': '__lt__',
		'LTEQ': '__le__',
		'EQEQ': '__eq__',
	}

	def __init__(this, name="Sanitize"):
		super().__init__(name)

		this.arg.kw.required.append('input')

		this.arg.mapping.append('input')
		
	def Function(this):
		return this.Clean(this.input)

	def Clean(this, input):
		if (isinstance(input, list)):
			return [this.Clean(item) for item in input]

		for keyword in this.keywords:
			input = re.sub(rf"(\\*['\"])\b{re.escape(keyword)}\b(\\*['\"])", rf"\1{keyword.upper()}\2", input)

		for type in this.types:
			input = re.sub(rf"(\\*)(['\"]*)(\(*)\b{re.escape(type)}\b(\\*)(['\"]*)(\)*)([^=])", rf"\3{type.upper()}\6\7", input)
			# input = re.sub(rf"(\\*)(['\"]*)(\(*)\b{re.escape(type)}\b(\\*)(['\"]*)(\)*)([^=])", rf"\1\2\3{type.upper()}\4\5\6\7", input)

		symbolBorder = rf"[a-zA-Z0-9{''.join([re.escape(sym) for sym in this.symbols.keys()])}]"
		for symbol,replacement in this.symbols.items():
			preBorder = symbolBorder.replace(re.escape(symbol), '')
			def ReplaceSymbol(match):
				prefix, expr, suffix = match.groups()
				ret = f"{prefix}{expr.replace(symbol, replacement.upper())}{suffix}"
				# logging.debug(ret)
				return ret
			toMatch = rf"(\\*['\"])({preBorder}*?{re.escape(symbol)}{symbolBorder}*)(\\*['\"])"
			# logging.debug(toMatch)
			input = re.sub(toMatch, ReplaceSymbol, input)

		for keyword in this.keywordInvokations:
			input = re.sub(rf"(\\*['\"]){keyword.upper()}(\\*['\"])", rf"\1{keyword.upper()}()\2", input)

		return input

	def Soil(this, input):
		if (isinstance(input, list)):
			return [this.Soil(item) for item in input]

		for keyword in this.keywords:
			input = re.sub(rf"\b{keyword.upper()}\b", rf"{keyword.lower()}", input)
		for type in this.types:
			input = re.sub(rf"(\(*)\b{type.upper()}\b(\)*)", rf"\1{type.lower()}\2", input)
		for symbol,replacement in this.symbols.items():
			input = re.sub(rf"(\\*['\"]?){(replacement.upper())}(\\*['\"]?)", rf"{symbol}", input)
		return input

class EldestFunctor (eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.feature.autoReturn = False
		this.feature.track = False

		# New features
		this.feature.cloneOnCall = True
		this.needs = eons.util.DotDict()

		this.fetch.possibilities = [
			'args',
			'this',
			'epidef',
			'stack_name',
			'stack_type',
			'context',
			'history',
			'globals',
			'config', #local (if applicable) or per Executor; should be before 'executor' if using a local config.
			'precursor',
			'caller', # Must be accessed directly.
			'executor',
			'environment',
		]

		this.fetch.use = [
			'args',
			'this',
			'stack_name',
			'context',
			'globals',
		]

		this.context = None

		this.prevent.copying.extend([
			'context',
			'home',
		])


	def __call__(this, *args, **kwargs):
		clone = this
		if (this.feature.cloneOnCall):
			clone = deepcopy(this)
			clone.executor = this.executor
		return super(EldestFunctor, clone).__call__(*args, **kwargs)


	def ValidateArgs(this):
		this.Set('context', this.Fetch('context', None, ['args', 'globals']))
		if (this.context is None and this.executor is not None):
			this.context = this.executor.context
		return super().ValidateArgs()


	def BeforeFunction(this):
		try:
			this.executor.stack.insert(
				0,
				(this.name, this)
			)
			logging.debug(f"Stack is now: {this.executor.stack}")
		except Exception as e:
			logging.error(f"Could not add {this.name} ({type(this)}) to the stack: {e}")

		super().BeforeFunction()


	def AfterFunction(this):
		super().AfterFunction()

		# Failure to remove items from the stack, history, etc. is fine.

		try:
			this.executor.stack.remove(
				(this.name, this)
			)
		except Exception as e:
			logging.debug(f"Could not remove {this.name} ({type(this)}) from the stack: {e}")

		try:
			this.context.history.insert(
				0,
				(this.name, this)
			)
			logging.debug(f"History is now: {this.context.history}")
		except Exception as e:
			logging.debug(f"Could not add {this.name} ({type(this)}) to the history: {e}")


	# NOTE: USE THIS METHOD WITH EXTREME CARE.
	# Because nested classes are defined before the parent, this will always return true from a parent class if it has nested children.
	# Consider checking if currentlyTryingToDefine is set (in globals, per executor).
	def IsCurrentlyInTypeParameterBlock(this, offset=0):
		
		# FIXME: Not having an executor should be an impossibility.
		# This appears to be happening in if.ldr, where the foremost Type() is attempting assignment to bool.
		if (not this.executor):
			return False

		try:
			for name, obj in this.executor.stack[offset:]:
				if (name == 'Autofill'):
					continue
				elif (name == 'eval'):
					continue
				elif (name == 'Within'):
					continue
				# Objs will be provided later, don't worry about where they come from.
				elif (isinstance(obj, Call.__class__)):
					continue
				elif (isinstance(obj, Type.__class__)):
					return True
				else:
					break
		except:
			pass
		return False
	
	def IsCurrentlyInTypeExecutionBlock(this):
		
		# FIXME: Not having an executor should be an impossibility.
		# This appears to be happening in if.ldr, where the foremost Type() is attempting assignment to bool.
		if (not this.executor):
			return False

		name, obj = this.executor.stack[0]
		if (obj == this.context):
			return True

		return False
	

	def CorrectForImproperQuotes(this, string):
		if (re.search(r"\('[a-zA-Z0-9]*\('", string)):
			string = string.replace("('", '("', 1)
			string = string.replace(")', '", ')", "', 1)
			string = re.sub(r"\)'(.*)$", r')"\1', string)
		elif (re.search(r"'[a-zA-Z0-9]*\('", string)):
			string = re.sub(r"'([a-zA-Z0-9]*)\('", r'"\1(\'', string)
			string = re.sub(r"\)'(.*)$", r')"\1', string)
		return string


	def fetch_location_stack_name(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False
		
		
		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False


		if (varName.upper() not in Sanitize.allBuiltins):
			return default, False

		for name, obj in this.executor.stack:
			if (name == varName):
				return obj, True

		return default, False
	
	def fetch_location_stack_type(this, varName, default, fetchFrom, attempted):
		if (this.executor is None):
			return default, False

		if (isinstance(varName, str)):
			try:
				typeToFind = eval(varName)
			except:
				return default, False

		if (inspect.isclass(varName)):
			typeToFind = varName

		# TODO: UnboundLocalError: cannot access local variable 'obj' where it is not associated with a value
		# elif (isinstance(varName, obj)):
		# 	typeToFind = varName.__class__

		if (typeToFind is None or not inspect.isclass(typeToFind)):
			logging.debug(f"Could not find type {varName} in stack.")
			return default, False

		for name, obj in this.executor.stack:
			if (isinstance(obj, typeToFind)):
				return obj, True

		return default, False

	# History should only be used for keywords like ELSE.
	def fetch_location_history(this, varName, default, fetchFrom, attempted):
		if (this.context is None):
			return default, False
		
		for name, obj in this.context.history:
			# Types should be retrieved through eons.SelfRegistering, etc.
			# Fetching a Functor and getting a Type is just rude.
			if (type(obj) is Type.__class__):
				continue

			if (name == varName):
				return obj, True

		return default, False
	

	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.context is None):
			return default, False
		
		return this.context.Fetch(varName, default, start=False, fetchFrom=fetchFrom,attempted=attempted)

class KEYWORD (EldestFunctor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)


class HaltExecution(Exception, metaclass=eons.ActualType): pass

class E___ (KEYWORD):
	def __init__(this, name = eons.INVALID_NAME()):
		super().__init__(name)

		this.arg.kw.optional['shouldAutoType'] = False
		this.arg.kw.optional['unwrapReturn'] = None
		this.arg.kw.optional['currentlyTryingToDefine'] = None
		this.arg.kw.optional['currentlyTryingToInvoke'] = None
		this.arg.kw.optional['shouldAttemptInvokation'] = False

		this.fetch.possibilities.append('current_invokation')

		this.fetch.attr.use = []

		this.fetch.useForFunctorEval = [
			'args', # used in for loops, etc.
			'this',
			'current_invokation',
			'history',
			'context',
			'executor',
			'globals'
		]

		this.prevent.copying.extend([
			'currentlyTryingToInvoke',
		])

		this.HALT = False

	def BeforeFunction(this):
		super().BeforeFunction()
		this.HALT = False

	def Halt(this):
		logging.debug(f"Halting {this.name} ({id(this)}). Will return {this.result.data.returned}.")
		this.HALT = True
		raise HaltExecution(str(id(this)))

	def CorrectReferencesToThis(this, statement):
		if (this.currentlyTryingToInvoke is not None and 'currentlyTryingToInvoke' not in statement):
			# Regex copied from eons.kind
			statement = re.sub(r"this([\s\[\]\.\(\)\}}\*\+/-=%,]|$)", r"this.currentlyTryingToInvoke\1", statement)
		statement = re.sub(r"E____OBJECT", r"this", statement)
		return statement

	def AttemptEvaluationOfFunctor(this, statement):
		# Check if the statement is a Functor name.
		if (not re.search(rf"^{ElderLexer.NAME}$", statement)
			or statement in Sanitize.allBuiltins
		):
			return None, False

		logging.debug(f"It looks like {statement} is a Functor or variable name.")

		possibleFunctor = None
		attemptedFetch = False
		if (this.context is not None):
			possibleFunctor = this.Fetch(statement, fetchFrom=this.fetch.useForFunctorEval)
			attemptedFetch = True

		if (possibleFunctor is None):
			if (this.shouldAutoType):
				logging.debug(f"Autotyping {statement}.")
				ret = eval(f"Type(name = '{statement}', kind = Kind())", globals().update({'currentlyTryingToDefine': this.currentlyTryingToDefine}), {'this': this})
				return ret, True

			possibleFunctorName = statement

			if (this.currentlyTryingToDefine is not None):
				possibleFunctorName = f"{this.currentlyTryingToDefine}_{statement}"
				attemptedFetch = False

			if (not attemptedFetch):
				possibleFunctor = this.Fetch(possibleFunctorName, fetchFrom=this.fetch.useForFunctorEval)

			if (possibleFunctor is None):
				try:
					possibleFunctor = eons.SelfRegistering(possibleFunctorName)
				except:
					try:
						possibleFunctor = this.executor.GetRegistered(possibleFunctorName)
					except:
						try:
							possibleFunctor = sys.modules[possibleFunctorName]
						except:
							pass

		if (possibleFunctor is not None):
			if (isinstance(possibleFunctor, Type.__class__)):
				possibleFunctor = possibleFunctor.product

			if (this.shouldAttemptInvokation 
				and (
					isinstance(possibleFunctor, eons.Functor)
					or isinstance(possibleFunctor, types.MethodType)
					or isinstance(possibleFunctor, types.FunctionType)
				)
			):
				logging.debug(f"Attempting to invoke {statement}.")
				return possibleFunctor(), True
			else:
				return possibleFunctor, True

	def fetch_location_current_invokation(this, varName, default, fetchFrom, attempted):
		try:
			if (this.currentlyTryingToInvoke is None):
				if (this.episcope is None):
					return default, False
				return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
			try:
				return getattr(this.currentlyTryingToInvoke, varName), True
			except:
				if (this.episcope is None):
					return default, False
				return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)
		except:
			return default, False

class EXEC (E___):
	def __init__(this):
		super().__init__(name="exec")

		this.arg.kw.required.append('execution')

		this.arg.kw.optional['shouldAttemptInvokation'] = True
		this.arg.kw.optional['home'] = None
		
		this.arg.mapping.append('execution')

		this.history = []

		this.episcope = None

		this.prevent.copying.extend([
			'episcope',
			'currentlyTryingToInvoke',
		])

	def Function(this):
		if (this.home is not None):
			logging.debug(f"Setting {id(this)} ({this}) as home.")
			this.home.exec = this

		if (type(this.execution) != list):
			this.execution = [this.execution]

		this.episcope = None
		try:
			this.Set('episcope', context) # From globals
		except:
			pass

		this.executor.SetGlobal('context', this)

		this.result.data.execution = []

		failMessage = None
		try:
			for instruction in this.execution:
				logging.debug(instruction)
				instruction = this.CorrectReferencesToThis(instruction)
				evaluatedFunctor, wasFunctor = this.AttemptEvaluationOfFunctor(instruction)
				if (wasFunctor):
					this.result.data.execution.append(evaluatedFunctor)
					continue

				# eval instead of exec to grab result.
				result = eval(instruction, globals().update({'context': this}), {'this': this.currentlyTryingToInvoke, 'currentlyTryingToInvoke': this.currentlyTryingToInvoke})
				if (isinstance(result, types.MethodType)
					or isinstance(result, types.FunctionType)
					or (
						isinstance(result, eons.Functor)
						and not hasattr(result, 'EXEC_NO_EXECUTE')
					)
				):
					result = result()
				this.result.data.execution.append(result)

		except HaltExecution as halt:
			if (str(id(this)) != str(halt)):
				logging.debug(f"Passing on halt: {halt} ({id(this)})")
				raise halt
			logging.debug(f"Caught halt: {halt} ({id(this)})")
			this.PrepareReturn()
			return this.result.data.returned

		except Exception as e:
			failMessage = f"Error in execution of {this.execution}: {e}"
			logging.error(failMessage)
			eons.util.LogStack()

		this.executor.SetGlobal('context', this.episcope)

		if (failMessage is not None):
			raise RuntimeError(failMessage)

		this.PrepareReturn()
		return this.result.data.returned

	# NOTE: my return value should be set by RETURN as this.result.data.returned
	def PrepareReturn(this):
		if (this.result.data.returned is not None):
			return
		if (not len(this.result.data.execution)):
			return
		this.result.data.returned = this.result.data.execution[-1]

	def fetch_location_context(this, varName, default, fetchFrom, attempted):
		if (this.episcope is None):
			return default, False
		
		return this.episcope.Fetch(varName, default, fetchFrom=fetchFrom, start=False, attempted=attempted)


class EVAL (E___):
	def __init__(this):
		super().__init__(name="eval")
		this.arg.kw.required.append('parameter')

		# used by Autofill
		this.arg.kw.optional['NEXTSOURCE'] = None

		this.arg.mapping.append('parameter')

		this.prevent.copying.extend([
			'NEXTSOURCE',
		])

	def Function(this):
		if (this.unwrapReturn is None):
			if (type(this.parameter) != list):
				this.unwrapReturn = True
				this.parameter = [this.parameter]
			if (type(this.parameter) == list and len(this.parameter) == 1):
				this.unwrapReturn = True

		this.result.data.evaluation = []
		
		failMessage = None
		try:
			for statement in this.parameter:

				if (type(statement) in [int, float, bool]):
					this.result.data.evaluation.append(statement)
					continue

				if (statement == 'true' or statement == 'True'):
					this.result.data.evaluation.append(True)
					continue

				if (statement == 'false' or statement == 'False'):
					this.result.data.evaluation.append(False)
					continue

				if (statement == 'null' or statement == 'Null'
					or statement == 'none' or statement == 'None'
					or statement == 'void' or statement == 'Void'
				):
					this.result.data.evaluation.append(None)
					continue

				# Check if the statement is an integer.
				if (re.search(r'^[0-9]+$', statement)):
					this.result.data.evaluation.append(int(statement))
					continue

				# Check if the statement is a float.
				if (re.search(r'^[0-9]+\.[0-9]+$', statement)):
					this.result.data.evaluation.append(float(statement))
					continue

				# Check if the statement is a string.
				# At this point, all strings should be wrapped in single quotes only.
				if ((statement.startswith("'") and statement.endswith("'"))):
					this.result.data.evaluation.append(statement[1:-1])
					continue

				statement = this.CorrectReferencesToThis(statement)

				evaluatedFunctor, wasFunctor = this.AttemptEvaluationOfFunctor(statement)
				if (wasFunctor):
					this.result.data.evaluation.append(evaluatedFunctor)
					continue

				statement = this.CorrectForImproperQuotes(statement)

				logging.debug(f"Evaluating: {statement}")
				evaluation = eval(statement, globals().update({'currentlyTryingToDefine': this.currentlyTryingToDefine}), {'this': this})
				if (isinstance(evaluation, types.MethodType) and this.shouldAttemptInvokation):
					evaluation = evaluation()
				this.result.data.evaluation.append(evaluation)

		except HaltExecution as halt:
			if (str(id(this)) != str(halt)):
				logging.debug(f"Passing on halt: {halt} ({id(this)})")
				raise halt
			this.PrepareReturn()
			logging.debug(f"Caught halt: {halt} ({id(this)})")
			return this.result.data.returned, this.unwrapReturn

		except Exception as e:
			failMessage = f"Error in evaluation of {this.parameter}: {e}"
			logging.error(failMessage)
			eons.util.LogStack()

		if (failMessage is not None):
			raise RuntimeError(failMessage)

		this.PrepareReturn()

		return this.result.data.returned, this.unwrapReturn

	def PrepareReturn(this):
		if (this.result.data.returned is not None):
			return
		
		if (this.unwrapReturn and len(this.result.data.evaluation)):
			this.result.data.returned = this.result.data.evaluation[0]
		else:
			this.result.data.returned = this.result.data.evaluation
# HOME is a singleton that stores the "globals" for elder.
# HOME can be explicitly referenced using the ~/ notation.
class HOME:
	def __init__(this):
		# Singletons man...
		if "instance" not in HOME.__dict__:
			HOME.instance = this
		else:
			return None
		
		this.exec = None

	@staticmethod
	def Instance():
		if "instance" not in HOME.__dict__:
			HOME()
		return HOME.instance

	def __getattr__(this, name):
		try:
			return object.__getattribute__(this, name)
		except:
			try:
				ex = object.__getattribute__(this, 'exec')
				return getattr(ex, name)
			except:
				return None

	def __setattr__(this, name, value):
		try:
			ex = object.__getattribute__(this, 'exec')
			setattr(ex, name, value)
		except:
			object.__setattr__(this, name, value)

class ELDERLANG(eons.Executor):

	def __init__(this, name="Eons Language of Development for Entropic Reduction (ELDER)", descriptionStr="The best programming language"):
		super().__init__(name, descriptionStr)

		this.lexer = ElderLexer()
		this.parser = ElderParser()

		this.stack = []
		this.exceptions = []
		this.context = None

		# For external access (these are pulled from globals, not import)
		this.EXEC = EXEC
		this.EVAL = EVAL
		this.Sanitize = Sanitize()

	# Register included files early so that they can be used by the rest of the system.
	# NOTE: this method needs to be overridden in all children which ship included Functors, Data, etc. This is because __file__ is unique to the eons.py file, not the child's location.
	def RegisterIncludedClasses(this):
		super().RegisterIncludedClasses()

	#Configure class defaults.
	#Override of eons.Executor method. See that class for details
	def Configure(this):
		super().Configure()

	#Override of eons.Executor method. See that class for details
	def AddArgs(this):
		super().AddArgs()
		this.arg.parser.add_argument(type = str, metavar = 'ldr', help = 'the Elderlang script to execute', dest = 'ldr')

	#Override of eons.Executor method. See that class for details
	def Function(this):
		super().Function()
		
		ldrFile = open(this.parsedArgs.ldr, 'r')
		ldr = ldrFile.read()
		ldrFile.close()
		
		# for tok in this.lexer.tokenize(ldr):
		# 	logging.info(tok)
		
		toExec = this.parser.parse(this.lexer.tokenize(ldr))
		toExec = this.Sanitize(toExec).returned
		logging.info(f"Sanitized: {toExec}")
		return EXEC(toExec, executor=this, home=HOME.Instance())
def GetArgs(*args):
	return args

def GetKWArgs(**kwargs):
	return kwargs

supportedBuiltins = [
	"__add__",
	"__sub__",
	"__mul__",
	"__matmul__",
	"__truediv__",
	"__floordiv__",
	"__mod__",
	"__divmod__",
	"__pow__",
	"__lshift__",
	"__rshift__",
	"__and__",
	"__xor__",
	"__or__",
	"__iadd__",
	"__isub__",
	"__imul__",
	"__imatmul__",
	"__itruediv__",
	"__ifloordiv__",
	"__imod__",
	"__ipow__",
	"__ilshift__",
	"__irshift__",
	"__iand__",
	"__ixor__",
	"__ior__",
	"__lt__",
	"__le__",
	# "__eq__", # cursed.
	"__ne__",
	"__gt__",
	"__ge__",
	"__bool__",
	"__str__",
	"__int__",
	"__float__",
	"__len__",
]

class TYPE(EldestFunctor):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.value = value
		this.useValue = True
		this.default = None
		this.needs.typeAssignment = True
		this.feature.cloneOnCall = False
		this.feature.track = True
		this.feature.sequential = False

		this.fetch.attr.use = []

		# Does not work. See ArithmeticFunctor, below.
		# for name in supportedBuiltins:
		# 	setattr(getattr(this, name).__func__, 'epidef', this)
		# 	setattr(this, name, types.MethodType(getattr(this, name), this))

	# This is generally what other types will use. Those that don't can override it.
	def Function(this):
		return this.value
	
	# IMPORTANT: Children should override this.
	# Return whether or not the value in *this should be set.
	def SomehowSet(this, value):
		if (this.useValue):
			this.value = value
			return True
		return False
	
	def IMPL_EQ(this, other):
		this = other

	def EQ(this, other):
		valueSet = False

		if (this.needs.typeAssignment):
			surrogate = None
			if (isinstance(other, bool)):
				surrogate = BOOL()
			elif (isinstance(other, int)):
				surrogate = INT()
			elif (isinstance(other, float)):
				surrogate = FLOAT()
			elif (isinstance(other, str)):
				surrogate = STRING()
			elif (isinstance(other, list)
				or isinstance(other, tuple)
				or isinstance(other, set)
				or isinstance(other, dict)
			):
				surrogate = CONTAINER()
			elif (isinstance(other, eons.Functor)):
				surrogate = POINTER.to(other)

			if (surrogate is not None):
				this.AssignTo(surrogate)

				logging.info(f"Making {this.name} a {surrogate.name} ({surrogate.__class__}) with value {other}")
				this.value = other
				valueSet = True
				this.needs.typeAssignment = False
			else:
				# It's complex, so we'll leave it as a functor.
				this.needs.typeAssignment = False

		if (this.IsCurrentlyInTypeParameterBlock()):
			logging.info(f"Setting default value of {this.name} to {other}")
			this.default = other
			valueSet = True

		if (not valueSet):
			logging.info(f"Setting {this.name} to {other}")
			if (this.useValue):
				this.value = this.PossiblyReduceOther(other)
			else:
				this.IMPL_EQ(other)

		return this

	def GT(this, other):
		return this.PossiblyReduceThis() > this.PossiblyReduceOther(other)

	def LT(this, other):
		return this.PossiblyReduceThis() < this.PossiblyReduceOther(other)

	def EQEQ(this, other):
		return this.PossiblyReduceThis() == this.PossiblyReduceOther(other)
	
	def NOTEQ(this, other):
		return this.PossiblyReduceThis() != this.PossiblyReduceOther(other)

	def GTEQ(this, other):
		return this.PossiblyReduceThis() >= this.PossiblyReduceOther(other)

	def LTEQ(this, other):
		return this.PossiblyReduceThis() <= this.PossiblyReduceOther(other)

	def POW(this, other):
		return pow(this.PossiblyReduceThis(), this.PossiblyReduceOther(other))

	def AND(this, other):
		return this.PossiblyReduceThis() and this.PossiblyReduceOther(other)

	def ANDAND(this, other):
		return this.AND(other)

	def OR(this, other):
		return this.PossiblyReduceThis() or this.PossiblyReduceOther(other)

	def OROR(this, other):
		return this.OR(other)

	def PLUS(this, other):
		return this.PossiblyReduceThis() + this.PossiblyReduceOther(other)

	def MINUS(this, other):
		return this.PossiblyReduceThis() - this.PossiblyReduceOther(other)

	def TIMES(this, other):
		return this.PossiblyReduceThis() * this.PossiblyReduceOther(other)

	def DIVIDE(this, other):
		return this.PossiblyReduceThis() / this.PossiblyReduceOther(other)

	def PLUSEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() + this.PossiblyReduceOther(other))
		return this

	def MINUSEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() - this.PossiblyReduceOther(other))
		return this

	def TIMESEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() * this.PossiblyReduceOther(other))
		return this

	def DIVIDEEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() / this.PossiblyReduceOther(other))
		return this

	def MOD(this, other):
		return this.PossiblyReduceThis() % this.PossiblyReduceOther(other)
	
	def MODEQ(this, other):
		this.SomehowSet(this.PossiblyReduceThis() % this.PossiblyReduceOther(other))
		return this
	
	def size(this):
		return len(this)

	def length(this):
		return this.size()

	def __eq__(this, other):
		reduction = this.PossiblyReduceThis()
		if (id(reduction) == id(this)):
			return super().__eq__(other)
		return reduction == this.PossiblyReduceOther(other)

	def PossiblyReduceOther(this, other):
		ret = other
		while(True):
			try:
				if (isinstance(ret, types.FunctionType) or isinstance(ret, types.MethodType)):
					ret = ret()
				elif (isinstance(ret, POINTER) or (isinstance(ret, TYPE) and ret.useValue)):
					ret = ret.value
				elif (this.useValue and isinstance(ret, eons.Functor)):
					ret = ret()
				else:
					break
			except:
				break
		return ret

	def PossiblyReduceThis(this):
		ret = this
		while (True):
			try:
				if (isinstance(ret, POINTER)): # POINTER cannot be imported, but that's fine. Just assume it exists.
					ret = ret.value
				elif (ret.useValue):
					ret = ret.value
				else:
					break
			except AttributeError:
				break

		return ret

# This approach does not work.
# built in methods are class-based, not object-based, so persisting values like epidef does so at a class level.
#
# class ArithmeticFunctor(eons.Functor):
# 	def __init__(this, name=eons.INVALID_NAME()):
# 		super().__init__(name)

# 		this.feature.autoReturn = False
# 		this.feature.mapArgs = False
# 		this.feature.sequential = False
# 		this.feature.track = False

# 		this.abort.function = False

# 	def PopulatePrecursor(this):
# 		try:
# 			if (inspect.isclass(this.epidef)):
# 				this.epidef = None

# 			if (this.epidef is None):
# 				logging.warning(f"Failed to setup {this.name}.")
# 				if (not inspect.isclass(this.args[0])):
# 					this.epidef = this.args[0]

# 			if (not this.executor):
# 				this.executor = this.epidef.executor
		
# 		except Exception as e:
# 			logging.warning(e)
# 			this.abort.function = True

# 	def Function(this):
# 		if (this.epidef is None):
# 			return this.abort.returnWhenAborting.function

# 		if (not hasattr(this.epidef, 'PossiblyReduceThis')):
# 			logging.warning(f"epidef {this.epidef} lacks PossiblyReduceThis")
# 			return this.abort.returnWhenAborting.function

# 		operateOn = this.epidef.PossiblyReduceThis()
# 		operation = getattr(operateOn, this.name)
# 		if (id(operateOn) == id(this)):
# 			return getattr(this.epidef.parent, this.name)(*this.args[1:])

# 		return operation(*this.args[1:])

# 	# Add disarmed compatibility with eons.Method.
# 	def UpdateSource(this):
# 		return

def CreateArithmeticFunction(functionName):
	# return types.MethodType(ArithmeticFunctor(functionName), TYPE)
	return lambda this, *args: getattr(this.PossiblyReduceThis(), functionName)(*args)

for name in supportedBuiltins:
	# DOES NOT WORK
	# Apparently casts like str() call essentially this.__class__.__str__(this), rather than this.__str__().
	# This makes this approach yield METHOD PENDING POPULATION errors all over the place.
	# eons.PrepareClassMethod(TYPE, name, ArithmeticFunctor(name))

	setattr(TYPE, name, CreateArithmeticFunction(name))

# We only handle error cases for basic type casts atm.
# Operations like len() should always be called on an object, not the class (so should everything else but python is buggy).
# TYPE.__str__.abort.returnWhenAborting.function = 'ERROR: STR CALLED WITHOUT OBJECT'
# TYPE.__int__.abort.returnWhenAborting.function = 0
# TYPE.__float__.abort.returnWhenAborting.function = 0.0
# TYPE.__bool__.abort.returnWhenAborting.function = False


class Autofill (EldestFunctor):
	def __init__(this, name="Autofill"):
		super().__init__(name)

		this.arg.kw.required.append('source')
		this.arg.kw.required.append('target')

		this.arg.mapping.append('source')
		this.arg.mapping.append('target')

	def Function(this):
		source = eons.util.DotDict()
		source.object = this.source
		source.type = 0
		if (type(this.source) == str):
			# Check if we should treat source.object as a Type & perform assignment.
			shouldAutoType = False
			if (type(this.target) == str and this.target == 'EQ' and this.executor is not None):
				for name, object in this.executor.stack:
					if (name == 'Autofill'):
						continue
					if (name == 'eval'):
						continue
					elif (name == 'exec'):
						logging.debug(f"Will attempt to autotype {this.source}.")
						shouldAutoType = True
					break
			source.object, unwrapped = EVAL(this.source, shouldAutoType = shouldAutoType)

		if (isinstance(source.object, types.FunctionType) or isinstance(source.object, types.MethodType)):
			source.type = 1
		elif (type(source.object) in [int, float, str, bool]):
			source.type = 2
		elif (isinstance(source.object, TYPE)):
			source.type = 3
		elif (isinstance(source.object, eons.Functor)):
			source.type = 4

		# elif (inspect.isclass(source.object)):
		# 	source.object = source.object()
		# 	source.type = 2

		target = eons.util.DotDict()
		target.name = None
		target.type = 0
		if (type(this.target) == str):
			if (not '(' in this.target):
				target.name = this.target
				target.type = 1
			elif (
				this.target.startswith('Within')
				or this.target.startswith('Invoke')
			):
				try:
					search = re.search(r'\(name=(.*?),', this.target)
					target.name = search.group(1)
					target.type = 2
				except Exception as e:
					if (this.target.startswith('Invoke')):
						argRetrieval = this.target.replace('Invoke', 'GetKWArgs')
						args = eval(argRetrieval)
						target.name = this.target
						toReplace = args['source']
						toReplace = re.sub(r'\\', r'\\\\', toReplace)
						toReplace = re.sub(r'\'', '\\\'', toReplace)
						toReplace = f"'{toReplace}'"
						newTarget = this.target.replace(toReplace, 'E____OBJECT.NEXTSOURCE')
						nextSource = EVAL([args['source']], unwrapReturn = True,)[0]
						target.object = EVAL([newTarget], unwrapReturn = True, NEXTSOURCE = nextSource)[0]
						target.type = 5
					else:
						raise e
			elif (
				this.target.startswith('Autofill')
				or this.target.startswith('Call')
				or this.target.startswith('Sequence')
				or this.target.startswith('Get')
			):
				search = re.search(r'\((.*?),', this.target)
				target.name = search.group(1)
				target.type = 3

			if (target.name == None or target.type == 0):
				raise RuntimeError(f"Invalid target for autofill on {source.object}: {this.target}")

			if (target.name[0] == target.name[-1] 
				and (
					target.name[0] == '"'
					or target.name[0] == "'"
				)
			):
				target.name = target.name[1:-1]

		else:
			target.name = this.target
			target.type = 4

		logging.debug(f"Target name: {target.name}; target type: {target.type}; source: {source.object} ({type(source.object)}) source type: {source.type}")

		if (target.type == 5):
			return source.object(target.object)

		attemptedAccess = False
		ret = None
		unwrapped = False
		try:
			# If member access works, use that.
			usableSource = eval(f"source.object.{target.name}")
			logging.debug(f"Found {target.name} on {source.object}")
			attemptedAccess = True
			if (target.type == 1):
				ret =  usableSource
			elif (target.type == 2):
				newTarget = re.sub(rf"name=(\\*['\"]?){target.name}(\\*['\"]?)", rf"source=E____OBJECT.NEXTSOURCE", this.target)
				ret, unwrapped =  EVAL(newTarget, NEXTSOURCE = usableSource)
			elif (target.type == 3):
				newTarget = re.sub(rf"(\\*['\"]?){target.name}(\\*['\"]?),", rf"E____OBJECT.NEXTSOURCE,", this.target)
				ret, unwrapped = EVAL(newTarget, NEXTSOURCE = usableSource)

		except Exception as e:
			if (not attemptedAccess):
				logging.debug(f"Could not find {target.name} on {source.object}")

				# Ensure non-functor types can be used with builtin symbols
				# e.g. greeting = 'hello'
				if (source.type == 1):
					if (target.type == 3 and this.target.startswith("Call")):
						source.object = source.object()
						return this.EvaluateCallAfterBasicType(source, target)
					elif (target.type == 4):
						return source.object(this.target)

				elif (source.type == 2):
					if (target.type == 1):
						toEval = f"source.object.{this.target}"
						for match, replace in Sanitize.operatorMap.items():
							toEval = toEval.replace(match, replace)
						logging.debug(f"Attempting to eval: {toEval}")
						return eval(toEval)

					elif (target.type == 2):
						if (this.target.startswith("Invoke") and target.name in Sanitize.operatorMap.keys()):
							try:
								usableSource = source.object.__getattribute__(Sanitize.operatorMap[target.name])
								newTarget = re.sub(rf"name=(\\*['\"]?){target.name}(\\*['\"]?)", rf"source=E____OBJECT.NEXTSOURCE", this.target)
								return EVAL(newTarget, NEXTSOURCE = usableSource)[0]
							except:
								pass

					elif (target.type == 3 and this.target.startswith("Call")):
						return this.EvaluateCallAfterBasicType(source, target)

				# Otherwise, treat the source.object as a function.
				logging.debug(f"Using it as an arg for: {source.object}({this.target})")

				target.object = EVAL(this.target)[0]

				if (target.type == 1 and '.EQ of ' not in str(source.object)):
					if (isinstance(target.object, eons.Functor)
						or isinstance(target.object, types.FunctionType)
						or isinstance(target.object, types.MethodType)
					):
						target.object = target.object()

				ret = source.object(target.object)

			else:
				logging.error(f"Error while attempting to autofill {source.object} with {target.name}: {e}")

		name, object = this.executor.stack[1]
		if ((
				isinstance(ret, eons.Functor)
				or isinstance(ret, types.MethodType)
				or isinstance(ret, types.FunctionType)
			)
			and (
				isinstance(object, EXEC.__class__)
				or isinstance(object, RETURN.__class__) # This may be a bug; it happens when a functor returns without any further action being taken, e.g. if(returns_false()){nop}THIS_AUTOFILL;
			)
		):
			logging.debug(f"It looks like I'm the last statement in this expression. I'll execute {ret}...")
			ret = ret()

		return ret
	
	def EvaluateCallAfterBasicType(this, source, target):
		argRetrieval = this.target.replace('Call', 'GetArgs')
		args = eval(argRetrieval)
		arg0 = this.executor.Sanitize.Soil(args[0])
		arg1 = args[1]
		if (type(source.object) in [str, list]):
			arg1 = f"'{args[1]}'"
		toEval = f"source.object {arg0} {arg1}"
		logging.debug(f"Attempting to eval: {toEval}")
		return eval(toEval)


class SourceTargetFunctor (EldestFunctor):
	def __init__(this, name="Call"):
		super().__init__(name)

		this.nameStack = [name]

		this.needs.source = True
		this.needs.target = True

		this.feature.mapArgs = False

	def BeforeFunction(this):
		if (this.needs.source):
			this.Set('name', f"source_name_{this.Fetch('name', None, ['args'])}")
			possibleSource = this.Fetch('source', None, ['args'])
			if (hasattr(this, 'source') and this.source is not None):
				possibleSource = this.source
			elif (this.name != 'source_name_None'):
				possibleSource = EVAL(this.name[len('source_name_'):])[0]
			else:
				if (len(this.args)):
					possibleSource = this.args[0]
				if (possibleSource is None):
					raise RuntimeError(f"Neither source nor name was provided to {this.nameStack[-1]}")
				elif (isinstance(possibleSource, str)):
					possibleSource = EVAL(possibleSource)[0]

		if (isinstance(possibleSource, Type.__class__)):
			possibleSource = possibleSource.product

		this.Set('source', possibleSource)

		# Not strictly necessary, but useful for keeping the nameStack indices static/
		this.nameStack.append(this.name)

		if (this.needs.target):
			possibleTarget = this.Fetch('target', None, ['args'])

			if (hasattr(this, 'target') and this.target is not None):
				possibleTarget = this.target
			else:
				if (len(this.args) > 1):
					possibleTarget = this.args[1:]
				else:
					raise RuntimeError(f"Target was not provided to {this.nameStack[-2]}")

			if (not isinstance(possibleTarget, list)):
				possibleTarget = [possibleTarget]

			this.Set('target', possibleTarget)

		super().BeforeFunction()

	def AfterFunction(this):
		this.name = this.nameStack.pop()
		super().AfterFunction()


class Call (SourceTargetFunctor):
	def __init__(this, name="Call"):
		super().__init__(name)

	def Function(this):
		return this.source(*this.target)

class Get (SourceTargetFunctor):
	def __init__(this, name="Get"):
		super().__init__(name)

	def Function(this):
		if (isinstance(this.target, list)):
			this.target = this.target[0]
		# elif (isinstance(this.target, str)):
		# 	this.target = EVAL(this.target, unwrapReturn=True)[0]

		source = this.source
		if (isinstance(source, eons.Functor)):
			if (not source.isWarm):
				source.WarmUp()
			try:
				return getattr(source, this.target)
			except AttributeError:
				source = source()
		elif (isinstance(source, types.FunctionType) or isinstance(source, types.MethodType)):
			source = source()

		if (type(source) in [int, float, str, bool] and this.target in Sanitize.operatorMap.keys()):
			return source.__getattribute__(Sanitize.operatorMap[this.target])

		return getattr(source, this.target)


class Invoke (SourceTargetFunctor):
	def __init__(this, name="Invoke"):
		super().__init__(name)

		this.needs.target = False

		this.arg.kw.optional['parameter'] = None
		this.arg.kw.optional['container'] = None
		this.arg.kw.optional['execution'] = None

		this.arg.kw.optional['skipParameterEvaluationFor'] = [
			'WHILE'
		]

		this.feature.mapArgs = False

	def Function(this):
		if (isinstance(this.source, str)):
			this.source = EVAL([this.source], unwrapReturn = True)[0]

		isFunctor = isinstance(this.source, eons.Functor)
		if (isFunctor):
			this.context.currentlyTryingToInvoke = this.source

		shouldEvaluateParameter = True
		if (isFunctor and this.source.name in this.skipParameterEvaluationFor):
			shouldEvaluateParameter = False

		evaluatedParameter = [this.parameter] # should be double nested list

		if (this.parameter is None or not len(this.parameter) or this.parameter == [[]]):
			shouldEvaluateParameter = False
			evaluatedParameter = []

		if (shouldEvaluateParameter):
			evaluatedParameter, unwrapped = EVAL(this.parameter, shouldAttemptInvokation = True)

			if (unwrapped):
				evaluatedParameter = [evaluatedParameter]

		logging.debug(f"Invoking {this.source} with {evaluatedParameter}")

		if (isFunctor):
			return this.source(*evaluatedParameter, container=this.container, execution=this.execution)
		else:
			return this.source(*evaluatedParameter)

class Kind (EldestFunctor):
	def __init__(this, name="Kind"):
		super().__init__(name)

		this.arg.kw.optional['kind'] = None

		this.arg.mapping.append('kind')

	def Function(this):
		if (this.kind is None):
			this.kind = [TYPE]
		elif (isinstance(this.kind, str)):
			this.kind = EVAL([this.kind], unwrapReturn=True)[0]

		if (type(this.kind) != list):
			this.kind = [this.kind]

		# We shouldn't need to actually do anything here.

		return this.kind


class FUNCTOR(TYPE):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.needs.typeAssignment = False
		this.useValue = False
		delattr(this, 'value')
		this.feature.track = True
		this.feature.sequential = True
		this.feature.sequence.clone = True
		this.feature.autoReturn = False

		# TODO: Solidify this behavior.
		# cloneOnCall being True is required to make changes from one call not persist to the next.
		# See the pointer.ldr unit test for an example.
		# FIXME: Making this True induces very strange behavior.
		this.feature.cloneOnCall = False #True

		this.fetch.use = [
			'args',
			'this',
			'precursor',
			'epidef',
			'caller',
			'context',
			'history',
			'globals',
			'executor',
			'config',
			'environment',
		]
		this.fetch.attr.use = [
			'precursor',
			'epidef',
		]

	def ValidateMethods(this):
		super().ValidateMethods()
		for okwarg in this.arg.kw.optional.keys():
			mem = getattr(this, okwarg)
			if (isinstance(mem, FUNCTOR)):
				mem.epidef = this

	def PrepareNext(this, next):
		next.feature.autoReturn = True # <- recommended if you'd like to be able to access the modified sequence result.

	def Function(this):
		pass

	# Restore lost sequence functionality (this method was overridden by TYPE).
	def __truediv__(this, next):
		return eons.Functor.__truediv__(this, next)

	def __str__(this = None):
		if (this is None):
			return 'FUNCTOR'
		return this.name

class Sequence (SourceTargetFunctor):
	def __init__(this, name="Sequence"):
		super().__init__(name)

	def Function(this):

		# FIXME: This is not the right place for this patch. So far as I can tell, next should NEVER be set to None, only emply list.
		if (isinstance(this.source, FUNCTOR) and this.source.next is None):
			this.source.next = []

		if (not this.source.isWarm):
			this.source.WarmUp(executor=this.executor)

		return this.source.__truediv__(EVAL(this.target, unwrapReturn=True, shouldAttemptInvokation=False)[0])


class String (EldestFunctor):
	def __init__(this, name="String"):
		super().__init__(name)

		this.feature.mapArgs = False

	def Function(this):
		template = this.args[0]
		ret = template
		if (len(this.args) > 1):
			arguments = []
			[arguments.append(arg) for lst in this.args[1:] for arg in lst]
			arguments = [EVAL(arg)[0] for arg in arguments]
			toEval = f"""'{template}' % ('{"', '".join([str(arg) for arg in arguments])}')"""
			logging.debug(f"Constructing string from: {toEval}")
			ret = eval (toEval)
		return ret

# Structors are Functors that lack an execution block.
class STRUCTOR(FUNCTOR):
	def __init__(this, name=eons.INVALID_NAME(), value=None):
		super().__init__(name)

		this.feature.autoReturn = True
		this.feature.stayWarm = True


class Type (EldestFunctor):
	def __init__(this, name="Type"):
		super().__init__(name)

		this.arg.kw.required.append('name')
		this.arg.kw.optional['kind'] = [TYPE]

		this.arg.kw.optional['parameter'] = None
		this.arg.kw.optional['execution'] = []


	def BeforeFunction(this):
		this.unsetCurrentlyTryingToDefine = False

		try:
			this.Set('currentlyTryingToDefine', currentlyTryingToDefine) # easy global fetch.
		except:
			this.Set('currentlyTryingToDefine', None)

		if (this.currentlyTryingToDefine):
			this.originalName = this.name
			this.originallyTryingToDefine = this.currentlyTryingToDefine
			this.name = f"{this.currentlyTryingToDefine}_{this.name}"
			this.executor.SetGlobal('currentlyTryingToDefine', this.name)
		else:
			this.executor.SetGlobal('currentlyTryingToDefine', this.name)
			this.unsetCurrentlyTryingToDefine = True

		return super().BeforeFunction()


	def Function(this):
		# alreadyDefined = None
		# try:
		# 	alreadyDefined = EVAL(this.parameter, unwrapReturn=False, shouldAutoType=False, currentlyTryingToDefine=this.name)
		# except:
		# 	pass

		parameters = {
			'constructor': eons.util.DotDict({
				'name': 'constructor',
				'kind': inspect.Parameter.POSITIONAL_OR_KEYWORD,
				'default': f'''
if (this.name is None):
	this.name = '{this.name}'

if ('value' in kwargs):
	this.value = kwargs['value']
	del kwargs['value']
'''
			})
		}
		if (this.parameter is not None):
			parameters = {
				a.name: eons.util.DotDict({
					'name': a.name,
					'kind': inspect.Parameter.POSITIONAL_OR_KEYWORD,
					'default': a.default if hasattr(a, 'default') else None,
					'type': a.__class__
				})
				for a in EVAL(this.parameter, unwrapReturn=False, shouldAutoType=True, currentlyTryingToDefine=this.name)[0]
				if a is not None # TODO: why???
			}

			# Having a parameter implies this is a functor or structor
			if (this.kind == [TYPE]):
				this.kind = [STRUCTOR]

		toDelete = []
		for key in parameters.keys():
			if (key.startswith(this.name)):
				toDelete.append(key)
		for key in toDelete:
			parameters[key[len(this.name)+1:]] = parameters[key]
			parameters[key[len(this.name)+1:]].update({'name': key[len(this.name)+1:]})
			del parameters[key]

		source = "return this.parent.Function(this)"
		if (this.execution is not None and len(this.execution) > 0):
			if (type(this.execution) != list):
				this.execution = [this.execution]
			source = f"return this.executor.EXEC({this.execution}, currentlyTryingToInvoke=this)"

			# Having an execution block implies this is a functor.
			if (this.kind == [TYPE] or this.kind == [STRUCTOR]):
				this.kind = [FUNCTOR]

		ret = eons.kind(this.kind) (
			None,
			this.name,
			parameters,
			source,
			strongType=True
		)
		ret = ret() # class -> object

		ret.WarmUp(executor=this.executor)

		# if (alreadyDefined is not None and this.kind == [TYPE]):
		# 	this.CombineWithExisting(alreadyDefined, ret)
		# 	return alreadyDefined

		# Export this symbol to the current context iff we're not adding a parameter to another type.
		if (this.currentlyTryingToDefine is None):
			this.context.Set(this.name, ret)

		ret.EXEC_NO_EXECUTE = True
		this.result.data.product = ret
		return ret


	def AfterFunction(this):
		# NOTE Python bug: any access of currentlyTryingToDefine here, even within uninterpreted code, will cause it to be set to None.
		if (this.unsetCurrentlyTryingToDefine):
			this.executor.ExpireGlobal('currentlyTryingToDefine')
			globals()['currentlyTryingToDefine'] = None # TODO: the above is not enough???

		# If nothing was added, i.e. no sub-types were declared, and we're done, but 
		# Only occurs with short-typed functor pointers, like 'inner' in pointer.ldr. 
		else:
			this.executor.SetGlobal('currentlyTryingToDefine', this.originallyTryingToDefine)

		return super().AfterFunction()


	def CombineWithExisting(this, existing, new):
		pass
		# for key, val in new.__dict__.items():
		# 	if (key in existing.__dict__):
		# 		if (isinstance(val, eons.Functor)):
		# 			this.CombineWithExisting(existing.__dict__[key], val)
		# 		else:
		# 			existing.__dict__[key] = val


class Within (SourceTargetFunctor):
	def __init__(this, name="Within"):
		super().__init__(name)

		this.arg.kw.optional['useInvokation'] = False

		this.arg.kw.required.append('container')

		this.needs.target = False

	def Function(this):
		if (
			this.useInvokation 
			or isinstance(this.source, types.FunctionType) 
			or isinstance(this.source, types.MethodType)
		):
			return this.source([EVAL(item, shouldAttemptInvokation=True)[0] for item in this.container])

		index = EVAL(this.container[0], shouldAttemptInvokation=True)[0]
		logging.debug(f"Indexing {this.source} ({type(this.source)}) with {index} ({type(index)}).")

		if (
			isinstance(this.source, list)
			or isinstance(this.source, tuple)
			or isinstance(this.source, CONTAINER)
		):
			if (isinstance(index, int)):
				return this.source[index]
			if (isinstance(index, NUMBER) or isinstance(index, float)):
				return this.source[int(index)]
			elif (isinstance(index, STRING) or isinstance(index, str)):
				return this.source[str(index)]
			else:
				raise RuntimeError(f"Cannot index a list with {index}.")

		elif (
			isinstance(this.source, dict)
		):
			if (isinstance(index, NUMBER)):
				return this.source[int(index)]
			elif (isinstance(index, STRING)):
				return this.source[str(index)]
			return this.source[index]
		
		elif (
			isinstance(this.source, str)
			or isinstance(this.source, STRING)
		):
			return this.source[int(index)]
		
		else:
			raise RuntimeError(f"Cannot index {this.source} with {index}.")
		


class LOOP (KEYWORD):
	def __init__(this, name = eons.INVALID_NAME()):
		super().__init__(name)
	
	def BeforeFunction(this):
		super().BeforeFunction()
		this.BREAK = False


class BREAK (KEYWORD):
	def __init__(this):
		super().__init__(name = "BREAK")

	def Function(this):
		loop = this.Fetch(LOOP, None, ['stack_type'])

		if (loop is None):
			raise RuntimeError("Cannot break outside of loop")

		loop.BREAK = True
		loop.context.Halt()

class CASE (KEYWORD):
	def __init__(this):
		super().__init__(name = "CASE")

		this.arg.kw.required.append('condition')
		this.arg.kw.required.append('execution')
		this.arg.kw.required.append('SWITCH')

		this.arg.mapping.append('condition')
		this.arg.mapping.append('execution')

	def Function(this):
		if (this.condition == this.SWITCH.condition):
			this.SWITCH.matched = this
			EXEC(this.execution)

class CATCH (KEYWORD):
	def __init__(this):
		super().__init__(name = "CATCH")

		this.arg.kw.required.append('execution')

		this.arg.kw.optional['parameter'] = None

	def Function(this):
		if (len(this.executor.exceptions) and this.executor.exceptions[-1][1] == False):
			if (this.parameter is None
				or eval(this.parameter) == this.executor.exceptions[-1][0]
			):
				this.executor.exceptions.pop()
				EXEC(this.execution)

class CONTINUE (KEYWORD):
	def __init__(this):
		super().__init__(name = "CONTINUE")

	def Function(this):
		loop = this.Fetch(LOOP, None, ['stack_type'])

		if (loop is None):
			raise RuntimeError("Cannot continue outside of loop")

		loop.context.Halt()

class DEFAULT (KEYWORD):
	def __init__(this):
		super().__init__(name = "DEFAULT")

		this.arg.kw.required.append('switch')
		this.arg.kw.required.append('execution')

	def Function(this):
		if (this.switch.matched is None):
			this.switch.matched = this
			EXEC(this.execution)

class ELSE (KEYWORD):
	def __init__(this):
		super().__init__(name = "ELSE")

		# this.arg.kw.required.append('IF')
		this.arg.kw.required.append('execution')
		

	def Function(this):
		this.IF = this.Fetch('IF', None, ['history'])
		if (this.IF is None):
			raise RuntimeError("ELSE keyword must be used after an IF keyword.")
		if (not this.IF.didExecute):
			EXEC(this.execution)

class FOR (LOOP):
	def __init__(this):
		super().__init__(name = "FOR")

		this.arg.kw.required.append('source')
		this.arg.kw.required.append('container')
		this.arg.kw.required.append('execution')

		this.arg.mapping.append('source')
		this.arg.mapping.append('container')
		this.arg.mapping.append('execution')

	def Function(this):
		capture = ', '.join([f"{arg}={arg}" for arg in this.container])
		if (len(capture)):
			capture = f", {capture}"

		toExec = f"""\
for {', '.join(this.container)} in this.source:
	EXEC(this.execution{capture})
	if (this.BREAK):
		break
"""
		logging.debug(toExec)
		exec(toExec)


class IF (KEYWORD):
	def __init__(this):
		super().__init__(name = "IF")

		this.arg.kw.required.append('condition')
		this.arg.kw.required.append('execution')

		this.arg.mapping.append('condition')

	def Function(this):
		this.didExecute = False
		if (this.condition):
			this.didExecute = True
			EXEC(this.execution)

class NOT (KEYWORD):
	def __init__(this):
		super().__init__(name = "NOT")

		this.arg.kw.required.append('parameter')
		this.arg.mapping.append('parameter')

	def Function(this):
		if (isinstance(this.parameter, bool)):
			return not this.parameter

		unwrapped = True
		if (isinstance(this.parameter, str)):
			this.parameter, unwrapped = EVAL([this.parameter])
		elif(isinstance(this.parameter, list)):
			unwrapped = False
		
		if (unwrapped):
			return not this.parameter
		else:
			# TODO: this isn't quite right, but it shouldn't be a common case. Let's improve it once we know if we should default to True or False.
			return [not i for i in this.parameter]


class RETURN (KEYWORD):
	def __init__(this):
		super().__init__(name = "RETURN")

		this.arg.kw.required.append('parameter')
		this.arg.mapping.append('parameter')

	def Function(this):
		toHalt = None
		for i, tup in enumerate(this.executor.stack):
			if (isinstance(tup[1], FUNCTOR)):
				logging.debug(f"Returning from {tup[1]}.name ({tup[1]}).")
				toHalt = this.executor.stack[i-1][1] # the exec for the current functor.
				break
		if (toHalt is None):
			raise RuntimeError(f"RETURN called outside of a functor.")
		
		toReturn = this.parameter #EVAL(this.parameter, unwrapReturn=True)[0]

		this.result.data.returned = toReturn
		toHalt.result.data.returned = toReturn
		toHalt.Halt()

class SWITCH (KEYWORD):
	def __init__(this):
		super().__init__(name = "SWITCH")

		this.arg.kw.required.append('condition')
		this.arg.kw.required.append('execution')

		this.arg.mapping.append('condition')
		this.arg.mapping.append('execution')

	def Function(this):
		this.matched = None

class TRY (KEYWORD):
	def __init__(this):
		super().__init__(name = "TRY")

		this.arg.kw.required.append('execution')

		this.arg.mapping.append('execution')

	def Function(this):
		try:
			EXEC(this.execution)
		except Exception as e:
			this.executor.exceptions.append((e,False))

class WHILE (LOOP):
	def __init__(this):
		super().__init__(name = "WHILE")

		this.arg.kw.required.append('parameter')
		this.arg.kw.required.append('execution')

		this.arg.mapping.append('parameter')
		this.arg.mapping.append('execution')

	def Function(this):
		while (EVAL(this.parameter, unwrapReturn=True)[0] and not this.BREAK):
			EXEC(this.execution)


EXEC = EXEC()
EVAL = EVAL()
Autofill = Autofill()
Call = Call()
Get = Get()
Invoke = Invoke()
Kind = Kind()
Sequence = Sequence()
String = String()
Type = Type()
Within = Within()

BREAK = BREAK()
CASE = CASE()
CATCH = CATCH()
CONTINUE = CONTINUE()
DEFAULT = DEFAULT()
ELSE = ELSE()
FOR = FOR()
IF = IF()
NOT = NOT()
RETURN = RETURN()
SWITCH = SWITCH()
TRY = TRY()
WHILE = WHILE()


class STRING(TYPE):
	def __init__(this, name="string", value=""):
		super().__init__(name)

		this.value = value
		this.useValue = True
		this.needs.typeAssignment = False

	def Function(this):
		return this.value

# The purpose of a pointer is to hold a value that lives elsewhere and allow special handling of write operations.
# For example, a POINTER could implement copy-on-write semantics.
class POINTER(TYPE):

	def __init__(this, name=None, value=None):
		if (name is None):
			name = f"Pointer to {repr(value)}"
		super().__init__()

		if (value is None and hasattr(this, 'target')):
			this.value = this.target()
		else:
			this.value = value

		this.useValue = False # But true in practice.
		this.needs.typeAssignment = False

		this.SET =  lambda val: setattr(this, 'value', val)

	@staticmethod
	def to(obj):
		cls = obj
		if (not inspect.isclass(obj)):
			cls = type(obj)

		ret = type(
			f"POINTER_TO_{cls.__name__.upper()}",
			(POINTER,),
			{'target': cls}
		)

		if (inspect.isclass(obj)):
			return ret

		return ret(None, obj)

	# Overriding the EQ method allows pointers to change how they are set.
	def EQ(this, other):
		try:
			this.SET(this.PossiblyReduceOther(other))
			logging.debug(f"Set {this} to {other}")
		except:
			try:
				this.value.EQ(other)
			except:
				try:
					this.value = other.value
				except:
					this.value = other
		return this

	# Explicit dereference operator.
	# Explicit dereferencing is not necessary at this time.
	# def TIMES(this, other=None):
	# 	if (other is not None):
	# 		try:
	# 			return this.value.TIMES(other)
	# 		except:
	# 			return super().TIMES(other)
	# 	logging.debug(f"Dereferencing {this.name}")
	# 	# object.__getattribute__(this, '__dict__').update(copy.deepcopy(object.__getattribute__(this, '__dict__')))
	# 	this.value = copy.copy(this.value)
	# 	return this

	def __getattribute__(this, attribute):
		if (attribute == "to"):
			return POINTER.to
		if (attribute in ["__class__", "__init__", "name", "value", "isPointer", "EQ", "SET"]):
			return object.__getattribute__(this, attribute)
		try:
			# Will fail if value is null.
			return object.__getattribute__(this, 'value').__getattribute__(attribute)
		except:
			# TODO: consider raising an exception when trying to dereference a null pointer.
			return super().__getattribute__(attribute)

	def __setattribute__(this, name, value):
		if (name in ["value", "SET", "to"]):
			super().__setattribute__(name, value)
		try:
			setattr(this.value, name, value)
		except:
			super().__setattribute__(name, value)

# Containers always store data by reference.
class CONTAINER(TYPE):
	def __init__(this, name="container", value=[]):
		super().__init__(name)

		this.value = []
		if (value is not None):
			for item in value:
				this.value.append(item)
		this.useValue = True
		this.needs.typeAssignment = False

	@staticmethod
	def of(value):
		return CONTAINER(value=value)

	def __list__(this):
		if (isinstance(this.value, dict)):
			return this.value.keys()
		return this.value

	def __dict__(this):
		if (isinstance(this.value, list)):
			return {key: key for key in this.value}

	def __getitem__(this, index):
		ret = POINTER(f"{this.name}[{index}]", this.value[index])
		ret.SET = lambda x: this.__setitem__(index, x)
		return ret

	def __setitem__(this, index, value):
			this.value[index] = value

	def insert(this, index, value):
		this.value.insert(index, value)

	def Function(this):
		return this.value

class BOOL(TYPE):
	def __init__(this, name="bool", value=False):
		super().__init__(name)

		this.value = value
		this.useValue = True
		this.needs.typeAssignment = False

	def __bool__(this):
		return this.value
	
	def Function(this):
		return this.value

class NUMBER(TYPE):
	def __init__(this, name=eons.INVALID_NAME, value=0):
		super().__init__(name)

		this.value = value
		this.useValue = True
		this.needs.typeAssignment = False

	def __int__(this):
		return int(this.value)
	
	def __float__(this):
		return float(this.value)
	
	def Function(this):
		return this.value
	
	def PLUSPLUS(this):
		this.value += 1
		return this
	
	def MINUSMINUS(this):
		this.value -= 1
		return this

class FLOAT(NUMBER):
	def __init__(this, name="float", value=0.0):
		super().__init__(name, value)


class INT(NUMBER):
	def __init__(this, name="integer", value=0):
		super().__init__(name, value)

