
Speech Rule Engine
==================
[![Build Status](https://travis-ci.org/zorkow/speech-rule-engine.svg?branch=master)](https://travis-ci.org/zorkow/speech-rule-engine) [![Dependencies](https://david-dm.org/zorkow/speech-rule-engine.svg)](https://david-dm.org/zorkow/speech-rule-engine) [![devDependency Status](https://david-dm.org/zorkow/speech-rule-engine/dev-status.svg)](https://david-dm.org/zorkow/speech-rule-engine#info=devDependencies) [![Coverage Status](https://coveralls.io/repos/zorkow/speech-rule-engine/badge.svg?branch=master&service=github)](https://coveralls.io/github/zorkow/speech-rule-engine?branch=master)

NodeJS version of the ChromeVox speech rule engine.
Forked from ChromeVox release 1.31.0

The speech rule engine can translate XML expression into speech strings according to rules that
can be specified in a syntax using Xpath expressions.  It was originally designed for translation
of MathML and MathJax DOM elements for the ChromeVox screen reader. 
Besides the rules originally designed for the use in ChromeVox, it also has an implemententation of the 
full set of Mathspeak rules. In addition it contains a library for semantic interpretation and enrichment
of MathML expressions.

There are two ways of using this engine. Either as a package via npm or by
building it as a standalone tool.  The former is the easiest way to use the
speech rule engine via its Api and is the preferred option if you just want to
include it in your project. The latter is useful if you want to use the speech
rule engine in batch mode or interactivley to add your own code.

Node Module
-----------

Install as a node module using npm:

     npm install speech-rule-engine

Then import into a running node or a source file using require:

     require('speech-rule-engine');
     
### API #######

Current API functions are divided into three categories.

#### Methods that take a string containing a MathML expression: 
     
| Method | Return Value |
| ---- | ---- |
| `toSpeech(mathml)` | Speech string for the MathML. |
| `toSemantic(mathml)` | String with XML representation of the semantic tree of given MathML. |
| `toJson(mathml)` | The semantic tree in JSON. This method only works in Node, not in browser mode. |
| `toDescription(mathml)` | The array of auditory description objects of the MathML expression. |
| `toEnriched(mathml)` | The semantically enriched MathML expression. |

#### Methods that take an input filename and optionally an output filename: 

If the output filename is not provided, output will be written to stdout.

| Method | Return Value |
| ---- | ---- |
| `file.toSpeech(input, output)` | Speech string for the MathML. |
| `file.toSemantic(input, output)` | String with XML representation of the semantic tree of given MathML. |
| `file.toJson(input, output)` | The semantic tree in JSON. This method only works in Node, not in browser mode. |
| `file.toDescription(input, output)` | The array of auditory description objects of the MathML expression. |
| `file.toEnriched(input, output)` | The semantically enriched MathML expression. |

#### A method for setting up and controlling the behaviour of the Speech Rule Engine:

It takes an object of option/value pairs to parameterise the Speech Rule Engine.

    setupEngine(options);

Valid options are:

| Option | Value |
| ---- | ---- |
| *domain* | Domain or subject area of speech rules (e.g., mathspeak, physics).|
| *style* | Style of speech rules (e.g., brief).|
| *semantics* | Boolean flag to swich on semantic interpretation.|

Observe that some speech rule domains only make sense with semantics switched on
or off and that not every domain implements every style. See also the
description of the command line parameters in the next section for more details.


#### The following are deprecated API functions #########

     processExpression(mathml); 

Takes a string containing a MathML expression and returns the corresponding
speech string. Same as `toSpeech(mathml)`.

     processFile(input, output);

Takes an input file containing a MathML expression and writes the corresponding
speech string to the output file. Same as `file.toSpeech(mathml)`.

Standalone Engine
-----------------

Node dependencies you have to install:

     closure
     closurecompiler
     closure-library
     xmldom
     xpath
     commander
     xml-mapping
 
Using npm run

     npm install closure closurecompiler closure-library xmldom xpath commander xml-mapping


In version 1.43 of the closure library there is a mistake in the file 

    closure-library/closure/bin/build/jscompiler.py 

You might need to change

    # Attempt 32-bit mode if we're <= Java 1.7
    if java_version >= 1.7:
      args += ['-d32']

to 

    # Attempt 32-bit mode if we're <= Java 1.7
    if java_version <= 1.7:
      args += ['-d32']

### Build #############

Depending on your setup you might need to adapt the NODEJS and NODE_MODULES
variable in the Makefile.  Then simply run

    make
    
This will make both the command line executable and the interactive load script.

### Run on command line ############


    bin/sre -i infile -o outfile

As an example run

    bin/sre -i samples/sample1.xml -o sample1.txt
    
### Run interactively ############

Import into a running node process

    require('./lib/sre4node.js');

Note, that this will import the full functionality of the speech rule engine in
the sre namespace and of the closure library in the goog namespace.
  

### Command Line Options ###########

The following is a list of command line options for the speech rule engine.

| Short | Long | Meaning | 
| ----- | ---- | :------- |
| -i | --input [name]  | Input file [name] |
| -o | --output [name] | Output file [name].
||| If not given output is printed to stdout. |
| | |
| | |
| | |
| -d | --domain [name] | Domain or subject area [name]. |
||| This refers to a particular subject type of speech rules or subject area rules are defined for (e.g., mathspeak, physics). |
||| If no domain parameter is provided, domain default is used. |
| -t | --style [name]  | Speech style [name]. |
||| Selects a particular speech style (e.g., brief). |
||| If no style parameter is provided, style default is used. |
| -s | --semantics     | Switch on semantics interpretation. |
||| Note, that some speech rule domains only make sense with semantics switched on or off. |
| -e | --enumerate     | Enumerates all available domains and styles. |
||| Note that not every style is implemented in every domain. |
| | |
| | |
| | |
| -a | --audit | Generate auditory descriptions (JSON format). |
| -j | --json  | Generate JSON of semantic tree. |
| -m | --mathml  | Generate enriched MathML. |
| -p | --speech  | Generate speech output (default). |
| -x | --xml  | Generate XML of semantic tree. |
| | |
| | |
| | |
| -v | --verbose       | Verbose mode. Print additional information, useful for debugging. |
| -l | --log [name]    | Log file [name]. Verbose output is redirected to this file. |
||| If not given verbose output is printed to stdout. |
| | |
| | |
| | |
| -h | --help   | output usage information |
| -V | --version  |      output the version number |




Developers Notes
----------------

### Build Options 

Other make targets useful during development are:

    make test
    
Runs all the tests using the Node's assert module. Output is pretty printed to stdout.

    make lint
    
Runs the closure linter tool. To use this option, you need to install the appropriate node package with

    npm install closure-linter-wrapper

To automatically fix some of linting errors run:
    
    make fixjsstyle

Note, that all JavaScript code in this repository is fully linted and compiles error free with respect to the strictest possible closure compiler settings.

When creating a pull request, please make sure that your code compiles and is fully linted.


### Node Package

The speech rule engine is published as a node package in fully compiled form, together with the JSON libraries for translating atomic expressions. All relevant files are in the lib subdirectory.

To publish the node package run

    npm publish

This first builds the package by executing

    make publish
    
This make command is also useful for local testing of the package.
