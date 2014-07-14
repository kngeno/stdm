# -*- coding: utf-8 -*-
"""
/***************************************************************************
 stdm
                                 A QGIS plugin
 Securing land and property rights for all
                              -------------------
        begin                : 2014-03-04
        copyright            : (C) 2014 by GLTN
        email                : njoroge.solomon@yahoo.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from stdm.data import FilePaths 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class LicenseDocument(object):
    def __init__(self):
        self.file=None
        self.filehandler=FilePaths()
        
    def openLicenseFile(self):
        '''get the path to the license file'''
        self.file=self.filehandler.STDMLicenseDoc()
        #self.file=docFile
    
    def readLicenseData(self):
        '''read license information for user '''
        try:
            self.openLicenseFile()
            with open(self.file,'r')as inf:
                lic_data=inf.read()
            return lic_data
        except IOError as ex:
            raise ex
        
    def textFont(self):
        '''set document font'''
        docFont=QFont('Helvetica [Cronyx]',10,QFont.Bold)
        #docFont.setBold(True)
        return docFont
        