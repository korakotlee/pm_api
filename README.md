# PM-API

## Usage

set up the directories to run
```
./setup.sh /var/api
```

set up crontab to run periodically.
```
pm-api <work-dir>
```

`pm-api` will look into the working directory and read all `.json`
files and run the request. Response will be placed in
the `<work-dir>/response/` directory.

The successful requests will be moved to `<work-dir>/success/` directory.
The failed requests will be moved to `<work-dir>/fail/` directory.

## Callback

If the `callback_ok` or `callback_fail` is specified, the tool will `POST` to the url with the response.

## The directories

The application create a json file and put in the working directory.

`pm-api` will run from crontab and will process all the `.json` files

If the request is successful, and the callback_ok exists, the json file will be move to `callback/` directory
else it will be moved to `success/` directory

If the request is fail, and the callback_fail exists, the json file will be move to `callback/` directory
else it will be moved to `fail/` directory

The latest response is saved within the json file.

All the responses are saved in `response/` directory.

json files in the callback directory will then try to call back to the specified url until success or reach maximum RETRY.
## TODO

- mask oauth1 after call success or fail
- X-API headers when callback
