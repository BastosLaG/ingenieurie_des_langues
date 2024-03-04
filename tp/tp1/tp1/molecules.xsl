<?xml version="1.0" encoding="UTF-8" ?> 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output method="html" version="html4.01" encoding="ISO-8859-1" doctype-public="-//W3C//DTD HTML 4.01//EN" doctype-system="http://www.w3.org/TR/html4/strict.dtd"/> 

<xsl:template match="/"> 
<html> 
	<head> 
		<title>Collection de médicaments : anti-douleurs</title> 
	</head> 
	<body> 
		<h1>Médicaments Sans Ordonnance</h1> 
		<xsl:for-each select="molecules/molecule"> 
			<h2>
				<xsl:number format="1" level="single"/>.  <xsl:apply-templates select="nom"/>
			</h2> 
			<p>
				Cette molécule est utilisée pour traiter les <xsl:value-of select="count(symptomes/symptome)"/> symptomes suivants:
			</p> 
			<ul> 
				<xsl:for-each select="symptomes/symptome">
				<li>
					<xsl:apply-templates select="."/>
				</li> 
				</xsl:for-each> 
			</ul> 
			<ul> 
				<p>la prise journalière est : 
					<xsl:value-of select="dosejournaliere/@prises"/>
				</p> 
			</ul> 
			<ul> 
				<xsl:if test="attention">
				<li>Attention si allergie à : 
					<xsl:value-of select="attention/allergie"/>
				</li>
				</xsl:if> 
			</ul>
			<ul>
				<xsl:if test="attention">
				<li>Parlez à votre médecin si antécédents de : 
					<xsl:value-of select="attention/antecedent"/>
				</li>
				</xsl:if> 
			</ul> 
		</xsl:for-each> 
	</body> 
</html> 
</xsl:template> 
</xsl:stylesheet>