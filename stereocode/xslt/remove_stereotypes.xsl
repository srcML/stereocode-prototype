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

    <xsl:param name="processing_mode">ReDocSrc</xsl:param>

    <xsl:template match="src:comment[contains(text(), '@stereotype')]" mode="redoc_src"/>
    <xsl:template match="@stereotype" mode="xml_attr"/>

    <xsl:template match="node()|@*">
      <xsl:choose>
            <xsl:when test="$processing_mode='ReDocSrc'">
              <xsl:copy>
                 <xsl:apply-templates select="." mode="redoc_src"/>
              </xsl:copy>
          </xsl:when>
          <xsl:when test="$processing_mode='XmlAttr'">
              <xsl:copy>
                 <xsl:apply-templates select="." mode="xml_attr"/>
              </xsl:copy>
          </xsl:when>
          <xsl:otherwise>
            <xsl:message terminate="yes">
              ERROR: Unknown mode.
            </xsl:message>
          </xsl:otherwise>
      </xsl:choose>
    </xsl:template>

    <xsl:template match="node()|@*" mode="xml_attr">
        <!-- [$processing_mode='XmlAttr']
    [$processing_mode='ReDocSrc']-->
      <xsl:copy>
         <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:template>

    <xsl:template match="node()|@*" mode="redoc_src">
      <xsl:copy>
         <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:template>
</xsl:stylesheet>