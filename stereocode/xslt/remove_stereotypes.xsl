<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:src="http://www.srcML.org/srcML/src" 
    xmlns:cpp="http://www.srcML.org/srcML/cpp"
    xmlns:exsl="http://exslt.org/common"
    xmlns:str="http://exslt.org/strings"
    extension-element-prefixes="exsl str"
    exclude-result-prefixes="src"
    version="1.0">

    <xsl:template match="src:comment[contains(text(), '@stereotype')]"/>
    <xsl:template match="node()|@*">
      <xsl:copy>
         <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:template>

    <!-- <xsl:template match="Element[@fruit='apple' and @animal='cat']"/> -->

    <!-- Copy all non-comment elements. -->
<!--     <xsl:template match="@*|node()">
        <xsl:copy-of select="."/>
    </xsl:template> -->
</xsl:stylesheet>