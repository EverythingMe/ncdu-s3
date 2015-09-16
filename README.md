# ncdu-s3
This tool generates ncdu formatted JSON data file for viewing with [ncdu](http://dev.yorhel.nl/ncdu)

# Usage
```bash
$ sudo pip install ncdu-s3
$ ncdu-s3 s3://my-bucket my-bucket.json
$ ncdu -f my-bucket.json
```

Please note you need boto configured for your user before using this tool.  
See how to configure boto [here](http://boto3.readthedocs.org/en/latest/guide/configuration.html)
