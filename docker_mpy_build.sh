
#!/bin/sh
echo "building mpy"
echo $(ls compiled)

find kmk/ -name "*.py" -exec sh -c 'mkdir -p compiled/8/$(dirname {}) &&\
 ./mpy-cross-8 -O2 {} -o compiled/8/$(dirname {})/$(basename -s .py {}).mpy' \;

find kmk/ -name "*.py" -exec sh -c 'mkdir -p compiled/7/$(dirname {}) &&\
 ./mpy-cross-7 -O2 {} -o compiled/7/$(dirname {})/$(basename -s .py {}).mpy' \;

echo $(ls compiled)

echo "done building"
