<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.01" encoding="UTF-8" doctype-public="-//W3C//DTD HTML 4.01//EN" doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>

<xsl:template match="/">
	<html lang="fr">
		<head>
			<title>Filmographies</title>
		</head>
		<body>
		<h1>Films disponibles</h1>
		<xsl:for-each select="films/film">
			<h2><xsl:value-of select="nom/text()"/></h2>
            
            <p>Ce film est réalisé par <xsl:value-of select="realisateur"/></p>
            <p>Publication : <xsl:value-of select="date"/></p>
			
            <p>Ce film possède <xsl:value-of select="count(acteur)"/> acteurs :</p>
	    	<ul>
                <xsl:for-each select="acteur">
                <li>
                    <xsl:value-of select="."/>
                </li>
                </xsl:for-each>
		    </ul>
            <p>Note :<xsl:value-of select="note"/></p>
            <p><xsl:value-of select="synopsis"></xsl:value-of></p>
        </xsl:for-each>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>