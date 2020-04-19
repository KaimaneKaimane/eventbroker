Use the main.py to run the tool (I used the docker image as my interpreter)

It will start 2 consumer and 1 source and will delete them after a while.
If you change any of the three test files in the file_test_folder the changes should be detected by the source and be
consumed and logged by one of the consumers.