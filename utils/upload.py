#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import dropbox

def find_files( files, dirs=[]):
    new_dirs = []
    for d in dirs:
        try:
            new_dirs += [ os.path.join(d, f) for f in os.listdir(d) ]
        except OSError:
            files.append(d)

    if new_dirs:
        find_files(files, new_dirs)
    else:
        return

def main():
    access_token = 'hBvzxGgIqvAAAAAAAAABA_BKxViXkLGf9KDLA719jQgt8iU5iRnRYViizcH4C_O9'

    files = []
    find_files(files, dirs = [
                         'scores/plots/'
                         ])

    prefix = '/works/researchs/transdreamer/'

    # API v2
    CHUNK_SIZE = 4 * 1024 * 1024
    for fpath in files:
        print(fpath+" is uploading")

        dbx = dropbox.Dropbox(access_token)

        with open(fpath, 'rb') as f:
            file_size = os.path.getsize(fpath)

            if file_size <= CHUNK_SIZE:
                print(dbx.files_upload(f.read(), prefix+fpath,mode=dropbox.files.WriteMode.overwrite))

            else:
                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                           offset=f.tell())
                commit = dropbox.files.CommitInfo(path=prefix+fpath)

                while f.tell() < file_size:
                    print(str((file_size - f.tell())/1024/1024/1024)+'gb'+' remain')
                    if ((file_size - f.tell()) <= CHUNK_SIZE):
                        print(dbx.files_upload_session_finish(f.read(CHUNK_SIZE),
                                                        cursor,
                                                        commit))
                    else:
                        dbx.files_upload_session_append(f.read(CHUNK_SIZE),
                                                        cursor.session_id,
                                                        cursor.offset)
                        cursor.offset = f.tell()

if __name__ == '__main__':
    main()

