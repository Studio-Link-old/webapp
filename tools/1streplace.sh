#!/bin/bash
echo "Really?"
exit 0
for I in `find ../app -name "*.py"` ; do
      cat python_header.txt $I > $I.tmp
      rm $I
      mv $I.tmp $I
done
