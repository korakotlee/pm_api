# PM-API

### Usage

set up the directories to run
```
./setup.sh /var/api
```

set up crontab to run periodically.
```
pm-api <input-dir>
```

`pm-api` will look into the directory and read `json`
file and run the request. Response will be placed in
the `<input-dir>/response` directory.

The successful requests will be moved to `<input-dir>/success` directory.
The failed requests will be moved to `<input-dir>/fail` directory.

### Callback

If the `callback` is specified, the tool will `POST` to the url with the response.
### TODO

- for file in files
    - call until success
    - save responses
    - if exist, callback when success
    - sleep 1/limit * margin
    - move file to success / fail
