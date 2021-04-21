[![Build Status - GitHub](https://github.com/YaPeL/dcr-be/workflows/test/badge.svg)](https://github.com/YaPeL/dcr-be/actions?query=workflow%3Atest)
[![](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/downloads/release/python-3710/)

## Configuration

make Sure you edited the .env file with the correct GMAP_API_KEY

## Running the code


You should have docker and docker compose installed. When starting, the application will search for a `.env` file.

To start you development environment just run :

```sh
  docker-compose up
```

Or if you want to run the container in detached mode:

```sh
  docker-compose up -d
```

To stop it:

```sh
  docker-compose down
```

## Running the tests


```sh
  virtualenv env/
  source env/bin/activate
  pip install -r test-requirements.txt
  pytest app/
```

## Future plans, what is missing 
* Currently, I generate the nearby points using heuristics, a better approach would be to rip all the valid points from the original project,
and store them in a database, probably PostGIS, benefits:
** We can get nearby points using a distance radio,
   currently, at the poles, the max distance between them is 2 km, but is around 100 km at the Equator
  ie: using my method you will always get at max, 5 points, using a radio, you should get more the further away you get from the Equator
** Since we can store previous request, we can use the db as a cache instead of dealing with Gmaps (saving money!) 
* More tests!
* While most of the integer points are going to fall in the middle of nowhere, some rare cases may end up in a city
  so implementing the other endpoint to reverse information from a point could be useful,
  caching could still be used, but we should be aware of when we need to invalidate it
* the geo/nearby endpoint has too much responsibilities, it could be splitted into 2 endpoints,
  get nearby points, get distance between points, I was aware of this from the start, but did it this way to save time
* the infoMark text should not be coming from the backend.
* Add metric and imperial system for distances.