from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

from lxml import etree


VAR_COLOUR_RANGES = {
    'salinity': {'colorBarMinimum': '0.0', 'colorBarMaximum': '34.0'},
    'temperature': {'colorBarMinimum': '4.0', 'colorBarMaximum': '20.0'},
    'uVelocity': {'colorBarMinimum': '-8.0', 'colorBarMaximum': '8.0'},
    'vVelocity': {'colorBarMinimum': '-8.0', 'colorBarMaximum': '8.0'},
    'ssh': {'colorBarMinimum': '-4.0', 'colorBarMaximum': '4.0'},
    'mixed_layer_depth': {'colorBarMinimum': '0', 'colorBarMaximum': '30.0'},
    'biogenic_silicon': {'colorBarMinimum': '0', 'colorBarMaximum': '70.0'},
    'nitrate': {'colorBarMinimum': '0', 'colorBarMaximum': '40.0'},
    'silicon': {'colorBarMinimum': '0', 'colorBarMaximum': '70.0'},
    'diatoms': {'colorBarMinimum': '0', 'colorBarMaximum': '20.0'},
    'longitude': {'colorBarMinimum': '-127.0', 'colorBarMaximum': '-121.0'},
    'latitude': {'colorBarMinimum': '46.0', 'colorBarMaximum': '52.0'},
    'bathymetry': {'colorBarMinimum': '0.0', 'colorBarMaximum': '450.0'},
}


IOOS_CATEGORIES = {
    'time': 'time',
    'gridX': 'location',
    'gridY': 'location',
    'gridZ': 'location',
    'latitude': 'location',
    'longitude': 'location',
    'bathymetry': 'bathymetry',
    'salinity': 'salinity',
    'temperature': 'temperature',
    'uVelocity': 'currents',
    'vVelocity': 'currents',
    'wVelocity': 'currents',
    'ssh': 'sea_level',
    'mixed_layer_depth': 'physical_oceanography',
    'dissipation': 'physical_oceanography',
    'vert_eddy_diff': 'physical_oceanography',
    'vert_eddy_visc': 'physical_oceanography',
    'fraser_river_tracer': 'physical_oceanography',
    'ammonium': 'dissolved_nutrients',
    'biogenic_silicon': 'dissolved_nutrients',
    'dissolved_organic_nitrogen': 'dissolved_nutrients',
    'nitrate': 'dissolved_nutrients',
    'particulate_organic_nitrogen': 'dissolved_nutrients',
    'silicon': 'dissolved_nutrients',
    'ciliates': 'biology',
    'diatoms': 'biology',
    'flagellates': 'biology',
    'mesozooplankton': 'biology',
    'microzooplankton': 'biology',
}

# Functions from UBC --------------------------
# Disclaimer: Functions below has been slightly modified.
# Source: https://bitbucket.org/salishsea/erddap-datasets


def print_tree(root):
    """Display an XML tree fragment with indentation.
    """
    print(etree.tostring(root, pretty_print=True).decode('ascii'))


def find_att(root, att):
    """Return the dataset attribute element named att
    or raise a ValueError exception if it cannot be found.
    """
    e = root.find('.//att[@name="{}"]'.format(att))
    if e is None:
        raise ValueError('{} attribute element not found'.format(att))
    return e


def replace_yx_with_lonlat(root):
    new_axes = {
        'y': {'sourceName': 'nav_lon', 'destinationName': 'longitude'},
        'x': {'sourceName': 'nav_lat', 'destinationName': 'latitude'},
    }
    for axis in root.findall('.//axisVariable'):
        if axis.find('.//sourceName').text in new_axes:
            key = axis.find('.//sourceName').text
            new_axis = etree.Element('axisVariable')
            etree.SubElement(new_axis, 'sourceName').text = new_axes[key]['sourceName']
            etree.SubElement(new_axis, 'destinationName').text = new_axes[key]['destinationName']
            axis.getparent().replace(axis, new_axis)


def update_xml(root, datasetID, metadata, datasets, dataset_vars):
    root.attrib['datasetID'] = datasetID
    root.find('.//fileNameRegex').text = datasets[datasetID]['fileNameRegex']

    title = datasets[datasetID]['title']
    if 'keywords' in datasets[datasetID]:
        keywords = find_att(root, 'keywords')
        keywords.text = datasets[datasetID]['keywords']
    summary = find_att(root, 'summary')
    summary.text = f'{title}\n\n{datasets[datasetID]["summary"]}'
    e = find_att(root, 'title')
    e.text = title
    #     summary.addnext(e)

    for att, info in metadata.items():
        e = etree.Element('att', name=att)
        e.text = info['text']
        try:
            root.find(f'''.//att[@name="{info['after']}"]''').addnext(e)
        except KeyError:
            find_att(root, att).text = info['text']

    attrs = root.find('addAttributes')
    etree.SubElement(attrs, 'att', name='NCO').text = 'null'
    if not 'Bathymetry' in datasetID:
        etree.SubElement(attrs, 'att', name='history').text = 'null'
        etree.SubElement(attrs, 'att', name='name').text = 'null'

    for axis_name in root.findall('.//axisVariable/sourceName'):
        # Since v1.80 the ERDDAP GenerateDatasetsXml.sh tool changes variables named y and x
        # into latitude and longitude variables. But our y and x are grid indices, so we fix them.
        if axis_name.text in ('y', 'x'):
            dest_name = axis_name.getparent().find('destinationName')
            dest_name.text = f'grid{axis_name.text.upper()}'
            attrs = axis_name.getparent().find('addAttributes')
            long_name = find_att(attrs, 'long_name')
            long_name.text = axis_name.text.upper()
            for att_name in ('source_name', 'standard_name', 'units'):
                att = find_att(attrs, att_name)
                att.getparent().remove(att)

    for axis_name in root.findall('.//axisVariable/destinationName'):
        attrs = axis_name.getparent().find('addAttributes')
        etree.SubElement(attrs, 'att', name='coverage_content_type').text = 'modelResult'

        if axis_name.text == 'time':
            etree.SubElement(attrs, 'att', name='comment').text = (
                'time values are UTC at the centre of the intervals over which the calculated model results are averaged')

        if axis_name.text in ('x', 'y', 'z'):
            axis_name.text = f'grid{axis_name.text.upper()}'

        if axis_name.text in IOOS_CATEGORIES:
            etree.SubElement(attrs, 'att', name='ioos_category').text = IOOS_CATEGORIES[axis_name.text]

    if datasets[datasetID]['type'] == 'tide gauge':
        replace_yx_with_lonlat(root)

    for var_name in root.findall('.//dataVariable/destinationName'):
        if var_name.text in dataset_vars:
            var_name.text = dataset_vars[var_name.text]['destinationName']

        if var_name.text in VAR_COLOUR_RANGES:
            for att_name in ('colorBarMinimum', 'colorBarMaximum'):
                cb_att = var_name.getparent().find(f'addAttributes/att[@name="{att_name}"]')
                if cb_att is not None:
                    cb_att.text = VAR_COLOUR_RANGES[var_name.text][att_name]
                else:
                    attrs = var_name.getparent().find('addAttributes')
                    etree.SubElement(attrs, 'att', name=att_name, type='double').text = (
                        VAR_COLOUR_RANGES[var_name.text][att_name])

        attrs = var_name.getparent().find('addAttributes')
        etree.SubElement(attrs, 'att', name='coverage_content_type').text = 'modelResult'
        etree.SubElement(attrs, 'att', name='cell_measures').text = 'null'
        etree.SubElement(attrs, 'att', name='cell_methods').text = 'null'
        etree.SubElement(attrs, 'att', name='interval_operation').text = 'null'
        etree.SubElement(attrs, 'att', name='interval_write').text = 'null'
        etree.SubElement(attrs, 'att', name='online_operation').text = 'null'

        if var_name.text in IOOS_CATEGORIES:
            etree.SubElement(attrs, 'att', name='ioos_category').text = IOOS_CATEGORIES[var_name.text]
# End functions from UBC --------------------------
