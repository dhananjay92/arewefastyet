import runners
import time
import os
import sys
import json

sys.path.insert(1, '../driver')
import utils

class ShellExecutor(object):
    def __init__(self, engineInfo):
        self.engineInfo = engineInfo
    
    def run(self, benchmark, config):
        env = os.environ.copy()
        env.update(config.env())
        env.update(self.engineInfo["env"])
        args = config.args() + self.engineInfo["args"]

        with utils.chdir(os.path.join(utils.config.BenchmarkPath, benchmark.folder)):
            return benchmark.benchmark(self.engineInfo["binary"], env, args)

class BrowserExecutor(object):
    
    def __init__(self, engineInfo):
        self.engineInfo = engineInfo
    
    def run(self, benchmark, config):
        env = os.environ.copy()
        env.update(config.env())
        env.update(self.engineInfo["env"])
        args = [benchmark.url] + config.args() + self.engineInfo["args"]

        self.execute(benchmark, env, args)

        fp = open("results", "r")
        results = json.loads(fp.read())
        fp.close()

        return benchmark.processResults(results)

    def resetResults(self):
        if not os.path.exists("results"):
            return

        os.unlink("results")

    def waitForResults(self):
        timeout = utils.config.Timeout * 60
        while not os.path.exists("results") and timeout > 0:
            print 'Results not ready yet. Going to sleep...'
            time.sleep(10)
            timeout -= 10
    
class FirefoxExecutor(BrowserExecutor):
    
    def execute(self, page, env, args):
        runner = runners.getRunner(self.engineInfo["platform"], {
            "osx_mount_point": "/Volumes/Nightly",
            "android_processname": "org.mozilla.fennec" 
        })

        # kill all possible running instances. 
        runner.killAllInstances()
        runner.killall("plugin-container")

        # if needed install the executable
        runner.install(self.engineInfo["binary"])

        # delete profile
        runner.rm("profile/")

        # create new profile
        runner.mkdir("profile/")

        # Update profile to disable slow script dialog 
        runner.write("profile/prefs.js", "user_pref(\"dom.max_script_run_time\", 0);")

        # reset the result
        self.resetResults()

        # start browser
        process = runner.start(self.engineInfo["binary"], args + ["--profile", runner.getdir("profile")], env)
        
        # wait for results
        self.waitForResults()

        # kill browser
        runner.kill(process)

class ServoExecutor(BrowserExecutor):
    def execute(self, page, env, args):
        print "ServoExecutor()..."
        runner = runners.getRunner(self.engineInfo["platform"], {
            "osx_mount_point": "/Volumes/Nightly",
            "android_processname": "org.mozilla.fennec"
        })

        # kill all possible running instances.
        runner.killall("servo")

        # reset the result
        self.resetResults()

        # start browser
        process = runner.start(self.engineInfo["binary"], args, env)
        print 'Returned from runner.start()'
        while process.poll() is None:
            print 'poll sleep...'
            time.sleep(0.5)
        print 'Breaking out of loop.'
        print 'Return Code: ' + str(process.returncode)
        (stdout, stderr) = process.communicate()
        print 'STDOUT: ' + str(stdout)
        print 'STDERR: ' + str(stderr)

        # wait for results
        self.waitForResults()

        # kill browser
        runner.kill(process)

#class NativeExecutor(Executor):
#
#    def execute(self, env, args):
#        pass

def getExecutor(engineInfo):
    if engineInfo["shell"]:
        return ShellExecutor(engineInfo)
    if engineInfo["engine_type"] == "firefox" and not engineInfo["shell"]:
        return FirefoxExecutor(engineInfo)
    if engineInfo["engine_type"] == "servo":
        return ServoExecutor(engineInfo)

