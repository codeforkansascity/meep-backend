import json
from datetime import datetime
from operator import itemgetter

import pandas as pd
import numpy as np

"""
Script for extracting address and contact data from 'Project Contact List.xlsx'
"""


def main():
    filename = 'raw/Project Contact List.xlsx'

    contacts = pd.read_excel(filename, header=None)

    columns = ['PROJECT', 'SUBRECIPIENT ORGANIZATION', 'ADDRESS 1', 'ADDRESS 2',
               'CITY', 'STATE', 'ZIP', 'PHONE', 'WEBSITE']
    target = pd.DataFrame({c:[] for c in columns})


    # get rows containing the text SUBRECIPIENT ORGANIZATION
    buffer_text = 'SUBRECIPIENT ORGANIZATION'
    filter = contacts.apply(lambda row: row.str.contains(buffer_text).any(), axis=1)
    buffers = list(contacts.index[filter]) + [-1]

    chunks = (contacts.iloc[i:j, :] for (i, j) in zip(buffers, buffers[1:]))
    projects = tuple(munge_chunk(chunk) for chunk in chunks)
    projects_json = [project.to_dict() for project in projects]
    locations = pd.concat([project.locations_df() for project in projects])
    contacts = pd.concat([project.contacts_df() for project in projects])

    contacts['contact_type'] = set_contact_type(contacts['contact_type'])

    date = datetime.now().strftime('%m-%d-%Y')

    #save to json and csv files
    with open(f'processed/project-contacts-{date}.json', 'w') as f:
        f.write(json.dumps(projects_json, indent=2, default=str))

    locations.to_csv(f'processed/project-locations-{date}.csv', index=False)
    contacts.to_csv(f'processed/project-contacts-{date}.csv', index=False)

    #create a projects table from the data


    #create addresses table from project locations
    addresses = locations.drop(['phone', 'project', 'subrecipient_organization', 'website'], axis=1)
    addresses['address'] = addresses['address2']
    addresses['address'] = addresses['address'].fillna(addresses['address1'])
    addresses = addresses.drop(['address1', 'address2'], axis=1)
    addresses = addresses[addresses.address != 'TBD']
    addresses['zip'] = addresses.zip.fillna(-1)
    addresses = addresses.astype({'zip': 'int64'})
    addresses['address'] = addresses.address.str.split(',').apply(itemgetter(0))
    addresses.index = pd.RangeIndex(len(addresses))
    fill_data = np.empty(len(addresses))
    fill_data[:] = np.nan
    addresses['latitude'] = pd.Series(data=fill_data)
    addresses['longitude'] = pd.Series(data=fill_data)
    addresses['project_id'] = pd.Series(data=fill_data)

    addresses.to_csv(f'processed/addresses-{date}.csv', index_label='id')

    return projects_json, locations, contacts, addresses


def set_contact_type(series):
    series = series.copy()
    series = series.str.split(n=1)\
             .apply(itemgetter(0))\
             .str.lower()
    return series


def munge_chunk(chunk):
    # get project name
    project = chunk.iloc[1,0]
    subrecipient_organization = chunk.iloc[1,2]
    pc = ProjectContact(project, subrecipient_organization)

    # get all contacts
    # get only rows starting with Primary contact or secondary contact
    filter = chunk.loc[:, 0].isin(['Primary Contact', 'Primary Contract',
                                  'Secondary Contact'])
    contacts = chunk[filter].copy()
    contacts = tuple(tuple(r for r in row) for row in contacts.itertuples())
    contacts = tuple((row[1], *row[3:10]) for row in contacts)
    pc.contacts = [Contact(*row) for row in contacts]

    # get all locations
    locations = chunk.loc[:, 6:].copy()
    locations = locations.loc[locations.loc[:,6].notnull()]
    [contact_idx] = list(locations[locations.loc[:,6] == 'PHONE'].index)
    locations = locations.loc[:contact_idx-1, :]
    locations = locations[np.logical_not(locations.loc[:,6].str.match('address', case=False))]
    locations = [tuple(row) for row in locations.itertuples(index=False)]
    pc.locations = [Location(*row) for row in locations]

    return pc



class ProjectContact:
    def __init__(self, project, subrecipient_organization, locations=None,
                 contacts=None):
        self.project = project
        self.subrecipient_organization = subrecipient_organization
        self.locations = locations if locations else []
        self.contacts = contacts if contacts else []

    def __repr__(self):
        return "ProjectContact(project={self.project}, subrecipient_organization={self.subrecipient_organization})"\
                .format(self=self)

    def to_dict(self):
        return {
            'project': self.project,
            'subrecipient_organization': self.subrecipient_organization,
            'locations': [loc.to_dict() for loc in self.locations],
            'contacts': [contact.to_dict() for contact in self.contacts]
        }

    def locations_df(self):
        records = []
        for location in self.locations:
            record = {
                        'project': self.project,
                        'subrecipient_organization': self.subrecipient_organization,
                        **location.to_dict()
                    }
            records.append(record)
        return pd.DataFrame.from_records(records)

    def contacts_df(self):
        records = []
        for contact in self.contacts:
            record = {
                'project': self.project,
                'subrecipient_organization': self.subrecipient_organization,
                **contact.to_dict()
            }
            records.append(record)
        return pd.DataFrame.from_records(records)

class Location:
    def __init__(self, address1, address2, city, state, zip, phone, website):
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.phone = phone
        self.zip = zip
        self.website = website

    def to_dict(self):
        return self.__dict__

class Contact:
    def __init__(self, contact_type, prefix, first, last, title, phone, cell, email):
        self.contact_type=contact_type
        self.prefix=prefix
        self.first=first
        self.last=last
        self.title=title
        self.phone=phone
        self.cell=cell
        self.email=email

    def to_dict(self):
        return self.__dict__


if __name__ == '__main__':
    projects, locations, contacts, addresses = main()
