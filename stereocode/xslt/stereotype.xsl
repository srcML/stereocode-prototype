<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:src="http://www.sdml.info/srcML/src" 
    xmlns:cpp="http://www.sdml.info/srcML/cpp"
    xmlns:set="http://exslt.org/sets"
    xmlns:exsl="http://exslt.org/common"
    xmlns:str="http://exslt.org/strings"
    xmlns:regexp="http://exslt.org/regular-expressions"
    xmlns:func="http://exslt.org/functions"
    xmlns:dyn="http://exslt.org/dynamic"
    
    extension-element-prefixes="exsl str func regexp"
    exclude-result-prefixes="set src"
    version="1.0">

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
      Global Constant Variables
    -->
    <!-- current encoding (XSLT cannot obtain internally) -->
    <xsl:param name="encoding" select="ISO-8859-1"/>

    <!-- provide identity transformation -->
    <xsl:output method="xml" encoding="ISO-8859-1"/>

    <!-- end of line -->
    <xsl:variable name="eol">
<xsl:text>
</xsl:text>
    </xsl:variable>

    <xsl:variable name="types" select="str:split('int double char long string')"/>


<!-- Unique signature of a function based on types of parameters -->
<func:function name="src:function_signature">
  <xsl:param name="function"/>

  <xsl:choose>
    <xsl:when test="$function/src:parameter_list/src:param">
<!--
<xsl:message><xsl:copy-of select="$function/src:name"/>:  <xsl:copy-of select="$function/src:parameter_list/src:param/src:decl/src:type//text()"/></xsl:message>
-->
  <xsl:variable name="raw0">
    <xsl:for-each select="$function/src:parameter_list/src:param/src:decl/src:type">
      <xsl:copy-of select="."/><xsl:text>|</xsl:text>
    </xsl:for-each>
  </xsl:variable>

  <xsl:variable name="raw1" select="normalize-space($raw0)"/>

  <xsl:variable name="raw2" select="str:replace($raw1, 'std::', '')"/>

  <xsl:variable name="raw3" select="str:replace(str:replace(str:replace($raw2, 'hippodraw::', ''), 'numeric::', ''), 'boost::python::', '')"/>

  <xsl:variable name="raw4" select="concat($raw3, '||', $function/src:specifier[.='const'])"/>

  <func:result select="translate(string($raw4), ' ', '')"/>
    </xsl:when>
    <xsl:otherwise>
      <func:result select="concat('||', $function/src:specifier[.='const'])"/>
    </xsl:otherwise>
  </xsl:choose>

</func:function>

<!-- pure virtual function declaration -->
<func:function name="src:isvirtual">
  <xsl:param name="function"/>

  <func:result select="normalize-space($function/src:specifier[last()])='= 0'"/>
</func:function>

<func:function name="src:function_fullname">
  <xsl:param name="declaration"/>

  <xsl:if test="not(contains($declaration/src:name, '::'))">
    <func:result select="concat($declaration/ancestor::src:class/src:name, '::', src:strip-space($declaration/src:name))"/>
  </xsl:if>

  <xsl:if test="contains($declaration/src:name, '::')">
    <func:result select="src:strip-space($declaration/src:name)"/>
  </xsl:if>

</func:function>

<func:function name="src:get_definition">
  <xsl:param name="declaration"/>

  <!-- full method name -->
  <xsl:variable name="function_name" select="src:function_fullname($declaration)"/>

  <!-- full signature -->
  <xsl:variable name="function_signature" select="src:function_signature($declaration)"/>

  <!-- method definition -->
  <xsl:variable name="defn" select="($definition_file//src:function | $declaration/ancestor::src:unit//src:function)
            [$function_name=str:replace(src:strip-space(src:name), 'hippodraw::', '')]
            "/>

  <xsl:variable name="defn2" select="$defn[$function_signature=src:function_signature(.)]
            "/>
  <xsl:choose>
    <xsl:when test="count($defn2)=1">
      <func:result select="$defn2"/>
    </xsl:when>

    <xsl:otherwise>
      <xsl:variable name="defn3" select="$declaration/ancestor::unit/descendant::src:function
            [$function_name=src:strip-space(src:name)]
            "/>

      <xsl:variable name="defn4" select="$defn3[$function_signature=src:function_signature(.)]
            "/>

      <func:result select="''"/>
    </xsl:otherwise>
  </xsl:choose>
</func:function>

<!-- strips all spaces from a string -->
<func:function name="src:strip-space">
  <xsl:param name="s"/>

  <func:result select="translate($s, '&#xa; 
', '')"/>
</func:function>

<func:function name="str:replace">
  <xsl:param name="string" select="''" />
   <xsl:param name="search" select="/.." />
   <xsl:param name="replace" select="/.." />
   <xsl:choose>
      <xsl:when test="not($string)">
        <func:result select="/.." />
      </xsl:when>
      <xsl:when test="function-available('exsl:node-set')">
         <!-- this converts the search and replace arguments to node sets
              if they are one of the other XPath types -->
         <xsl:variable name="search-nodes-rtf">
           <xsl:copy-of select="$search" />
         </xsl:variable>
         <xsl:variable name="replace-nodes-rtf">
           <xsl:copy-of select="$replace" />
         </xsl:variable>
         <xsl:variable name="replacements-rtf">
            <xsl:for-each select="exsl:node-set($search-nodes-rtf)/node()">
               <xsl:variable name="pos" select="position()" />
               <replace search="{.}">
                  <xsl:copy-of select="exsl:node-set($replace-nodes-rtf)/node()[$pos]" />
               </replace>
            </xsl:for-each>
         </xsl:variable>
         <xsl:variable name="sorted-replacements-rtf">
            <xsl:for-each select="exsl:node-set($replacements-rtf)/replace">
               <xsl:sort select="string-length(@search)" data-type="number" order="descending" />
               <xsl:copy-of select="." />
            </xsl:for-each>
         </xsl:variable>
         <xsl:variable name="result">
           <xsl:choose>
              <xsl:when test="not($search)">
                <xsl:value-of select="$string" />
              </xsl:when>
             <xsl:otherwise>
               <xsl:call-template name="str:_replace">
                  <xsl:with-param name="string" select="$string" />
                  <xsl:with-param name="replacements" select="exsl:node-set($sorted-replacements-rtf)/replace" />
               </xsl:call-template>
             </xsl:otherwise>
           </xsl:choose>
         </xsl:variable>
         <func:result select="exsl:node-set($result)/node()" />
      </xsl:when>
      <xsl:otherwise>
         <xsl:message terminate="yes">
            ERROR: function implementation of str:replace() relies on exsl:node-set().
         </xsl:message>
      </xsl:otherwise>
   </xsl:choose>
</func:function>

<xsl:template name="str:_replace">
  <xsl:param name="string" select="''" />
  <xsl:param name="replacements" select="/.." />
  <xsl:choose>
    <xsl:when test="not($string)" />
    <xsl:when test="not($replacements)">
      <xsl:value-of select="$string" />
    </xsl:when>
    <xsl:otherwise>
      <xsl:variable name="replacement" select="$replacements[1]" />
      <xsl:variable name="search" select="$replacement/@search" />
      <xsl:choose>
        <xsl:when test="not(string($search))">
          <xsl:value-of select="substring($string, 1, 1)" />
          <xsl:copy-of select="$replacement/node()" />
          <xsl:call-template name="str:_replace">
            <xsl:with-param name="string" select="substring($string, 2)" />
            <xsl:with-param name="replacements" select="$replacements" />
          </xsl:call-template>
        </xsl:when>
        <xsl:when test="contains($string, $search)">
          <xsl:call-template name="str:_replace">
            <xsl:with-param name="string" select="substring-before($string, $search)" />
            <xsl:with-param name="replacements" select="$replacements[position() > 1]" />
          </xsl:call-template>      
          <xsl:copy-of select="$replacement/node()" />
          <xsl:call-template name="str:_replace">
            <xsl:with-param name="string" select="substring-after($string, $search)" />
            <xsl:with-param name="replacements" select="$replacements" />
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="str:_replace">
            <xsl:with-param name="string" select="$string" />
            <xsl:with-param name="replacements" select="$replacements[position() > 1]" />
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!--
    Definition of native types.  Additional types can be declared in
    the variable more_types
-->
<xsl:variable name="more_native" select="''"/>
<xsl:variable name="native" select="str:split(concat('int long double float string char unsigned bool register vector list map static ', $more_native))"/>

<!--
    Definition of names that occur in types, but are modifiers, etc.
    More types can be declared in the variable more_modifiers
-->
<xsl:variable name="more_modifiers" select="''"/>
<xsl:variable name="modifiers" select="str:split(concat('std void emit virtual inline static const ', $more_modifiers))"/>

<!--
    Definition of calls that aren't really calls, e.g., dynamic_cast.
    More types can be declared in the variable more_modifiers
-->
<xsl:variable name="more_ignore_calls" select="''"/>
<xsl:variable name="ignore_calls" select="str:split(concat('assert static_cast const_cast dynamic_cast reinterpret_cast ', $more_ignore_calls))"/>

<!-- top-level function -->
<func:function name="src:function">

  <func:result select="ancestor-or-self::src:function[1]"/>

</func:function>

<func:function name="src:trace">
   <xsl:param name="context"/>

  <xsl:message><xsl:value-of select="$context"/></xsl:message>

  <func:result select="true()"/>

</func:function>

<func:function name="src:trace2">
   <xsl:param name="field"/>
   <xsl:param name="context"/>

  <xsl:message><xsl:value-of select="$field"/><xsl:text> </xsl:text><xsl:value-of select="$context"/></xsl:message>

  <func:result select="true()"/>

</func:function>

<!-- class name -->
<func:function name="src:class_name">

  <func:result select="src:function()/src:name/src:name[1]"/>

</func:function>

<!-- return expression -->
<func:function name="src:return">

  <func:result select="src:function()/src:block/descendant::src:return/src:expr"/>

</func:function>

<!-- variable names that are a parameter -->
<func:function name="src:param_name">

  <func:result select="src:final_name(src:function()/src:parameter_list/src:param/src:decl/src:name)"/>

</func:function>

<!-- identifiers in parameter types -->
<func:function name="src:param_type_name">

  <func:result select="src:all_type_names(src:function()/src:parameter_list/src:param/src:decl/src:type/src:name)"/>

</func:function>

<!-- identifiers in declaration types -->
<func:function name="src:decl_type_name">

  <func:result select="src:all_type_names(src:function()/src:block/descendant::src:decl_stmt/src:decl/src:type/src:name)"/>

</func:function>

<!-- variable names in declarations (not including parameters)  -->
<func:function name="src:decl_name">

  <func:result select="src:final_name(src:function()/src:block/descendant::src:decl/src:name)"/>

</func:function>

<func:function name="src:variable_type">
   <xsl:param name="context"/>

  <func:result select="src:function()/descendant::src:decl[src:name=$context]/src:type"/>

</func:function>

<func:function name="src:final_name">
  <xsl:param name="cur"/>

  <func:result select="$cur/self::src:name[not(src:name)] | $cur/self::src:name/src:name[1]"/>

</func:function>

<func:function name="src:calling_object">
  <xsl:param name="context" select="."/>

  <func:result select="src:final_name(self::*[not(src:is_pure_call())]/preceding-sibling::*[2][self::src:name])"/>

</func:function>

<func:function name="src:data_members_write">

  <func:result select="src:expr_stmt_name()[src:is_written() and src:is_data_member()]"/>

</func:function>

<func:function name="src:one_data_members_write">

  <func:result select="src:expr_stmt_name()[src:is_written() and src:is_data_member()][1]"/>

</func:function>

<!-- is this variable a data member -->
<func:function name="src:data_members">

  <func:result select="src:function()/src:block/descendant::src:expr/src:name[src:is_data_member()]"/>

</func:function>

<func:function name="src:one_data_members">

  <func:result select="src:function()/src:block/descendant::src:expr/src:name[src:is_data_member()][1]"/>

</func:function>

<func:function name="src:is_static">

  <func:result select="src:name/src:name[1] and src:name/src:name[1]!=src:class_name()"/>

</func:function>

<func:function name="src:is_data_member">

  <func:result select="not(.=src:param_name() or .=src:decl_name() or
           (.//src:operator='::' and not(./src:name[1]=src:class_name())))"/>

</func:function>

<!-- is this variable declared -->
<func:function name="src:is_declared">

  <func:result select=".=src:param_name() or .=src:decl_name()"/>

</func:function>

<!-- variable name in expression (including return expressions) -->
<func:function name="src:expr_name">

  <func:result select="src:function()/descendant::src:expr/src:name"/>

</func:function>

<!-- variable name in expression statements -->
<func:function name="src:expr_stmt_name">

  <func:result select="src:final_name(src:function()/src:block/descendant::src:expr_stmt/src:expr/src:name)"/>

</func:function>

<!-- variable name in expression statements -->
<func:function name="src:call">

  <func:result select="src:function()/src:block/descendant::src:expr/src:call"/>

</func:function>

<func:function name="src:real_call">

  <func:result select="src:function()/src:block/descendant::src:expr/src:call[
           not(src:name[.=$ignore_calls]) and
           not(src:name/src:name[1][.=$ignore_calls]) and
                       not(preceding-sibling::*[1][self::src:operator='new']) and
           not(ancestor::src:throw) and
           not(src:name[src:is_native_type()]) and
           not(src:name/src:name[1][src:is_native_type()])
]"/>

</func:function>

<func:function name="src:stateless_real_call">

  <func:result select="src:function()/src:block/descendant::src:expr/src:call[
           not(src:name[.=$ignore_calls]) and
           not(src:name/src:name[1][.=$ignore_calls]) and
           not(ancestor::src:throw) and
           not(src:name[src:is_native_type()]) and
           not(src:name/src:name[1][src:is_native_type()])
]"/>

</func:function>

<func:function name="src:one_real_call">

  <func:result select="src:function()/src:block/descendant::src:expr/src:call[
           not((src:name | src:name/src:name)[.=$ignore_calls]) and
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

<func:function name="src:all_type_names_nonclass_object">
   <xsl:param name="context"/>
   <xsl:param name="class"/>

   <func:result select="$context[not(src:name)][not(.='std') and not(.=$class) and src:is_object()] |
      $context//src:name[not(src:name) and not(.='std') and
      not(preceding-sibling::src:name[1][not(.='std')]) and not(.=$class) and src:is_object()]"/>

</func:function>

<!--

-->

<!-- type name is a native type -->
<func:function name="src:is_native_type">

<!--  <xsl:message><xsl:value-of select="."/></xsl:message> -->

   <func:result select=".=$native"/>

</func:function>

<func:function name="src:is_modifier">

   <func:result select=".=$modifiers"/>

</func:function>

<!--

-->

<func:function name="src:is_pure_call">

   <func:result select="not(preceding-sibling::*[1][self::src:operator='.' or self::src:operator='-&gt;'])"/>

</func:function>

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

<func:function name="src:union">
  <xsl:param name="first"/>
  <xsl:param name="second"/>

  <func:result select="$first | $second"/>

</func:function>


    <!--
      Functions
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
<!--       <xsl:apply-templates select="." mode="get"/>
      <xsl:apply-templates select="." mode="predicate"/>
      <xsl:apply-templates select="." mode="property"/>
      <xsl:apply-templates select="." mode="voidaccessor"/>
      <xsl:apply-templates select="." mode="set"/>
      <xsl:apply-templates select="." mode="command"/>
      <xsl:apply-templates select="." mode="collaborator"/>
      <xsl:apply-templates select="." mode="factory"/>
      <xsl:apply-templates select="." mode="empty"/> -->
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


    </xsl:template>

        
    <!-- Accessors -->
    <!-- stereotype get -->
<!--     <xsl:template match="src:function
                 [src:specifier='const']
                 
                 [descendant::src:return/src:expr=(descendant::src:return/src:expr/src:name | descendant::src:return/src:expr/src:call)
                     or descendant::src:return/src:expr=concat('*', descendant::src:return/src:expr/src:name[1])
                 ]
                 
                 [not(descendant::src:return/src:expr/src:call)]
                 
                 [not(descendant::src:return/src:expr/src:name=descendant::src:decl/src:name) and
                     
                     (not(descendant::src:return/src:expr/src:name/src:name) 
                      or
                      not(descendant::src:return/src:expr/src:name/src:name=descendant::src:decl/src:name)
                     )
                 ]
                 
                 [not(descendant::src:return/src:expr = 'false')]
                 [not(descendant::src:return/src:expr = 'true')]
                 [descendant::src:type != 'void']
                 
                 " mode="get">get </xsl:template>

    <xsl:template match="src:function" mode="get"/>

    <xsl:template match="src:function
                 [not(src:specifier='const')]
                 
                 [descendant::src:return/src:expr=(descendant::src:return/src:expr/src:name | descendant::src:return/src:expr/src:call)
                     or descendant::src:return/src:expr=concat('*', descendant::src:return/src:expr/src:name[1])
                 ]
                 
                 [not(descendant::src:return/src:expr/src:call)]
                 
                 [not(descendant::src:return/src:expr/src:name=descendant::src:decl/src:name) and
                     
                     (not(descendant::src:return/src:expr/src:name/src:name) 
                      or
                      not(descendant::src:return/src:expr/src:name/src:name=descendant::src:decl/src:name)
                     )
                 ]
                 
                 [not(descendant::src:return/src:expr = 'false')]
                 [not(descendant::src:return/src:expr = 'true')]
                 [descendant::src:type != 'void']
                 
                 " mode="nonconstget">nonconstget </xsl:template>

    <xsl:template match="src:function" mode="nonconstget"/> -->


    <!-- stereotype predicate -->
<!--     <xsl:template match="src:function
             [src:specifier='const']
             
             [src:type/src:name='bool']
             
             [descendant::src:return/src:expr/src:name=descendant::src:decl/src:name
                or descendant::src:return/src:expr='false'
                or descendant::src:return/src:expr='true'
             ]
             
             " mode="predicate">predicate </xsl:template>

    <xsl:template match="src:function" mode="predicate"/> -->

    <!-- stereotype property -->
<!--     <xsl:template match="src:function
             [src:specifier='const']
             
             [not(src:type/src:name='void' or src:type/src:name='bool')]
             
             [descendant::src:return/src:expr/src:name=descendant::src:decl/src:name
             
                or descendant::src:return/src:expr/src:name/src:name=descendant::src:decl/src:name
                
                or descendant::src:return/src:expr[count(src:name)&gt;1]
                
                or descendant::src:return/src:expr/src:call
                
                or descendant::src:return/src:expr and 
                   (count(descendant::src:return/src:expr/src:name)+count(descendant::src:return/src:expr/src:call)=0)
                
                or (descendant::src:return/src:expr/src:name and descendant::src:return/src:expr[.!=src:name[1]])
             ]
                                  
             " mode="property">property </xsl:template>
 -->
    <!-- <xsl:template match="src:function" mode="property"/> -->


    <!-- stereotype voidaccessor -->
<!--     <xsl:template match="src:function
             [src:specifier='const']
             
             [src:type/src:name[contains(., 'void')]]
             
             " mode="voidaccessor">voidaccessor </xsl:template>
    <xsl:template match="src:function" mode="voidaccessor"/> -->


    <!-- Mutators -->

    <!-- stereotype set -->
<!--     <xsl:template match="src:function
             [not(src:specifier)]
             
                         [src:type/src:name[contains(., 'void') or contains(., 'bool')]]
             
             [count(descendant::src:expr_stmt/src:expr/src:name[1]
                   [not(.=ancestor::src:function/descendant::src:decl/src:name)])=1
             ]
             
             [descendant::src:expr_stmt/src:expr/src:name[1][not(.=ancestor::src:function/descendant::src:decl/src:name)]
                   [contains(following-sibling::text()[1], '=')]
             ]
             
             [count(descendant::src:expr_stmt/src:expr/src:name[1]/src:name
                   [not(.=ancestor::src:function/descendant::src:decl/src:name)])=0
             ]
                   
             " mode="set">set </xsl:template>

    <xsl:template match="src:function" mode="set"/>

 -->    <!-- stereotype command -->
<!--     <xsl:template match="src:function
             [not(src:specifier)]
             
             [src:type/src:name[contains(., 'void') or contains(., 'bool')]]
             
             [count(descendant::src:expr_stmt/src:expr/src:name[1][not(.=ancestor::src:function/descendant::src:decl/src:name)])&gt;1
                
              or
              count( descendant::src:expr_stmt/src:expr/src:name[1][not(.=ancestor::src:function/descendant::src:decl/src:name) 
                     and not(contains(following-sibling::text()[1], '='))] )=1
                     
              or
              count(descendant::src:expr_stmt/src:expr/src:name[1][not(.=ancestor::src:function/descendant::src:decl/src:name)])=0 
                 and descendant::src:expr_stmt/src:expr/src:call
             ]
                          
             " mode="command">command </xsl:template>

    <xsl:template match="src:function" mode="command"/> -->

    <!-- stereotype collaborator -->                                                                                        
<!--     <xsl:template match="src:function[ 
                                      src:type/src:name[not(contains(., 'std') or contains(., 'int') or contains(., 'long') 
                                                or contains(., 'double') or contains(., 'string') or contains(., 'char') or contains(., 'void') or contains(., 'bool') or contains(., 'inline') or contains(., 'unsigned') or contains(., 'static') or contains(., 'const'))]    
                                     
                                      or src:block/descendant::src:decl_stmt/src:decl/src:type
                                           [not (contains(., 'std') or contains(., 'int') or contains(., 'long') 
                                                or contains(., 'double') or contains(., 'string') or contains(., 'char') or contains(., 'unsigned') or contains(., 'const') or contains(., 'bool') )] 

                                      or src:parameter_list/src:param/src:decl/src:type/src:name
                                           [not (contains(., 'std')or contains(., 'int') or contains(., 'long') 
                                                 or contains(., 'double') or contains(., 'string') or contains(., 'char') or contains(., 'unsigned') or contains(., 'const') or contains(., 'bool') )]
            
                                     ]
                                              
                   " mode="collaborator">collaborator </xsl:template>

    <xsl:template match="src:function" mode="collaborator"/> -->

    <!-- Factory -->

    <!-- stereotype factory -->
<!--     <xsl:template match="src:function
                        
                         [not(src:type/src:name='void')]
                         
                         [contains(descendant::src:type,'*')]
            
             [descendant::src:return/src:expr/src:name[1]=src:parameter_list/src:param/src:decl/src:name
             
                            or descendant::src:return/src:expr/src:name[1]=src:block/src:decl_stmt/src:decl/src:name[1]  

                or descendant::src:return/*[not(src:name)][contains(., 'new')]
                         ]
                         

             " mode="factory">factory </xsl:template>

    <xsl:template match="src:function" mode="factory"/>
 -->
    <!-- stereotype empty -->
<!--     <xsl:template match="src:function
             [not(src:block/*[not(src:comment)])]
             
             " mode="empty">empty </xsl:template>

    <xsl:template match="src:function" mode="empty"/> -->



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


    <!--
        Section responsible for actually applying all of the stereotypes and annotating
        the source code with a comment.
    -->
    <!-- annotate function declaration/definition with passed definition  -->
    <xsl:template match="src:function[src:name/src:operator[.='::'] or ancestor::src:class or ancestor::src:struct] ">

      <!-- calculate stereotype -->
      <xsl:variable name="stereotype">
        <xsl:apply-templates select="." mode="stereotype_list"/>
      </xsl:variable>

      <!-- insert stereotype comment -->
      <comment xmlns="http://www.sdml.info/srcML/src" type="block">/** @stereotype <xsl:value-of select="$stereotype"/>*/</comment>
      <xsl:value-of select="$eol"/>

      <!-- calculate the indent currently on the declaration so we can duplicate it on the comment -->
      <xsl:variable name="indent" select="src:last_ws(preceding-sibling::text()[1])"/>
     
      <!-- insert indentation -->
      <xsl:value-of select="$indent"/>

      <!-- copy of function declaration -->
      <xsl:copy-of select="."/>

    </xsl:template>

    <!-- classifies stereotypes using criteria from stereotypes.xsl -->
    <xsl:template match="src:function" mode="stereotype_list">

      <xsl:variable name="raw_stereotype"><xsl:apply-templates select="." mode="stereotype"/></xsl:variable>

      <xsl:choose>
        <xsl:when test="$raw_stereotype!=''"><xsl:value-of select="$raw_stereotype"/></xsl:when>
        <xsl:otherwise>unclassified </xsl:otherwise>
      </xsl:choose>

    </xsl:template>

    <!-- copy any element which does not contain a function -->
    <xsl:template match="@*|node()">
      <xsl:copy-of select="."/>
    </xsl:template>

    <!-- default identity copy -->
    <xsl:template match="*[.//src:function]">
      <xsl:copy>

        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:template>

</xsl:stylesheet>