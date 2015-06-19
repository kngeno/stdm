"""
/***************************************************************************
Name                 : FKMapperDialog
Description          : class supporting access to foreign key attribute of another class
                        foreign key relations.
Date                 : 8/April/2015
copyright            : (C) 2015 by UN-Habitat and implementing partners.
                       See the accompanying file CONTRIBUTORS.txt in the root
email                : stdm@unhabitat.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ****
"""

from .foreign_key_mapper import ForeignKeyMapper
from stdm.ui.stdmdialog import DeclareMapping
from PyQt4.QtGui import QMessageBox, QWidget, QApplication
from stdm.ui.customcontrols import FKBrowserProperty

class FKMapperDialog(QWidget):
    def __init__(self, parent = None, model =None, display_col = None):
        QWidget.__init__(self, parent)
        self._model = model
        self._dbModel = model
        self.attribute = None
        self.display_col =display_col
        self.mapping = DeclareMapping.instance()

    def foreign_key_modeller(self):
        from stdm.ui import ForeignKeyBrowser
        self.model()
        self.personFKMapper = ForeignKeyMapper()
        self.personFKMapper.setDatabaseModel(self._dbModel)
        self.personFKMapper.setEntitySelector(ForeignKeyBrowser)
        self.personFKMapper.setSupportsList(True)
        self.personFKMapper.setDeleteonRemove(False)
        self.personFKMapper.onAddEntity()
        self.personFKMapper.initialize()
        self.personFKMapper.display_column = self.display_col

    def model(self):
        if not self._model:
            QMessageBox.information(None, QApplication.translate("AttributeBrowser","Loading foreign keys"),
                                    QApplication.translate("AttributeBrowser","Foreign Key cannot be loaded"))
            return
            #self._dbModel = self.mapping.tableMapping('party')
        else:
            self._dbModel = self.mapping.tableMapping(self._model)
        return self._dbModel

    def model_fkid(self):
        try:
            if not self.personFKMapper.global_id.baseid():
                return
            else:
                return self.personFKMapper.global_id.baseid()
        except:
            pass

    def model_display_value(self):
        try:
            if not self.personFKMapper.global_id.display_value():
                return "0"
            else:
                return self.personFKMapper.global_id.display_value()
        except:
            pass




