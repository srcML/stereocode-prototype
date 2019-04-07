<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:src="http://www.srcML.org/srcML/src" 
    xmlns:cpp="http://www.srcML.org/srcML/cpp"
    xmlns:set="http://exslt.org/sets"
    xmlns:exsl="http://exslt.org/common"
    xmlns:str="http://exslt.org/strings"
    xmlns:regexp="http://exslt.org/regular-expressions"
    xmlns:func="http://exslt.org/functions"
    xmlns:dyn="http://exslt.org/dynamic"
    xmlns:src_old="http://www.sdml.info/srcML/src"
    extension-element-prefixes="exsl str func regexp"
    exclude-result-prefixes="set src dyn src_old"
    version="1.0">
<!-- 
@file stereotype.xsl

@copyright Copyright (C) 2013-2014 srcML, LLC. (www.srcML.org)

The stereocode is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

The stereocode Toolkit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the stereocode Toolkit; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 -->
    <!--

To identify the stereotype Accessor::Get the following conditions need to be satisfied: 
  • method is const 
  • returns a data member 
  • return type is primitive or container of a primitives 

To identify the stereotype Accessor::Predicate the following conditions need to be satisfied: 
  • method is const 
  • returns a Boolean value that is not a data member 

To identify the stereotype Accessor::Property the following conditions need to be satisfied: 
  • method is const 
  • does not return a data member 
  • return type is primitive or container of primitives 
  • return type is not Boolean 

To identify the stereotype Mutator::Set the following conditions need to be satisfied: 
  • method is not const 
  • return type is void or Boolean 
  • only one data member is changed 

To identify the stereotype Mutator::Command the following conditions need to be satisfied: 
  • method is not const 
  • return type is void or Boolean 
  • complex change to the object’s state is performed 
  e.g., more than one data member was changed 

To identify the stereotype Collaborator one of the following statements needs to be satisfied: 
  • returns void and at least one of the method’s 
    parameters or local variables is an object 
  • returns a parameter or local variable that is an 
    object 

To identify the stereotype Creator::Factory the following conditions need to be satisfied: 
  • returns an object created in the method’s body
     -->
  <!--
    Global/Constant Variables
  -->
  <!-- current encoding (XSLT cannot obtain internally) -->
  <xsl:param name="encoding" select="ISO-8859-1"/>
  <xsl:param name="processing_mode">ReDocSrc</xsl:param>
  <xsl:param name="more_namespaces"></xsl:param>
  <xsl:param name="more_native"></xsl:param>
  <xsl:param name="more_modifiers"></xsl:param>
  <xsl:param name="more_ignorable_calls"></xsl:param>

  <!-- <xsl:param name="" select=""/> -->
  <!-- provide identity transformation -->
  <xsl:output method="xml" encoding="ISO-8859-1"/>

  <!-- end of line -->
  <xsl:variable name="eol">
<xsl:text>
</xsl:text>
  </xsl:variable>

  <xsl:variable name="namespaces" select="str:split($more_namespaces)"/>

  <!--
      Definition of native types.  Additional types can be declared in
      the variable more_types
  -->
  <xsl:variable name="native" select="str:split(concat('int long double float string char unsigned signed wchar_t char16_t char32_t bool vector list map ', $more_native))"/>

  <!--
      Definition of names that occur in types, but are modifiers, etc.
      More types can be declared in the variable more_modifiers
  -->
  <xsl:variable name="modifiers" select="str:split(concat('std void emit virtual inline static const ', $more_modifiers))"/>

  <!--
      Definition of calls that aren't really calls, e.g., dynamic_cast.
      More types can be declared in the variable more_modifiers
  -->
  <xsl:variable name="ignorable_calls" select="str:split(concat('assert static_cast const_cast dynamic_cast reinterpret_cast ', $more_ignorable_calls))"/>

  <!-- 
    Namespace matching function
  -->
  <func:function name="src:str-join">
    <xsl:param name="collection"/>
    <xsl:param name="index"/>
    <xsl:param name="length"/>
    <func:result select="src:str-join_impl($collection, $index, $length)"/>
  </func:function>

  <func:function name="src:str-join_impl">
    <xsl:param name="collection"/>
    <xsl:param name="index"/>
    <xsl:param name="length"/>
    <xsl:variable name="next_value" select="translate(normalize-space(($collection)[$index]), ' ', '')"/>
    <xsl:choose>
      <xsl:when test="$index &lt; $length">
        <func:result select="concat($next_value, src:str-join_impl($collection, $index + 1, $length))"/>
      </xsl:when>
      <xsl:otherwise>
        <func:result select="$next_value"/>
      </xsl:otherwise>
    </xsl:choose>
  </func:function>

  <func:function name="src:has_namespace_prefix">
    <xsl:param name="func"/>
    <xsl:choose>
      <xsl:when test="$namespaces != ''">
        <xsl:choose>
          <xsl:when test="count($func/src:name/*) >= 2">
            <xsl:variable name="func_name" select="src:str-join($func/src:name/*, 1, (count($func/src:name/*) - 2))"/>
            <func:result select="$func_name = $namespaces"/>
          </xsl:when>
          <xsl:otherwise>
            <func:result select="false()" />
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        <func:result select="false()"/>
      </xsl:otherwise>
    </xsl:choose>
  </func:function>



  <!--
    Functions - For stereotype matching.
  -->

  <!--
    pure virtual function declaration
  -->
  <func:function name="src:isvirtual">
    <xsl:param name="function"/>

    <func:result select="normalize-space($function/src:specifier[last()])='= 0'"/>
  </func:function>

  <!--
    locate all top-level function
  -->
  <func:function name="src:function">

    <func:result select="ancestor-or-self::src:function[1]"/>

  </func:function>

  <!--
    return the name of a class to a function/method.
  -->
  <func:function name="src:class_name">

    <func:result select="src:function()/src:name/src:name[1]"/>

  </func:function>

  <!--
    Locate all return expressions within a function.
  -->
  <func:function name="src:return">

    <func:result select="src:function()/src:block/descendant::src:return/src:expr"/>

  </func:function>

  <!--
    Get the names of all parameters.
  -->
  <func:function name="src:param_name">

    <func:result select="src:final_name(src:function()/src:parameter_list/src:parameter/src:decl/src:name)"/>

  </func:function>

  <!--
    Identifiers in parameter types
  -->
  <func:function name="src:param_type_name">

    <func:result select="src:all_type_names(src:function()/src:parameter_list/src:parameter/src:decl/src:type/src:name)"/>

  </func:function>

  <!--
    Identifiers in declaration types
  -->
  <func:function name="src:decl_type_name">

    <func:result select="src:all_type_names(src:function()/src:block/descendant::src:decl_stmt/src:decl/src:type/src:name)"/>

  </func:function>

  <!-- variable names in declarations (not including parameters)  -->
  <func:function name="src:decl_name">

    <func:result select="src:final_name(src:function()/src:block/descendant::src:decl/src:name)"/>

  </func:function>

  <!-- 
    Check for the type of a variable.
  -->
  <func:function name="src:variable_type">
     <xsl:param name="context"/>

    <func:result select="src:function()/descendant::src:decl[src:name=$context]/src:type"/>

  </func:function>

  <!--
    Returns the last name in a list of names, that isn't a nested list of names.
  -->
  <func:function name="src:final_name">
    <xsl:param name="cur"/>

    <func:result select="$cur/self::src:name[not(src:name)] | $cur/self::src:name/src:name[1]"/>

  </func:function>

  <!--
    The object being used to make the call.
  -->
  <func:function name="src:calling_object">
    <xsl:param name="context" select="."/>

    <func:result select="src:final_name(self::*[not(src:is_pure_call())]/preceding-sibling::*[2][self::src:name])"/>

  </func:function>

  <!--
    Check if a data member is being written into.
  -->
  <func:function name="src:data_members_write">

    <func:result select="src:expr_stmt_name()[src:is_written() and src:is_data_member()]"/>

  </func:function>

  <!-- 
    Check if there is a data member being written into.
  -->
  <func:function name="src:one_data_members_write">

    <func:result select="src:expr_stmt_name()[src:is_written() and src:is_data_member()][1]"/>

  </func:function>

  <!--
    Test to see if a variable is a data member of a class.
  -->
  <func:function name="src:data_members">

    <func:result select="src:function()/src:block/descendant::src:expr/src:name[src:is_data_member()]"/>

  </func:function>

  <!--
    Returns the first data member like the data_members function.
  -->
  <func:function name="src:one_data_members">

    <func:result select="src:function()/src:block/descendant::src:expr/src:name[src:is_data_member()][1]"/>

  </func:function>

  <!--
    Check if something is static.
  -->
  <func:function name="src:is_static">

    <func:result select="src:name/src:name[1] and src:name/src:name[1]!=src:class_name()"/>

  </func:function>


  <!--
    Check if a function is a data member.
  -->
  <func:function name="src:is_data_member">

    <func:result select="not(.=src:param_name() or .=src:decl_name() or
             (.//src:operator='::' and not(./src:name[1]=src:class_name())))"/>

  </func:function>

  <!--
    Check if a variable is declared as part of a method.
  -->
  <func:function name="src:is_declared">

    <func:result select=".=src:param_name() or .=src:decl_name()"/>

  </func:function>

  <!--
    Variable name in expression (including return expressions).
  -->
  <func:function name="src:expr_name">

    <func:result select="src:function()/descendant::src:expr/src:name"/>

  </func:function>

  <!--
    Variable name in expression statements
  -->
  <func:function name="src:expr_stmt_name">

    <func:result select="src:final_name(src:function()/src:block/descendant::src:expr_stmt/src:expr/src:name)"/>

  </func:function>

  <!--
    Variable name in expression statements.
  -->
  <func:function name="src:call">

    <func:result select="src:function()/src:block/descendant::src:expr/src:call"/>

  </func:function>

  <!--
    Make sure that the call is not a call to a constructor.
  -->
  <func:function name="src:real_call">

    <func:result select="src:function()/src:block/descendant::src:expr/src:call[
             not(src:name[.=$ignorable_calls]) and
             not(src:name/src:name[1][.=$ignorable_calls]) and
                         not(preceding-sibling::*[1][self::src:operator='new']) and
             not(ancestor::src:throw) and
             not(src:name[src:is_native_type()]) and
             not(src:name/src:name[1][src:is_native_type()])
  ]"/>

  </func:function>


  <!-- 
    Check if the call is a stateless one.
  -->
  <func:function name="src:stateless_real_call">

    <func:result select="src:function()/src:block/descendant::src:expr/src:call[
             not(src:name[.=$ignorable_calls]) and
             not(src:name/src:name[1][.=$ignorable_calls]) and
             not(ancestor::src:throw) and
             not(src:name[src:is_native_type()]) and
             not(src:name/src:name[1][src:is_native_type()])
  ]"/>

  </func:function>


  <!--
    Returns the first real call.
  -->
  <func:function name="src:one_real_call">

    <func:result select="src:function()/src:block/descendant::src:expr/src:call[
             not((src:name | src:name/src:name)[.=$ignorable_calls]) and
                         not(preceding-sibling::*[1][self::src:operator='new']) and
             not(ancestor::src:throw) and
             not((src:name | src:name/src:name[1])[src:is_native_type()])
  ][1]"/>

  </func:function>

  <!--
      Primary variable name.

      Either the direct name, or for a complex name with multiple subnames, the last one.

      E.g.,

          a  -> a
          b::a -> a
          c::b::a -> a
  -->
  <func:function name="src:primary_variable_name">
     <xsl:param name="context"/>

     <func:result select="$context[not(src:name)] | $context/src:name[last()]"/>

  </func:function>

  <!--
      All names in a type

      Includes a direct name, or for a complex name, multiple subnames.
      E.g.,

          a  -> a
          b::a -> b
    std::a -> a
    a<b> -> {a, b}
    a<b<c> > -> {a, b, c}
  -->
  <func:function name="src:all_type_names">
     <xsl:param name="context"/>

     <func:result select="$context[not(src:name) and not(.='std')] |
        $context//src:name[not(src:name) and not(.='std') and
        not(preceding-sibling::src:name[1][not(.='std')])]"/>

  </func:function>

  <!-- 
    A derivative of all_type_names not sure what this does.
  -->
  <func:function name="src:all_type_names_nonclass_object">
     <xsl:param name="context"/>
     <xsl:param name="class"/>

     <func:result select="$context[not(src:name)][not(.='std') and not(.=$class) and src:is_object()] |
        $context//src:name[not(src:name) and not(.='std') and
        not(preceding-sibling::src:name[1][not(.='std')]) and not(.=$class) and src:is_object()]"/>

  </func:function>


  <!--
    Type name is a native type
  -->
  <func:function name="src:is_native_type">

     <func:result select=".=$native"/>

  </func:function>

  <!-- 
    Not sure if this is necessary anymore because modifier has been migrated into
    the src namespace.
  -->
<!--   <func:function name="src:is_modifier">

     <func:result select=".=$modifiers"/>

  </func:function> -->


  <!-- 
    Not sure what this means exactly.
  -->
  <func:function name="src:is_pure_call">

     <func:result select="not(preceding-sibling::*[1][self::src:operator='.' or self::src:operator='-&gt;'])"/>

  </func:function>

  <!--  -->
  <func:function name="src:is_object">

     <func:result select="not(.=$modifiers or .=$native)"/>

  </func:function>

  <!-- -->
  <func:function name="src:is_written">

    <func:result select="following-sibling::*[1][contains(self::src:operator, '=') or
             self::src:operator='&lt;&lt;' or
             self::src:operator='&gt;&gt;'
             ]"/>

  </func:function>

  <!--
    Union two lists together.
  -->
  <func:function name="src:union">
    <xsl:param name="first"/>
    <xsl:param name="second"/>

    <func:result select="$first | $second"/>

  </func:function>


  <!--
    Used for calculating whitespace indentation level.
  -->
  <func:function name="src:last_ws">
    <xsl:param name="s"/>

    <xsl:choose>
      <xsl:when test="contains($s, '&#xa;')">
        <func:result select="src:last_ws(substring-after($s, '&#xa;'))"/>
      </xsl:when>
      <xsl:otherwise>
        <func:result select="$s"/>
      </xsl:otherwise>
    </xsl:choose>
  </func:function>

  <!--
    Stereotype matching function
    Classifies stereotypes using criteria on function definition

  -->
<xsl:template match="src:function" mode="stereotype">
    <xsl:apply-templates select="." mode="get"/>
    <xsl:apply-templates select="." mode="nonconstget"/>
    <xsl:apply-templates select="." mode="predicate"/>
    <xsl:apply-templates select="." mode="property"/>
    <xsl:apply-templates select="." mode="voidaccessor"/>
    <xsl:apply-templates select="." mode="set"/>
    <xsl:apply-templates select="." mode="command"/>
    <xsl:apply-templates select="." mode="non-void-command"/>
    <xsl:apply-templates select="." mode="collaborational-predicate"/>
    <xsl:apply-templates select="." mode="collaborational-property"/>
    <xsl:apply-templates select="." mode="collaborational-voidaccessor"/>
    <xsl:apply-templates select="." mode="collaborational-command"/>
    <xsl:apply-templates select="." mode="collaborator"/>
    <xsl:apply-templates select="." mode="factory"/>
    <xsl:apply-templates select="." mode="stateless"/>
    <xsl:apply-templates select="." mode="pure_stateless"/>
    <xsl:apply-templates select="." mode="empty"/>
    <xsl:apply-templates select="." mode="boolean_verifier"/>
    <xsl:apply-templates select="." mode="equality_verifier"/>
    <xsl:apply-templates select="." mode="doubles_equality_verifier"/>
    <xsl:apply-templates select="." mode="exception_verifier"/>
    <xsl:apply-templates select="." mode="no_exception_verifier"/>
    <xsl:apply-templates select="." mode="assertion_verifier"/>
    <xsl:apply-templates select="." mode="test_cleaner"/>
    <xsl:apply-templates select="." mode="test_initializer"/>
    <xsl:apply-templates select="." mode="utility_verifier"/>
    <xsl:apply-templates select="." mode="hybrid_verifier"/> 
    <xsl:apply-templates select="." mode="unclassified"/> 
    <xsl:apply-templates select="." mode="branch_verifier"/>
    <xsl:apply-templates select="." mode="iterative_verifier"/>
    <xsl:apply-templates select="." mode="execution_tester"/>
    <xsl:apply-templates select="." mode="api_utility_verifier"/>
    <xsl:apply-templates select="." mode="public_field_verifier"/>
  </xsl:template>



  <!-- Accessors -->

  <!-- stereotype get 

       method is const

       return type is not void

       contains at least one return statement which is:

              a single variable
        pointer to a variable
              has no calls
              variable is a data member

      in other words, it is of the form:

                 return n;
                 return *n;

      where the n is a data member.
  -->
  <xsl:template match="src:function[

         src:specifier='const' and

         not(src:type[src:name='void']) and

         src:return()[
                    (count(*)=1 and src:name or
           count(*)=2 and *[1][self::src:operator='*'] and *[2][self::src:name]) and

                    src:primary_variable_name(src:name)[src:is_data_member()]][1]

         ]" mode="get">get </xsl:template>

  <xsl:template match="src:function" mode="get"/>

  <xsl:template match="src:function[

         not(src:specifier='const') and

         not(src:type[src:name='void']) and

               not(src:data_members()[src:is_written()]) and 

         src:return()[
                    (count(*)=1 and src:name or
           count(*)=2 and *[1][self::src:operator='*'] and *[2][self::src:name]) and

                    src:primary_variable_name(src:name)[src:is_data_member() and not(.='this')]][1]

         ]" mode="nonconstget">nonconstget </xsl:template>

  <xsl:template match="src:function" mode="nonconstget"/>

  <!-- stereotype predicate 

       method is const

       return type includes bool
       
       data members are used or there is a pure call or call on data members

       at least one return expression contains:

        false
        true
        no variable, or more then one variable
        call
        variable plus an operators
        one of the variables is not a data member
  -->
  <xsl:template match="src:function[

         src:specifier='const' and
           
               src:type/src:name='bool' and
               
               (src:data_members() or
                      
                          (src:real_call()[src:is_pure_call() and 
                 
                            (not(src:name/src:operator='::') or src:name/src:name[1]=src:class_name()) or
                             
                                src:calling_object()[src:is_data_member()]]
                        )
         ) and 
           
         src:return()[

                     .='false' or .='true' or

                     src:call[1] or

                     count(src:name)!=1 or

                     *[2][self::src:operator] or

                     src:primary_variable_name(src:name)[src:is_declared()]][1]

         ]" mode="predicate">predicate </xsl:template>

  <xsl:template match="src:function" mode="predicate"/>

  <!-- stereotype property

       method is const

       return type is not void or bool
       
       data members are used or data or there is a pure call or call on data members 
       
       return expression contains one of the following:

           more then one variable, or no variables
     a call
     single variable with an operator
     single variable that is not a data member
  -->
  <xsl:template match="src:function[

         src:specifier='const' and
           
               not(src:type[src:name='void' or src:name='bool']) and
               
               
               (src:data_members() or
               
                  (src:real_call()[src:is_pure_call() and 
          
                      (not(src:name/src:operator='::') or src:name/src:name[1]=src:class_name()) or
                       
                          src:calling_object()[src:is_data_member()]]
                  )
         ) and 
                        
           
         src:return()[1] and
           
               not(src:return()[
        not(
            *[2][self::src:operator] or

            src:call[1] or

                        count(src:name)!=1 or

                        src:primary_variable_name(src:name)[src:is_declared()]
         )
         ][1])

              ]" mode="property">property </xsl:template>

  <xsl:template match="src:function" mode="property"/>

  <!-- stereotype voidaccessor 

       specifier is const
       
       data members are used

       return is void (??? void * allowed ???)
  -->
  <xsl:template match="src:function[

               src:specifier='const' and 
               
               (src:data_members() or
                      
                          (src:real_call()[src:is_pure_call() and 
                 
                            (not(src:name/src:operator='::') or src:name/src:name[1]=src:class_name()) or
                             
                                src:calling_object()[src:is_data_member()]]
                        )
         ) and  
               
               src:type/src:name='void'
         ]
         " mode="voidaccessor">voidaccessor </xsl:template>

  <xsl:template match="src:function" mode="voidaccessor"/>


  <!-- Mutators -->

  <!-- stereotype set 

       method is not const

       return type is void or bool, or return the object (for chaining), i.e., 'return *this'

       number of real calls in expression statements is at most 1

       number of data members written to in expression statements is 1
  -->
  <xsl:template match="src:function[

               not(src:specifier='const') and

               (src:type[src:name='void' or src:name='bool'] or

                 count(src:return())=count(src:return()[
               count(*)=2 and *[1][self::src:operator='*'] and *[2][self::src:name='this']])

               ) and

         not(src:real_call()[2]) and

         count(src:data_members_write())=1
              ]
              " mode="set">set </xsl:template>

  <xsl:template match="src:function" mode="set"/>

  <!-- stereotype command

       method is not const

       return type contains void or bool

       for expression statements at least one of the following holds:

           more then one data member is written to

           exactly one data member is written to and the number of calls
     in expression statements or returns is at least 2

           no data members are written to and their is a call not
     in a throw statement that is a simple real call (not a constructor call)
     or a complex call for a data member

           Note:  A set is formed by src:union with the written data members and the
     src:type.  This way, the predicate is always evaluated, even if there are
     no data members written.  The actual number of data members written is one
     less then last().  So, "last()=1 and ..." is evaluated when there are no
     data members written.
  -->
  <xsl:template match="src:function[

               not(src:specifier='const') and

               src:type[src:name='void' or src:name='bool'] and

               src:union(src:data_members_write(), src:type)[

                   last()&gt;2 or last()=2 and src:real_call()[2] or last()=1 and

       src:real_call()[

           src:is_pure_call() and

           not(src:is_static()) or src:calling_object()[src:is_data_member()][1]
       ][1]
               ][1]
        ]" mode="command">command </xsl:template>

  <xsl:template match="src:function" mode="command"/>

  <!-- stereotype non-void-command

       method is not const

       return type is not void or bool (??? void* ???)

       for expression statements at least one of the following holds:

           more then one data member is written to

           exactly one data member is written to and the number of real calls
     is at least 2

           no data members are written to and their is a call not
     in a throw statement that is a simple real call (not a constructor call from new)
     or a complex call for a data member

           Note:  A set is formed by src:union with the written data members and the
     src:type.  This way, the predicate is always evaluated, even if there are
     no data members written.  The actual number of data members written is one
     less then last().  So, "last()=1 and ..." is evaluated when there are no
     data members written.
  -->
  <xsl:template match="src:function[

               not(src:specifier='const') and

               not(src:type[src:name='void' or src:name='bool']) and

               src:union(src:data_members_write(), src:type)[

                    last()&gt;2 or last()=2 and src:real_call()[2] or last()=1 and

                    src:real_call()[src:is_pure_call() and
                        not(src:is_static()) or src:calling_object()[src:is_data_member()][1]][1]][1]

              ]
              " mode="non-void-command">non-void-command </xsl:template>

  <xsl:template match="src:function" mode="non-void-command"/>


  <!-- Controllers -->


  <!-- stereotype collaborational-predicate 

       method is const

       return type includes bool
       
       data members are not used
       
       no pure calls, a() a::b(); no calls on data members 

       at least one return expression contains:

        false
        true
        no variable, or more then one variable
        call
        variable plus an operators
        one of the variables is not a data member
  -->
  <xsl:template match="src:function[

         src:specifier='const' and
           
               src:type/src:name='bool' and
               
               not(src:data_members()) and
               
               not(
                            src:real_call()[src:is_pure_call() and 
               
                          (not(src:name/src:operator='::') or src:name/src:name[1]=src:class_name()) or
               
                          src:calling_object()[src:is_data_member()]]
         ) and 
           
         src:return()[

                     .='false' or .='true' or

                     src:call[1] or

                     count(src:name)!=1 or

                     *[2][self::src:operator] or

                     src:primary_variable_name(src:name)[src:is_declared()]][1]

         ]" mode="collaborational-predicate">collaborational-predicate </xsl:template>

  <xsl:template match="src:function" mode="collaborational-predicate"/>

  <!-- stereotype collaborational-property

       method is const

       return type is not void or bool
       
       data members are not used
       
       no pure calls, a() a::b(); no calls on data members 

       return expression contains one of the following:

           more then one variable, or no variables
     a call
     single variable with an operator
     single variable that is not a data member
  -->
  <xsl:template match="src:function[

         src:specifier='const' and
           
               not(src:type[src:name='void' or src:name='bool']) and
           
         not(src:data_members()) and
         
         not(
                      src:real_call()[src:is_pure_call() and 
         
                    (not(src:name/src:operator='::') or src:name/src:name[1]=src:class_name()) or
         
                    src:calling_object()[src:is_data_member()]]
         ) and 
         
         src:return()[1] and
           
               not(src:return()[
        not(
            *[2][self::src:operator] or

            src:call[1] or

                        count(src:name)!=1 or

                        src:primary_variable_name(src:name)[src:is_declared()]
         )
         ][1])

              ]" mode="collaborational-property">collaborational-property </xsl:template>

  <xsl:template match="src:function" mode="collaborational-property"/>


  <!-- stereotype collaborational-voidaccessor 

       specifier is const
       
       data members are not used
       
       no pure calls, a() a::b(); no calls on data members 

       return is void (??? void * allowed ???)
  -->
  <xsl:template match="src:function[

               src:specifier='const' and 
               
               not(src:data_members()) and
         
         not(
                      src:real_call()[src:is_pure_call() and 
         
                    (not(src:name/src:operator='::') or src:name/src:name[1]=src:class_name()) or
         
                    src:calling_object()[src:is_data_member()]]
         ) and  
               
               src:type/src:name='void'
               ]
         " mode="collaborational-voidaccessor">collaborational-voidaccessor </xsl:template>

  <xsl:template match="src:function" mode="collaborational-voidaccessor"/>


  <!-- stereotype collaborational-command

       method is not const

       no data members are written

       (
       (one or more calls:

           no pure calls, a() a::b()

           no calls on data members)

       or parameter or local variable is written
       )

      Calls allowed:  f->g() where f is not a data member, new f() (which isn't a real call)
  --> 
  <xsl:template match="src:function[

               not(src:specifier='const') and

         not(src:one_data_members_write()) and

               not(
              src:real_call()[src:is_pure_call() and 

              (not(src:name/src:operator='::') or src:name/src:name[1]=src:class_name()) or

              src:calling_object()[src:is_data_member()]]
         ) and 

               (src:one_real_call()

               or

               src:expr_name()[src:is_written() and src:primary_variable_name(.)[not(src:is_data_member())]] or

               src:block//src:decl[src:type/src:name[src:is_object()]][src:init]
               )
              ]
        " mode="collaborational-command">collaborational-command </xsl:template>
        

  <xsl:template match="src:function" mode="collaborational-command"/>


  <!-- stereotype collaborator 

       A type name is an object, but not of this class
  -->                                                                                 
  <xsl:template match="src:function[

                src:all_type_names_nonclass_object(.//src:type/src:name, src:class_name())[1]
               ]
         " mode="collaborator">collaborator </xsl:template>

  <xsl:template match="src:function" mode="collaborator"/>


  <!-- Factory -->

  <!-- stereotype factory

       return type includes pointer to object

       a return statement includes a new operator, or a variable which is a parameter or a local variable
  -->
  <xsl:template match="src:function[

                src:type[src:modifier='*' and src:name[src:is_object()]] and
          
                src:return()[

              src:operator='new' or

        src:primary_variable_name(src:name)[src:is_declared()]
          ][1]
               ]
         " mode="factory">factory </xsl:template>

  <xsl:template match="src:function" mode="factory"/>


  <!-- Degenerate  -->    


  <!-- stereotype stateless
       
       includes at least one non-comment statement

       one real call (including new calls)

       no data members used (except for read on 'this')
  -->
  <xsl:template match="src:function[

                src:block/*[not(self::src:comment)][1] and

          count(src:stateless_real_call())=1 and

          not(src:data_members()[not(.='this' and not(src:is_written()))])

         ]" mode="stateless">stateless </xsl:template>

  <xsl:template match="src:function" mode="stateless"/>

  <!-- stereotype pure_stateless
       
       includes at least one non-comment statement

       no real calls (including new calls)

       no data members used
          not(src:stateless_real_call()) and
  -->
  <xsl:template match="src:function[

                src:block/*[not(self::src:comment)][1] and

                (
          count(src:block/src:return) + count(src:block/src:throw) +
          count(src:block/src:expr_stmt[.//src:expr/src:call/src:name='assert']))=
          count(src:block/*[not(self::src:comment)]) and

                not(src:block/src:return//src:name) and 

          not(src:data_members())

         ]" mode="pure_stateless">pure_stateless </xsl:template>

  <xsl:template match="src:function" mode="pure_stateless"/>

  <!-- stereotype empty

       no statements, except for comments
  -->
  <xsl:template match="src:function[

          not(src:block/*[not(self::src:comment)][1])

         ]" mode="empty">empty </xsl:template>

  <xsl:template match="src:function" mode="empty"/>

<xsl:template match="src:function[descendant::src:block[descendant::src:name='CPPUNIT_ASSERT' or 
        descendant::src:name='CPPUNIT_ASSERT_MESSAGE']]" 
        mode="boolean_verifier">boolean_verifier </xsl:template>
<xsl:template match="src:function" mode="boolean_verifier"/>

<xsl:template match="src:function[descendant::src:block[descendant::src:name='CPPUNIT_FAIL']]" 
  mode="utility_verifier">utility_verifier </xsl:template>
<xsl:template match="src:function" mode="utility_verifier"/>
  
  <xsl:template match="src:function[descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_EQUAL' or 
    descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE']]" 
    mode="equality_verifier">equality_verifier </xsl:template>
<xsl:template match="src:function" mode="equality_verifier"/>

  <xsl:template match="src:function[descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL' or 
    descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE']]" 
    mode="doubles_equality_verifier">doubles_equality_verifier </xsl:template>
<xsl:template match="src:function" mode="doubles_equality_verifier"/>

  <xsl:template match="src:function[descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']]" 
    mode="exception_verifier">exception_verifier </xsl:template>
<xsl:template match="src:function" mode="exception_verifier"/>

<xsl:template match="src:function[descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']]" 
  mode="no_exception_verifier">no_exception_verifier </xsl:template>
<xsl:template match="src:function" mode="no_exception_verifier"/>

<xsl:template match="src:function[descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL' or 
  descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS']]" mode="assertion_verifier">assertion_verifier </xsl:template>
<xsl:template match="src:function" mode="assertion_verifier"/>

<xsl:template match="src:function[src:name='setUp' or src:name[src:name='setUp']]" mode="test_initializer">test_initializer </xsl:template>
<xsl:template match="src:function" mode="test_initializer"/>

<xsl:template match="src:function[src:name='tearDown' or src:name[src:name='tearDown']]" mode="test_cleaner">test_cleaner </xsl:template>
<xsl:template match="src:function" mode="test_cleaner"/>



<xsl:template match="src:function[
  (
  round(count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) div (count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) + 1)) + 
  round(count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) div (count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 1)) + 
  round(count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) div (count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')])+ 1)) + 
  round(count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) div (count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 1)) + 
  round(count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) div (count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 1))+ 
  round(count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) div (count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 1))+ 
  round(count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')]) div (count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')]) + 1)) &gt; 1)
    ]" mode="hybrid_verifier">hybrid_verifier </xsl:template>
<xsl:template match="src:function" mode="hybrid_verifier"/>

<xsl:template match="src:function[
  (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')]) = 0) and not(src:name='setUp') and 
  not(src:name='tearDown') and not(src:name[src:name='setUp']) and 
  not(src:name[src:name='tearDown'])]" mode="unclassified">unclassified </xsl:template>
<xsl:template match="src:function" mode="unclassified"/>

<xsl:template match="src:function[descendant::src:if/src:then[
   (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')])  &gt; 0
  )]
  or descendant::src:elseif[
   (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')])  &gt; 0
  )]
  or descendant::src:else[
   (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')])  &gt; 0
  )] 
  ]" mode="branch_verifier">branch_verifier </xsl:template>
<xsl:template match="src:function" mode="branch_verifier"/>

<xsl:template match="src:function[descendant::src:for[
   (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')])  &gt; 0
  )] 
  or descendant::src:while[
   (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')])  &gt; 0
  )]
  or descendant::src:do[
  (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')])  &gt; 0
  )]
  ]" mode="iterative_verifier">iterative_verifier </xsl:template>
<xsl:template match="src:function" mode="iterative_verifier"/>

<xsl:template match="src:function[descendant::src:expr/src:call[descendant::src:operator='.'] 
  and not(descendant::src:name='setUp') and not(descendant::src:name='tearDown') and 
   (
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT') or 
        (descendant::src:name='CPPUNIT_ASSERT_MESSAGE')]) +
  count(descendant::src:block[(descendant::src:name='CPPUNIT_FAIL')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL') or 
    (descendant::src:name='CPPUNIT_ASSERT_DOUBLES_EQUAL_MESSAGE')]) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_THROW']) + 
  count(descendant::src:block[descendant::src:name='CPPUNIT_ASSERT_NO_THROW']) + 
  count(descendant::src:block[(descendant::src:name='CPPUNIT_ASSERT_ASSERTION_FAIL') or 
  (descendant::src:name='CPPUNIT_ASSERT_ASSERTION_PASS')])=0)
  ]" 
  mode="execution_tester">execution_tester </xsl:template>
<xsl:template match="src:function" mode="execution_tester"/>


<xsl:template match="src:function[descendant::src:expr_stmt/src:expr/src:call[contains(src:name,'CPPUNIT_ASSERT')]/descendant::src:expr/descendant::src:name[src:operator='.']]" mode="public_field_verifier">
    <xsl:variable name="object_name" select="descendant::src:expr_stmt/src:expr/src:call/descendant::src:expr/descendant::src:name/src:name"/>
    <xsl:if test="descendant::src:decl_stmt/src:decl/src:name = $object_name">
        <xsl:variable name="name_of_class" select="descendant::src:decl_stmt/src:decl/src:type/src:name"/>
          <xsl:if test="not(/src:unit/src:class/src:name = $name_of_class)">public_field_verifier </xsl:if>
    </xsl:if>
  </xsl:template>
<xsl:template match="src:function" mode="public_field_verifier"/>

<xsl:template match="src:function[descendant::src:expr_stmt/src:expr]" mode="api_utility_verifier">
  <xsl:if test="descendant::src:expr_stmt/src:expr[not(src:operator)]/src:call[not(contains(src:name,'CPPUNIT')) and not(src:argument_list='()')]/src:name[not(src:operator)]">api_utility_verifier </xsl:if>
</xsl:template>
<xsl:template match="src:function" mode="api_utility_verifier"/>
  <!--
      Section responsible for actually applying all of the stereotypes and annotating
      the source code with a comment.
  -->
  <!-- annotate function declaration/definition with passed definition  -->
  <xsl:template match="src:function[(src:name/src:operator[.='::'] and not(src:has_namespace_prefix(.)))or ancestor::src:class or ancestor::src:struct or ancestor::src:interface or ancestor::annotation_defn or ancestor::src:union]">

    <!-- calculate stereotype -->
    <xsl:variable name="stereotype">
      <xsl:apply-templates select="." mode="stereotype_list"/>
    </xsl:variable>

    <!-- insert stereotype comment -->
    <xsl:choose>
      <xsl:when test="$processing_mode='ReDocSrc'">
        <comment xmlns="http://www.srcML.org/srcML/src" type="block">/** @stereotype <xsl:value-of select="$stereotype"/>*/</comment>
        <xsl:value-of select="$eol"/>

        <!-- calculate the indent currently on the declaration so we can duplicate it on the comment -->
        <xsl:variable name="indent" select="src:last_ws(preceding-sibling::text()[1])"/>
       
        <!-- insert indentation -->
        <xsl:value-of select="$indent"/>

        <!-- copy of function -->
        <xsl:copy>
          <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
      </xsl:when>
      <xsl:when test="$processing_mode='XmlAttr'">
        <xsl:copy>
          <xsl:attribute name="stereotype">
            <xsl:value-of select="$stereotype"/>
          </xsl:attribute>
          <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
      </xsl:when>
      <xsl:otherwise>
           <xsl:message terminate="yes">ERROR: Unknown processing mode.</xsl:message>
      </xsl:otherwise>
    </xsl:choose>

  </xsl:template>


  <!-- classifies stereotypes using criteria from stereotypes.xsl -->
  <xsl:template match="src:function" mode="stereotype_list">
    <xsl:variable name="raw_stereotype"><xsl:apply-templates select="." mode="stereotype"/></xsl:variable>
    <xsl:choose>
      <xsl:when test="$raw_stereotype!=''"><xsl:value-of select="$raw_stereotype"/></xsl:when>
      <xsl:otherwise>unclassified </xsl:otherwise>
    </xsl:choose>

  </xsl:template>

  <xsl:template match="/src_old:unit">
    <xsl:message terminate="yes">ERROR: Newer version of srcML required.</xsl:message>
  </xsl:template>

  <xsl:template match="src:unit[number(concat(str:split(@revision, '.'),'')) >= 95]">
    <xsl:message terminate="yes">ERROR: Newer version of srcML required.</xsl:message>
  </xsl:template>

  <!-- copy any element which does not contain a function -->
  <xsl:template match="@*|node()">
    <xsl:copy-of select="."/>
  </xsl:template>

  <!-- default function copy -->
  <xsl:template match="*[.//src:function]">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>