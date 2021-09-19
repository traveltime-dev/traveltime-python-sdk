from .utils import traveltime_api, APIError, build_body


def map_info():
    """Map Info

    Returns information about currently supported countries.
    See https://traveltime.com/docs/api/reference/map-info for details

    Returns:
        dict: API response parsed as a dictionary
    """
    return traveltime_api(path=['map-info'])


def supported_locations(locations):
    """Supported Locations

    Find out what points are supported by the api.
    The returned map name for a point can be used to determine what features are supported.
    See https://traveltime.com/docs/api/reference/supported-locations for details

    Args:
        locations (dict): Locations to use. Each location requires an id and lat/lng values

    Returns:
        dict: API response parsed as a dictionary
    """
    return traveltime_api(path=['supported-locations'], body=build_body(locals()))


def geocoding(query, within_country=None, exclude_location_types=None):
    """Geocoding (Search)

    Match a query string to geographic coordinates.
    See https://traveltime.com/docs/api/reference/geocoding-search for details

    Args:
        query (str): A query to geocode. Can be an address, a postcode or a venue.
        within_country (str, optional): Only return the results that are within the specified country.
         If no results are found it will return the country itself. Format:ISO 3166-1 alpha-2 or alpha-3
        exclude_location_types (str, optional): Exclude location types from results. Available values: "country".

    Returns:
        dict: API response parsed as a dictionary
    """
    queryFull = {'query': query,
                 'within.country': within_country,
                 'exclude.location.types': exclude_location_types}

    return traveltime_api(path=['geocoding', 'search'], query={key: value for (
        key, value) in queryFull.items() if not value is None})


def geocoding_reverse(lat, lng, within_country=None, exclude_location_types=None):
    """Reverse Geocoding

    Attempt to match a latitude, longitude pair to an address.
    See https://traveltime.com/docs/api/reference/geocoding-reverse for details

    Args:
        lat (float): Latitude of the point to reverse geocode.
        lng (float): Longitude of the point to reverse geocode.
        within_country (str, optional): Only return the results that are within the specified country.
         If no results are found it will return the country itself. Format:ISO 3166-1 alpha-2 or alpha-3
        exclude_location_types (str, optional): Exclude location types from results. Available values: "country".

    Returns:
        dict: API response parsed as a dictionary
    """
    queryFull = {'lat': lat,
                 'lng': lng,
                 'within.country': within_country,
                 'exclude.location.types': exclude_location_types}

    return traveltime_api(path=['geocoding', 'reverse'], query={key: value for (
        key, value) in queryFull.items() if not value is None})


def time_map(departure_searches=None, arrival_searches=None, unions=None, intersections=None):
    """Isochrones (Time Map)

    Given origin coordinates, find shapes of zones reachable within corresponding travel time.
    Find unions/intersections between different searches
    See https://traveltime.com/docs/api/reference/isochrones for details

    Args:
        departure_searches (dict, optional): Searches based on departure times.
         Leave departure location at no earlier than given time. You can define a maximum of 10 searches
        arrival_searches (dict, optional): Searches based on arrival times.
         Arrive at destination location at no later than given time. You can define a maximum of 10 searches
        unions (dict, optional): Define unions of shapes that are results of previously defined searches.
        intersections (dict, optional): Define intersections of shapes that are results of previously defined searches.

    Returns:
         dict: API response parsed as a dictionary
    """
    if departure_searches is None and arrival_searches is None:
        raise APIError(
            "At least one of arrival_searches/departure_searches required!")

    return traveltime_api(path=['time-map'], body=build_body(locals()))


def routes(locations, departure_searches=None, arrival_searches=None):
    """Routes

    Returns routing information between source and destinations.
    See https://traveltime.com/docs/api/reference/routes for details

    Args:
        locations (dict): Locations to use. Each location requires an id and lat/lng values
        departure_searches (dict, optional): Searches based on departure times.
         Leave departure location at no earlier than given time. You can define a maximum of 10 searches
        arrival_searches (dict, optional): Searches based on arrival times.
         Arrive at destination location at no later than given time. You can define a maximum of 10 searches

    Returns:
        dict: API response parsed as a dictionary
    """
    if departure_searches is None and arrival_searches is None:
        raise APIError(
            "At least one of arrival_searches/departure_searches required!")

    return traveltime_api(path=['routes'], body=build_body(locals()))


def time_filter(locations, departure_searches=None, arrival_searches=None):
    """Distance Matrix (Time Filter)

    Given origin and destination points filter out points that cannot be reached within specified time limit.
    Find out travel times, distances and costs between an origin and up to 2,000 destination points.
    See https://traveltime.com/docs/api/reference/distance-matrix for details

    Args:
        locations (dict): Locations to use. Each location requires an id and lat/lng values
        departure_searches (dict, optional): Searches based on departure times.
         Leave departure location at no earlier than given time. You can define a maximum of 10 searches
        arrival_searches (dict, optional): Searches based on arrival times.
         Arrive at destination location at no later than given time. You can define a maximum of 10 searches

    Returns:
        dict: API response parsed as a dictionary
    """
    if departure_searches is None and arrival_searches is None:
        raise APIError(
            "At least one of arrival_searches/departure_searches required!")

    return traveltime_api(path=['time-filter'], body=build_body(locals()))


def time_filter_fast(locations, arrival_many_to_one=None, arrival_one_to_many=None):
    """Time Filter (Fast)

    A very fast version of time_filter().
    However, the request parameters are much more limited.
    Currently only supports UK and Ireland.
    See https://traveltime.com/docs/api/reference/time-filter-fast for details

    Args:
        locations (dict): Locations to use. Each location requires an id and lat/lng values
        arrival_many_to_one (dict, optional): Specify a single arrival location and multiple departure locations. Max 10.
        arrival_one_to_many (dict, optional): Specify a single departure location and multiple arrival locations. Max 10.

    Returns:
         dict: API response parsed as a dictionary
    """
    if arrival_many_to_one is None and arrival_one_to_many is None:
        raise APIError(
            "At least one of arrival_many_to_one/arrival_one_to_many required!")

    bodyPrep = build_body(locals())
    body = {'arrival_searches': {}, 'locations': bodyPrep['locations']}

    if 'arrival_many_to_one' in bodyPrep:
      body['arrival_searches']['many_to_one'] = bodyPrep['arrival_many_to_one']
    if 'arrival_one_to_many' in bodyPrep:
      body['arrival_searches']['one_to_many'] = bodyPrep['arrival_one_to_many']

    return traveltime_api(path=['time-filter', 'fast'], body=body)


def time_filter_postcodes(departure_searches=None, arrival_searches=None):
    """Time Filter (Postcodes)

    Find reachable postcodes from origin (or to destination) and get statistics about such postcodes.
    Currently only supports United Kingdom.
    See https://traveltime.com/docs/api/reference/postcode-search for details

    Args:
        departure_searches (dict, optional): Searches based on departure times.
         Leave departure location at no earlier than given time. You can define a maximum of 10 searches
        arrival_searches (dict, optional): Searches based on arrival times.
         Arrive at destination location at no later than given time. You can define a maximum of 10 searches

    Returns:
        dict: API response parsed as a dictionary
    """
    if departure_searches is None and arrival_searches is None:
        raise APIError(
            "At least one of arrival_searches/departure_searches required!")

    return traveltime_api(path=['time-filter', 'postcodes'], body=build_body(locals()))


def time_filter_postcode_districts(departure_searches=None, arrival_searches=None):
    """Time Filter (Postcode Districts)

    Find districts that have a certain coverage from origin (or to destination) and get statistics about postcodes within such districts.
    Currently only supports United Kingdom.
    See https://traveltime.com/docs/api/reference/postcode-district-filter for details

    Args:
        departure_searches (dict, optional): Searches based on departure times.
         Leave departure location at no earlier than given time. You can define a maximum of 10 searches
        arrival_searches (dict, optional): Searches based on arrival times.
         Arrive at destination location at no later than given time. You can define a maximum of 10 searches

    Returns:
        dict: API response parsed as a dictionary
    """
    if departure_searches is None and arrival_searches is None:
        raise APIError(
            "At least one of arrival_searches/departure_searches required!")

    return traveltime_api(path=['time-filter', 'postcode-districts'], body=build_body(locals()))


def time_filter_postcode_sectors(departure_searches=None, arrival_searches=None):
    """Time Filter (Postcode Sectors)

    Find sectors that have a certain coverage from origin (or to destination) and get statistics about postcodes within such sectors.
    Currently only supports United Kingdom.
    See https://traveltime.com/docs/api/reference/postcode-sector-filter for details

    Args:
        departure_searches (dict, optional): Searches based on departure times.
         Leave departure location at no earlier than given time. You can define a maximum of 10 searches
        arrival_searches (dict, optional): Searches based on arrival times.
         Arrive at destination location at no later than given time. You can define a maximum of 10 searches

    Returns:
       dict: API response parsed as a dictionary
    """
    if departure_searches is None and arrival_searches is None:
        raise APIError(
            "At least one of arrival_searches/departure_searches required!")

    return traveltime_api(path=['time-filter', 'postcode-sectors'], body=build_body(locals()))
