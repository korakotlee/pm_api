# PM-API

### Usage

set up crontab to run periodically.
```
pm-api <input-dir>
```

`pm-api` will look into the directory and read `yaml`
file and run the request. Response will be placed in
the `<input-dir>/response` directory.

The successful requests will be moved to `<input-dir>/success` directory.
The failed requests will be moved to `<input-dir>/fail` directory.

Servers can be configured using a config file

### TODO

- check dirs is exists, create `response`, `success`, `fail` if necessary 
- read config if it exists
- for file in files
- retry = read from config / default ( = 3)
- limit = read from config / default (per second) default = 10
- while retry:
    - call until success
    - save responses
    - if exist, callback when success
    - sleep 1/limit * margin
- move file to success / fail
