<?xml version="1.0" encoding="UTF-8"?>
<!--

Transform plain XML cities XML to valid GML.

Author:  Federico Cantini (federico.cantini@epfl.ch)

based on https://github.com/justb4/stetl/blob/master/examples/basics/6_cmdargs/cities2gml.xsl
-->
<xsl:stylesheet version="1.0"
                xmlns:ogr="http://ogr.maptools.org/"
                xmlns:gml="http://www.opengis.net/gml"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                 >
    <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <ogr:FeatureCollection
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:ogr="http://ogr.maptools.org/"
                xmlns:gml="http://www.opengis.net/gml"
                xsi:schemaLocation="http://ogr.maptools.org/ ../gmlcities.xsd  http://www.opengis.net/gml http://schemas.opengis.net/gml/2.1.2/feature.xsd"
                >
            <gml:boundedBy>
              <gml:Box>
                <gml:coord><gml:X>0.0</gml:X><gml:Y>-90.0</gml:Y></gml:coord>
                <gml:coord><gml:X>360.0</gml:X><gml:Y>90.0</gml:Y></gml:coord>
              </gml:Box>
            </gml:boundedBy>
             <!-- Loop through all points. -->
            <xsl:apply-templates/>
        </ogr:FeatureCollection>
    </xsl:template>

    <!-- Make each point an ogr:featureMember. -->
    <xsl:template match="orbit_point">
        <gml:featureMember>
            <ogr:orbit_point>
                <ogr:geometry>
                    <gml:Point srsName="urn:ogc:def:crs:IAU2000:49901">
                        <gml:coordinates><xsl:value-of select="ScELon"/>,<xsl:value-of select="ScLat"/></gml:coordinates>
                     </gml:Point>
                </ogr:geometry>
            
            <xsl:for-each select="*">
                
                <xsl:variable name="a" select="name()" />
                <xsl:element name="ogr:{$a}">
                    <xsl:value-of select="." />
                </xsl:element> 
            </xsl:for-each>
            </ogr:orbit_point>
        </gml:featureMember>
    </xsl:template>
</xsl:stylesheet>

