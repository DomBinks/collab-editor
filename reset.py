# Used to clear all the download files
for i in ['.py', '.js', '.c', '.hs']:
    file = open('dynamic/download' + i, "w")
    file.write('')
    file.close()