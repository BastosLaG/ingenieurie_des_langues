<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" version="html4.01" encoding="ISO-8859-1" doctype-public="-//W3C//DTD HTML 4.01//EN" doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>
<xsl:template match="/">
	<html>
		<head>
			<title>Collection de nuages</title>
		</head>
		<body>
			<h1>Les nuages</h1>
			<xsl:for-each select="nuages/nuage">
				<h2><xsl:number format="1" level="single"/>. <xsl:apply-templates select="nom"/></h2>
				<p>Ce type de nuage possède les <xsl:value-of select="count(nom/espece)"/> espèces suivantes :</p>
				<ul>
					<xsl:for-each select="nom/espece"><li><xsl:apply-templates select="."/></li></xsl:for-each>	
				</ul>
				
			</xsl:for-each>
		</body>
	</html>
</xsl:template>

<xsl:template match="espece">
	<i><xsl:value-of select="."/></i>
</xsl:template>

<xsl:template match="nom">
	<xsl:variable name="name" select="text()"/><xsl:value-of select="concat(translate(substring($name,1,1),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),substring-after($name,substring($name,1,1)))"/>
</xsl:template>

</xsl:stylesheet>
