# pCloud Sync Fixer

A Python script to fix stuck pCloud sync processes by manipulating the local
SQLite database.

## Overview

This tool helps resolve issues when the pCloud client gets stuck in a sync loop
and is not uploading new files. The problem typically occurs due to duplicate
folder creation tasks in the pCloud local database that prevent other tasks
from being processed.

## How It Works

The pCloud client uses a SQLite database (`data.db`) to manage its sync state.
When sync gets stuck, there are usually many folder creation tasks (type 3) in
a pending state (status 2) that block the queue. This script:

1. Connects to the pCloud `data.db` file
2. Finds the first stuck folder creation task (lowest ID with type=3 and
   status=2)
3. Moves this task to the end of the queue by updating its ID to be one
   greater than the maximum ID in the task table

This approach resolves the bottleneck without deleting any data, providing a
safe and repeatable way to fix the sync issue.

## pCloud Database Structure

The pCloud client uses a SQLite database named `data.db` to manage its sync
state. This file is located in the pCloud cache directory.

### Key Tables

The following tables appear to be the most relevant to the sync process:

* `baccountemail`
* `baccountteam`
* `bsharedfolder`
* `contacts`
* `cryptofilekey`
* `cryptofolderkey`
* `devices`
* `filerevision`
* `fstaskdepend`
* `fstaskfileid`
* `fstaskupload`
* `fsxattr`
* `hashchecksum`
* `links`
* `localfileupload`
* `myteams`
* `pagecache`
* `pagecachetask`
* `resolver`
* `setting`
* `sharedfolder`
* `sharerequest`
* `syncedfolder`
* `syncfolder`
* `syncfolderdelayed`
* `task`
* `upload_tasks`
* `uptask_fileupload`

* `fstask`: This table contains a queue of filesystem tasks, such as creating
  folders and uploading files.
* `file`: This table contains metadata about the files on the pCloud servers.
* `localfile`: This table contains metadata about the files on the local
  machine.
* `folder`: This table contains metadata about the folders on the pCloud
  servers.
* `localfolder`: This table contains metadata about the folders on the local
  machine.

### The `fstask` Table

The `fstask` table is the key to understanding the sync issue. It has the
following relevant columns:

* `id`: The unique ID of the task.
* `type`: The type of the task.
* `status`: The status of the task.
* `folderid`: The ID of the folder that the task operates on.
* `fileid`: The ID of the file that the task operates on.
* `text1`: A text field that can contain a filename or encoded data.
* `text2`: A text field that can contain encoded data.

#### Task Types

* **`type` 3:** Folder or file creation.
  * If `text2` is not empty, it's a folder creation task, and `text1` and
    `text2` contain encoded data.
  * If `text2` is empty, it's a file creation task, and `text1` contains the
    filename.
* **`type` 5:** File upload. These tasks appear to be dependent on `type` 3
  tasks.
* **`type` 6:** Unknown, but appears to be dependent on `type` 5 tasks.
* **`type` 9:** Unknown.

#### Task Statuses

* **`status` 2:** A pending or stuck state for `type` 3 and `type` 9 tasks.
* **`status` 10:** A pending or stuck state for `type` 5 tasks.
* **`status` 0:** A pending or stuck state for `type` 6 tasks.

## Requirements

* Python 3.6+
* pCloud desktop client installed
* SQLite3 (usually included with Python)

## Usage

1. Close the pCloud desktop client
2. Run the script:

   ```bash
   python3 fix_pcloud_sync.py
   ```

3. Reopen the pCloud desktop client

## License

This project is licensed under the Creative Commons Attribution 4.0
International License - see the [LICENSE](LICENSE.md) file for details.

## Disclaimer

This tool manipulates the internal database of the pCloud client. While it's
designed to be safe, always backup your `data.db` file before use. Use at your
own risk.
