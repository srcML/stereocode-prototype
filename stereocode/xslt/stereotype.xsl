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
    extension-element-prefixes="exsl str func regexp"
    exclude-result-prefixes="set src"
    version="1.0">

    <!-- <xsl:namespace-alias stylesheet-prefix="#default" result-prefix="#default"/> -->
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
      <xsl:apply-templates select="." mode="get"/>
<!--       <xsl:apply-templates select="." mode="nonconstget"/> -->
      <xsl:apply-templates select="." mode="predicate"/>
      <xsl:apply-templates select="." mode="property"/>
      <xsl:apply-templates select="." mode="voidaccessor"/>
      <xsl:apply-templates select="." mode="set"/>
      <xsl:apply-templates select="." mode="command"/>
      <xsl:apply-templates select="." mode="collaborator"/>
      <xsl:apply-templates select="." mode="factory"/>
      <xsl:apply-templates select="." mode="empty"/>
<!-- 



  predicate"/>

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

  <xsl:apply-templates select="." mode="empty"/> -->
    </xsl:template>

        
    <!-- Accessors -->
    <!-- stereotype get -->
    <xsl:template match="src:function
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

    <xsl:template match="src:function" mode="nonconstget"/>


    <!-- stereotype predicate -->
    <xsl:template match="src:function
             [src:specifier='const']
             
             [src:type/src:name='bool']
             
             [descendant::src:return/src:expr/src:name=descendant::src:decl/src:name
                or descendant::src:return/src:expr='false'
                or descendant::src:return/src:expr='true'
             ]
             
             " mode="predicate">predicate </xsl:template>

    <xsl:template match="src:function" mode="predicate"/>

    <!-- stereotype property -->
    <xsl:template match="src:function
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

    <!--
    -->

    <xsl:template match="src:function" mode="property"/>


    <!-- stereotype voidaccessor -->
    <xsl:template match="src:function
             [src:specifier='const']
             
             [src:type/src:name[contains(., 'void')]]
             
             " mode="voidaccessor">voidaccessor </xsl:template>

    <!--
    -->

    <xsl:template match="src:function" mode="voidaccessor"/>


    <!-- Mutators -->

    <!-- stereotype set -->
    <xsl:template match="src:function
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

    <!-- stereotype command -->
    <xsl:template match="src:function
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

    <xsl:template match="src:function" mode="command"/>

    <!-- stereotype collaborator -->                                                                                        
    <xsl:template match="src:function[ 
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

    <xsl:template match="src:function" mode="collaborator"/>

    <!-- Factory -->

    <!-- stereotype factory -->
    <xsl:template match="src:function
                        
                         [not(src:type/src:name='void')]
                         
                         [contains(descendant::src:type,'*')]
            
             [descendant::src:return/src:expr/src:name[1]=src:parameter_list/src:param/src:decl/src:name
             
                            or descendant::src:return/src:expr/src:name[1]=src:block/src:decl_stmt/src:decl/src:name[1]  

                or descendant::src:return/*[not(src:name)][contains(., 'new')]
                         ]
                         

             " mode="factory">factory </xsl:template>

    <xsl:template match="src:function" mode="factory"/>

    <!-- stereotype empty -->
    <xsl:template match="src:function
             [not(src:block/*[not(src:comment)])]
             
             " mode="empty">empty </xsl:template>

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