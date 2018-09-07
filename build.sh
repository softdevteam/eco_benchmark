ECOV=0483b1e
experimentdir=`pwd`

if [ ! -d eco ]; then
    git clone https://github.com/softdevteam/eco
    cd eco
    git checkout ${ECOV}
    cd ..
fi

if [ -f results.csv ]; then
    echo "results.csv already exists. Abort."
    exit
fi

if [ -f performance.pdf ]; then
    echo "performance.pdf already exists. Abort."
    exit
fi

cp benchmark.py eco/lib/eco/
cd eco/lib/eco/
find $experimentdir/javastdlib5/ -iname \*.java -exec ./benchmark.py {} \;
mv results.csv $experimentdir/
