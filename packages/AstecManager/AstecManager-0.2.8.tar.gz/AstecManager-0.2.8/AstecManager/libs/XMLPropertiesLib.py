import xml.etree.ElementTree as XMLtree

cell_key_property = 'cell'
cell_identifier_property = 'cell-id'

# region Cell class

class Cell:
    """A class to represent a person.
    
        ...


    Attributes
    ----------
    id : int
        Cell identifier in the segmentation
    t : int
        Cell time point
    mothers : list
       cells that have this cell as a daughter
    daughters : list
       cells linked to this cell in lineage
    Methods
    -------
    add_mother(cell):
        Add the cell in input as a mother by reference. No propagation to daughters is done in this function
    
    add_daughter(cell):
        Add the cell in input as a daughter by reference. No propagation to mothers is done in this function
    """

    id = -1
    t = -1
    mothers = []
    daughters = []

    def __init__(self, id_cell, time_cell):
        self.id = id_cell
        self.t = time_cell
        self.mothers = []
        self.daughters = []

    def add_mother(self, cell):
        """

        :param cell: 

        """
        if self.mothers is None:
            self.mothers = []
        if not cell in self.mothers:
            self.mothers.append(cell)

    def add_daughter(self, cell):
        """

        :param cell: 

        """
        if self.daughters is None:
            self.daughters = []
        if not cell in self.daughters:
            self.daughters.append(cell)

# endregion

# region Utils
def indent_xml(elem, level=0):
    """Take a xml tree as input, and compute it's indentation

    :param elem: input xml tree
    :type elem: XML tree
    :param level:  (Default value = 0)

    
    """
    i = "\n" + level * "  "
    j = "\n" + (level - 1) * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent_xml(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


def getCellTimeId(idl):
    """Return the cell t,id

    :param idl: 
    :type idl: basestring

    
    """
    t = int(int(idl) / (10 ** 4))
    cell_id = int(idl) - int(t) * 10 ** 4
    return t, cell_id


def getCellKey(t, idc):
    """Return the cell information id

    :param t: Cell time point
    :type t: int
    :param idc: Cell id
    :type idc: int

    
    """
    if t == 0 or t == "0":
        return idc
    return t * 10 ** 4 + idc

# endregion

# region Load from XML
def LoadKeyValue(property_element, filter_background=True):
    """From a cell specific element in a property , retrieve the cell key and its value as string

    :param property_element: Cell element in the xml file to get value
    :type property_element: XMLTreeElement
    :param filter_background: if True, does not return property of background (Default value = True)
    :type filter_background: bool

    
    """
    value = None
    cell_id = property_element.get(
        cell_identifier_property)  # In the element , the key can be found in the "cell-id" tag
    c_t, c_id = getCellTimeId(cell_id)  # Split time and identifier from the key
    if not filter_background or c_id != 1:  # Filter out the background if asked (background key is 1 in our data)
        cell_child = property_element.text  # Load cell value
        if cell_child is not None and cell_child != "None":
            value = cell_child.replace("'", "").replace(" ", "")
    return cell_id, value

def LoadCellToCellKeyValue(property_element, filter_background=True):
    """From a cell specific element in a property , retrieve the cell key and its values with cell in relations

    :param property_element: Cell element in the xml file to get value
    :type property_element: XMLTreeElement
    :param filter_background: if True, does not return property of background (Default value = True)
    :type filter_background: bool

    
    """
    values = []
    cell_id = property_element.get(
        cell_identifier_property)  # In the element , the key can be found in the "cell-id" tag
    c_t, c_id = getCellTimeId(cell_id)  # Split time and identifier from the key
    if not filter_background or c_id != 1:  # Filter out the background if asked (background key is 1 in our data)
        for cell_child in property_element.findall('cell'):
            cell_child_id = cell_child.get(
                cell_identifier_property)
            cc_t,cc_id = getCellTimeId(cell_child_id)
            if not filter_background or cc_id != 1:  # Filter out the background if asked (background key is 1 in our data)
                cell_child_val = cell_child.text  # Load cell value
                if cell_child_val is not None and cell_child_val != "None":
                    values.append((cell_child_id,cell_child_val.replace("'", "").replace(" ", "")))
    return cell_id, values


def LoadPropertyFromFile(xml_path, property_name, filter_background=True):
    """Load all lines from a specific property in the xml file as dict

    :param xml_path: Path to the xml file
    :type xml_path: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring
    :param filter_background: if True, does not return property of background (Default value = True)
    :type filter_background: bool

    
    """
    tree = LoadXMLTree(xml_path)
    if tree is None:
        return None
    return LoadPropertyFromTree(tree, property_name, filter_background)

def LoadCellToCellPropertyFromFile(xml_path, property_name, filter_background=True):
    """Load value for a specific cell in  a property in the xml file , for cell to cell relation ship property

    :param xml_path: Path to the xml file
    :type xml_path: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring
    :param filter_background: if True, does not return property of background (Default value = True)
    :type filter_background: bool

    
    """
    tree = LoadXMLTree(xml_path)
    if tree is None:
        return None
    return LoadCellToCellPropertyFromTree(tree, property_name, filter_background)
def LoadCellPropertyFromFile(cell_key, xml_path, property_name):
    """Load value for a specific cell in  a property in the xml file

    :param cell_key: Cell key to search
    :type cell_key: basestring
    :param xml_path: Path to the xml file
    :type xml_path: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring

    
    """
    tree = LoadXMLTree(xml_path)
    if tree is None:
        return None
    return LoadCellPropertyFromTree(cell_key, tree, property_name)


def LoadCellToCellPropertyFromFileForCell(cell_key, xml_path, property_name):
    """Load value for a specific cell in  a property in the xml file

    :param cell_key: Cell key to search
    :type cell_key: basestring
    :param xml_path: Path to the xml file
    :type xml_path: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring

    
    """
    tree = LoadXMLTree(xml_path)
    if tree is None:
        return None
    return LoadCellToCellPropertyFromTreeForCell(cell_key, tree, property_name)

def LoadCellPropertyFromTree(cell_key, xml_tree, property_name):
    """Load value for a specific cell in  a property in the xml tree

    :param cell_key: Cell key to search
    :type cell_key: basestring
    :param xml_tree: Path to the xml file
    :type xml_tree: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring

    
    """
    value = None
    tree = xml_tree.getroot()
    property_xml = tree.find(property_name)
    if property_xml is not None:
        for cell in property_xml.findall('cell'):
            cellid = cell.get(cell_identifier_property)
            if cell_key.lower() == cellid.lower():
                cell_key, value = LoadKeyValue(cell)
        return value
    return None

def LoadCellToCellPropertyFromTreeForCell(cell_key, xml_tree, property_name):
    """Load value for a specific cell in  a property in the xml tree , for a cell to cell relationship property

    :param cell_key: Cell key to search
    :type cell_key: basestring
    :param xml_tree: Path to the xml file
    :type xml_tree: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring

    
    """
    value = None
    tree = xml_tree.getroot()
    property_xml = tree.find(property_name)
    if property_xml is not None:
        for cell in property_xml.findall('cell'):
            cellid = cell.get(cell_identifier_property)
            if cell_key.lower() == cellid.lower():
                cell_key, value = LoadCellToCellKeyValue(cell)
        return value
    return None


def LoadPropertyFromTree(xml_tree, property_name, filter_background=True):
    """Load all lines from a specific property in the xml tree as dict

    :param xml_tree: XML tree
    :type xml_tree: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring
    :param filter_background: if True, does not return property of background (Default value = True)
    :type filter_background: bool

    
    """
    values = {}
    tree = xml_tree.getroot()
    property_xml = tree.find(property_name)
    if property_xml is not None:
        for cell in property_xml.findall(cell_key_property):
            cell_key, value = LoadKeyValue(cell, filter_background)
            if value is not None:
                values[cell_key] = value
        return values
    return None


def LoadCellToCellPropertyFromTree(xml_tree, property_name, filter_background=True):
    """Load all lines from a specific property in the xml tree as dict , property being cell to cell relationship values

    :param xml_tree: XML tree
    :type xml_tree: basestring
    :param property_name: if True, does not return property of background
    :type property_name: basestring
    :param filter_background: if True, does not return property of background (Default value = True)
    :type filter_background: bool

    
    """
    values = {}
    tree = xml_tree.getroot()
    property_xml = tree.find(property_name)
    if property_xml is not None:
        for cell in property_xml.findall(cell_key_property):
            cell_key, value = LoadCellToCellKeyValue(cell, filter_background)
            if value is not None:
                values[cell_key] = value
        return values
    return None

def LoadXMLTree(xml_path):
    """Parse the property file given in parameter , and returns it. Returns None if unable to find the file or read it

    :param xml_path: Path to the xml file
    :type xml_path: basestring

    
    """
    try:
        source = open(xml_path)
    except:
        return None
    return XMLtree.parse(source)


def LoadCellListFromFile(xml_path, lineage_property_name='cell_lineage'):
    """Load all cell keys from the lineage information of the xml file

    :param xml_path: Path to the xml file
    :type xml_path: basestring
    :param lineage_property_name: if True, does not return property of background (Default value = 'cell_lineage')
    :type lineage_property_name: basestring

    
    """
    tree = LoadXMLTree(xml_path)
    if tree is None:
        return None
    return LoadCellListFromTree(tree, lineage_property_name)


def LoadCellListFromTree(xml_tree, lineage_property_name='cell_lineage'):
    """Load all cell keys from the lineage information of the xml file

    :param xml_tree: XML tree of the properties
    :type xml_tree: basestring
    :param lineage_property_name: if True, does not return property of background (Default value = 'cell_lineage')
    :type lineage_property_name: basestring

    
    """
    cells = {}
    tree = xml_tree.getroot()
    lineage_elem = tree.find(lineage_property_name)
    if lineage_elem is not None:
        for cell in lineage_elem.findall(cell_key_property):
            cell_t, cell_id = getCellTimeId(
                cell.get(cell_identifier_property).replace("'", "").replace('[', '').replace(']', '').replace(" ", ""))
            cell_key = str(getCellKey(cell_t, cell_id))
            # cell_key = str(cell_t)+","+str(cell_id)
            if not cell_key in cells:
                cell_object = Cell(int(cell_id), int(cell_t))
                cells[cell_key] = cell_object
            cell_childs = cell.text.split(',')
            for cell_child_in_list in cell_childs:
                cell_child_t, cell_child_id = getCellTimeId(
                    cell_child_in_list.replace("'", "").replace('[', '').replace(']', '').replace(" ", ""))
                cell_child_key = str(getCellKey(cell_child_t, cell_child_id))
                if not cell_child_key in cells:
                    cell_child_object = Cell(int(cell_child_id), int(cell_child_t))
                    cells[cell_child_key] = cell_child_object

                if not cells[cell_child_key] in cells[cell_key].daughters:
                    cells[cell_child_key].add_mother(cells[cell_key])
        return cells
    return None


def SaveDictToXML(xml_path, xml_output_path, values_dict, property_name):
    """Load all cell keys from the lineage information of the xml file

    :param xml_path: 
    :param xml_output_path: 
    :param values_dict: 
    :param property_name: 

    
    """
    source = open(xml_path)
    tree = LoadXMLTree(xml_path)
    if tree is None:
        return None
    tree = tree.getroot()
    selec_node = property_name
    name_selec_elem = tree.find(selec_node)
    if name_selec_elem is None:
        name_selec_elem = XMLtree.SubElement(tree, selec_node)
    for cell in name_selec_elem.findall(cell_key_property):
        if int(cell.get(cell_identifier_property)) in values_dict.keys() or cell.get(
                cell_identifier_property) in values_dict.keys() and values_dict is not None and values_dict[cell.get(cell_identifier_property)] is not None:
            cell.text =str(values_dict[cell.get(cell_identifier_property)])
            values_dict.pop(cell.get(cell_identifier_property), None)
    for cell in values_dict:
        new_cell = XMLtree.SubElement(name_selec_elem, cell_key_property)
        new_cell.set(cell_identifier_property, cell)
        new_cell.text = str(values_dict[cell])
    indent_xml(tree)
    source.close()
    mydata = XMLtree.tostring(tree, encoding='utf8', method='xml').decode("utf8")
    myfile = open(xml_output_path, "w+")
    myfile.write(mydata)
    myfile.close()

def ListIdsByTimePoint(xml_tree):
    """List all cells ids by time point

    :param xml_tree: Root of xml properties
        Name of the property to save (or update) in the xml file
    :type xml_tree: xml_element

    
    """
    ids = {}
    local_list = LoadCellListFromTree(xml_tree)
    for cell in local_list:
        tc,idc=getCellTimeId(cell)
        if not tc in ids:
            ids[tc] = [idc]
        else :
            ids[tc].append(idc)
    return ids
# endregion
