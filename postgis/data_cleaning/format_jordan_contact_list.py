from functools import partial

import pandas as pd

def project_type_id(project_class, project_types):
    project_types = project_types.copy()
    if project_class == 'Fleet':
        type_name = 'Vehicle Transportation'
    elif project_class == 'Fuel station':
        type_name = 'Building'
    else:
        type_name = 'NULL'
    [idx] = project_types.index[project_types.type_name == type_name]
    return idx


def format_column_name(c):
    return c.lower().strip().replace(' ', '_')


def make_projects(contacts, project_types):
    contacts = contacts.copy()
    project_types = project_types.copy()
    projects = contacts[['name', 'year', 'ghg_reduced']].copy()

    projects['project_type_id'] = contacts.project_class\
                                  .apply(partial(project_type_id, project_types=project_types))

    return projects


def make_locations(contacts):
    contacts = contacts.copy()

    locations = contacts[['address', 'state', 'zip_code', 'longitude', 'latitude']]

    locations['project_id'] = contacts.index

    locations = locations.dropna(how='all',
                                 subset=['address', 'state', 'zip_code',
                                         'longitude', 'latitude'],
                                 axis='index')

    locations = locations.fillna({'zip_code': -1, 'longitude': -1000, 'latitude': -1000})


    locations = locations.astype({'address': 'object', 'state': 'object',
                                  'zip_code': 'int64', 'longitude': 'float64',
                                  'latitude': 'float64', 'project_id': 'int64'})

    return locations


def main():
    contacts = pd.read_excel('processed/jordan-contacts-06-17-2019.xlsx')
    unnamed = [c for c in contacts.columns if 'unnamed' in c.lower()]
    contacts = contacts.drop(unnamed, axis=1)
    contacts.columns = [format_column_name(c) for c in contacts.columns]

    project_types = pd.DataFrame({'type_name': ['Building', 'Vehicle Transportation', 'Infrastructure Transportation', 'NULL']})

    projects = make_projects(contacts, project_types)

    locations = make_locations(contacts)

    return project_types, contacts, projects, locations

if __name__ == '__main__':
    project_types, contacts, projects, locations = main()
