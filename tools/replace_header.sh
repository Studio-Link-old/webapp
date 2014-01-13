#!/bin/bash

for I in `find ../app -name "*.py"` ; do
      grep "Copyright Sebastian Reimers" $I > /dev/null
      if [ 1 == $? ]; then
          echo "Add header: $I"
          cat python_header.txt $I > $I.tmp
      else
          echo "Replace header: $I"
          cat python_header.txt > $I.tmp
          sed '0,/^.*License.*$/d' $I | sed 1,2d >> $I.tmp
      fi
      rm $I
      mv $I.tmp $I
done
