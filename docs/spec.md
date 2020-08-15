# Meep APIs

## Resources

### Location

| Property | Description 
| --- | ---
`id` | `Int`
`address` | `String`
`city` | `String`
`latitude` | `Double`
`longitude` | `Double`
`state` | `String` 
`zipCode` | `Int`

### Project

| Property | Description 
| --- | ---
 `id` | `Int`
 `name` | `String`
`description` | `String` 
`photo_url` | `String` 
`website_url` | `String` 
`year` | `Int`  
`gge_reduced` | `Double`  
`ghg_reduced` | `Double` 
`project_type_id` | `Int`


## Operations

### Operation: Get Location Markers

__URL__: `/location-markers`

__Example__: `GET http://127.0.0.1:5000/location-markers`

```json 
{
    "locationMarkers":[
        {
            "center":{
                "lat":-95.2632409,
                "lng":38.9930314
            },
            "gge_reduced":1995.0,
            "ghg_reduced":2.5845225,
            "points":[
                {
                    "lat":-95.2632409,
                    "lng":38.9930314
                }
            ],
            "project_ids":[1],
            "project_name":"Black Hills Energy- KS",
            "project_types":["Building"]
        },
        {
            "center":{
                "lat":-94.6095686,
                "lng":38.8705357
            },
            "gge_reduced":2891.461077,
            "ghg_reduced":1.133452742,
            "points":[
                {
                    "lat":-94.6095686,
                    "lng":38.8705357
                }
            ],
            "project_ids":[2],
            "project_name":"Central States Beverage Company",
            "project_types":["Building"]
        }
    ]
}
```

### Operation: Get Location by ID

__URL__: `/locations/<int:id>`

__Example__: `GET http://127.0.0.1:5000/locations/1`

```json
{
    "address":"601 N Iowa St",
    "city":"Lawrence",
    "latitude":-95.2632409,
    "longitude":38.9930314,
    "state":"KS",
    "zipCode":66044
}
```

### Operation: Get Locations

Returns a list of all locations.

__URL__: `/locations`

__EXAMPLE__: `GET http://127.0.0.1:5000/locations/`

```json
{
    "locations":[
        {
            "address":"601 N Iowa St",
            "city":"Lawrence",
            "id":1,
            "latitude":-95.2632409,
            "longitude":38.9930314,
            "state":"KS",
            "zipCode":66044
        },
        {
            "address":"14220 Wyandotte St",
            "city":"Kansas City",
            "id":2,
            "latitude":-94.6095686,
            "longitude":38.8705357,
            "state":"MO",
            "zipCode":64145
        }
    ]
}

```

### Operation: GET Project by Location ID

__URL__: `/locations/<int:id>/project`

__Example__: `GET http://127.0.0.1:5000/locations/1/project`

```json
{
    "id": 1, 
    "name": "Black Hills Energy- KS", 
    "description": null, 
    "photo_url": null, 
    "website_url": null, 
    "year": 2013, 
    "gge_reduced": 1995.0, 
    "ghg_reduced": 2.5845225, 
    "project_type_id": 1
}
```

### Operation: GET Projects

__URL__: `/projects`

__Example__: `GET http://127.0.0.1:5000/projects`

```json
{
    "projects": [
        {
            "id": 1, 
            "name": "Black Hills Energy- KS", 
            "description": null, 
            "photoUrl": null, 
            "websiteUrl": null, 
            "year": 2013, 
            "ggeReduced": 1995.0, 
            "ghgReduced": 2.5845225
        },
        {
            "id": 2, 
            "name": "Central States Beverage Company", 
            "description": null, 
            "photoUrl": null, 
            "websiteUrl": null, 
            "year": 2012, 
            "ggeReduced": 2891.461077, 
            "ghgReduced": 1.133452742
        }
    ]
}
```

### Operation: GET Project by ID

__URL__: `/projects/<int:id>`

__Example:__ `GET http://127.0.0.1:5000/projects/1`

```json
{   
    "id": 1, 
    "name": "Black Hills Energy- KS", 
    "description": null, 
    "photoUrl": null, 
    "websiteUrl": null, 
    "year": 2013, 
    "ggeReduced": 1995.0, 
    "ghgReduced": 2.5845225
}
```

### Operation: GET Project Types

__URL__: `/project-types`

__Example:__ `GET http://127.0.0.1:5000/project-types`

```json 
{
    "project_types": [
        {
            "id": 1, 
            "typeName": "Building"
        }, 
        {
            "id": 2, 
            "typeName": "Vehicle Transportation"
        }, 
        {
            "id": 3, 
            "typeName": "Infastructure Transportation"
        }
    ]
}
```

### Operation: Get Project Type by ID

__URL__: `/project-types/<int:id>`

__Example__: `GET http://127.0.0.1:5000/project-types/1` 

```json 
{
    "id": 1, 
    "typeName": "Building"
}
```

### Operation: GET Projects by Project Type 

__URL__: `/project-type/<ind:id>/project`

__Example__: `GET http://127.0.0.1:5000/project-types/1/projects`

```json
{
    "projects": [
        {
            "id": 1, 
            "name": "Black Hills Energy- KS", 
            "description": null, 
            "photo_url": null, 
            "website_url": null, 
            "year": 2013, 
            "gge_reduced": 1995.0, 
            "ghg_reduced": 2.5845225, 
            "project_type_id": 1
        },
        {
            "id": 2, 
            "name": "Central States Beverage Company", 
            "description": null, 
            "photo_url": null, 
            "website_url": null, 
            "year": 2012, 
            "gge_reduced": 2891.461077, 
            "ghg_reduced": 1.133452742, 
            "project_type_id": 1
        },
        {
            "id": 6, 
            "name": "Lincoln Airport Authority -CNG", 
            "description": null, 
            "photo_url": null, 
            "website_url": null, 
            "year": 2017, 
            "gge_reduced": 11970.0, 
            "ghg_reduced": 15.507135, 
            "project_type_id": 1
        },
        {
            "id": 7, 
            "name": " State of Missouri - Propane", 
            "description": null, 
            "photo_url": null, 
            "website_url": null, 
            "year": 2017, 
            "gge_reduced": 903.101, 
            "ghg_reduced": 1.276533264, 
            "project_type_id": 1
        }
    ]
}
```

### Operation: GET All Locations by Project ID

__URL__: `/projects/<int:id>/locations`

__Example:__ `GET http://127.0.0.1:5000/projects/1/locations`

```json
{
    "locations": [
        {
            "address": "601 N Iowa St",
            "city": "Lawrence",
            "state": "KS",
            "zip_code": 66044,
            "longitude": 38.9930314,
            "latitude": -95.2632409
        }
    ]
}
```

### Operation: GET Project Detail by Project ID

__URL__: `/projects/1/detail`

__Example:__ `GET http://127.0.0.1:5000/projects/1/detail`

```json 
{
    "date":"2013",
    "details":null,
    "emissions_data":{
        "gge_reduced":1995.0,
        "ghg_reduced":2.5845225
    },
    "img":null,
    "project_name":"Black Hills Energy- KS",
    "project_type":"Building"
}
```

### Operation: GET Project Summary by Project ID

__URL__: `/projects/<int:id>/summary`

__Example:__ `GET http://127.0.0.1:5000/projects/1/summary`

```json
{
    "date":"2013",
    "img":null,
    "project_details":null,
    "project_name":"Black Hills Energy- KS"
}
```

### Operation: POST Project New from CSV

__URL__: `/projects/upload/csv`

__Example__: `POST 127.0.0.1:5000/projects/upload/csv`