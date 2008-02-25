#characterSymbols.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Maps for character symbols.
@ivar characterSymbols: a dictionary of character-to-word mappings
@type characterSymbols: dict
@ivar blankList: a list of characters which should be treated as blank
@type blankList: list
"""

blankList=[' ','\n','\r','\0','',None]

names={
None:_("blank"),
"":_("blank"),
"\0":_("null"),
"\11":_("tab"),
"\n":_("line feed"),
"\r":_("carriage return"),
" ":_("space"),
"!":_("bang"),
'"':_("quote"),
"#":_("number"),
"$":_("dollar"),
"%":_("percent"),
"&":_("and"),
"'":_("tick"),
"(":_("left paren"),
")":_("right paren"),
"*":_("star"),
"+":_("plus"),
",":_("comma"),
"-":_("dash"),
".":_("dot"),
"/":_("slash"),
":":_("colon"),
";":_("semi"),
"<":_("less"),
"=":_("equals"),
">":_("greater"),
"?":_("question"),
"@":_("at"),
"[":_("left bracket"),
"\\":_("back slash"),
"]":_("right bracket"),
"^":_("caret"),
"_":_("underline"),
"`":_("graav"),
"{":_("left brace"),
"|":_("bar"),
"}":_("right brace"),
"~":_("tilda"),
u"\u2022":_("bullet"),
}
