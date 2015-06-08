# Stereocode

## Description

Stereocode is a static analysis tool used with srcML in order to annotate methods with stereotypes.
Stereoctypes can be added as to the XML as an attribute or directly to the source code as a comment. Basic
analysis tools are available as part of the command-line interface such as stereotype function extraction,
and histogram generation based on the annotated stereotypes.

Currently, stereocode only works on C++ source code and based on srcML 0.9.5. Other languages annotations are
planned for future releases of stereocode.


srcML can be downloaded at: `http://www.srcml.org/`.


# Original Work
This work is a direct result of the work done previously:

Dragan, N., Collard, M.L., Maletic, J. I., "Automatic Identification of Class Stereotypes", in the Proceedings of the IEEE 26th IEEE International Conference on Software Maintenance (ICSM'10), Timisoara, Romania, Sept 12 - 18, 2010, pp. 10 pages.


## Stereotypes

* get
* nonconstget
* predicate
* property
* voidaccessor
* set
* command
* non-void-command
* collaborational-predicate
* collaborational-property
* collaborational-voidaccessor
* collaborational-command
* collaborator
* factory
* stateless
* pure_stateless
* empty


## Stereocode Command-Line Arguments


### -h, --help

Show the help message and exit.

### -i INPUT, --input INPUT

Specify the input file name which must be a srcML archive. Only one input file at a time is valid.
if the input file is not specified then stdin is used instead.

### -o [OUTPUT], --output [OUTPUT]

Specify the output file for an archive. The output archive will contain the annotations or redocumentation
unless -n or --no-redoc is used. If the output file isn't specified, stdout is used instead.


### -m {ReDocSrc,XmlAttr}, --mode {ReDocSrc,XmlAttr}

The annotation mode to use for processing source code. When added to the document stereotypes
are separated by a space. If not specified ReDocSrc is used.
There are two modes:

1) ReDocSrc
2) XmlAttr

**ReDocSrc** - Redocument source code and annotate it with comments before each method definition.
Comments take the form:

```C++
/** @stereotype ... */
```

Where the `...` is the method's stereotypes.



**XmlAttr** - Annotate the provided srcML's `<function>` elements with a `stereotype` attribute.
The comments take the following form:
```XML
<function stereotype="..."> ..Function contents.. </function>
```
Where the `...` is the method's stereotypes.


### -v, --verbose

Enables logging of debug information. This only exists for debugging stereocode and should be used.



### -t, --enable-timing

Outputs execution timing information to the console on the stderr stream.


### --histogram HISTOGRAM_PATH

Output a histogram count of the occurrences of all stereotypes that annotate functions
into the specified file path. The resulting number of occurrences is **NOT** the total
number of functions that were annotated. Stereotypes are tallied by counting their
occurrence from each function.


### --unique-histogram UNIQUE_HISTOGRAM_PATH

Outputs a histogram using the combination of stereotypes from each function as an
entry into the histogram. The total number of tallied stereotype occurrences **IS**
the total number of annotated functions within the system.



### -n, --no-redoc

No redoc or no redocumentation prevents the redocumentation of the input archive so that
provided static analysis tools can extract information from a srcML archive. This works
for extracting a function list, histogram, or unique histogram.


### -f FUNC_LIST_PATH, --extract-func-list FUNC_LIST_PATH

Extract a list of annotated functions, line numbers, etc... within the provided archive.
The function list output in a CSV format so that it can be viewed using other tools
such as excel or LibreOffice.

The CSV contains the following columns:
 * filename - The name of the file associated with the unit the function was located within.
 * function name - The actual name of the function. This includes namespace and class qualifiers.
 * function signature - The signature of the function.
 * stereotypes - A comma separated list of stereotypes within quotations.
 * archive line number - The line number within the archive that the function occurred within.
 * file line number - The line number relative to the start of the unit it occurred within.
 * class defined within - If the function was defined within a class or multiple classes those names are placed here separated by `::`.


### --remove-redoc
The removes a specified type of stereotype from an archive, based on the given mode.
Additional information can be collected before removeing stereotypes from an archive
such as histogram generation, or function list extraction.


## Heuristics Modifiers

Arguments that are used by stereocode to augment the way it matches methods, and assigns stereotypes.
Be aware that using these can alter the way that stereotypes are assigned to your source code.

### --ns-file NAMESPACE_PATH

A file containing the qualifiers to ignore when determining if a function is a method or free function.
Namespace qualifiers are specified per line.  File should contain a list of `::` namespace qualifiers
that appear before a functions name and could be mistaken for a class per line. The heuristic for matching method
definitions is "does the function name contain :: or is it within the body of a class, struct, or union?".
When a namespace prefix is specified, it changes the heuristic to exclude those functions whose qualifiers
are equal to one of those specified within the namespace file. This Only excludes functions that have the
qualifiers equal to one of those within the file.

For example

Namespace file: `namespace-file.txt`.
```txt
ns1::ns2
```

Source Code Example Pre-srcML (test.cpp):
```C++
void ns1::ns2::obj::print() const {
    std::cout << this->name() << std::endl;
}

void ns1::ns2::swap(obj& x,obj& y) {
    
}
```

Run through srcML (test.cpp.xml):
```XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<unit xmlns="http://www.srcML.org/srcML/src" xmlns:cpp="http://www.srcML.org/srcML/cpp" revision="0.8.0" language="C++" filename="test.cpp"><function><type><name>void</name></type> <name><name>ns1</name><operator>::</operator><name>ns2</name><operator>::</operator><name>obj</name><operator>::</operator><name>print</name></name><parameter_list>()</parameter_list> <specifier>const</specifier> <block>{
    <expr_stmt><expr><name><name>std</name><operator>::</operator><name>cout</name></name> <operator>&lt;&lt;</operator> <call><name><name>this</name><operator>-&gt;</operator><name>name</name></name><argument_list>()</argument_list></call> <operator>&lt;&lt;</operator> <name><name>std</name><operator>::</operator><name>endl</name></name></expr>;</expr_stmt>
}</block></function>

<function><type><name>void</name></type> <name><name>ns1</name><operator>::</operator><name>ns2</name><operator>::</operator><name>swap</name></name><parameter_list>(<parameter><decl><type><name>obj</name><modifier>&amp;</modifier></type> <name>x</name></decl></parameter>,<parameter><decl><type><name>obj</name><modifier>&amp;</modifier></type> <name>y</name></decl></parameter>)</parameter_list> <block>{
    
}</block></function>
</unit>
```

Command: `stereocode -i test.cpp.xml --ns-file namespace-file.txt -o test.ann.cpp.xml`


Run through stereocode (with namespace file and XML tags removed):
```C++
/** @stereotype voidaccessor stateless */
void ns1::ns2::obj::print() const {
    std::cout << this->name() << std::endl;
}

void ns1::ns2::swap(obj& x,obj& y) {
    
}
```



Command: `stereocode -i test.cpp.xml -o test.ann.cpp.xml`

Run through stereocode (without namespace file and XML tags removed):
```C++
/** @stereotype voidaccessor stateless */
void ns1::ns2::obj::print() const {
    std::cout << this->name() << std::endl;
}

/** @stereotype collaborator empty */
void ns1::ns2::swap(obj& x,obj& y) {
    
}
```

### --modifiers-file MODIFIERS_FILE_PATH
A file containing a list of modifiers that could be mistaken for types, such as macro names or compiler specific annotations.
The file should contain one modifier per line. This modifies the way in which some stereotypes are matched and handled, by
treating some things as type modifiers that would otherwise be considered a non-native type by stereocode, which can cause the
application of an incorrect stereotype.

For example:

modifiers.txt
```txt
EXPORT_MACRO
```

test.cpp
```C++
EXPORT_MACRO int ns1::ns2::obj::print() const {
    return var;
}
```

Stereocode with modifiers file and XML removed:
```C++
/** @stereotype get */
EXPORT_MACRO int ns1::ns2::obj::print() const {
    return var;
}
```

Stereocode without modifiers file and XML removed:
```C++
/** @stereotype get collaborator */
EXPORT_MACRO int ns1::ns2::obj::print() const {
    return 0;
}
```



### --native-types-file NATIVE_TYPES_FILE_PATH
The names of types that should be treated as native types while processing stereocode. One type per line.
This heuristic already includes most standard typedefs and all native type names for C++. Types that should
be included here are containers and other typedefs used throughout the system. This only requires the
name of the typedef and not and name qualifiers before it, in order to match the type.

For example,
native-types.txt
```txt
graph
```

Source code:
```C++
graph<int> obj::computation() {
    
}
```

Stereocode with native types file:
```C++
/** @stereotype empty */
graph<int> obj::computation() {
    
}
```

Stereocode without native types file:
```C++
/** @stereotype collaborator empty */
graph<int> obj::computation() {
    
}
```


### --ignorable-calls-file IGNORABLE_CALLS_FILE_PATH
A list of function or macro calls that can be excluded from the heuristics during
stereotype evaluation. One function name per line. This already includes all C++
cast functions. Functions that one should ignore is any macro that looks like a call,
a good example of this is a debugging function that only exists to output a message
during execution, and should alter the execution of the stereotype.

For example:
ignorable-calls.txt
```txt
DEBUG
```

Source Code:
```C++
int bar::foo() const {
    DEBUG("called var");
    return var;
    
}

```
Stereocode with ignorable calls file:
```C++
/** @stereotype nonconstget */
int bar::foo() const {
    DEBUG("called var");
    return var;
    
}

```

Stereocode without ignorable calls file:
```C++
/** @stereotype nonconstget non-void-command */
int bar::foo() const {
    DEBUG("called var", this->name);
    return var;
    
}

```