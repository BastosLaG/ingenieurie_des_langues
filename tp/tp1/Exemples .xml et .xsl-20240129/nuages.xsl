<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.01" encoding="ISO-8859-1" doctype-public="-//W3C//DTD HTML 4.01//EN" doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>

<xsl:template match="/">
	<html lang="fr">
		<head>
			<title>Collection des nuages</title>
		</head>
		<body>
		<h1>Les nuages</h1>
		<xsl:for-each select="nuages/nuage">
			<h2><xsl:value-of select="nom/text()"/> :</h2>
			<p>Ce nuage possède les <xsl:value-of select="count(nom/espece)"/> espèces suivantes :</p>
		<ul>
		<xsl:for-each select="nom/espece">
		<li>
		<xsl:value-of select="."/>
		</li>
		</xsl:for-each>
		</ul>
		
		</xsl:for-each>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>
