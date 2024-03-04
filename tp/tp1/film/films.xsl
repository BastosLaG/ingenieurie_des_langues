<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.01" encoding="UTF-8" doctype-public="-//W3C//DTD HTML 4.01//EN" doctype-system="http://www.w3.org/TR/html4/strict.dtd"/>

<xsl:template match="/">
	<html lang="fr">
		<head>
			<title>Filmographies</title>
		</head>
		<style type="text/css">
			body {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 14px;
                line-height: 1.42857143;
                color: #333;
			    background-color: #fff;
            }
			h2 {
				font-family: Arial, Helvetica, sans-serif;
                font-weight: normal;
                color: red;
			}
			article {
				border-collapse: collapse;
				margin-left: 10px;
                margin-right: 10px;
				padding: 10px;
				border: 1px solid #000;
				border-radius: 10px; 
			}
		</style>
		<body>
			<h1>Films disponibles</h1>
			<xsl:for-each select="films/film">
				<h2><xsl:value-of select="nom/text()"/></h2>
				<article>
					<h3>Ce film est réalisé par <xsl:value-of select="realisateur"/></h3>
					<h4>Publication : <xsl:value-of select="date"/></h4>
					
					<h4>Ce film possède <xsl:value-of select="count(acteur)"/> acteurs :</h4>
					<ul>
						<xsl:for-each select="acteur">
						<li>
							<xsl:value-of select="."/>
						</li>
						</xsl:for-each>
					</ul>
					<h4>Note :<xsl:value-of select="note"/></h4>
					<p><xsl:value-of select="synopsis"></xsl:value-of></p>
				</article>
			</xsl:for-each>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>