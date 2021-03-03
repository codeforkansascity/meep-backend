with
    projects_and_types
    as
    (
        select
            projects.id,
            name,
            year as project_year,
            gge_reduced,
            ghg_reduced,
            type_name as project_type
        from
            projects
            join
            project_types
            on projects.project_type_id = project_types.id
    ),
    proj_locs
    as
    (
        select
            name,
            sum(project_year) as project_year,
            sum(gge_reduced) as gge_reduced,
            sum(ghg_reduced) as ghg_reduced,
            array_agg(project_type) as project_types,
            array_agg(projects_and_types.id) as project_ids,
            ST_Collect(location) as points
        from
            projects_and_types
            join
            locations
            on projects_and_types.id = locations.id
        group by name
    )
select
    ST_AsGeoJSON(points)::json -> 'coordinates' as points,
    name as project_name,
    project_year, 
    ST_AsGeoJSON(ST_Centroid(points))::json -> 'coordinates' as center,
    project_ids, 
    project_types, 
    ghg_reduced, 
    gge_reduced
from proj_locs;