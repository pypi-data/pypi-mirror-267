# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys
import json
import slugify
from functools import partial

from r3xa.utils import get_schema, slugify_file_name, pprint
from r3xa.validation import validate
from r3xa.metadata import MetaData, Setting, DataSource, DataSet


def pyqtislameaf(field):
    if isinstance(field, QLineEdit):
        try:
            return float(field.text())
        except Exception:
            return field.text()
    elif isinstance(field, QTextEdit):
        return field.toPlainText()

    return field.text()


class Window(QDialog):
    def __init__(self, json_file_name: str = None):
        super(Window, self).__init__()

        # set output
        output = self.outputWidget()

        self.schema = get_schema()
        self.json_file_name = json_file_name
        try:
            self.json = json.load(open(self.json_file_name, "r")) if self.json_file_name else {}
        except FileNotFoundError as e:
            self.json = {}
            print(e)
            self.outputText.setText(str(e))
            self.outputText.setStyleSheet("color: #e22;")

        self.metadata = MetaData(payload=self.json)

        # setting window title
        self.setWindowTitle("R3XA meta data editor")

        # buid header
        header = self.headerWidget()

        # build tabs for meta data forms
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        # scroll_area.setFixedHeight(False)
        tab_holder = QWidget()
        tab_layout = QVBoxLayout(tab_holder)
        tab_widget = QTabWidget()

        root_tab = self.rootTab()
        tab_widget.addTab(root_tab, "Root")

        settings_tab = self.settingsTab()
        tab_widget.addTab(settings_tab, "Settings")

        data_sources_tab = self.dataSourcesTab()
        tab_widget.addTab(data_sources_tab, "Data sources")

        json_tab = self.jsonTab()
        tab_widget.addTab(json_tab, "JSON")

        tab_layout.addWidget(tab_widget)
        tab_holder.setLayout(tab_layout)
        scroll_area.setWidget(tab_holder)

        # save / load button
        buttons = self.buttonsWidget()

        # main layout
        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addWidget(scroll_area)
        layout.addWidget(output)
        layout.addWidget(buttons)
        # layout.addStretch()

        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttons.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setLayout(layout)

    def headerWidget(self):
        header = f"""<h3>{self.schema["title"]}</h3>
        <p>{self.schema["description"]}</p>
        <p><i>Version {self.schema["properties"]["version"]["const"]}</i></p>
        <p></p>
        """
        return QLabel(header)

    def addItem(self, setting_id):
        """add a raw in the item"""
        self.clearLayout(self.settingFormLayout)
        for k, widget in [(k, v) for k, v in self.__dict__.items() if k[:15] == "field:settings/"]:
            delattr(self, k)

        payload = [s for s in self.json["settings"] if s["id"] == setting_id][0]
        kind = payload["kind"].split("/")[1]
        section_key = f"field:settings/{kind}"
        self.display_form(section_key, payload, self.settingFormLayout)

    def display_form_line(self, section_key, k, v, required, payload, layout, idx: int = None):
        """Displays a single line of the form
        section_key: something like field:settings/specimen used to setup the input attribute name
        k, v: the key value of the properties from the schema
        required: the requried field from the schema
        payload: the current value of the meta data like {'title': "I'm setting 3", 'description': 'This is my second setting', ...}
        layout: the QFormLayout
        idx: idx of the list if line is part of a list
        """
        r = "*" if k in required else ""
        label = QLabel(f'<b>{v["title"]}{r}</b>')
        if r:
            label.setStyleSheet("color: #e22;")

        attribute_key = f"{section_key}/{k}"

        if idx is not None:
            attribute_key += "__" + str(idx)
            # print(attribute_key)
            description = QHBoxLayout()
            t = QLabel(f'<i>{v["description"]}</i>')
            b = QPushButton("Resize list")
            # setattr(self, attribute_key.replace("field:", "button:"), b)
            description.addWidget(t)
            description.addWidget(b)
            # pprint(payload)
            b.clicked.connect(partial(self.addItem, payload["id"]))
        else:
            description = QLabel(f'<i>{v["description"]}</i>')

        # if k == "kind":
        #     # ignore kind classes should be clever enough to guess it... I guess
        #     # otherwise just don't add the raw but keep the input_field
        #     return

        string_like = ["string", "#/$defs/types/uri", "#/$defs/types/string"]
        if v.get("type") in string_like or v.get("$ref") in string_like:
            # handle field type and default value
            if k == "description":
                input_field = QTextEdit()
                input_field.setFixedHeight(150)
                input_field.setText(payload.get(k, ""))
                input_field.setTabChangesFocus(True)
            else:
                input_field = QLineEdit()
                if idx is not None:
                    try:
                        input_field.setText(payload.get(k, "")[idx])
                    except:
                        input_field.setText("")
                else:
                    input_field.setText(payload.get(k, ""))
                input_field.editingFinished.connect(self.onEditingFinished)

            # handle read only
            if "const" in v:
                input_field.setText(v["const"])
                input_field.setReadOnly(True)
                input_field.setStyleSheet("color: #aaa;")
            elif k == "id":
                input_field.setReadOnly(True)
                input_field.setStyleSheet("color: #aaa;")

            print("set input_field attribute", attribute_key)
            setattr(self, attribute_key, input_field)

            if k == "kind":
                return

            if idx is None:
                layout.addRow(label, description)
                layout.addRow(input_field)
            else:
                if idx == 0:
                    layout.addRow(label, description)
                layout.addRow(QLabel(f"item {idx}"), input_field)

            # handle example
            if isinstance(v.get("examples"), list):
                examples = QLabel(f'<i>e.g.</i> {"; ".join(v["examples"])}')
                examples.setStyleSheet("color: #aaa; margin-bottom: 10px;")
                layout.addRow(examples)

        elif v.get("$ref") in ["#/$defs/types/unit"]:
            lineEdit = QHBoxLayout()
            unit = self.schema["$defs"]["types"]["unit"]
            unit_required = unit["required"]
            for unit_k, unit_v in unit["properties"].items():
                r = "*" if unit_k in unit_required else ""
                label_unit = QLabel(f"{unit_k}{r}")
                if r:
                    label_unit.setStyleSheet("color: #e22;")
                input_field = QLineEdit()
                if idx is not None:
                    try:
                        input_field.setText(str(payload.get(k, [])[idx].get(unit_k, "")))
                    except:
                        input_field.setText("")
                else:
                    input_field.setText(str(payload.get(k, {}).get(unit_k, "")))
                input_field.editingFinished.connect(self.onEditingFinished)

                attribute_key_deap = f"{attribute_key}/{unit_k}"
                print("set input_field attribute", attribute_key_deap)
                setattr(self, attribute_key_deap, input_field)

                if unit_k == "kind":
                    # do not display kind
                    input_field.setText("unit")
                    continue

                lineEdit.addWidget(label_unit)
                lineEdit.addWidget(input_field)

            if idx is None:
                layout.addRow(label, description)
                layout.addRow(lineEdit)
            else:
                if idx == 0:
                    layout.addRow(label, description)
                layout.addRow(QLabel(f"item {idx}"), lineEdit)

        else:
            print("NOT HANDLED", k, v)

    def display_form(self, section_key, payload, layout, ignored=[]):
        """Display the form
        section_key: something like field:settings/specimen used to setup the input attribute name
        payload: the current value of the meta data like {'title': "I'm setting 3", 'description': 'This is my second setting', ...}
        ignored: the fields from the schema we don't want to display
        layout: QFormLayout
        """

        #  the schema properties and required from the section_key
        if section_key == "field:root":
            properties = {k: v for k, v in self.schema["properties"].items() if k not in ignored}
            required = self.schema["required"]
        else:
            # print(section_key)
            if len(section_key.split("/")) > 2:
                print(f"WARNING: section key with two /: {section_key}")
            a = section_key.split("/")[0].split(":")[1]
            b = section_key.split("/")[1]
            properties = self.schema["$defs"][a][b]["properties"]
            required = self.schema["$defs"][a][b]["required"]

        # get required arguments for root parameters
        for k, v in properties.items():
            if v.get("type") in ["array"]:
                print(section_key, k, v)
                v_array = v.copy()
                if "type" in v["items"]:
                    v_array["type"] = v["items"]["type"]
                elif "$ref" in v["items"]:
                    v_array["$ref"] = v["items"]["$ref"]
                else:
                    print("WARNING: array hasn't type or ref (might be anyOf")
                del v_array["items"]

                # loop over the values of the payload and add one empty line
                n = len(payload.get(k, []))
                # print("copucou", payload[k])
                for i in range(n + 1):
                    self.display_form_line(section_key, k, v_array, required, payload, layout, idx=i)

            else:
                self.display_form_line(section_key, k, v, required, payload, layout)

    def rootTab(self):
        layout = QFormLayout()
        layout.addRow(QLabel("<h3>Root meta data</h3>"))

        self.json_file_name_field = QLineEdit(self.json_file_name if self.json_file_name else "")
        self.json_file_name_field.editingFinished.connect(self.onEditingFileName)
        layout.addRow(f"<b>JSON file</b>", self.json_file_name_field)

        self.display_form("field:root", self.json, layout, ignored=["data_sets", "settings", "data_sources"])

        tab = QWidget()
        tab.setLayout(layout)

        return tab

    def jsonTab(self):
        layout = QVBoxLayout()
        self.rawJson = QTextEdit()
        self.rawJson.setText(json.dumps(self.json, indent=2))
        self.rawJson.setReadOnly(True)
        self.rawJson.setAcceptRichText(True)
        self.rawJson.setStyleSheet("color: #aaa;")
        layout.addWidget(self.rawJson)

        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def setSettingsComboBox(self):
        # unconnect to reset the combo box
        try:
            self.settingComboBox.currentIndexChanged.disconnect(self.onSettingComboBox)
        except TypeError:
            # the box was not connected
            pass

        self.settingComboBox.clear()

        # default un triggreable
        self.settingComboBox.addItem(f"--- Manage your settings ---", userData=None)
        self.settingComboBox.model().item(0).setEnabled(False)

        # create a new settings from schema
        for k, v in self.schema["$defs"]["settings"].items():
            self.settingComboBox.addItem(f"New {k} setting", userData=f"new_{k}")

        # get all settings from schema
        for setting in self.metadata.settings:
            self.settingComboBox.addItem(f"Edit {setting.title}", userData=f"edit_{setting.id}")

        # reconnect again
        self.settingComboBox.currentIndexChanged.connect(self.onSettingComboBox)

    def settingsTab(self):
        mainLayout = QVBoxLayout()

        #######
        # Combo box to select edit/create setting
        #######

        selectLayout = QFormLayout()
        self.settingComboBox = QComboBox()
        self.setSettingsComboBox()

        # setup layout
        selectLayout.addRow(self.settingComboBox)
        selectWidget = QWidget()
        selectWidget.setLayout(selectLayout)
        mainLayout.addWidget(selectWidget)

        ######
        # Form to edit/create settings
        ######
        self.settingFormLayout = QFormLayout()
        # formLayout.addRow(QLabel("coucou"))
        formWidget = QWidget()
        formWidget.setLayout(self.settingFormLayout)
        mainLayout.addWidget(formWidget)
        mainLayout.addStretch()

        tab = QWidget()
        tab.setLayout(mainLayout)
        return tab

    def onSettingComboBox(self, index):
        if not index:
            return

        # delete all self attribute of previous settingCombo
        self.clearLayout(self.settingFormLayout)
        for k, widget in [(k, v) for k, v in self.__dict__.items() if k[:15] == "field:settings/"]:
            delattr(self, k)

        key = self.settingComboBox.currentData()

        # parse key
        # new settings
        #     new_generic
        #     new_specimen
        # edit settings
        #     edit_lskhdflqsdhf

        action = key.split("_")[0]

        print(key, action)

        if action == "edit":
            setting_id = "_".join(key.split("_")[1:])
            # get setting from json
            setting = [s for s in self.json["settings"] if s["id"] == setting_id][0]
            kind = setting["kind"].split("/")[1]
            section_key = f"field:settings/{kind}"
            self.display_form(section_key, setting, self.settingFormLayout)

            title = getattr(self, section_key + "/title")
            self.outputText.setText(f"{action.title()} {title.text()} [{setting_id}]")
            self.outputText.setStyleSheet("color: #aaa;")
        elif action == "new":
            kind = "_".join(key.split("_")[1:])
            section_key = f"field:settings/{kind}"
            title = f"New {kind}"
            setting = Setting(title=title, kind=f"settings/{kind}", check=False)
            self.display_form(section_key, dict(setting), self.settingFormLayout)

    def dataSourcesTab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("WIP"))
        layout.addStretch()

        tab = QWidget()
        tab.setLayout(layout)
        return tab

    def outputWidget(self):
        layout = QFormLayout()
        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        self.outputText.setFixedHeight(50)
        layout.addRow(self.outputText)
        output = QWidget()
        output.setLayout(layout)
        return output

    def buttonsWidget(self):
        layout = QFormLayout()
        saveButton = QPushButton("save file")
        layout.addRow(saveButton)
        buttons = QWidget()
        buttons.setLayout(layout)

        saveButton.clicked.connect(self.save)
        return buttons

    def parse_attribute(self, k):
        # field:root/title                         root: True  object: False list: False
        # field:settings/specimen/title            root: False object: False list: False
        # field:settings/specimen/names__0         root: False object: False list: True
        # field:settings/specimen/size/title       root: False object: True  list: False
        # field:settings/specimen/sizes__0/title   root: False object: True  list: True

        parsed_key = {"attribute": False, "key": k, "depth": 0, "base": "", "keys": [], "array": False, "idx": 0}

        if "field:" not in k:
            return parsed_key

        # remove field
        k = k.replace("field:", "")

        # get root
        splt = k.split("/")
        parsed_key["key"] = k
        parsed_key["attribute"] = True
        parsed_key["depth"] = len(splt)
        parsed_key["base"] = splt[0]
        parsed_key["keys"] = [_.split("__")[0] for _ in splt[1:]]

        if len(splt) == 2:
            # WARNING this will break if root have lists which is not the case for now
            return parsed_key

        if "__" in splt[2]:
            # we have a list
            parsed_key["array"] = True
            parsed_key["idx"] = int(splt[2].split("__")[1])

        return parsed_key

    def update_metadata_from_fields(self):
        print("Updating self.metadata from fields values (detla update)")

        # the payload to build and load to the self.metadata class
        # note that .load() is a delta update so not all
        # settings, data_sources and data_sets needs to be there
        # actually there can be only one of each as a tab switch from one to another

        object_selector = {"settings": {}, "data_sources": {}, "data_sets": {}}

        # the  object selector thing is just a hack to select the good object based on a string
        payload = {"settings": [object_selector["settings"]], "data_sources": [object_selector["data_sources"]], "data_sets": [object_selector["data_sets"]]}

        # loop over all attributes of the main class
        for field_key, field_value in self.__dict__.items():
            # the parsed key from the fields to navigate throught the json structure
            parsed_key = self.parse_attribute(field_key)

            # example of a parsed key which is not a list
            # {
            #     'attribute': True,
            #     'key': 'settings/specimen/description',
            #     'depth': 3,
            #     'base': 'settings',
            #     'keys': ['specimen', 'description'],
            #     'array': False,
            #     'idx': 0
            # }
            # and which is a list
            # {
            #     'attribute': True,
            #     'key': 'settings/specimen/names__1',
            #     'depth': 3,
            #     'base': 'settings',
            #     'keys': ['specimen', 'names'],
            #     'array': True,
            #     'idx': '1'
            # }

            # we ignore attributes of the class that are not fields
            if not parsed_key["attribute"]:
                continue

            # the value to set
            json_val = pyqtislameaf(field_value)

            print(f"{field_key: <40}: {json_val}")

            if parsed_key["base"] == "root":
                # we are here in the root metadata
                # for now only simple values are handled

                json_key = parsed_key["keys"][0]
                payload[json_key] = json_val

            elif parsed_key["base"] in ["settings", "data_sources", "data_sets"]:
                current_object = object_selector[parsed_key["base"]]

                # here we enter setting, data_source or data_sets
                # print(parsed_key)

                if parsed_key["array"]:
                    if parsed_key["depth"] == 3:
                        # here we have a list of simple types like
                        # settings/specimen/sizes__0/title
                        # settings/specimen/sizes__1/value

                        k1 = parsed_key["keys"][1]
                        idx = parsed_key["idx"]
                        # STEP 1: initialise the list
                        if k1 not in current_object:
                            current_object[k1] = []
                        # STEP 2: set size of the list to be at least idx (fill with "")
                        while len(current_object[k1]) < idx + 1:
                            current_object[k1].append("")
                        # STEP 3: set value to index idx of the list
                        current_object[k1][idx] = json_val

                    elif parsed_key["depth"] == 4:
                        # here we have list object type like
                        # settings/specimen/sizes__0/unit
                        # settings/specimen/sizes__1/value
                        k1 = parsed_key["keys"][1]
                        k2 = parsed_key["keys"][2]
                        idx = parsed_key["idx"]
                        # STEP 1: initialise the list
                        if k1 not in current_object:
                            current_object[k1] = []
                        # STEP 2: set size of the list to be at least idx (fill with empty dict)
                        while len(current_object[k1]) < idx + 1:
                            current_object[k1].append({})
                        # STEP 3: set value for key k2 to index idx of the list
                        current_object[k1][idx][k2] = json_val

                else:
                    if parsed_key["depth"] == 3:
                        # here we have simple type like
                        # settings/specimen/id
                        # data_sources/generic/title

                        k1 = parsed_key["keys"][1]
                        current_object[k1] = json_val

                    elif parsed_key["depth"] == 4:
                        # here we have object type like
                        # settings/specimen/size/unit
                        # settings/specimen/size/value

                        k1 = parsed_key["keys"][1]
                        k2 = parsed_key["keys"][2]
                        # STEP 1: initialise the object
                        if k1 not in current_object:
                            current_object[k1] = {}
                        # STEP 2: set value for key k2
                        current_object[k1][k2] = json_val

        print("------------")
        pprint(payload)
        self.metadata.load(payload)
        print("------------")
        print(self.metadata)
        self.json = dict(self.metadata)

        # update combo boxes:
        print("UPDATE settings combo boc")
        self.setSettingsComboBox()

    def validate_metadata(self):
        try:
            validate(self.json)
        except Exception as e:
            print(e)
            self.outputText.setText(str(e))
            self.outputText.setStyleSheet("color: #e22;")
        else:
            self.outputText.setText("Valid JSON file")
            self.outputText.setStyleSheet("color: #2a2;")

    def save(self):
        # update json file name
        self.onEditingFinished()  # update display if last edit is a text field
        self.json_file_name = pyqtislameaf(self.json_file_name_field)
        self.update_metadata_from_fields()

        try:
            name = self.json_file_name
            if self.json_file_name[-5:] == ".json":
                name = self.json_file_name.replace(".json", "")
            self.metadata.save_json(name=name)
            self.outputText.setText(f"JSON file saved: {name}.json")
            self.outputText.setStyleSheet("color: #2a2;")

        except Exception as e:
            print(e)
            self.outputText.setText(str(e))
            self.outputText.setStyleSheet("color: #e22;")

    def onEditingFileName(self):
        self.json_file_name = pyqtislameaf(self.json_file_name_field)
        if not len(self.json_file_name):
            self.json_file_name = None
            return

        if not self.json_file_name[-5:] == ".json":
            self.json_file_name += ".json"
        self.json_file_name = slugify_file_name(self.json_file_name)
        self.json_file_name_field.setText(self.json_file_name)

    def onEditingFinished(self):
        self.update_metadata_from_fields()

        # edit file name if None and title set
        if self.json_file_name is None and "title" in self.json:
            self.json_file_name = slugify.slugify(self.json["title"]) + ".json"
            self.json_file_name_field.setText(self.json_file_name)

        # edit json raw
        self.rawJson.setText(json.dumps(self.json, indent=2))
        self.validate_metadata()

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clearLayout(item.layout())
