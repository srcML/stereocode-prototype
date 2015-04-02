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
        exclude-result-prefixes="src"
        version="1.0">


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

    <xsl:variable name="types" select="str:split('int double char long string')"/>

    <!-- classifies stereotypes using criteria on function definition -->
    <xsl:template match="src:function" mode="stereotype">
      <xsl:apply-templates select="." mode="get"/>
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
                 
                 " mode="get">get</xsl:template>

    <xsl:template match="src:function" mode="get"/>

    <!-- current encoding (XSLT cannot obtain internally) -->
    <xsl:param name="encoding" select="ISO-8859-1"/>

    <!-- provide identity transformation -->
    <xsl:output method="xml" encoding="ISO-8859-1"/>

    <!-- end of line -->
    <xsl:variable name="eol">
    <xsl:text>
    </xsl:text>
    </xsl:variable>

    <!-- annotate function declaration/definition with passed definition -->
    <xsl:template match="src:function[src:name/src:operator[.='::'] or ancestor::src:class or ancestor::src:struct] ">

      <!-- calculate stereotype -->
      <xsl:variable name="stereotype">
        <xsl:apply-templates select="." mode="stereotype_list"/>
      </xsl:variable>

      <!-- insert stereotype comment -->
      <src:comment type="block">/** @stereotype <xsl:value-of select="$stereotype"/>*/</src:comment>
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
        <xsl:when test="$raw_stereotype!=''"><xsl:value-of select="$raw_stereotype"/><xsl:text> </xsl:text></xsl:when>
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