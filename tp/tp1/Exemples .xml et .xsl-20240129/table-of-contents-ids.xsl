<?xml version="1.0" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

   <xsl:template match="document">
    <html> 
      <head> 
        <title> <xsl:value-of select="title"/>
      </title>
     </head>
     <body bgcolor="#ffffff">
       <!-- generate the TOC -->
       <div style="float:right;background-color:yellow;margin:10px; padding:5px">
       <p>Contents:</p>
       <ul><xsl:apply-templates select="chapter/title" mode="toc"/></ul>
       </div>

       <!-- trigger the templates that deal with all the rest -->
       <xsl:apply-templates/>
     </body>
    </html>
   </xsl:template>
 
   <!-- creates an entry for the TOC -->
   <!-- this will only work for titles that are children of chapter element and that have a toc_id -->
   <xsl:template match="chapter/title[@toc_id]" mode="toc">
    <li> <a href="#{@toc_id}"><xsl:value-of select="."/></a> </li>
   </xsl:template>

   <xsl:template match="chapter">
     <xsl:apply-templates/>
     <hr width="70%"/>
   </xsl:template>

   <!-- will insert a name attribute for each element that has a toc_id -->
   <xsl:template match="chapter/title[@toc_id]">
     <h1 style="color:blue;text-align:center">
       <a name="{@toc_id}"><xsl:apply-templates/></a>
     </h1>
   </xsl:template>

   <!-- if the toc_id is missing then we do not insert a toc_id -->
   <xsl:template match="chapter/title[not(@toc_id)]">
    <h1 style="color:green;text-align:center;"> <xsl:apply-templates/> </h1>
   </xsl:template>

   <xsl:template match="section/title">
    <h2 align="center"> <xsl:apply-templates/> </h2>
   </xsl:template>
 
   <xsl:template match="para">
    <p align="center"> <xsl:apply-templates/> </p>
   </xsl:template>

</xsl:stylesheet>
