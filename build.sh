ECOV=0483b1e
experimentdir=`pwd`

if [ ! -d eco ]; then
    git clone https://github.com/softdevteam/eco
    cd eco
    git checkout ${ECOV}
    cd ..
fi

if [ ! -d error_recovery_experiment ]; then
    git clone https://github.com/softdevteam/error_recovery_experiment.git
    cd error_recovery_experiment/runner/java_parser/
    cargo build --release
fi

if [ ! -f results.csv ]; then
    echo "Running Eco:incremental"
    cp benchmark.py eco/lib/eco/
    cd eco/lib/eco/
    find $experimentdir/javastdlib5/ -iname \*.java -exec ./benchmark.py {} \;
    mv results.csv $experimentdir/
fi

if [ ! -f results_t.csv ]; then
    echo "Running Eco:traditional"
    cp traditional.py eco/lib/eco/
    cd eco/lib/eco/
    find $experimentdir/javastdlib5/ -iname \*.java -exec ./traditional.py {} \;
    mv results_t.csv $experimentdir/
fi

if [ ! -f results_c.csv ]; then
    echo "Running grmtools:traditional"
    find $experimentdir/javastdlib5/ -iname \*.java -exec ./compiled.py {} \;
fi

if [ ! -f results_c_nolex.csv ]; then
    echo "Running grmtools:traditional"
    find $experimentdir/javastdlib5/ -iname \*.java -exec ./compiled.py {} nolex \;
fi

if [ -f performance.pdf ]; then
    echo "performance.pdf already exists. Abort."
    exit
fi
