# Brainrot Dictionary – UMDCTF 2025

## Problem Description

The challenge allowed users to upload `.brainrot` files, which were processed and displayed on the `/dict` page. Internally, the server executed the following command:

```bash
find <upload_dir> -name "*.brainrot" | xargs sort | uniq
This meant that all uploaded .brainrot files were collected using find, passed to xargs, and then sorted and deduplicated using sort and uniq. The final result was printed to the /dict page.

The objective was to retrieve the contents of a flag.txt file located on the server, which was not directly accessible.

Solution
The vulnerability lay in how the sort command interpreted filenames passed through xargs. Specifically, if a filename began with a dash (-), sort would treat it as a command-line option rather than a filename. This created a classic argument injection scenario.

To exploit this, we uploaded a file named:

diff
Copy
Edit
-eflag.brainrot
When /dict was accessed, the filename -eflag.brainrot was passed as an argument to sort. Since -e is a valid option for sort (in some implementations), it altered how sort processed input, causing the output to include unintended file content.

This worked because xargs and sort were used without safe-guards like --, which is commonly used to signal the end of options. Without this, filenames that begin with dashes can be interpreted as flags, resulting in undefined or exploitable behavior.
