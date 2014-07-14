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
from ui_table import Ui_table
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QApplication, QMessageBox
from stdm.data import writeTable, renameTable,inheritTableColumn, writeTableColumn,writeLookup,checktableExist,ConfigTableReader

class TableEditor(QDialog, Ui_table):
    def __init__(self,actionMode,tableName,parent):
        QDialog.__init__(self,parent)
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.table=tableName
        self.state=actionMode[1]
        self.profile=actionMode[0]
        self.lookup=None
        self.checkBox.clicked.connect(self.actionInherit)
        self.txtTable.editingFinished.connect(self.checkTableExist)
        self.initGui()
        
        
    def initGui(self):
        if self.state==QApplication.translate("TableEditor","Edit Table"):
            self.groupBox.setTitle(self.state +" "+ self.table)
        if self.state==QApplication.translate("TableEditor","Add Lookup"):
            self.groupBox.setTitle(self.state + " Note: lookup tables must begin with 'check_' followed by 'table name'")
            self.chkDefault.setVisible(False)
        else:
            self.groupBox.setTitle(self.state)
            self.chkDefault.setChecked(True)
        self.widget.hide()
       
    def actionInherit(self):
        '''check if the user want to inherit other table columns'''
        if self.checkBox.isChecked():
            self.widget.show()
            self.tableModel()
        else: 
            self.widget.hide()
            items=self.cboInheritTable.count()
            model=self.cboInheritTable.model()
            model.removeColumns(0,items)
        
    def tableModel(self):
        tableHandler=ConfigTableReader()
        tableModel=tableHandler.tableListModel(self.profile)
        self.cboInheritTable.setModel(tableModel)
        
    def setTableData(self):
        attrib={}
        self.table=self.setTableName(self.txtTable.text())
        tableDesc=str(self.txtDesc.text())
        attrib['name']=self.table
        attrib['fullname']=tableDesc
        writeTable(attrib,self.profile,self.table)
        self.tableCapabilities()
        
    def tableCapabilities(self):
        options=['create','select','update','delete']
        capabilities={}
        for opt in options:
            capabilities['name']=opt
            capabilities['code']=self.capabilityCode()
            writeTableColumn(capabilities, self.profile, 'table', self.table, 'contentgroups')
            
    def capabilityCode(self):
        codGen=QUuid()
        code=codGen.createUuid()
        return code.toString().upper()
        
    def setLookupTable(self):
        '''def add lookup table'''
        tableName=self.setTableName(self.txtTable.text())
        if str(tableName).startswith("check"):
            self.table=tableName
        if not str(tableName).startswith("check"):
            self.table='check_'+tableName
        attrib={}
        tableDesc=str(self.txtDesc.text())
        attrib['name']=self.table
        attrib['fullname']=tableDesc
        writeLookup(attrib,self.profile,self.table)
        self.autoCreatePrimaryKeyColumn('lookup')
        self.dataColumnForLookup('lookup')
    
    def updateTableName(self):
        tableName=self.setTableName(self.txtTable.text())
        renameTable(self.profile,self.table,tableName)
    
    def inheritsColumns(self):
        sourceTable=self.cboInheritTable.currentText()
        destTable=self.setTableName(self.txtTable.text())
        #try:
        inheritTableColumn(self.profile,sourceTable,destTable)
        #except:
        #    self.ErrorInfoMessage(QApplication.translate("TableEditor","Cannot copy columns from "+sourceTable))
        
    def setTableName(self, tabName):
        formattedName=str(tabName).strip()
        formattedName=formattedName.replace(' ', "_")
        return formattedName.lower()
    
    def autoCreatePrimaryKeyColumn(self,Node):
        '''Allow automatic created of primary column in the table'''
        attrib={}
        attrib['name']='id'
        attrib['fullname']='Primary Key'
        attrib['type']='serial'
        attrib['size']=''
        attrib['key']='1'
        writeTableColumn(attrib,self.profile,Node,self.table,'columns')
    
    def dataColumnForLookup(self,Node):
        attrib={}
        attrib['name']='value'
        attrib['fullname']='Choice list'
        attrib['type']='character varying'
        attrib['size']='50'
        #attrib['key']='1'
        writeTableColumn(attrib,self.profile,Node,self.table,'columns')
    
    def checkTableExist(self):
        '''check if the table has been defined already'''
        tableName=self.setTableName(self.txtTable.text())
        status=checktableExist(self.profile,tableName)
        if status==True:
            QMessageBox.critical(self, QApplication.translate("TableEditor","Table Exist Warning"), 
                                 QApplication.translate("TableEditor","Table name cannot be defined twice"))
            self.txtTable.setFocus()
            return
                
    def accept(self):
        if self.txtTable.text()=='':
            self.ErrorInfoMessage(QApplication.translate("TableEditor","Table name is not given"))
            return
        if self.state==QApplication.translate("TableEditor","Edit Table"):
            self.updateTableName()
        if self.state==QApplication.translate("TableEditor","Add Table"):
            self.setTableData()
        if self.state==QApplication.translate("TableEditor","Add Lookup"):
            self.setLookupTable()
        if self.chkDefault.isChecked():
            self.autoCreatePrimaryKeyColumn('table')
        if self.checkBox.isChecked():
            self.inheritsColumns()
        self.close()
    
    def ErrorInfoMessage(self, Message):
        # Error Message Box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("STDM")
        msg.setText(Message)
        msg.exec_()  