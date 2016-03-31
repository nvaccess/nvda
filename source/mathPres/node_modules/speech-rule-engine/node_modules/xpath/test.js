var xpath = require('./xpath.js')
, dom = require('xmldom').DOMParser
, assert = require('assert');

module.exports = {
	'api': function(test) {
		assert.ok(xpath.evaluate, 'evaluate api ok.');
		assert.ok(xpath.select, 'select api ok.');
        assert.ok(xpath.parse, 'parse api ok.');
		test.done();
	},

	'evaluate': function(test) {
		var xml = '<book><title>Harry Potter</title></book>';
		var doc = new dom().parseFromString(xml);
		var nodes = xpath.evaluate('//title', doc, null, xpath.XPathResult.ANY_TYPE, null).nodes;
		assert.equal('title', nodes[0].localName);
		assert.equal('Harry Potter', nodes[0].firstChild.data);
		assert.equal('<title>Harry Potter</title>', nodes[0].toString());
		test.done();
	},

	'select': function(test) {
		var xml = '<book><title>Harry Potter</title></book>';
		var doc = new dom().parseFromString(xml);
		var nodes = xpath.select('//title', doc);
		assert.equal('title', nodes[0].localName);
		assert.equal('Harry Potter', nodes[0].firstChild.data);
		assert.equal('<title>Harry Potter</title>', nodes[0].toString());
		test.done();
	},

	'select single node': function(test) {
		var xml = '<book><title>Harry Potter</title></book>';
		var doc = new dom().parseFromString(xml);

		assert.equal('title', xpath.select('//title[1]', doc)[0].localName);

		test.done();
	},

	'select text node': function (test) {
		var xml = '<book><title>Harry</title><title>Potter</title></book>';
		var doc = new dom().parseFromString(xml);

		assert.deepEqual('book', xpath.select('local-name(/book)', doc));
		assert.deepEqual('Harry,Potter', xpath.select('//title/text()', doc).toString());

		test.done();
	},

	'select number node': function(test) {
		var xml = '<book><title>Harry</title><title>Potter</title></book>';
		var doc = new dom().parseFromString(xml);

		assert.deepEqual(2, xpath.select('count(//title)', doc));

		test.done();
	},

	'select xpath with namespaces': function (test) {
		var xml = '<book><title xmlns="myns">Harry Potter</title></book>';
		var doc = new dom().parseFromString(xml);

		var nodes = xpath.select('//*[local-name(.)="title" and namespace-uri(.)="myns"]', doc);
		assert.equal('title', nodes[0].localName);
		assert.equal('myns', nodes[0].namespaceURI) ;

		test.done();
	},

	'select xpath with namespaces, using a resolver': function (test) {
		var xml = '<book xmlns:testns="http://example.com/test"><testns:title>Harry Potter</testns:title><testns:field testns:type="author">JKR</testns:field></book>';
		var doc = new dom().parseFromString(xml);

		var resolver = {
			mappings: {
				'testns': 'http://example.com/test'
			},
			lookupNamespaceURI: function(prefix) {
				return this.mappings[prefix];
			}
		}

		var nodes = xpath.selectWithResolver('//testns:title/text()', doc, resolver);
		assert.equal('Harry Potter', xpath.selectWithResolver('//testns:title/text()', doc, resolver)[0].nodeValue);
		assert.equal('JKR', xpath.selectWithResolver('//testns:field[@testns:type="author"]/text()', doc, resolver)[0].nodeValue);

		test.done();
	},

	'select xpath with default namespace, using a resolver': function (test) {
		var xml = '<book xmlns="http://example.com/test"><title>Harry Potter</title><field type="author">JKR</field></book>';
		var doc = new dom().parseFromString(xml);

		var resolver = {
			mappings: {
				'testns': 'http://example.com/test'
			},
			lookupNamespaceURI: function(prefix) {
				return this.mappings[prefix];
			}
		}

		var nodes = xpath.selectWithResolver('//testns:title/text()', doc, resolver);
		assert.equal('Harry Potter', xpath.selectWithResolver('//testns:title/text()', doc, resolver)[0].nodeValue);
		assert.equal('JKR', xpath.selectWithResolver('//testns:field[@type="author"]/text()', doc, resolver)[0].nodeValue);

		test.done();
	},

	'select xpath with namespaces, prefixes different in xml and xpath, using a resolver': function (test) {
		var xml = '<book xmlns:testns="http://example.com/test"><testns:title>Harry Potter</testns:title><testns:field testns:type="author">JKR</testns:field></book>';
		var doc = new dom().parseFromString(xml);

		var resolver = {
			mappings: {
				'ns': 'http://example.com/test'
			},
			lookupNamespaceURI: function(prefix) {
				return this.mappings[prefix];
			}
		}

		var nodes = xpath.selectWithResolver('//ns:title/text()', doc, resolver);
		assert.equal('Harry Potter', xpath.selectWithResolver('//ns:title/text()', doc, resolver)[0].nodeValue);
		assert.equal('JKR', xpath.selectWithResolver('//ns:field[@ns:type="author"]/text()', doc, resolver)[0].nodeValue);

		test.done();
	},

	'select xpath with namespaces, using namespace mappings': function (test) {
		var xml = '<book xmlns:testns="http://example.com/test"><testns:title>Harry Potter</testns:title><testns:field testns:type="author">JKR</testns:field></book>';
		var doc = new dom().parseFromString(xml);
		var select = xpath.useNamespaces({'testns': 'http://example.com/test'});

		assert.equal('Harry Potter', select('//testns:title/text()', doc)[0].nodeValue);
		assert.equal('JKR', select('//testns:field[@testns:type="author"]/text()', doc)[0].nodeValue);

		test.done();
	},


	'select attribute': function (test) {
		var xml = '<author name="J. K. Rowling"></author>';
		var doc = new dom().parseFromString(xml);

		var author = xpath.select1('/author/@name', doc).value;
		assert.equal('J. K. Rowling', author);

		test.done();
	}

    // https://github.com/goto100/xpath/issues/37
	,'select multiple attributes': function (test) {
		var xml = '<authors><author name="J. K. Rowling" /><author name="Saeed Akl" /></authors>';
		var doc = new dom().parseFromString(xml);

		var authors = xpath.select('/authors/author/@name', doc);
		assert.equal(2, authors.length);
        assert.equal('J. K. Rowling', authors[0].value);

        // https://github.com/goto100/xpath/issues/41
        doc = new dom().parseFromString('<chapters><chapter v="1"/><chapter v="2"/><chapter v="3"/></chapters>');
        var nodes = xpath.select("/chapters/chapter/@v", doc);
	    var values = nodes.map(function(n) { return n.value; });

        assert.equal(3, values.length);
        assert.equal("1", values[0]);
        assert.equal("2", values[1]);
        assert.equal("3", values[2]);

		test.done();
	}

	,'XPathException acts like Error': function (test) {
		try {
		    xpath.evaluate('1', null, null, null);
			assert.fail(null, null, 'evaluate() should throw exception');
		} catch (e) {
			assert.ok('code' in e, 'must have a code');
			assert.ok('stack' in e, 'must have a stack');
		}
		
		test.done();
	},
	
	'string() with no arguments': function (test) {
		var doc = new dom().parseFromString('<book>Harry Potter</book>');
		
		var rootElement = xpath.select1('/book', doc);
		assert.ok(rootElement, 'rootElement is null');
		
		assert.equal('Harry Potter', xpath.select1('string()', doc));
	
		test.done();
	},
	
	'string value of document fragment': function (test) {
		var doc = new dom().parseFromString('<n />');
		var docFragment = doc.createDocumentFragment();

		var el = doc.createElement("book");
		docFragment.appendChild(el);
		
		var testValue = "Harry Potter";
		
		el.appendChild(doc.createTextNode(testValue));

		assert.equal(testValue, xpath.select1("string()", docFragment));
		
		test.done();
	},

	'compare string of a number with a number': function (test) {
		assert.ok(xpath.select1('"000" = 0'), '000');
		assert.ok(xpath.select1('"45.0" = 45'), '45');
		
		test.done();
	},

	'string(boolean) is a string': function (test) {
		assert.equal('string', typeof xpath.select1('string(true())'));
		assert.equal('string', typeof xpath.select1('string(false())'));
		assert.equal('string', typeof xpath.select1('string(1 = 2)'));
		assert.ok(xpath.select1('"true" = string(true())'), '"true" = string(true())');
		
		test.done();
	},
	
	'string should downcast to boolean': function (test) {
		assert.equal(false, xpath.select1('"false" = false()'), '"false" = false()');
		assert.equal(true, xpath.select1('"a" = true()'), '"a" = true()');
		assert.equal(true, xpath.select1('"" = false()'), '"" = false()');
		
		test.done();
	},
	
	'string(number) is a string': function (test) {
		assert.equal('string', typeof xpath.select1('string(45)'));
		assert.ok(xpath.select1('"45" = string(45)'), '"45" = string(45)');
		
		test.done();
	},
	
	'correct string to number conversion': function (test) {
	    assert.equal(45.2, xpath.select1('number("45.200")'));
	    assert.equal(55.0, xpath.select1('number("000055")'));
	    assert.equal(65.0, xpath.select1('number("  65  ")'));

		assert.equal(true, xpath.select1('"" != 0'), '"" != 0');
	    assert.equal(false, xpath.select1('"" = 0'), '"" = 0');
		assert.equal(false, xpath.select1('0 = ""'), '0 = ""');
		assert.equal(false, xpath.select1('0 = "   "'), '0 = "   "');

		assert.ok(Number.isNaN(xpath.select('number("")')), 'number("")');
		assert.ok(Number.isNaN(xpath.select('number("45.8g")')), 'number("45.8g")');
		assert.ok(Number.isNaN(xpath.select('number("2e9")')), 'number("2e9")');
		assert.ok(Number.isNaN(xpath.select('number("+33")')), 'number("+33")');
		
		test.done();
	},	
	
	'local-name() and name() of processing instruction': function (test) {
	    var xml = '<?book-record added="2015-01-16" author="J.K. Rowling" ?><book>Harry Potter</book>';
		var doc = new dom().parseFromString(xml);
		var expectedName = 'book-record';
		var localName = xpath.select('local-name(/processing-instruction())', doc);
		var name = xpath.select('name(/processing-instruction())', doc);
		
		assert.deepEqual(expectedName, localName, 'local-name() - "' + expectedName + '" !== "' + localName + '"');
		assert.deepEqual(expectedName, name, 'name() - "' + expectedName + '" !== "' + name + '"');
		
		test.done();
	},

	'evaluate substring-after': function (test) {
	    var xml = '<classmate>Hermione</classmate>';
		var doc = new dom().parseFromString(xml);
		
		var part = xpath.select('substring-after(/classmate, "Her")', doc);
		assert.deepEqual('mione', part);
		
		test.done();
    }
    
    ,'parsed expression with no options': function (test) {
        var parsed = xpath.parse('5 + 7');
        
        assert.equal(typeof parsed, "object", "parse() should return an object");
        assert.equal(typeof parsed.evaluate, "function", "parsed.evaluate should be a function");
        assert.equal(typeof parsed.evaluateNumber, "function", "parsed.evaluateNumber should be a function");
 
        assert.equal(parsed.evaluateNumber(), 12);

        // evaluating twice should yield the same result
        assert.equal(parsed.evaluateNumber(), 12);
 
        test.done();
    }
    
    ,'select1() on parsed expression': function (test) {
		var xml = '<book><title>Harry Potter</title></book>';
		var doc = new dom().parseFromString(xml);
        var parsed = xpath.parse('/*/title');
        
        assert.equal(typeof parsed, 'object', 'parse() should return an object');
        
        assert.equal(typeof parsed.select1, 'function', 'parsed.select1 should be a function');
        
        var single = parsed.select1({ node: doc });
        
		assert.equal('title', single.localName);
		assert.equal('Harry Potter', single.firstChild.data);
		assert.equal('<title>Harry Potter</title>', single.toString());
        
        test.done();
    }

    ,'select() on parsed expression': function (test) {
		var xml = '<book><title>Harry Potter</title></book>';
		var doc = new dom().parseFromString(xml);
        var parsed = xpath.parse('/*/title');
        
        assert.equal(typeof parsed, 'object', 'parse() should return an object');
        
        assert.equal(typeof parsed.select, 'function', 'parsed.select should be a function');
        
        var nodes = parsed.select({ node: doc });
        
        assert.ok(nodes, 'parsed.select() should return a value');
        assert.equal(1, nodes.length);
		assert.equal('title', nodes[0].localName);
		assert.equal('Harry Potter', nodes[0].firstChild.data);
		assert.equal('<title>Harry Potter</title>', nodes[0].toString());
        
        test.done();
    }

    ,'evaluateString(), and evaluateNumber() on parsed expression with node': function (test) {
		var xml = '<book><title>Harry Potter</title><numVolumes>7</numVolumes></book>';
		var doc = new dom().parseFromString(xml);
        var parsed = xpath.parse('/*/numVolumes');
        
        assert.equal(typeof parsed, 'object', 'parse() should return an object');
        
        assert.equal(typeof parsed.evaluateString, 'function', 'parsed.evaluateString should be a function');
        assert.equal('7', parsed.evaluateString({ node: doc }));
        
        assert.equal(typeof parsed.evaluateBoolean, 'function', 'parsed.evaluateBoolean should be a function');
        assert.equal(true, parsed.evaluateBoolean({ node: doc }));

        assert.equal(typeof parsed.evaluateNumber, 'function', 'parsed.evaluateNumber should be a function');
        assert.equal(7, parsed.evaluateNumber({ node: doc }));

        test.done();
    }
    
    ,'evaluateBoolean() on parsed empty node set and boolean expressions': function (test) {
		var xml = '<book><title>Harry Potter</title></book>';
		var doc = new dom().parseFromString(xml);
        var context = { node: doc };
        
        function evaluate(path) {
            return xpath.parse(path).evaluateBoolean({ node: doc });
        }

        assert.equal(false, evaluate('/*/myrtle'), 'boolean value of empty node set should be false');
        
        assert.equal(true, evaluate('not(/*/myrtle)'), 'not() of empty nodeset should be true');

        assert.equal(true, evaluate('/*/title'), 'boolean value of non-empty nodeset should be true');
        
        assert.equal(true, evaluate('/*/title = "Harry Potter"'), 'title equals Harry Potter');

        assert.equal(false, evaluate('/*/title != "Harry Potter"'), 'title != Harry Potter should be false');

        assert.equal(false, evaluate('/*/title = "Percy Jackson"'), 'title should not equal Percy Jackson');
        
        test.done();
    }
    
    ,'namespaces with parsed expression': function (test) {
        var xml = '<characters xmlns:ps="http://philosophers-stone.com" xmlns:cs="http://chamber-secrets.com">' +
                  '<ps:character>Quirrell</ps:character><ps:character>Fluffy</ps:character>' +
                  '<cs:character>Myrtle</cs:character><cs:character>Tom Riddle</cs:character>' +
                  '</characters>';
        var doc = new dom().parseFromString(xml);

        var expr = xpath.parse('/characters/c:character');
        var countExpr = xpath.parse('count(/characters/c:character)');
        var csns = 'http://chamber-secrets.com';
        
        function resolve(prefix) {
            if (prefix === 'c') {
                return csns;
            }
        }
        
        function testContext(context, description) {
            try {
                var value = expr.evaluateString(context);
                var count = countExpr.evaluateNumber(context);

                assert.equal('Myrtle', value, description + ' - string value - ' + value);
                assert.equal(2, count, description + ' map - count - ' + count);
            } catch(e) {
                e.message = description + ': ' + (e.message || '');
                throw e;
            }
        }
        
        testContext({
            node: doc,
            namespaces: {
                c: csns
            }
        }, 'Namespace map');
        
        testContext({
            node: doc,
            namespaces: resolve
        }, 'Namespace function');
        
        testContext({
            node: doc,
            namespaces: {
                getNamespace: resolve
            }
        }, 'Namespace object');
        
        test.done();
    }
    
    ,'custom functions': function (test) {
		var xml = '<book><title>Harry Potter</title></book>';
        var doc = new dom().parseFromString(xml);

        var parsed = xpath.parse('concat(double(/*/title), " is cool")');
        
        function doubleString(context, value) {
            assert.equal(2, arguments.length);
            var str = value.stringValue();
            return str + str;
        }
        
        function functions(name, namespace) {
            if(name === 'double') {
                return doubleString;
            }
            return null;
        }
        
        function testContext(context, description) {
            try{
                var actual = parsed.evaluateString(context);
                var expected = 'Harry PotterHarry Potter is cool';
                assert.equal(expected, actual, description + ' - ' + expected + ' != ' + actual);
            } catch (e) {
                e.message = description + ": " + (e.message || '');
                throw e;
            }
        }
        
        testContext({
            node: doc,
            functions: functions
        }, 'Functions function');
        
        testContext({
            node: doc,
            functions: {
                getFunction: functions
            }
        }, 'Functions object');
        
        testContext({
            node: doc,
            functions: {
                double: doubleString
            }
        }, 'Functions map');
        
        test.done();
    }
    
    ,'custom function namespaces': function (test) {
		var xml = '<book><title>Harry Potter</title><friend>Ron</friend><friend>Hermione</friend><friend>Neville</friend></book>';
        var doc = new dom().parseFromString(xml);

        var parsed = xpath.parse('concat(hp:double(/*/title), " is 2 cool ", hp:square(2), " school")');
        var hpns = 'http://harry-potter.com';
        
        var namespaces = {
            hp: hpns
        };
        
        var context = {
            node: doc,
            namespaces: {
                hp: hpns
            },
            functions: function (name, namespace) {
                if (namespace === hpns) {
                    switch (name) {
                        case "double":
                            return function (context, value) {
                                assert.equal(2, arguments.length);
                                var str = value.stringValue();
                                return str + str;
                            };
                        case "square":
                            return function (context, value) {
                                var num = value.numberValue();
                                return num * num;
                            };

                        case "xor":
                            return function (context, l, r) {
                                assert.equal(3, arguments.length);
                                var lbool = l.booleanValue();
                                var rbool = r.booleanValue();
                                return (lbool || rbool) && !(lbool && rbool);
                            };

                        case "second":
                            return function (context, nodes) {
                                var nodesArr = nodes.toArray();
                                var second = nodesArr[1];
                                return second ? [second] : [];
                            };
                    }
                }
                return null;
            }
        };
        
        assert.equal('Harry PotterHarry Potter is 2 cool 4 school', parsed.evaluateString(context));

        assert.equal(false, xpath.parse('hp:xor(false(), false())').evaluateBoolean(context));
        assert.equal(true, xpath.parse('hp:xor(false(), true())').evaluateBoolean(context));
        assert.equal(true, xpath.parse('hp:xor(true(), false())').evaluateBoolean(context));
        assert.equal(false, xpath.parse('hp:xor(true(), true())').evaluateBoolean(context));

        assert.equal('Hermione', xpath.parse('hp:second(/*/friend)').evaluateString(context));
        assert.equal(1, xpath.parse('count(hp:second(/*/friend))').evaluateNumber(context));
        assert.equal(0, xpath.parse('count(hp:second(/*/friendz))').evaluateNumber(context));
        
        test.done();
    }
    
    ,'xpath variables': function (test) {
		var xml = '<book><title>Harry Potter</title><volumes>7</volumes></book>';
        var doc = new dom().parseFromString(xml);
        
        var variables = {
            title: 'Harry Potter',
            notTitle: 'Percy Jackson',
            houses: 4
        };
        
        function variableFunction(name) {
            return variables[name];
        }
        
        function testContext(context, description) {
            try{
                assert.equal(true, xpath.parse('$title = /*/title').evaluateBoolean(context));
                assert.equal(false, xpath.parse('$notTitle = /*/title').evaluateBoolean(context));
                assert.equal(11, xpath.parse('$houses + /*/volumes').evaluateNumber(context));
            } catch (e) {
                e.message = description + ": " + (e.message || '');
                throw e;
            }
        }

        testContext({
            node: doc,
            variables: variableFunction
        }, 'Variables function');

        testContext({
            node: doc,
            variables: {
                getVariable: variableFunction
            }
        }, 'Variables object');
        
        testContext({
            node: doc,
            variables: variables
        }, 'Variables map');
        
        test.done();
    }
    
    ,'xpath variable namespaces': function (test) {
		var xml = '<book><title>Harry Potter</title><volumes>7</volumes></book>';
        var doc = new dom().parseFromString(xml);
        var hpns = 'http://harry-potter.com';
        
        var context = {
            node: doc,
            namespaces: {
                hp: hpns
            },
            variables: function(name, namespace) {
                if (namespace === hpns) {
                    switch (name) {
                        case 'title': return 'Harry Potter';
                        case 'houses': return 4;
                        case 'false': return false;
                        case 'falseStr': return 'false';
                    }
                } else if (namespace === '') {
                    switch (name) {
                        case 'title': return 'World';
                    }
                }
            
                return null;
            }
        };
        
        assert.equal(true, xpath.parse('$hp:title = /*/title').evaluateBoolean(context));
        assert.equal(false, xpath.parse('$title = /*/title').evaluateBoolean(context));
        assert.equal('World', xpath.parse('$title').evaluateString(context));
        assert.equal(false, xpath.parse('$hp:false').evaluateBoolean(context));
        assert.notEqual(false, xpath.parse('$hp:falseStr').evaluateBoolean(context));
        assert.throws(function () {
            xpath.parse('$hp:hello').evaluateString(context);
        }, function (err) {
            return err.message === 'Undeclared variable: $hp:hello';
        });
        
        test.done();
    }

    ,"detect unterminated string literals": function (test) {
        function testUnterminated(path) {
            assert.throws(function () {
                xpath.evaluate('"hello');
            }, function (err) {
                return err.message.indexOf('Unterminated') !== -1;
            });
        }
        
        testUnterminated('"Hello');
        testUnterminated("'Hello");
        testUnterminated('self::text() = "\""');
        testUnterminated('"\""');

        test.done();
    }
    
    ,"string value for CDATA sections": function (test) {
        var xml = "<people><person><![CDATA[Harry Potter]]></person><person>Ron <![CDATA[Weasley]]></person></people>",
            doc = new dom().parseFromString(xml),
            person1 = xpath.parse("/people/person").evaluateString({ node: doc }),
            person2 = xpath.parse("/people/person/text()").evaluateString({ node: doc }),
            person3 = xpath.select("string(/people/person/text())", doc);
            person4 = xpath.parse("/people/person[2]").evaluateString({ node: doc });

        assert.equal(person1, 'Harry Potter');
        assert.equal(person2, 'Harry Potter');
        assert.equal(person3, 'Harry Potter');
        assert.equal(person4, 'Ron Weasley');
        
        test.done();
    }
    
    ,"string value of various node types": function (test) {
        var xml = "<book xmlns:hp='http://harry'><!-- This describes the Harry Potter Book --><?author name='J.K. Rowling' ?><title lang='en'><![CDATA[Harry Potter & the Philosopher's Stone]]></title><character>Harry Potter</character></book>",
            doc = new dom().parseFromString(xml),
            allText = xpath.parse('.').evaluateString({ node: doc }),
            ns = xpath.parse('*/namespace::*[name() = "hp"]').evaluateString({ node: doc }),
            title = xpath.parse('*/title').evaluateString({ node: doc }),
            child = xpath.parse('*/*').evaluateString({ node: doc }),
            titleLang = xpath.parse('*/*/@lang').evaluateString({ node: doc }),
            pi = xpath.parse('*/processing-instruction()').evaluateString({ node: doc }),
            comment = xpath.parse('*/comment()').evaluateString({ node: doc });
    
        assert.equal(allText, "Harry Potter & the Philosopher's StoneHarry Potter");
        assert.equal(ns, 'http://harry');
        assert.equal(title, "Harry Potter & the Philosopher's Stone");
        assert.equal(child, "Harry Potter & the Philosopher's Stone");
        assert.equal(titleLang, 'en');
        assert.equal(pi.trim(), "name='J.K. Rowling'");
        assert.equal(comment, ' This describes the Harry Potter Book ');
        
        test.done();
    }
    
    ,"exposes custom types": function (test) {
        assert.ok(xpath.XPath, "xpath.XPath");
        assert.ok(xpath.XPathParser, "xpath.XPathParser");
        assert.ok(xpath.XPathResult, "xpath.XPathResult");
        
        assert.ok(xpath.Step, "xpath.Step");
        assert.ok(xpath.NodeTest, "xpath.NodeTest");
        assert.ok(xpath.BarOperation, "xpath.BarOperation");
        
        assert.ok(xpath.NamespaceResolver, "xpath.NamespaceResolver");
        assert.ok(xpath.FunctionResolver, "xpath.FunctionResolver");
        assert.ok(xpath.VariableResolver, "xpath.VariableResolver");
        
        assert.ok(xpath.Utilities, "xpath.Utilities");
        
        assert.ok(xpath.XPathContext, "xpath.XPathContext");
        assert.ok(xpath.XNodeSet, "xpath.XNodeSet");
        assert.ok(xpath.XBoolean, "xpath.XBoolean");
        assert.ok(xpath.XString, "xpath.XString");
        assert.ok(xpath.XNumber, "xpath.XNumber");
        
        test.done();
    }
    
    ,"work with nodes created using DOM1 createElement()": function (test) {
        var doc = new dom().parseFromString('<book />');
        
        doc.documentElement.appendChild(doc.createElement('characters'));
        
        assert.ok(xpath.select1('/book/characters', doc));
        
        assert.equal(xpath.select1('local-name(/book/characters)', doc), 'characters');

        test.done();
    }
        
    ,"preceding:: axis works on document fragments": function (test) {
        var doc = new dom().parseFromString('<n />'),
            df = doc.createDocumentFragment(),
            root = doc.createElement('book');
            
        df.appendChild(root);
        
        for (var i = 0; i < 10; i += 1) {
            root.appendChild(doc.createElement('chapter'));
        }
        
        var chapter = xpath.select1("book/chapter[5]", df);
        
        assert.ok(chapter, 'chapter');
        
        assert.equal(xpath.select("count(preceding::chapter)", chapter), 4);
         
        test.done();
    }
    
    ,"node set sorted and unsorted arrays": function (test) {
        var doc = new dom().parseFromString('<book><character>Harry</character><character>Ron</character><character>Hermione</character></book>'),
            path = xpath.parse("/*/*[3] | /*/*[2] | /*/*[1]")
            nset = path.evaluateNodeSet({ node: doc }),
            sorted = nset.toArray(),
            unsorted = nset.toUnsortedArray();
            
        assert.equal(sorted.length, 3);
        assert.equal(unsorted.length, 3);
        
        assert.equal(sorted[0].textContent, 'Harry');
        assert.equal(sorted[1].textContent, 'Ron');
        assert.equal(sorted[2].textContent, 'Hermione');
        
        assert.notEqual(sorted[0], unsorted[0], "first nodeset element equal");        
        
        test.done();
    }
    
    // https://github.com/goto100/xpath/issues/32
    ,'supports contains() function on attributes': function (test) {
        var doc = new dom().parseFromString("<books><book title='Harry Potter and the Philosopher\"s Stone' /><book title='Harry Potter and the Chamber of Secrets' /></books>"),
            andTheBooks = xpath.select("/books/book[contains(@title, ' ')]", doc),
            secretBooks = xpath.select("/books/book[contains(@title, 'Secrets')]", doc);
            
        assert.equal(andTheBooks.length, 2);
        assert.equal(secretBooks.length, 1);
            
        test.done();
    }
}
