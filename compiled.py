#! /usr/bin/env python2.7
import subprocess, sys, os, time

pwd = os.getcwd()
javap = pwd+"/error_recovery_experiment/runner/java_parser/target/release/java_parser"
incl_lexing = True
output = "results_c.csv"

if __name__ == "__main__":
    filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "nolex":
        incl_lexing = False
        output = "results_c_nolex.csv"
    filesize = os.path.getsize(filename)

    sys.stdout.write("Running {} {}: ".format(filename, "with lexing" if incl_lexing else "without lexing"))
    e = [javap, filename]
    try:
        r = subprocess.check_output(e)
    except subprocess.CalledProcessError:
        print("Skipped (error).")
        exit()

    timings = []
    for i in range(1, 6):
        start = time.time()
        nolex = int(subprocess.check_output(e)) / 1000.0 / 1000.0 / 1000.0 # convert from nano to seconds
        result = time.time() - start
        if incl_lexing:
            timings.append(result)
        else:
            timings.append(nolex)

    sys.stdout.write(str(sum(timings) / len(timings)))
    with open(output, "a+") as f:
        f.write("{} {} {}".format(filename, filesize, ",".join([str(x) for x in timings])))
        f.write("\n")

    sys.stdout.write("\n")

